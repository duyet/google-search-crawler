"""
Google Search Crawler - Elegant Python library for crawling Google Search results.

Copyright (c) 2009-2016, Mario Vilas
Copyright (c) 2024, Van-Duyet Le
All rights reserved.

Redistribution and use in source and binary forms, with or without
modification, are permitted provided that the following conditions are met:

    * Redistributions of source code must retain the above copyright notice,
      this list of conditions and the following disclaimer.
    * Redistributions in binary form must reproduce the above copyright
      notice, this list of conditions and the following disclaimer in the
      documentation and/or other materials provided with the distribution.
    * Neither the name of the copyright holder nor the names of its
      contributors may be used to endorse or promote products derived from
      this software without specific prior written permission.

THIS SOFTWARE IS PROVIDED BY THE COPYRIGHT HOLDERS AND CONTRIBUTORS "AS IS"
AND ANY EXPRESS OR IMPLIED WARRANTIES, INCLUDING, BUT NOT LIMITED TO, THE
IMPLIED WARRANTIES OF MERCHANTABILITY AND FITNESS FOR A PARTICULAR PURPOSE
ARE DISCLAIMED. IN NO EVENT SHALL THE COPYRIGHT OWNER OR CONTRIBUTORS BE
LIABLE FOR ANY DIRECT, INDIRECT, INCIDENTAL, SPECIAL, EXEMPLARY, OR
CONSEQUENTIAL DAMAGES (INCLUDING, BUT NOT LIMITED TO, PROCUREMENT OF
SUBSTITUTE GOODS OR SERVICES; LOSS OF USE, DATA, OR PROFITS; OR BUSINESS
INTERRUPTION) HOWEVER CAUSED AND ON ANY THEORY OF LIABILITY, WHETHER IN
CONTRACT, STRICT LIABILITY, OR TORT (INCLUDING NEGLIGENCE OR OTHERWISE)
ARISING IN ANY WAY OUT OF THE USE OF THIS SOFTWARE, EVEN IF ADVISED OF THE
POSSIBILITY OF SUCH DAMAGE.
"""

from __future__ import annotations

import logging
import time
from http.cookiejar import LWPCookieJar
from pathlib import Path
from typing import Any, Generator, TypedDict
from urllib.parse import quote_plus

import requests
from bs4 import BeautifulSoup
from tenacity import retry, retry_if_exception_type, stop_after_attempt, wait_exponential

from google.config import Config, get_config
from google.exceptions import (
    BlockedError,
    HTTPError,
    InvalidParameterError,
    ParsingError,
    RateLimitError,
    SearchError,
)
from google.utils import (
    build_search_url,
    filter_result,
    get_random_user_agent,
    load_user_agents,
    setup_logging,
)

__version__ = "2.0.0"
__all__ = [
    "search",
    "search_images",
    "search_news",
    "search_videos",
    "search_shop",
    "search_books",
    "search_apps",
    "lucky",
    "SearchResult",
]

logger = logging.getLogger(__name__)

# Load user agents list globally
_USER_AGENTS = load_user_agents()

# Cookie jar stored at user's home folder
_COOKIE_FILE = Path.home() / ".google-cookie"
_cookie_jar = LWPCookieJar(str(_COOKIE_FILE))

try:
    _cookie_jar.load(ignore_discard=True, ignore_expires=True)
    logger.debug(f"Loaded cookies from {_COOKIE_FILE}")
except FileNotFoundError:
    logger.debug("No existing cookie file found, will create new one")
except Exception as e:
    logger.warning(f"Failed to load cookies: {e}")


class SearchResult(TypedDict):
    """Typed dictionary for search results.

    Attributes:
        url: The URL of the search result
        title: The title of the search result
        description: The description/snippet of the search result
    """

    url: str
    title: str
    description: str


@retry(
    retry=retry_if_exception_type((requests.ConnectionError, requests.Timeout)),
    stop=stop_after_attempt(3),
    wait=wait_exponential(multiplier=1, min=2, max=10),
)
def _get_page(url: str, user_agent: str | None = None, timeout: int = 10) -> str:
    """Request a URL and return the response HTML.

    Args:
        url: URL to retrieve
        user_agent: User agent string (None for random)
        timeout: Request timeout in seconds

    Returns:
        HTML content of the page

    Raises:
        HTTPError: If the request fails
        RateLimitError: If rate limiting is detected
        BlockedError: If access is blocked
    """
    if user_agent is None:
        user_agent = get_random_user_agent(_USER_AGENTS)

    headers = {
        "User-Agent": user_agent,
        "Accept": "text/html,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8",
        "Accept-Language": "en-US,en;q=0.5",
        "Accept-Encoding": "gzip, deflate",
        "DNT": "1",
        "Connection": "keep-alive",
        "Upgrade-Insecure-Requests": "1",
    }

    try:
        # Create a session with cookies
        session = requests.Session()
        session.cookies = _cookie_jar  # type: ignore

        logger.debug(f"Requesting URL: {url}")
        response = session.get(url, headers=headers, timeout=timeout)

        # Save cookies
        _cookie_jar.save(ignore_discard=True, ignore_expires=True)

        # Check for blocking or rate limiting
        if response.status_code == 429:
            logger.error("Rate limit detected (HTTP 429)")
            raise RateLimitError("Too many requests. Please wait before trying again.")

        if response.status_code == 403:
            logger.error("Access forbidden (HTTP 403)")
            raise BlockedError("Access blocked by Google. Try using a different IP or user agent.")

        response.raise_for_status()
        logger.debug(f"Successfully fetched {len(response.text)} bytes")

        return response.text

    except (RateLimitError, BlockedError):
        raise

    except requests.Timeout as e:
        logger.error(f"Request timeout: {e}")
        raise HTTPError(f"Request timeout: {url}", status_code=None) from e

    except requests.ConnectionError as e:
        logger.error(f"Connection error: {e}")
        raise HTTPError(f"Connection error: {url}", status_code=None) from e

    except requests.HTTPError as e:
        status_code = e.response.status_code if e.response is not None else None
        logger.error(f"HTTP error {status_code}: {e}")
        raise HTTPError(f"HTTP error for {url}", status_code=status_code) from e

    except Exception as e:
        logger.error(f"Unexpected error fetching page: {e}")
        raise HTTPError(f"Failed to fetch {url}: {e}", status_code=None) from e


def _parse_search_results(html: str, only_standard: bool = False) -> list[SearchResult]:
    """Parse search results from Google's HTML.

    Args:
        html: HTML content to parse
        only_standard: If True, only return standard results

    Returns:
        List of SearchResult dictionaries

    Raises:
        ParsingError: If parsing fails
    """
    try:
        soup = BeautifulSoup(html, "html.parser")

        # Find the search results container
        search_div = soup.find(id="search")
        if not search_div:
            logger.warning("No search results container found")
            return []

        # Find all anchor tags
        anchors = search_div.find_all("a")
        results: list[SearchResult] = []

        for anchor in anchors:
            # Filter by parent tag if only_standard is True
            if only_standard and (not anchor.parent or anchor.parent.name.lower() != "h3"):
                continue

            # Get the URL
            try:
                link = anchor.get("href")
                if not link:
                    continue
            except (KeyError, AttributeError):
                continue

            # Filter invalid links
            filtered_link = filter_result(link)
            if not filtered_link:
                continue

            # Extract title
            try:
                title = anchor.get_text(strip=True) or ""
            except (AttributeError, TypeError):
                title = ""

            # Extract description
            try:
                description_elem = anchor.parent.parent.find(class_="st")  # type: ignore
                description = description_elem.get_text(strip=True) if description_elem else ""
            except (AttributeError, TypeError):
                description = ""

            results.append(
                SearchResult(
                    url=filtered_link,
                    title=title,
                    description=description,
                )
            )

        logger.debug(f"Parsed {len(results)} results from page")
        return results

    except Exception as e:
        logger.error(f"Failed to parse search results: {e}")
        raise ParsingError(f"Failed to parse HTML: {e}") from e


def search(
    query: str,
    tld: str = "com",
    lang: str = "en",
    tbs: str = "0",
    safe: str = "off",
    num: int = 10,
    start: int = 0,
    stop: int | None = None,
    pause: float = 2.0,
    only_standard: bool = False,
    extra_params: dict[str, Any] | None = None,
    tpe: str = "",
    user_agent: str | None = None,
    config: Config | None = None,
) -> Generator[SearchResult, None, None]:
    """Search Google and yield result dictionaries.

    This is the main search function that yields search results one by one
    using a generator pattern. It handles pagination automatically and
    implements respectful rate limiting.

    Args:
        query: Search query string (will be URL-encoded automatically)
        tld: Top-level domain (e.g., 'com', 'co.uk', 'com.vn')
        lang: Language code (e.g., 'en', 'vi', 'fr')
        tbs: Time-based search (e.g., 'qdr:h' for last hour, 'qdr:d' for last day)
        safe: Safe search mode ('off', 'medium', 'high')
        num: Number of results per page (1-100)
        start: Starting index for results
        stop: Maximum number of results to return (None for unlimited)
        pause: Seconds to pause between requests (minimum 2.0 recommended)
        only_standard: If True, only return standard results (not related searches, etc.)
        extra_params: Additional URL parameters as a dictionary
        tpe: Search type ('isch' for images, 'nws' for news, 'vid' for videos, etc.)
        user_agent: Custom user agent string (None for random)
        config: Custom configuration object (None to use global config)

    Yields:
        SearchResult dictionaries with 'url', 'title', and 'description' keys

    Raises:
        InvalidParameterError: If parameters are invalid
        SearchError: If the search fails
        HTTPError: If HTTP requests fail
        ParsingError: If result parsing fails

    Example:
        >>> for result in search('python programming', stop=10):
        ...     print(f"{result['title']}: {result['url']}")
    """
    # Use provided config or get global config
    if config is None:
        config = get_config()

    # Setup logging
    setup_logging(config.log_level)

    # Validate parameters
    if not query:
        raise InvalidParameterError("Query cannot be empty")

    if num < 1 or num > 100:
        raise InvalidParameterError("num must be between 1 and 100")

    if pause < 0:
        raise InvalidParameterError("pause must be non-negative")

    # Check for overlapping parameters
    builtin_params = {"hl", "q", "btnG", "tbs", "safe", "tbm", "num", "start"}
    if extra_params:
        overlapping = builtin_params & set(extra_params.keys())
        if overlapping:
            raise InvalidParameterError(
                f"Extra params {overlapping} overlap with built-in parameters"
            )

    # URL-encode the query
    encoded_query = quote_plus(query)

    # Track seen results to avoid duplicates
    seen_hashes: set[int] = set()

    # Current position in results
    current_start = start

    logger.info(f"Starting search for query: {query}")

    try:
        # Loop until we reach the maximum result count
        while stop is None or current_start < stop:
            # Build the search URL
            url = build_search_url(
                query=encoded_query,
                tld=tld,
                lang=lang,
                tbs=tbs,
                safe=safe,
                num=num,
                start=current_start,
                tpe=tpe,
                extra_params=extra_params,
            )

            # Pause between requests (respectful crawling)
            if current_start > start:
                logger.debug(f"Pausing {pause} seconds before next request")
                time.sleep(pause)

            # Fetch the page
            try:
                html = _get_page(url, user_agent=user_agent, timeout=config.timeout)
            except (HTTPError, RateLimitError, BlockedError) as e:
                logger.error(f"Failed to fetch search results: {e}")
                raise SearchError(f"Search failed: {e}") from e

            # Parse results
            try:
                results = _parse_search_results(html, only_standard=only_standard)
            except ParsingError as e:
                logger.error(f"Failed to parse search results: {e}")
                raise

            # If no results found, we've reached the end
            if not results:
                logger.info("No more results found, ending search")
                break

            # Yield results, avoiding duplicates
            results_yielded = 0
            for result in results:
                # Check for duplicates
                result_hash = hash(result["url"])
                if result_hash in seen_hashes:
                    continue

                seen_hashes.add(result_hash)

                # Check if we've hit the stop limit
                if stop is not None and len(seen_hashes) >= stop:
                    logger.info(f"Reached stop limit of {stop} results")
                    return

                yield result
                results_yielded += 1

            logger.info(f"Yielded {results_yielded} results from page")

            # Check if there's a "next page" link
            soup = BeautifulSoup(html, "html.parser")
            if not soup.find(id="nav"):
                logger.info("No navigation element found, ending search")
                break

            # Move to next page
            current_start += num

    except KeyboardInterrupt:
        logger.info("Search interrupted by user")
        return
    except Exception as e:
        logger.error(f"Unexpected error during search: {e}")
        raise SearchError(f"Search failed unexpectedly: {e}") from e


def search_images(
    query: str,
    tld: str = "com",
    lang: str = "en",
    tbs: str = "0",
    safe: str = "off",
    num: int = 10,
    start: int = 0,
    stop: int | None = None,
    pause: float = 2.0,
    only_standard: bool = False,
    extra_params: dict[str, Any] | None = None,
    user_agent: str | None = None,
    config: Config | None = None,
) -> Generator[SearchResult, None, None]:
    """Search Google Images. See search() for parameter documentation."""
    return search(
        query=query,
        tld=tld,
        lang=lang,
        tbs=tbs,
        safe=safe,
        num=num,
        start=start,
        stop=stop,
        pause=pause,
        only_standard=only_standard,
        extra_params=extra_params,
        tpe="isch",
        user_agent=user_agent,
        config=config,
    )


def search_news(
    query: str,
    tld: str = "com",
    lang: str = "en",
    tbs: str = "0",
    safe: str = "off",
    num: int = 10,
    start: int = 0,
    stop: int | None = None,
    pause: float = 2.0,
    only_standard: bool = False,
    extra_params: dict[str, Any] | None = None,
    user_agent: str | None = None,
    config: Config | None = None,
) -> Generator[SearchResult, None, None]:
    """Search Google News. See search() for parameter documentation."""
    return search(
        query=query,
        tld=tld,
        lang=lang,
        tbs=tbs,
        safe=safe,
        num=num,
        start=start,
        stop=stop,
        pause=pause,
        only_standard=only_standard,
        extra_params=extra_params,
        tpe="nws",
        user_agent=user_agent,
        config=config,
    )


def search_videos(
    query: str,
    tld: str = "com",
    lang: str = "en",
    tbs: str = "0",
    safe: str = "off",
    num: int = 10,
    start: int = 0,
    stop: int | None = None,
    pause: float = 2.0,
    only_standard: bool = False,
    extra_params: dict[str, Any] | None = None,
    user_agent: str | None = None,
    config: Config | None = None,
) -> Generator[SearchResult, None, None]:
    """Search Google Videos. See search() for parameter documentation."""
    return search(
        query=query,
        tld=tld,
        lang=lang,
        tbs=tbs,
        safe=safe,
        num=num,
        start=start,
        stop=stop,
        pause=pause,
        only_standard=only_standard,
        extra_params=extra_params,
        tpe="vid",
        user_agent=user_agent,
        config=config,
    )


def search_shop(
    query: str,
    tld: str = "com",
    lang: str = "en",
    tbs: str = "0",
    safe: str = "off",
    num: int = 10,
    start: int = 0,
    stop: int | None = None,
    pause: float = 2.0,
    only_standard: bool = False,
    extra_params: dict[str, Any] | None = None,
    user_agent: str | None = None,
    config: Config | None = None,
) -> Generator[SearchResult, None, None]:
    """Search Google Shopping. See search() for parameter documentation."""
    return search(
        query=query,
        tld=tld,
        lang=lang,
        tbs=tbs,
        safe=safe,
        num=num,
        start=start,
        stop=stop,
        pause=pause,
        only_standard=only_standard,
        extra_params=extra_params,
        tpe="shop",
        user_agent=user_agent,
        config=config,
    )


def search_books(
    query: str,
    tld: str = "com",
    lang: str = "en",
    tbs: str = "0",
    safe: str = "off",
    num: int = 10,
    start: int = 0,
    stop: int | None = None,
    pause: float = 2.0,
    only_standard: bool = False,
    extra_params: dict[str, Any] | None = None,
    user_agent: str | None = None,
    config: Config | None = None,
) -> Generator[SearchResult, None, None]:
    """Search Google Books. See search() for parameter documentation."""
    return search(
        query=query,
        tld=tld,
        lang=lang,
        tbs=tbs,
        safe=safe,
        num=num,
        start=start,
        stop=stop,
        pause=pause,
        only_standard=only_standard,
        extra_params=extra_params,
        tpe="bks",
        user_agent=user_agent,
        config=config,
    )


def search_apps(
    query: str,
    tld: str = "com",
    lang: str = "en",
    tbs: str = "0",
    safe: str = "off",
    num: int = 10,
    start: int = 0,
    stop: int | None = None,
    pause: float = 2.0,
    only_standard: bool = False,
    extra_params: dict[str, Any] | None = None,
    user_agent: str | None = None,
    config: Config | None = None,
) -> Generator[SearchResult, None, None]:
    """Search Google Apps. See search() for parameter documentation."""
    return search(
        query=query,
        tld=tld,
        lang=lang,
        tbs=tbs,
        safe=safe,
        num=num,
        start=start,
        stop=stop,
        pause=pause,
        only_standard=only_standard,
        extra_params=extra_params,
        tpe="app",
        user_agent=user_agent,
        config=config,
    )


def lucky(
    query: str,
    tld: str = "com",
    lang: str = "en",
    tbs: str = "0",
    safe: str = "off",
    only_standard: bool = False,
    extra_params: dict[str, Any] | None = None,
    tpe: str = "",
    user_agent: str | None = None,
    config: Config | None = None,
) -> SearchResult:
    """Get the first search result (I'm Feeling Lucky).

    Args:
        See search() for parameter documentation

    Returns:
        The first SearchResult

    Raises:
        SearchError: If no results are found
    """
    gen = search(
        query=query,
        tld=tld,
        lang=lang,
        tbs=tbs,
        safe=safe,
        num=1,
        start=0,
        stop=1,
        pause=0.0,
        only_standard=only_standard,
        extra_params=extra_params,
        tpe=tpe,
        user_agent=user_agent,
        config=config,
    )

    try:
        return next(gen)
    except StopIteration:
        raise SearchError("No results found for query") from None
