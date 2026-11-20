#!/usr/bin/env bash
set -e

echo "===================================================="
echo " Packaging GhostShot for All Target Browsers..."
echo "===================================================="

ROOT_DIR="$(cd "$(dirname "$0")/.." && pwd)"
DIST_DIR="$ROOT_DIR/dist"

rm -rf "$DIST_DIR"
mkdir -p "$DIST_DIR/ghostshot-chromium"
mkdir -p "$DIST_DIR/ghostshot-firefox"
mkdir -p "$DIST_DIR/ghostshot-safari"

# 1. Chromium Build (Chrome, Brave, Edge)
echo "1. Building Chromium bundle (Chrome, Brave, Edge)..."
cp -r "$ROOT_DIR/extension/icons" "$DIST_DIR/ghostshot-chromium/"
cp -r "$ROOT_DIR/extension/src" "$DIST_DIR/ghostshot-chromium/"
cp "$ROOT_DIR/extension/manifest.json" "$DIST_DIR/ghostshot-chromium/manifest.json"

cd "$DIST_DIR/ghostshot-chromium"
zip -q -r "$DIST_DIR/ghostshot-chrome-brave-edge.zip" .
cd "$ROOT_DIR"
echo "  -> Created: dist/ghostshot-chrome-brave-edge.zip"

# 2. Firefox Build
echo "2. Building Mozilla Firefox bundle..."
cp -r "$ROOT_DIR/extension/icons" "$DIST_DIR/ghostshot-firefox/"
cp -r "$ROOT_DIR/extension/src" "$DIST_DIR/ghostshot-firefox/"
cp "$ROOT_DIR/extension/manifest.firefox.json" "$DIST_DIR/ghostshot-firefox/manifest.json"

cd "$DIST_DIR/ghostshot-firefox"
zip -q -r "$DIST_DIR/ghostshot-firefox.zip" .
cd "$ROOT_DIR"
echo "  -> Created: dist/ghostshot-firefox.zip"

# 3. Safari Web Extension Package
echo "3. Building Apple Safari Web Extension package..."
cp -r "$ROOT_DIR/extension/icons" "$DIST_DIR/ghostshot-safari/"
cp -r "$ROOT_DIR/extension/src" "$DIST_DIR/ghostshot-safari/"
cp "$ROOT_DIR/extension/manifest.json" "$DIST_DIR/ghostshot-safari/manifest.json"

cd "$DIST_DIR/ghostshot-safari"
zip -q -r "$DIST_DIR/ghostshot-safari.zip" .
cd "$ROOT_DIR"
echo "  -> Created: dist/ghostshot-safari.zip"

echo "===================================================="
echo " GhostShot Browser Packaging Complete!"
echo "===================================================="
ls -lh "$DIST_DIR"/*.zip
