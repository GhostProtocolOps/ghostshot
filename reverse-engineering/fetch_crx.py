#!/usr/bin/env python3
import urllib.request
import zipfile
import io
import os
import sys

EXTENSION_ID = "fdpohaocaechififmbbbbbknoalclacl"
CRX_URL = f"https://clients2.google.com/service/update2/crx?response=redirect&prodversion=128.0&acceptformat=crx2,crx3&x=id%3D{EXTENSION_ID}%26uc"
OUT_DIR = os.path.abspath("reverse-engineering/gofullpage-src")

def unpack_crx(data, out_path):
    # CRX header parsing: CRX3 has header magic 'Cr24' followed by version (3) and header size.
    # The actual zip payload starts right after the CRX header.
    if data[:4] == b'Cr24':
        version = int.from_bytes(data[4:8], 'little')
        if version == 3:
            header_len = int.from_bytes(data[8:12], 'little')
            zip_start = 12 + header_len
        elif version == 2:
            pk_len = int.from_bytes(data[8:12], 'little')
            sig_len = int.from_bytes(data[12:16], 'little')
            zip_start = 16 + pk_len + sig_len
        else:
            raise ValueError(f"Unknown CRX version: {version}")
        zip_bytes = data[zip_start:]
    else:
        # Might already be a pure zip file
        zip_bytes = data

    os.makedirs(out_path, exist_ok=True)
    with zipfile.ZipFile(io.BytesIO(zip_bytes)) as z:
        z.extractall(out_path)
    print(f"Extracted {len(z.namelist())} files into {out_path}")

def main():
    print(f"Downloading GoFullPage CRX ({EXTENSION_ID})...")
    req = urllib.request.Request(
        CRX_URL,
        headers={"User-Agent": "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/128.0.0.0 Safari/537.36"}
    )
    try:
        with urllib.request.urlopen(req, timeout=30) as resp:
            data = resp.read()
            print(f"Downloaded {len(data)} bytes.")
            unpack_crx(data, OUT_DIR)
            print("Successfully unpacked GoFullPage extension!")
    except Exception as e:
        print(f"Error fetching CRX: {e}", file=sys.stderr)
        sys.exit(1)

if __name__ == "__main__":
    main()
