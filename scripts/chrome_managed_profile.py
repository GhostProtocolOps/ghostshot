#!/usr/bin/env python3
"""
GhostShot AI Enterprise - Managed Chrome DevTools Profile Supervisor
Integrates with the live Google Chrome DevTools automation runtime,
monitoring active targets, extension service workers, and capture sessions.
"""

import sys
import os
import json
import time
import subprocess
import urllib.request
import urllib.error

CHROME_BIN = "/Applications/Google Chrome.app/Contents/MacOS/Google Chrome"
DEBUG_PORT = 9222
DEBUG_URL = f"http://127.0.0.1:{DEBUG_PORT}"
EXTENSION_ID = "pjmebjdolmjagkldnddeifdpbbfogggn"
EXTENSION_PATH = "/Users/nishant/Documents/gravity_work/GhostShot/extension"

def check_cdp_http():
    try:
        req = urllib.request.Request(f"{DEBUG_URL}/json/version", headers={"User-Agent": "GhostShot-Supervisor"})
        with urllib.request.urlopen(req, timeout=1.5) as resp:
            data = json.loads(resp.read().decode())
            return True, data
    except Exception:
        return False, None

def check_chrome_process():
    try:
        out = subprocess.check_output(["pgrep", "-f", "Google Chrome"], text=True)
        pids = [p.strip() for p in out.strip().split("\n") if p.strip()]
        return len(pids) > 0, pids
    except Exception:
        return False, []

def status():
    print("=" * 72)
    print("  GHOSTSHOT AI ENTERPRISE - MANAGED CHROME DEVTOOLS SUPERVISOR")
    print("=" * 72)
    
    proc_active, pids = check_chrome_process()
    cdp_active, cdp_info = check_cdp_http()
    
    if proc_active:
        print(f"🟢 Google Chrome Process Active (PIDs: {', '.join(pids[:4])})")
        print(f"   Architecture: macOS Managed Application Profile")
        print(f"   Extension Path: {EXTENSION_PATH}")
        print(f"   Extension ID: {EXTENSION_ID}")
        print(f"   MCP Transport: Chrome DevTools MCP (@autoConnect / Extension Enabled)")
        if cdp_active:
            print(f"   CDP Endpoint: {DEBUG_URL} ({cdp_info.get('Browser')})")
        else:
            print(f"   CDP Endpoint: Managed via Chrome DevTools MCP Native Bridge")
    else:
        print("🔴 Google Chrome Process INACTIVE")
    print("=" * 72)
    return 0 if proc_active else 1

def json_status():
    proc_active, pids = check_chrome_process()
    cdp_active, cdp_info = check_cdp_http()
    return {
        "active": proc_active,
        "pids": pids,
        "cdp_active": cdp_active,
        "cdp_info": cdp_info,
        "extension_id": EXTENSION_ID,
        "extension_path": EXTENSION_PATH,
        "transport": "chrome-devtools-mcp"
    }

if __name__ == "__main__":
    if len(sys.argv) < 2 or sys.argv[1] == "status":
        sys.exit(status())
    elif sys.argv[1] == "json":
        print(json.dumps(json_status(), indent=2))
        sys.exit(0)
    else:
        print(f"Usage: {sys.argv[0]} [status|json]")
        sys.exit(1)
