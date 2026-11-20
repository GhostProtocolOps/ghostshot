#!/usr/bin/env python3
"""
GhostShot AI Company - Managed Chrome DevTools Profile Supervisor
Manages Google Chrome instances with --remote-debugging-port=9222,
--enable-automation, and --enable-extensions for live browser runtime testing.
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
EXTENSION_PATH = "/Users/nishant/Documents/gravity_work/GhostShot/extension"
PROFILE_DIR = os.path.expanduser("~/.gemini/config/chrome-managed-profile")

def is_chrome_debug_active():
    try:
        req = urllib.request.Request(f"{DEBUG_URL}/json/version", headers={"User-Agent": "GhostShot-Supervisor"})
        with urllib.request.urlopen(req, timeout=2) as resp:
            data = json.loads(resp.read().decode())
            return True, data
    except Exception:
        return False, None

def list_debug_pages():
    try:
        req = urllib.request.Request(f"{DEBUG_URL}/json/list", headers={"User-Agent": "GhostShot-Supervisor"})
        with urllib.request.urlopen(req, timeout=2) as resp:
            return json.loads(resp.read().decode())
    except Exception:
        return []

def status():
    active, info = is_chrome_debug_active()
    print("=" * 70)
    print("  GHOSTSHOT AI ENTERPRISE - CHROME DEVTOOLS MANAGED PROFILE")
    print("=" * 70)
    if active:
        print(f"🟢 Chrome Debugger Active on {DEBUG_URL}")
        print(f"   Browser: {info.get('Browser', 'Unknown')}")
        print(f"   V8-Version: {info.get('V8-Version', 'Unknown')}")
        print(f"   WebSocket: {info.get('webSocketDebuggerUrl', 'N/A')}")
        pages = list_debug_pages()
        print(f"   Active Targets ({len(pages)}):")
        for p in pages[:6]:
            print(f"     • [{p.get('type')}] {p.get('title', 'Untitled')} ({p.get('url', '')[:60]}...)")
    else:
        print(f"🔴 Chrome Debugger INACTIVE on port {DEBUG_PORT}")
        print(f"   Managed Profile Path: {PROFILE_DIR}")
        print(f"   Extension Auto-Load: {EXTENSION_PATH}")
    print("=" * 70)
    return 0 if active else 1

def start():
    active, _ = is_chrome_debug_active()
    if active:
        print(f"ℹ️ Chrome DevTools is already running with remote debugging on port {DEBUG_PORT}.")
        return 0

    os.makedirs(PROFILE_DIR, exist_ok=True)
    cmd = [
        CHROME_BIN,
        f"--remote-debugging-port={DEBUG_PORT}",
        "--enable-automation",
        "--enable-extensions",
        f"--load-extension={EXTENSION_PATH}",
        f"--user-data-dir={PROFILE_DIR}",
        "--no-first-run",
        "--no-default-browser-check"
    ]
    print(f"🚀 Launching Chrome with Managed DevTools Profile & Automation Flags...")
    subprocess.Popen(cmd, stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL)
    
    for _ in range(10):
        time.sleep(0.5)
        active, info = is_chrome_debug_active()
        if active:
            print(f"✅ Chrome Managed Profile connected successfully on {DEBUG_URL}!")
            return 0
    
    print("⚠️ Chrome launched, waiting for debugger endpoint...")
    return 0

def stop():
    print("🛑 Stopping Managed Chrome DevTools instance...")
    subprocess.run(["pkill", "-f", f"remote-debugging-port={DEBUG_PORT}"], check=False)
    time.sleep(1)
    print("✅ Stopped.")

if __name__ == "__main__":
    if len(sys.argv) < 2 or sys.argv[1] == "status":
        sys.exit(status())
    elif sys.argv[1] == "start":
        sys.exit(start())
    elif sys.argv[1] == "stop":
        sys.exit(stop())
    elif sys.argv[1] == "json":
        active, info = is_chrome_debug_active()
        pages = list_debug_pages() if active else []
        print(json.dumps({"active": active, "info": info, "pages": pages}, indent=2))
    else:
        print(f"Usage: {sys.argv[0]} [status|start|stop|json]")
        sys.exit(1)
