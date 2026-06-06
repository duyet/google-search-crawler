# Google Search Crawler

[![CI](https://github.com/duyetdev/google-search-crawler/workflows/CI/badge.svg)](https://github.com/duyetdev/google-search-crawler/actions)
[![Python 3.8+](https://img.shields.io/badge/python-3.8+-blue.svg)](https://www.python.org/downloads/)
[![Code style: black](https://img.shields.io/badge/code%20style-black-000000.svg)](https://github.com/psf/black)
[![Type checked: mypy](https://img.shields.io/badge/type%20checked-mypy-blue.svg)](http://mypy-lang.org/)
[![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)](https://opensource.org/licenses/MIT)

**Elegant Python library for crawling Google Search results with a beautiful, generator-based API.**

Google Search Crawler is a modern, type-safe Python library that makes web scraping feel intuitive. It transforms the complexity of HTTP requests, cookie management, pagination, and HTML parsing into a simple, beautiful generator pattern.

---

## ✨ Features

- **🎯 Simple & Intuitive** - Single function API that just works
- **⚡ Generator-Based** - Memory efficient, handles unlimited results
- **🔒 Type-Safe** - Full type hints for better IDE support
- **🛡️ Robust** - Automatic retries, rate limiting, error handling
- **🎨 Modern Python** - Built for Python 3.8+ with modern best practices
- **🧪 Well-Tested** - Comprehensive test suite with 80%+ coverage
- **📝 Fully Documented** - Clear documentation and examples
- **🔧 Configurable** - YAML/ENV configuration support
- **🎭 Respectful** - Built-in rate limiting and user agent rotation

---

## 📦 Installation

### From PyPI (when published)

```bash
pip install google-search-crawler
```

### From Source

```bash
git clone https://github.com/duyetdev/google-search-crawler.git
cd google-search-crawler
pip install -e .
```

### Development Installation

```bash
git clone https://github.com/duyetdev/google-search-crawler.git
cd google-search-crawler
pip install -r requirements-dev.txt
pre-commit install
```

---

## 🚀 Quick Start

### Basic Search

```python
from google import search

# Simple search
for result in search('python programming', stop=10):
    print(f"{result['title']}: {result['url']}")
```

### Advanced Usage

```python
from google import search

# Search with custom parameters
results = search(
    query='machine learning',
    tld='com',           # Top-level domain
    lang='en',           # Language
    num=10,              # Results per page
    stop=50,             # Total results to retrieve
    pause=2.0,           # Pause between requests (seconds)
)

for result in results:
    print(f"Title: {result['title']}")
    print(f"URL: {result['url']}")
    print(f"Description: {result['description']}")
    print("---")
```

### Search Images, News, Videos

```python
from google import search_images, search_news, search_videos

# Search for images
for result in search_images('cats', stop=20):
    print(result['url'])

# Search for news
for result in search_news('technology', stop=10):
    print(result['title'])

# Search for videos
for result in search_videos('python tutorial', stop=15):
    print(result['url'])
```

### "I'm Feeling Lucky" - Get First Result

```python
from google import lucky

# Get the first result
result = lucky('python documentation')
print(f"First result: {result['url']}")
```

---

## 🎛️ Configuration

### Using Config Object

```python
from google import search
from google.config import Config

# Create custom configuration
config = Config(
    tld='co.uk',
    lang='en-gb',
    num=20,
    pause=3.0,
    timeout=15,
    max_retries=5,
)

# Use configuration in search
for result in search('british history', config=config, stop=30):
    print(result['url'])
```

### Using YAML Configuration

```python
from google import search
from google.config import Config

# Load from YAML file
config = Config.from_yaml('config.yaml')
results = list(search('query', config=config, stop=10))
```

Example `config.yaml`:

```yaml
tld: com.vn
lang: vi
num: 50
pause: 2.5
timeout: 10
max_retries: 3
log_level: INFO
```

### Using Environment Variables

```bash
export GOOGLE_CRAWLER_TLD=co.uk
export GOOGLE_CRAWLER_LANG=en
export GOOGLE_CRAWLER_NUM=20
export GOOGLE_CRAWLER_PAUSE=2.0
```

```python
from google import search
from google.config import Config

# Load from environment variables
config = Config.from_env()
results = list(search('query', config=config))
```

---

## 📚 API Reference

### `search(query, **kwargs)`

Main search function that yields results as dictionaries.

**Parameters:**

- `query` (str): Search query string
- `tld` (str): Top-level domain (default: 'com')
- `lang` (str): Language code (default: 'en')
- `tbs` (str): Time-based search (e.g., 'qdr:h' for last hour)
- `safe` (str): Safe search mode ('off', 'medium', 'high')
- `num` (int): Results per page, 1-100 (default: 10)
- `start` (int): Starting index (default: 0)
- `stop` (int | None): Maximum results (None for unlimited)
- `pause` (float): Pause between requests in seconds (default: 2.0)
- `only_standard` (bool): Return only standard results (default: False)
- `extra_params` (dict): Additional URL parameters
- `tpe` (str): Search type ('isch', 'nws', 'vid', etc.)
- `user_agent` (str | None): Custom user agent
- `config` (Config | None): Configuration object

**Returns:** Generator yielding `SearchResult` dictionaries

**SearchResult Structure:**

```python
{
    'url': str,          # Result URL
    'title': str,        # Result title
    'description': str,  # Result description/snippet
}
```

**Raises:**

- `InvalidParameterError`: Invalid parameters
- `SearchError`: Search operation failed
- `HTTPError`: HTTP request failed
- `ParsingError`: HTML parsing failed
- `RateLimitError`: Rate limit detected
- `BlockedError`: Access blocked by Google

---

## 🔧 Advanced Examples

### Site-Specific Search

```python
from google import search

# Search within a specific domain
for result in search('site:github.com python', stop=20):
    print(result['url'])
```

### Time-Based Search

```python
from google import search

# Search for results from the last 24 hours
for result in search('breaking news', tbs='qdr:d', stop=10):
    print(f"{result['title']} - {result['url']}")

# Time-based search options:
# qdr:h - Past hour
# qdr:d - Past 24 hours
# qdr:w - Past week
# qdr:m - Past month
# qdr:y - Past year
```

### Batch Processing Multiple Domains

```python
from google import search
import json
from pathlib import Path

domains = ['example.com', 'test.com', 'demo.org']
results_dir = Path('results')
results_dir.mkdir(exist_ok=True)

for domain in domains:
    results = []
    for result in search(f'site:{domain}', stop=40):
        results.append(result)

    # Save to JSON
    output_file = results_dir / f'{domain}.json'
    with open(output_file, 'w', encoding='utf-8') as f:
        json.dump(results, f, indent=2, ensure_ascii=False)

    print(f'✓ Saved {len(results)} results for {domain}')
```

### Custom Error Handling

```python
from google import search
from google.exceptions import RateLimitError, BlockedError, SearchError

try:
    results = list(search('sensitive query', stop=100))
except RateLimitError:
    print("⚠️  Rate limit hit. Please wait before trying again.")
except BlockedError:
    print("🚫 Access blocked. Try using a different IP or user agent.")
except SearchError as e:
    print(f"❌ Search failed: {e}")
```

---

## 🧪 Development

### Running Tests

```bash
# Install development dependencies
pip install -r requirements-dev.txt

# Run all tests
pytest

# Run with coverage
pytest --cov=google --cov-report=html

# Run specific test file
pytest tests/unit/test_search.py -v
```

### Code Quality

```bash
# Format code
black google/ tests/

# Sort imports
isort google/ tests/

# Lint code
ruff check google/ tests/

# Type check
mypy google/

# Security scan
bandit -r google/

# Run all checks
pre-commit run --all-files
```

### Pre-commit Hooks

Pre-commit hooks automatically run code quality checks before each commit:

```bash
# Install pre-commit hooks
pre-commit install

# Run manually
pre-commit run --all-files
```

---

## 📖 Project Philosophy

This project embodies the principle that **elegant code is inevitable code**. We believe:

- **Simplicity Through Elegance** - Complex problems deserve simple, intuitive solutions
- **Generator-First** - Infinite streams are natural for search results
- **Type Safety** - Catch errors at development time, not runtime
- **Respectful Crawling** - Built-in rate limiting and best practices
- **Quality Over Speed** - Every line should feel inevitable

Read more in [CLAUDE.md](CLAUDE.md) about our architecture and design decisions.

---

## ⚠️ Important Notes

### Legal & Ethical Considerations

**This library is for educational and research purposes only.**

- Scraping Google Search results may violate [Google's Terms of Service](https://policies.google.com/terms)
- For production use, consider using [Google Custom Search API](https://developers.google.com/custom-search)
- Always respect `robots.txt` and implement proper rate limiting
- Be mindful of the load you place on Google's servers

### Rate Limiting

The library implements respectful rate limiting by default (2 seconds between requests). Please do not:

- Reduce the pause duration below 2 seconds
- Make excessive concurrent requests
- Attempt to bypass rate limiting mechanisms

### Reliability

Google frequently changes their HTML structure. This library:

- May break when Google updates their search results page
- Includes error handling for common failures
- Logs warnings when parsing issues occur

---

## 🤝 Contributing

Contributions are welcome! Please follow these guidelines:

1. **Fork** the repository
2. **Create** a feature branch (`git checkout -b feature/amazing-feature`)
3. **Make** your changes
4. **Test** thoroughly (`pytest`, `pre-commit run --all-files`)
5. **Commit** with clear messages (`git commit -m 'Add amazing feature'`)
6. **Push** to your branch (`git push origin feature/amazing-feature`)
7. **Open** a Pull Request

### Code Standards

- Follow PEP 8 and use `black` for formatting
- Add type hints to all functions
- Write tests for new features
- Update documentation as needed
- Ensure all CI checks pass

---

## 📄 License

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.

Original library by Mario Vilas. Modernized and enhanced by Van-Duyet Le.

---

## 🙏 Acknowledgments

- Original library: [python-google](https://pypi.org/project/google/) by Mario Vilas
- BeautifulSoup4 for HTML parsing
- The Python community for amazing tools and libraries

---

## 📬 Contact & Support

- **Author**: Van-Duyet Le
- **Email**: me@duyetdev.com
- **GitHub**: [@duyetdev](https://github.com/duyetdev)
- **Issues**: [GitHub Issues](https://github.com/duyetdev/google-search-crawler/issues)

---

## 🌟 Star History

If you find this project useful, please consider giving it a star! ⭐

---

**Built with ❤️ and an obsession for quality.**

*"Simplicity is the ultimate sophistication." - Leonardo da Vinci*
