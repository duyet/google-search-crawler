#!/usr/bin/env python3
"""Simple example demonstrating Google Search Crawler usage."""

from google import search

# Search keywords
KEYWORDS = "duyetdev"

# Collect results
data = []
for result in search(KEYWORDS, tld="com.vn", lang="vi", stop=10):
    data.append(result)

# Print results
print(f"\nFound {len(data)} results for '{KEYWORDS}':\n")
for i, result in enumerate(data, 1):
    print(f"{i}. {result['title']}")
    print(f"   URL: {result['url']}")
    print(f"   Description: {result['description'][:100]}...")
    print()
