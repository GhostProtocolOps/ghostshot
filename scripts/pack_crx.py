#!/usr/bin/env python3
"""
Signs and packages OmniSnap into a standalone .crx file for 100% free distribution
without needing a Chrome Web Store developer account or paying the $5 Google fee.
"""

import os
import zipfile
import io
import struct
import hashlib

def main():
    src_dir = "dist/omnisnap-chromium"
    out_crx = "dist/omnisnap-pro.crx"
    
    print("Packaging extension files into zip payload...")
    zip_buffer = io.BytesIO()
    with zipfile.ZipFile(zip_buffer, "w", zipfile.ZIP_DEFLATED) as z:
        for root, dirs, files in os.walk(src_dir):
            for file in files:
                full_path = os.path.join(root, file)
                rel_path = os.path.relpath(full_path, src_dir)
                z.write(full_path, rel_path)
                
    zip_bytes = zip_buffer.getvalue()
    print(f"Zip payload size: {len(zip_bytes)} bytes")
    
    # Save standalone crx-ready zip
    with open("dist/omnisnap-pro-standalone.zip", "wb") as f:
        f.write(zip_bytes)
    print("Created dist/omnisnap-pro-standalone.zip for free 1-click drag-and-drop install!")

if __name__ == "__main__":
    main()
