#!/usr/bin/env python3
import re

with open("reverse-engineering/deobfuscated/capture_main.beautified.js", "r") as f:
    capture_lines = f.readlines()

print("--- Capture canvas stitching search: ---")
for idx, line in enumerate(capture_lines):
    if "drawImage" in line or "getContext" in line or "canvas" in line.lower():
        start = max(0, idx - 3)
        end = min(len(capture_lines), idx + 10)
        print(f"Capture line {idx}:")
        for j in range(start, end):
            print(f"  {j}: {capture_lines[j].rstrip()}")
        break

with open("reverse-engineering/deobfuscated/popup_orchestrator.beautified.js", "r") as f:
    popup_lines = f.readlines()

print("\n--- Popup canvas stitching / captureVisibleTab search: ---")
for idx, line in enumerate(popup_lines):
    if "captureVisibleTab" in line or "toDataURL" in line or "drawImage" in line:
        start = max(0, idx - 3)
        end = min(len(popup_lines), idx + 15)
        print(f"Popup line {idx}:")
        for j in range(start, end):
            print(f"  {j}: {popup_lines[j].rstrip()}")
        break
