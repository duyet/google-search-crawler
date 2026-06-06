"""Custom exceptions for the Google Search Crawler."""

from __future__ import annotations


class GoogleSearchError(Exception):
    """Base exception for all Google Search Crawler errors."""

    pass


class InvalidParameterError(GoogleSearchError):
    """Raised when an invalid parameter is provided."""

    pass


class SearchError(GoogleSearchError):
    """Raised when a search operation fails."""

    pass


class HTTPError(GoogleSearchError):
    """Raised when an HTTP request fails."""

    def __init__(self, message: str, status_code: int | None = None) -> None:
        """Initialize HTTPError.

        Args:
            message: Error message
            status_code: HTTP status code if available
        """
        super().__init__(message)
        self.status_code = status_code


class ParsingError(GoogleSearchError):
    """Raised when HTML parsing fails."""

    pass


class RateLimitError(GoogleSearchError):
    """Raised when rate limiting is detected."""

    pass


class BlockedError(GoogleSearchError):
    """Raised when the client appears to be blocked by Google."""

    pass
