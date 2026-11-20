#!/usr/bin/env bash
set -e

echo "===================================================="
echo " Packaging OmniSnap for All Target Browsers..."
echo "===================================================="

ROOT_DIR="$(cd "$(dirname "$0")/.." && pwd)"
DIST_DIR="$ROOT_DIR/dist"

rm -rf "$DIST_DIR"
mkdir -p "$DIST_DIR/omnisnap-chromium"
mkdir -p "$DIST_DIR/omnisnap-firefox"
mkdir -p "$DIST_DIR/omnisnap-safari"

# 1. Chromium Build (Chrome, Brave, Edge)
echo "1. Building Chromium bundle (Chrome, Brave, Edge)..."
cp -r "$ROOT_DIR/extension/icons" "$DIST_DIR/omnisnap-chromium/"
cp -r "$ROOT_DIR/extension/src" "$DIST_DIR/omnisnap-chromium/"
cp "$ROOT_DIR/extension/manifest.json" "$DIST_DIR/omnisnap-chromium/manifest.json"

cd "$DIST_DIR/omnisnap-chromium"
zip -q -r "$DIST_DIR/omnisnap-chrome-brave-edge.zip" .
cd "$ROOT_DIR"
echo "  -> Created: dist/omnisnap-chrome-brave-edge.zip"

# 2. Firefox Build
echo "2. Building Mozilla Firefox bundle..."
cp -r "$ROOT_DIR/extension/icons" "$DIST_DIR/omnisnap-firefox/"
cp -r "$ROOT_DIR/extension/src" "$DIST_DIR/omnisnap-firefox/"
cp "$ROOT_DIR/extension/manifest.firefox.json" "$DIST_DIR/omnisnap-firefox/manifest.json"

cd "$DIST_DIR/omnisnap-firefox"
zip -q -r "$DIST_DIR/omnisnap-firefox.zip" .
cd "$ROOT_DIR"
echo "  -> Created: dist/omnisnap-firefox.zip"

# 3. Safari Web Extension Package
echo "3. Building Apple Safari Web Extension package..."
cp -r "$ROOT_DIR/extension/icons" "$DIST_DIR/omnisnap-safari/"
cp -r "$ROOT_DIR/extension/src" "$DIST_DIR/omnisnap-safari/"
cp "$ROOT_DIR/extension/manifest.json" "$DIST_DIR/omnisnap-safari/manifest.json"

cd "$DIST_DIR/omnisnap-safari"
zip -q -r "$DIST_DIR/omnisnap-safari.zip" .
cd "$ROOT_DIR"
echo "  -> Created: dist/omnisnap-safari.zip"

echo "===================================================="
echo " OmniSnap Browser Packaging Complete!"
echo "===================================================="
ls -lh "$DIST_DIR"/*.zip
