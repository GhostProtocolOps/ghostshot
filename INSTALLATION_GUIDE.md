# GhostShot Pro — Cross-Browser Installation & Verification Guide

This guide walks through loading and verifying **GhostShot Pro** across **Chrome, Brave, Edge, Firefox, and Safari**.

---

## 1. Google Chrome, Brave Browser & Microsoft Edge (Manifest V3)

All Chromium-based browsers use the unpacked directory at:  
`file:///Users/nishant/Documents/gravity_work/GhostShot/dist/ghostshot-chromium`

### For Google Chrome:
1. Open Google Chrome.
2. In the URL address bar, navigate to: `chrome://extensions`
3. Toggle on **Developer mode** in the top-right corner.
4. Click the **Load unpacked** button (top-left).
5. Select the directory:
   `/Users/nishant/Documents/gravity_work/GhostShot/dist/ghostshot-chromium`
6. GhostShot Pro will appear in your extensions toolbar! Click the extension pin or press `Alt+Shift+P` (`Option+Shift+P` on Mac).

### For Brave Browser:
1. Open Brave.
2. Navigate to: `brave://extensions`
3. Toggle on **Developer mode** (top-right).
4. Click **Load unpacked** and select:
   `/Users/nishant/Documents/gravity_work/GhostShot/dist/ghostshot-chromium`

### For Microsoft Edge:
1. Open Microsoft Edge.
2. Navigate to: `edge://extensions`
3. Toggle on **Developer mode** in the left sidebar.
4. Click **Load unpacked** and select:
   `/Users/nishant/Documents/gravity_work/GhostShot/dist/ghostshot-chromium`

---

## 2. Mozilla Firefox (Gecko WebExtension)

Firefox uses the bundle at:  
`file:///Users/nishant/Documents/gravity_work/GhostShot/dist/ghostshot-firefox`

1. Open Firefox.
2. In the URL address bar, enter: `about:debugging#/runtime/this-firefox`
3. Click the **Load Temporary Add-on...** button.
4. Browse to and select:
   `/Users/nishant/Documents/gravity_work/GhostShot/dist/ghostshot-firefox/manifest.json`
5. GhostShot Pro is now active in Firefox for testing and capturing.

---

## 3. Apple Safari (macOS Web Extension)

Safari supports W3C WebExtensions natively on macOS Ventura, Sonoma, and Sequoia:

1. Open **Safari**.
2. Go to **Safari > Settings...** (or `Cmd+,`) in the macOS menu bar.
3. Click the **Advanced** tab and check **"Show features for web developers"** (or **"Show Develop menu in menu bar"**).
4. In the Safari menu bar, click the new **Develop** menu and check **"Allow Unsigned Extensions"**.
5. You can now load the unpacked extension directly from:
   `/Users/nishant/Documents/gravity_work/GhostShot/dist/ghostshot-safari`  
   or import the Xcode companion wrapper.

---

## 4. Key Verification Checklist & Features to Test

1. **Full Page Capture**: Press `Option+Shift+P` on a long webpage (e.g. GitHub or Wikipedia). Verify the in-page floating HUD shows progress and opens the Studio editor.
2. **Sticky Header Suppression**: Notice that fixed navigation bars do not repeat across vertical slices.
3. **Studio Editor Annotations**: Test Drawing Arrows, Rectangles, Numbered Step Badges (1, 2, 3), and Privacy Redaction Blur boxes.
4. **Mockup Studio**: Toggle macOS Dark window header, padding, and Indigo Flare gradient background.
5. **1-Click Copy**: Click "Copy Image" and paste directly into Slack, Discord, Twitter, or an image editor.
