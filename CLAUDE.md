# CLAUDE.md - Google Search Crawler

## Project Philosophy

This project embodies the principle that **elegant code is inevitable code**. Every component, every function, every line exists not because it can, but because it must. We build tools that feel like natural extensions of the developer's mind.

## Vision

Google Search Crawler is a Python library that makes web scraping feel intuitive. It transforms the complexity of HTTP requests, cookie management, pagination, and HTML parsing into a simple, beautiful generator pattern that any developer can understand in seconds.

## Core Principles

### 1. Simplicity Through Elegance

The entire API surfaces through a single function: `search()`. Everything else is either a convenience wrapper or an internal implementation detail. Users shouldn't need to understand cookies, user agents, or URL encoding to get results.

```python
for result in search('python programming', stop=10):
    print(result['title'], result['url'])
```

That's it. That's the entire interface. Beautiful.

### 2. Generator-First Architecture

We use Python generators not for performance (though that's a bonus), but because they match the mental model perfectly. Search results are inherently sequential and potentially infinite. A generator captures this truth elegantly.

### 3. Fail Gracefully, Always

The web is unpredictable. Google changes their HTML. Networks fail. Rate limits trigger. Our code handles every failure gracefully, logs it properly, and recovers when possible. Users should never see a cryptic stack trace.

### 4. Respect The Web

We implement rate limiting not because we have to, but because it's the right thing to do. We randomize user agents to avoid detection, but we also pause between requests to be respectful. Good tools should make it easy to do the right thing.

## Architecture

### The Three Layers

```
┌─────────────────────────────────────┐
│   API Layer (search, search_images) │
│   - User-facing functions            │
│   - Parameter validation             │
│   - Convenience wrappers             │
└─────────────────────────────────────┘
                  ↓
┌─────────────────────────────────────┐
│   Core Engine (search generator)     │
│   - Pagination logic                 │
│   - Result parsing                   │
│   - Deduplication                    │
└─────────────────────────────────────┘
                  ↓
┌─────────────────────────────────────┐
│   Foundation (get_page, filter)      │
│   - HTTP requests                    │
│   - Cookie management                │
│   - HTML parsing                     │
└─────────────────────────────────────┘
```

### Key Design Decisions

**Why generators over lists?**
- Memory efficiency for large result sets
- Natural pagination handling
- Allows infinite searches
- Matches the sequential nature of web scraping

**Why BeautifulSoup over regex?**
- HTML is not regular - regex fails on edge cases
- BeautifulSoup handles malformed HTML gracefully
- More maintainable when Google changes their markup
- Type-safe DOM traversal

**Why cookie persistence?**
- Reduces the chance of being blocked by Google
- Maintains session state across requests
- More respectful to Google's servers
- Faster subsequent requests

**Why random user agents?**
- Distributes requests across different "browser types"
- Reduces pattern detection
- More resilient against blocking
- Mimics real user behavior

## Code Quality Standards

### Type Safety

Every function has type hints. Every parameter, every return value. This makes the code self-documenting and catches errors at development time, not runtime.

### Error Handling

- Use specific exception types, never bare `except:`
- Always log errors with context
- Retry transient failures with exponential backoff
- Fail fast on unrecoverable errors

### Testing

- Unit tests for all core functions
- Integration tests for HTTP interactions (mocked)
- Property-based tests for edge cases
- Minimum 80% code coverage

### Documentation

- Docstrings for all public functions (Google style)
- Inline comments for non-obvious logic
- Examples in README
- Architecture documentation in CLAUDE.md (this file)

## Development Workflow

### Before You Code

1. **Understand the "why"** - What problem are we solving?
2. **Design the interface** - What should the API feel like?
3. **Consider edge cases** - What can go wrong?
4. **Write tests first** - Define success before implementation

### While You Code

1. **One change, one purpose** - Small, focused commits
2. **Type hints everywhere** - Make the IDE your ally
3. **Log, don't print** - Structured logging for debugging
4. **Test as you go** - Don't batch testing at the end

### After You Code

1. **Run the full suite** - Linters, tests, type checker
2. **Review your diff** - Read your own code critically
3. **Update documentation** - Keep CLAUDE.md in sync
4. **Clean commit messages** - Explain the "why", not the "what"

## Technical Stack

- **Python 3.8+** - Modern Python with type hints
- **BeautifulSoup4** - HTML/XML parsing
- **requests** - HTTP client library (cleaner than urllib)
- **pytest** - Testing framework
- **mypy** - Static type checking
- **black** - Code formatting
- **ruff** - Fast linting

## Project Structure

```
google-search-crawler/
├── google/              # Core library
│   ├── __init__.py     # Main search API
│   ├── config.py       # Configuration management
│   ├── exceptions.py   # Custom exceptions
│   └── utils.py        # Helper functions
├── tests/              # Test suite
│   ├── unit/          # Unit tests
│   ├── integration/   # Integration tests
│   └── conftest.py    # Pytest configuration
├── examples/          # Usage examples
│   ├── basic.py      # Simple search example
│   └── advanced.py   # Advanced features
├── .github/
│   └── workflows/    # CI/CD pipelines
│       └── ci.yml
├── pyproject.toml    # Project metadata & dependencies
├── README.md         # User documentation
└── CLAUDE.md         # This file - Architecture & philosophy
```

## Future Vision

### Near Term (Next Release)

- Async support via `asyncio` for parallel requests
- Built-in caching layer (Redis/SQLite)
- More robust anti-blocking mechanisms
- Structured result objects (not just dicts)

### Long Term (Future Releases)

- Support for other search engines (Bing, DuckDuckGo)
- ML-based result quality scoring
- Natural language query understanding
- GraphQL API for result exploration

## Contributing Philosophy

We don't accept contributions that work. We accept contributions that feel **inevitable**.

Before submitting a PR, ask yourself:
- Is this the simplest solution?
- Would a new user understand this immediately?
- Does this make the library more elegant or more complex?
- Have I considered all edge cases?
- Are there tests that prove this works?

Code is poetry. Make every line sing.

## Lessons Learned

### What Worked

- Generator pattern for search results
- BeautifulSoup for HTML parsing
- Cookie persistence for session management
- Random user agent rotation

### What Didn't Work

- Python 2 support - added complexity for diminishing returns
- Bare exception handlers - hid bugs and made debugging harder
- Hardcoded configuration - reduced flexibility
- Manual dependency management - caused version conflicts

### What We Changed

- Dropped Python 2 support - focused on modern Python (3.8+)
- Added type hints everywhere - caught bugs at dev time
- Implemented structured logging - made debugging trivial
- Added comprehensive tests - increased confidence in changes
- Introduced pre-commit hooks - maintained code quality automatically

## The Bottom Line

This project isn't about crawling Google. It's about showing that even a simple web scraper can be crafted with care, tested thoroughly, and documented beautifully.

It's about proving that **elegance scales**.

Every function, every variable name, every abstraction should make the next developer say, "Of course. That's exactly how it should be."

That's the standard. That's the vision.

---

**"Simplicity is the ultimate sophistication."** - Leonardo da Vinci

Built with ❤️ and an obsession for quality.
