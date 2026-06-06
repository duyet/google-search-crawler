"""Utility functions for Google Search Crawler."""

from __future__ import annotations

import logging
import random
from pathlib import Path
from typing import Any
from urllib.parse import parse_qs, urlparse

logger = logging.getLogger(__name__)


def load_user_agents(file_path: str | Path | None = None) -> list[str]:
    """Load user agent strings from a file.

    Args:
        file_path: Path to user agents file. If None, uses default location.

    Returns:
        List of user agent strings

    Raises:
        FileNotFoundError: If the user agents file doesn't exist
    """
    if file_path is None:
        # Default location: same directory as this module
        module_dir = Path(__file__).parent
        file_path = module_dir / "user_agents.txt"
    else:
        file_path = Path(file_path)

    if not file_path.exists():
        logger.warning(f"User agents file not found: {file_path}, using default")
        return ["Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36"]

    try:
        with open(file_path, encoding="utf-8") as f:
            user_agents = [line.strip() for line in f if line.strip()]
        logger.debug(f"Loaded {len(user_agents)} user agents from {file_path}")
        return user_agents
    except Exception as e:
        logger.error(f"Failed to load user agents from {file_path}: {e}")
        return ["Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36"]


def get_random_user_agent(user_agents: list[str] | None = None) -> str:
    """Get a random user agent string.

    Args:
        user_agents: List of user agent strings. If None, loads from default file.

    Returns:
        Random user agent string
    """
    if user_agents is None:
        user_agents = load_user_agents()

    if not user_agents:
        return "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36"

    return random.choice(user_agents)  # nosec B311 - not used for cryptographic purposes


def filter_result(link: str) -> str | None:
    """Filter links found in Google result pages.

    Args:
        link: URL to filter

    Returns:
        Filtered URL if valid, None otherwise
    """
    try:
        # Parse the URL
        parsed = urlparse(link)

        # Valid results are absolute URLs not pointing to Google domains
        if parsed.netloc and "google" not in parsed.netloc:
            return link

        # Decode hidden URLs (e.g., /url?q=https://example.com)
        if link.startswith("/url?"):
            query_params = parse_qs(parsed.query)
            if "q" in query_params:
                actual_url = query_params["q"][0]
                parsed_actual = urlparse(actual_url)

                # Check if the decoded URL is valid
                if parsed_actual.netloc and "google" not in parsed_actual.netloc:
                    return actual_url

    except Exception as e:
        logger.debug(f"Failed to filter URL {link}: {e}")
        pass

    return None


def build_search_url(
    query: str,
    tld: str = "com",
    lang: str = "en",
    tbs: str = "0",
    safe: str = "off",
    num: int = 10,
    start: int = 0,
    tpe: str = "",
    extra_params: dict[str, Any] | None = None,
) -> str:
    """Build a Google search URL with the given parameters.

    Args:
        query: Search query (URL-encoded)
        tld: Top-level domain
        lang: Language code
        tbs: Time-based search parameter
        safe: Safe search mode
        num: Number of results
        start: Starting index
        tpe: Search type (images, videos, etc.)
        extra_params: Additional query parameters

    Returns:
        Complete Google search URL
    """
    # Base URL template
    if start > 0:
        if num == 10:
            url = (
                f"https://www.google.{tld}/search?"
                f"hl={lang}&q={query}&start={start}&tbs={tbs}&safe={safe}"
            )
        else:
            url = (
                f"https://www.google.{tld}/search?"
                f"hl={lang}&q={query}&num={num}&start={start}&tbs={tbs}&safe={safe}"
            )
    else:
        if num == 10:
            url = f"https://www.google.{tld}/search?" f"hl={lang}&q={query}&tbs={tbs}&safe={safe}"
        else:
            url = (
                f"https://www.google.{tld}/search?"
                f"hl={lang}&q={query}&num={num}&tbs={tbs}&safe={safe}"
            )

    # Add search type if specified
    if tpe:
        url += f"&tbm={tpe}"

    # Add extra parameters
    if extra_params:
        for key, value in extra_params.items():
            url += f"&{key}={value}"

    return url


def setup_logging(log_level: str = "INFO") -> None:
    """Set up logging configuration.

    Args:
        log_level: Logging level (DEBUG, INFO, WARNING, ERROR, CRITICAL)
    """
    logging.basicConfig(
        level=getattr(logging, log_level.upper()),
        format="%(asctime)s - %(name)s - %(levelname)s - %(message)s",
        datefmt="%Y-%m-%d %H:%M:%S",
    )
