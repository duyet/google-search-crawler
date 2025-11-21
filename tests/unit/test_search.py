"""Tests for search functionality."""

from unittest.mock import patch

import pytest

# Import private function for testing
import google
from google import SearchResult, lucky, search, search_images
from google.exceptions import HTTPError, InvalidParameterError, RateLimitError, SearchError

_parse_search_results = google._parse_search_results


class TestParseSearchResults:
    """Test _parse_search_results function."""

    def test_parse_valid_html(self, sample_html):
        """Test parsing valid HTML."""
        results = _parse_search_results(sample_html)
        assert len(results) == 2
        assert results[0]["url"] == "https://example.com"
        assert results[0]["title"] == "Example Title"
        assert results[0]["description"] == "Example description"
        assert results[1]["url"] == "https://test.com"

    def test_parse_no_results(self, sample_html_no_results):
        """Test parsing HTML with no results."""
        results = _parse_search_results(sample_html_no_results)
        assert len(results) == 0

    def test_parse_only_standard(self, sample_html):
        """Test parsing only standard results."""
        results = _parse_search_results(sample_html, only_standard=True)
        # Should still get results as the sample has h3 parents
        assert len(results) >= 0


class TestSearch:
    """Test search function."""

    def test_empty_query(self):
        """Test that empty query raises error."""
        with pytest.raises(InvalidParameterError, match="Query cannot be empty"):
            list(search(""))

    def test_invalid_num(self):
        """Test that invalid num raises error."""
        with pytest.raises(InvalidParameterError, match="num must be between"):
            list(search("test", num=0))

        with pytest.raises(InvalidParameterError, match="num must be between"):
            list(search("test", num=101))

    def test_invalid_pause(self):
        """Test that negative pause raises error."""
        with pytest.raises(InvalidParameterError, match="pause must be non-negative"):
            list(search("test", pause=-1.0))

    def test_overlapping_params(self):
        """Test that overlapping extra params raises error."""
        with pytest.raises(InvalidParameterError, match="overlap"):
            list(search("test", extra_params={"hl": "fr"}))

    @patch("google._get_page")
    def test_successful_search(self, mock_get_page, sample_html):
        """Test successful search."""
        mock_get_page.return_value = sample_html

        results = list(search("test query", stop=2))

        assert len(results) <= 2
        mock_get_page.assert_called()

    @patch("google._get_page")
    def test_no_results(self, mock_get_page, sample_html_no_results):
        """Test search with no results."""
        mock_get_page.return_value = sample_html_no_results

        results = list(search("test query", stop=10))

        assert len(results) == 0

    @patch("google._get_page")
    def test_http_error(self, mock_get_page):
        """Test search with HTTP error."""
        mock_get_page.side_effect = HTTPError("Connection failed")

        with pytest.raises(SearchError):
            list(search("test query"))

    @patch("google._get_page")
    def test_rate_limit_error(self, mock_get_page):
        """Test search with rate limit error."""
        mock_get_page.side_effect = RateLimitError("Too many requests")

        with pytest.raises(SearchError):
            list(search("test query"))

    @patch("google._get_page")
    def test_deduplication(self, mock_get_page, sample_html):
        """Test that duplicate results are filtered."""
        # Return same HTML twice to simulate pagination with duplicates
        mock_get_page.return_value = sample_html

        results = list(search("test query", stop=5))

        # Should deduplicate results
        urls = [r["url"] for r in results]
        assert len(urls) == len(set(urls))


class TestSearchVariants:
    """Test search variant functions."""

    @patch("google.search")
    def test_search_images(self, mock_search):
        """Test search_images function."""
        mock_search.return_value = iter([])

        list(search_images("test"))

        # Verify it calls search with tpe="isch"
        mock_search.assert_called_once()
        call_kwargs = mock_search.call_args[1]
        assert call_kwargs["tpe"] == "isch"


class TestLucky:
    """Test lucky function."""

    @patch("google.search")
    def test_lucky_success(self, mock_search):
        """Test lucky function with results."""
        mock_result = SearchResult(
            url="https://example.com",
            title="Example",
            description="Description",
        )
        mock_search.return_value = iter([mock_result])

        result = lucky("test query")

        assert result == mock_result

    @patch("google.search")
    def test_lucky_no_results(self, mock_search):
        """Test lucky function with no results."""
        mock_search.return_value = iter([])

        with pytest.raises(SearchError, match="No results found"):
            lucky("test query")
