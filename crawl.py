#!/usr/bin/env python3
"""Batch crawler script for multiple domains."""

import json
from pathlib import Path

import pandas as pd

from google import search

# Read domains from CSV
df = pd.read_csv("comscore_gender.csv")
domains = df.domain.tolist()

# Create results directory if it doesn't exist
results_dir = Path("results")
results_dir.mkdir(exist_ok=True)

# Crawl each domain
for domain in domains:
    save_path = results_dir / f"{domain}.json"

    # Skip if already crawled
    if save_path.exists():
        print(f"Skipping {domain} (already crawled)")
        continue

    print(f"Crawling {domain}...")

    # Collect results
    result_list = []
    try:
        for data in search(f"site:{domain}", tld="com.vn", lang="vi", stop=40):
            result_list.append(data)

        # Save to JSON
        with open(save_path, "w", encoding="utf-8") as f:
            json.dump(result_list, f, ensure_ascii=False, indent=2)

        print(f"✓ Saved {len(result_list)} results to {save_path}")

    except Exception as e:
        print(f"✗ Error crawling {domain}: {e}")
        continue

print("\nAll done!")
