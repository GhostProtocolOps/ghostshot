#!/usr/bin/env python3
"""
Deep Static & Behavioral Analyzer for GoFullPage Chrome Extension
Reverse engineers:
1. Page content script (js/page/index.js)
2. Popup orchestrator (popup.*.js)
3. Capture & Canvas stitching engine (capture.*.js)
4. Editor and Options
"""

import os
import re
import json

SRC_DIR = "reverse-engineering/gofullpage-src"
DEOBF_DIR = "reverse-engineering/deobfuscated"

os.makedirs(DEOBF_DIR, exist_ok=True)

def simple_beautify(js_code):
    # Basic indentation and formatting for readable analysis
    out = []
    indent = 0
    in_str = False
    str_char = ''
    escape = False
    
    i = 0
    n = len(js_code)
    while i < n:
        c = js_code[i]
        
        if escape:
            out.append(c)
            escape = False
            i += 1
            continue
            
        if c == '\\':
            escape = True
            out.append(c)
            i += 1
            continue
            
        if in_str:
            out.append(c)
            if c == str_char:
                in_str = False
            i += 1
            continue
            
        if c in ("'", '"', '`'):
            in_str = True
            str_char = c
            out.append(c)
            i += 1
            continue
            
        if c == '{':
            indent += 1
            out.append('{\n' + '  ' * indent)
        elif c == '}':
            indent = max(0, indent - 1)
            out.append('\n' + '  ' * indent + '}\n' + '  ' * indent)
        elif c == ';':
            out.append(';\n' + '  ' * indent)
        else:
            out.append(c)
        i += 1
        
    return "".join(out)

def analyze_file(filename, rel_path):
    filepath = os.path.join(SRC_DIR, rel_path)
    if not os.path.exists(filepath):
        print(f"File not found: {filepath}")
        return None
        
    with open(filepath, "r", encoding="utf-8", errors="ignore") as f:
        content = f.read()
        
    print(f"\n==========================================")
    print(f"Analyzing: {rel_path} ({len(content)} bytes)")
    print(f"==========================================")
    
    # Extract patterns of interest
    messages = re.findall(r'(\b[a-zA-Z0-9_$]+\.sendMessage\([^)]+\)|chrome\.runtime\.onMessage\.addListener\([^)]+\))', content)
    apis = set(re.findall(r'(chrome\.[a-zA-Z0-9_.]+|window\.[a-zA-Z0-9_.]+|document\.[a-zA-Z0-9_.]+)', content))
    
    # Look for canvas operations
    canvas_ops = set(re.findall(r'(\.getContext\([^)]+\)|\.drawImage\([^)]+\)|\.toDataURL\([^)]+\)|\.toBlob\([^)]+\))', content))
    
    # Look for scroll and dimension calculations
    scroll_ops = set(re.findall(r'([a-zA-Z0-9_.]*(?:scroll(?:To|By|Height|Width|Top|Left)|clientHeight|clientWidth|innerHeight|innerWidth|devicePixelRatio)[a-zA-Z0-9_.]*)', content))
    
    # Look for fixed/sticky handling
    fixed_sticky = set(re.findall(r'([a-zA-Z0-9_.]*(?:fixed|sticky|getComputedStyle|position)[a-zA-Z0-9_.]*)', content, re.IGNORECASE))
    
    print(f"  Chrome / Web APIs used: {len(apis)}")
    print(f"  Canvas operations: {canvas_ops}")
    print(f"  Scroll / Dimension keywords: {scroll_ops}")
    print(f"  Fixed/Sticky keywords: {list(fixed_sticky)[:15]}")
    
    # Save beautified version
    beautified = simple_beautify(content)
    deobf_path = os.path.join(DEOBF_DIR, filename + ".beautified.js")
    with open(deobf_path, "w", encoding="utf-8") as f:
        f.write(beautified)
    print(f"  Saved beautified script to: {deobf_path}")
    
    return {
        "file": rel_path,
        "size": len(content),
        "canvas_ops": list(canvas_ops),
        "scroll_ops": list(scroll_ops),
        "fixed_sticky": list(fixed_sticky),
        "apis": list(apis)
    }

def main():
    targets = [
        ("page_index", "js/page/index.js"),
        ("bg_index", "js/background/index.js"),
        ("capture_main", "capture.2c6db7ae.js"),
        ("popup_orchestrator", "popup.88c38d4b.js"),
        ("popup_main", "popup.c624c211.js"),
        ("options_main", "options.4dd58e80.js"),
    ]
    
    results = {}
    for name, rel_path in targets:
        res = analyze_file(name, rel_path)
        if res:
            results[name] = res
            
    with open("reverse-engineering/analysis_summary.json", "w") as f:
        json.dump(results, f, indent=2)
    print("\nSummary written to reverse-engineering/analysis_summary.json")

if __name__ == "__main__":
    main()
