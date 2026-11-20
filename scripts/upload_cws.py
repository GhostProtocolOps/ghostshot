#!/usr/bin/env python3
"""
GhostShot - Chrome Web Store Automated Package & Release Pipeline
Handles OAuth2 token exchange, zip package validation, and upload to the
Chrome Web Store Developer API (https://chrome.google.com/webstore/devconsole).
"""

import os
import sys
import json
import zipfile
import hashlib
import argparse
import urllib.request
import urllib.error

DEFAULT_ZIP_PATH = os.path.join(os.path.dirname(__file__), "..", "dist", "ghostshot-chrome-brave-edge.zip")

def calculate_sha256(filepath):
    h = hashlib.sha256()
    with open(filepath, "rb") as f:
        while chunk := f.read(8192):
            h.update(chunk)
    return h.hexdigest()

def inspect_zip(zip_path):
    if not os.path.exists(zip_path):
        raise FileNotFoundError(f"Package zip not found: {zip_path}")

    with zipfile.ZipFile(zip_path, "r") as z:
        namelist = z.namelist()
        if "manifest.json" not in namelist:
            raise ValueError("Invalid extension package: manifest.json missing from root!")
        
        manifest_data = json.loads(z.read("manifest.json").decode("utf-8"))
        size_kb = os.path.getsize(zip_path) / 1024.0
        sha = calculate_sha256(zip_path)
        
        return {
            "name": manifest_data.get("name"),
            "version": manifest_data.get("version"),
            "manifest_version": manifest_data.get("manifest_version"),
            "total_files": len(namelist),
            "size_kb": round(size_kb, 2),
            "sha256": sha
        }

def get_access_token(client_id, client_secret, refresh_token):
    token_url = "https://oauth2.googleapis.com/token"
    payload = json.dumps({
        "client_id": client_id,
        "client_secret": client_secret,
        "refresh_token": refresh_token,
        "grant_type": "refresh_token"
    }).encode("utf-8")

    req = urllib.request.Request(
        token_url,
        data=payload,
        headers={"Content-Type": "application/json"}
    )
    with urllib.request.urlopen(req) as resp:
        data = json.loads(resp.read().decode("utf-8"))
        return data["access_token"]

def upload_to_cws(access_token, item_id, zip_path):
    upload_url = f"https://www.googleapis.com/upload/chromewebstore/v1.1/items/{item_id}"
    with open(zip_path, "rb") as f:
        zip_bytes = f.read()

    req = urllib.request.Request(
        upload_url,
        data=zip_bytes,
        headers={
            "Authorization": f"Bearer {access_token}",
            "x-goog-api-version": "2"
        },
        method="PUT"
    )
    with urllib.request.urlopen(req) as resp:
        return json.loads(resp.read().decode("utf-8"))

def publish_cws(access_token, item_id, target="default"):
    publish_url = f"https://www.googleapis.com/chromewebstore/v1.1/items/{item_id}/publish?publishTarget={target}"
    req = urllib.request.Request(
        publish_url,
        data=b"",
        headers={
            "Authorization": f"Bearer {access_token}",
            "x-goog-api-version": "2",
            "Content-Length": "0"
        },
        method="POST"
    )
    with urllib.request.urlopen(req) as resp:
        return json.loads(resp.read().decode("utf-8"))

def main():
    parser = argparse.ArgumentParser(description="Upload GhostShot extension package to Chrome Web Store")
    parser.add_argument("--zip", default=DEFAULT_ZIP_PATH, help="Path to extension ZIP package")
    parser.add_argument("--item-id", default=os.getenv("CHROME_ITEM_ID"), help="Chrome Web Store Extension Item ID")
    parser.add_argument("--client-id", default=os.getenv("CHROME_CLIENT_ID"), help="Google API Client ID")
    parser.add_argument("--client-secret", default=os.getenv("CHROME_CLIENT_SECRET"), help="Google API Client Secret")
    parser.add_argument("--refresh-token", default=os.getenv("CHROME_REFRESH_TOKEN"), help="OAuth2 Refresh Token")
    parser.add_argument("--publish", action="store_true", help="Automatically submit for review / publish after upload")

    args = parser.parse_args()

    print("==================================================================")
    print(" 🚀 GhostShot - Chrome Web Store Developer Release Pipeline")
    print("==================================================================")

    zip_info = inspect_zip(args.zip)
    print(f"📦 Package Name      : {zip_info['name']}")
    print(f"📌 Version           : {zip_info['version']} (Manifest V{zip_info['manifest_version']})")
    print(f"📁 Total Files       : {zip_info['total_files']} files inside zip")
    print(f"⚖️  Package Size      : {zip_info['size_kb']} KB")
    print(f"🔒 SHA256 Checksum   : {zip_info['sha256']}")
    print(f"📍 Package Location  : {os.path.abspath(args.zip)}")
    print("------------------------------------------------------------------")

    if args.client_id and args.client_secret and args.refresh_token and args.item_id:
        print("🔑 API Credentials detected. Initiating automated CWS upload...")
        try:
            token = get_access_token(args.client_id, args.client_secret, args.refresh_token)
            print("✅ OAuth2 Access Token acquired successfully.")
            
            upload_res = upload_to_cws(token, args.item_id, args.zip)
            print(f"✅ Package uploaded to CWS Item ID {args.item_id}:", json.dumps(upload_res, indent=2))

            if args.publish:
                pub_res = publish_cws(token, args.item_id)
                print(f"✅ Item published to Chrome Web Store:", json.dumps(pub_res, indent=2))
        except Exception as e:
            print(f"❌ CWS API Upload Error: {e}", file=sys.stderr)
            sys.exit(1)
    else:
        print("💡 Automated API credentials (CHROME_ITEM_ID, CHROME_CLIENT_ID, etc.) not set.")
        print("   The verified ZIP is ready for manual 1-click update in the CWS Developer Console:")
        print("   1. Open: https://chrome.google.com/webstore/devconsole")
        print(f"   2. Select your extension item: {args.item_id or 'GhostShot'}")
        print("   3. Click 'Package' -> 'Upload new package'")
        print(f"   4. Upload: {os.path.abspath(args.zip)}")
        print("   5. Submit for Review!")
    print("==================================================================")

if __name__ == "__main__":
    main()
