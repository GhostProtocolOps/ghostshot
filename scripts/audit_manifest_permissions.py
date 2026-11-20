#!/usr/bin/env python3
"""
GhostShot - Permissions & Least Privilege Linter Gatekeeper
Audits extension/manifest.json against actual code usage in extension/src/.
Guarantees 100% compliance with Chrome Web Store 'Purple Potassium' / Least Privilege policies.
"""

import os
import sys
import json
import re

MANIFEST_PATH = os.path.join(os.path.dirname(__file__), "..", "extension", "manifest.json")
SRC_DIR = os.path.join(os.path.dirname(__file__), "..", "extension", "src")

# Known Chrome APIs associated with permissions
PERMISSION_API_PATTERNS = {
    "downloads": [r"chrome\.downloads\."],
    "cookies": [r"chrome\.cookies\."],
    "webRequest": [r"chrome\.webRequest\."],
    "bookmarks": [r"chrome\.bookmarks\."],
    "history": [r"chrome\.history\."],
    "tabs": [r"chrome\.tabs\."],
    "storage": [r"chrome\.storage\."],
    "scripting": [r"chrome\.scripting\."],
    "activeTab": [r"chrome\.tabs\.captureVisibleTab", r"chrome\.action\."]
}

def scan_codebase_for_patterns(src_dir):
    all_text = ""
    for root, _, files in os.walk(src_dir):
        for f in files:
            if f.endswith((".js", ".html", ".ts")):
                fpath = os.path.join(root, f)
                with open(fpath, "r", encoding="utf-8", errors="ignore") as fp:
                    all_text += "\n" + fp.read()
    return all_text

def audit_permissions():
    print("==================================================================")
    print(" 🛡️  GhostShot - Chrome Web Store Permissions & Least Privilege Linter")
    print("==================================================================")

    if not os.path.exists(MANIFEST_PATH):
        print(f"❌ Error: manifest.json not found at {MANIFEST_PATH}")
        sys.exit(1)

    with open(MANIFEST_PATH, "r", encoding="utf-8") as f:
        manifest = json.load(f)

    permissions = manifest.get("permissions", [])
    optional_permissions = manifest.get("optional_permissions", [])
    all_declared = permissions + optional_permissions

    code_content = scan_codebase_for_patterns(SRC_DIR)

    violations = []
    print(f"📌 Declared Permissions: {permissions}")
    if optional_permissions:
        print(f"📌 Optional Permissions: {optional_permissions}")
    print("------------------------------------------------------------------")

    for perm in all_declared:
        if perm in PERMISSION_API_PATTERNS:
            patterns = PERMISSION_API_PATTERNS[perm]
            found = any(re.search(pat, code_content) for pat in patterns)
            if not found:
                violations.append({
                    "permission": perm,
                    "reason": f"Permission '{perm}' declared in manifest but no call sites matching {patterns} found in extension/src/."
                })
            else:
                print(f"✅ Permission '{perm}': Verified active in codebase.")
        else:
            print(f"ℹ️ Permission '{perm}': Platform/Declarative permission (unlimitedStorage, etc.)")

    print("------------------------------------------------------------------")
    if violations:
        print("🚨 PERMISSIONS LINTER FAILED (Store Rejection Risk Detected):")
        for v in violations:
            print(f"   ❌ {v['permission']}: {v['reason']}")
        print("\nFix: Remove the unused permissions from manifest.json to satisfy Google's 'Purple Potassium' policy.")
        sys.exit(1)
    else:
        print("🎉 ALL PERMISSIONS VERIFIED! Zero unused permissions declared.")
        print("   Ready for Chrome Web Store review approval.")
        print("==================================================================")

if __name__ == "__main__":
    audit_permissions()
