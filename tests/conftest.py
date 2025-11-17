"""Pytest configuration and fixtures."""


import pytest


@pytest.fixture
def sample_html():
    """Sample Google search results HTML."""
    return """
    <html>
        <div id="search">
            <div>
                <h3><a href="https://example.com">Example Title</a></h3>
                <div class="st">Example description</div>
            </div>
            <div>
                <h3><a href="/url?q=https://test.com&sa=U">Test Title</a></h3>
                <div class="st">Test description</div>
            </div>
        </div>
        <div id="nav">More results</div>
    </html>
    """


@pytest.fixture
def sample_html_no_results():
    """Sample HTML with no search results."""
    return '<html><div id="search"></div></html>'


@pytest.fixture
def user_agents_file(tmp_path):
    """Create a temporary user agents file."""
    ua_file = tmp_path / "user_agents.txt"
    ua_file.write_text(
        "Mozilla/5.0 (Windows NT 10.0; Win64; x64)\n"
        "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7)\n"
        "Mozilla/5.0 (X11; Linux x86_64)\n"
    )
    return ua_file
