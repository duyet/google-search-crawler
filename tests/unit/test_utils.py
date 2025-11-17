"""Tests for utils module."""

from pathlib import Path

from google.utils import (
    build_search_url,
    filter_result,
    get_random_user_agent,
    load_user_agents,
)


class TestLoadUserAgents:
    """Test load_user_agents function."""

    def test_load_from_file(self, user_agents_file):
        """Test loading user agents from file."""
        user_agents = load_user_agents(user_agents_file)
        assert len(user_agents) == 3
        assert "Windows" in user_agents[0]
        assert "Macintosh" in user_agents[1]
        assert "Linux" in user_agents[2]

    def test_load_from_nonexistent_file(self):
        """Test loading from non-existent file returns default."""
        user_agents = load_user_agents(Path("/nonexistent/file.txt"))
        assert len(user_agents) > 0
        assert "Mozilla" in user_agents[0]

    def test_load_default_location(self):
        """Test loading from default location."""
        # This will use the actual user_agents.txt file in the package
        user_agents = load_user_agents()
        assert len(user_agents) > 0


class TestGetRandomUserAgent:
    """Test get_random_user_agent function."""

    def test_random_selection(self):
        """Test that a random user agent is returned."""
        user_agents = ["UA1", "UA2", "UA3"]
        ua = get_random_user_agent(user_agents)
        assert ua in user_agents

    def test_none_user_agents(self):
        """Test with None user agents list."""
        ua = get_random_user_agent(None)
        assert isinstance(ua, str)
        assert len(ua) > 0

    def test_empty_list(self):
        """Test with empty user agents list."""
        ua = get_random_user_agent([])
        assert isinstance(ua, str)
        assert "Mozilla" in ua


class TestFilterResult:
    """Test filter_result function."""

    def test_valid_url(self):
        """Test filtering valid external URL."""
        url = "https://example.com/page"
        result = filter_result(url)
        assert result == url

    def test_google_url(self):
        """Test filtering Google URL returns None."""
        url = "https://www.google.com/search"
        result = filter_result(url)
        assert result is None

    def test_encoded_url(self):
        """Test filtering encoded URL."""
        url = "/url?q=https://example.com&sa=U"
        result = filter_result(url)
        assert result == "https://example.com"

    def test_encoded_google_url(self):
        """Test filtering encoded Google URL returns None."""
        url = "/url?q=https://google.com/search&sa=U"
        result = filter_result(url)
        assert result is None

    def test_invalid_url(self):
        """Test filtering invalid URL returns None."""
        url = "not-a-url"
        result = filter_result(url)
        assert result is None

    def test_relative_url(self):
        """Test filtering relative URL returns None."""
        url = "/search?q=test"
        result = filter_result(url)
        assert result is None


class TestBuildSearchUrl:
    """Test build_search_url function."""

    def test_basic_url(self):
        """Test building basic search URL."""
        url = build_search_url(
            query="test",
            tld="com",
            lang="en",
        )
        assert "google.com" in url
        assert "hl=en" in url
        assert "q=test" in url

    def test_with_num(self):
        """Test building URL with custom num."""
        url = build_search_url(
            query="test",
            num=50,
        )
        assert "num=50" in url

    def test_with_start(self):
        """Test building URL with start parameter."""
        url = build_search_url(
            query="test",
            start=10,
        )
        assert "start=10" in url

    def test_with_search_type(self):
        """Test building URL with search type."""
        url = build_search_url(
            query="test",
            tpe="isch",
        )
        assert "tbm=isch" in url

    def test_with_extra_params(self):
        """Test building URL with extra parameters."""
        url = build_search_url(
            query="test",
            extra_params={"filter": "0", "cr": "countryUS"},
        )
        assert "filter=0" in url
        assert "cr=countryUS" in url

    def test_different_tld(self):
        """Test building URL with different TLD."""
        url = build_search_url(
            query="test",
            tld="co.uk",
        )
        assert "google.co.uk" in url

    def test_safe_search(self):
        """Test building URL with safe search."""
        url = build_search_url(
            query="test",
            safe="high",
        )
        assert "safe=high" in url

    def test_time_based_search(self):
        """Test building URL with time-based search."""
        url = build_search_url(
            query="test",
            tbs="qdr:d",
        )
        assert "tbs=qdr:d" in url
