#!/usr/bin/env python3
import re

with open("reverse-engineering/deobfuscated/page_index.beautified.js", "r") as f:
    lines = f.readlines()

print(f"Total lines in page_index.beautified.js: {len(lines)}")

# Search for key functions
keywords = ["_getFixedAndStickyElts", "popAllFixed", "scrollTo", "devicePixelRatio", "originalParams", "capture"]
for kw in keywords:
    print(f"\n--- Matches for '{kw}': ---")
    matches = 0
    for idx, line in enumerate(lines):
        if kw in line:
            start = max(0, idx - 5)
            end = min(len(lines), idx + 15)
            print(f"Around line {idx}:")
            for j in range(start, end):
                print(f"  {j}: {lines[j].rstrip()}")
            matches += 1
            if matches >= 2:
                break
