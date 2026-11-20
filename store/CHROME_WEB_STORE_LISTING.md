# Chrome Web Store — Complete Listing & Review Submission Kit

Use this document to fill out the **Chrome Web Store Developer Dashboard** (`https://chrome.google.com/webstore/devconsole`).

---

## 1. Product Details

- **Extension Name**: GhostShot - Full Page Screen Capture & Studio
- **Version**: `2.0.0`
- **Primary Category**: Productivity
- **Secondary Category**: Photos
- **Language**: English (United States)
- **ZIP Package**: `dist/ghostshot-chrome-brave-edge.zip`

---

## 2. Summary & Descriptions

### Short Description (Max 132 Characters):
> Capture full-page screenshots, scroll containers, and edit with pro annotations, privacy blur, and mockups. 100% free & private.

### Detailed Description:
```markdown
GhostShot is the next-generation, 100% free, and private full-page screenshot capture extension and annotation studio.

Tired of screenshot tools that paywall basic features like cropping, annotations, and PDF exports? GhostShot gives you a full-featured professional studio directly in your browser with ZERO paywalls and ZERO tracking telemetry.

━━━━━━━━━━━━━━━━━━━━━━━━━━
⭐ KEY CAPABILITIES
━━━━━━━━━━━━━━━━━━━━━━━━━━

📸 4 POWERFUL CAPTURE MODES
• Full Page Capture (Alt+Shift+P / Option+Shift+P): Automatically scrolls and stitches the entire document.
• Smart Scroll Container Capture: Automatically detects and scrolls inner scrollable containers (Notion, Slack, Twitter/X, linear).
• Selected Region (Alt+Shift+S): Interactive crosshair box to snip exact screen areas.
• Visible Viewport (Alt+Shift+V): Instant 0ms snapshot of what you see on screen.

🎨 BUILT-IN STUDIO EDITOR (100% FREE & UNLIMITED)
• Annotations: Draw crisp Arrows, Rectangles, Circles, Highlighters, and Freehand curves.
• Numbered Step Badges (1, 2, 3...): Auto-incrementing step indicators perfect for QA bug reports, tutorials, and SOPs.
• Privacy Redaction: Blur or Pixelate sensitive credentials, emails, and personal data before sharing.
• Crop & Rotate: Non-destructive crop tool with precision dimension handles.

🖼️ MOCKUP STUDIO (SHARE-READY GRAPHICS)
• Add sleek macOS Dark/Light or Windows 11 window frames with traffic light buttons.
• Wrap captures with curated mesh and linear gradients (Indigo Flare, Sunset, Emerald Matrix).
• Realistic drop shadows for instant publication-ready images on Twitter, LinkedIn, and Dribbble.

⚡ INSTANT EXPORT & SMART PDF
• 1-Click Copy: Copy merged screenshot directly to clipboard as PNG.
• Multi-Format: PNG (Lossless Retina 2x), JPG (with quality slider), WebP.
• Smart Multi-Page PDF: Splits tall pages into clean A4/Letter pages with preserved clickable hyperlinks!

🔒 PRIVACY & ZERO TELEMETRY GUARANTEE
• 100% On-Device: All processing, stitching, and editing happen locally in your browser memory.
• Zero Analytics: No Google Analytics, no tracking pixels, no telemetry.
• Open & Transparent.
```

---

## 3. Single Purpose & Permissions Justification (For Google Reviewers)

When submitting, Google's review team requires an explanation for every requested permission:

| Permission | Reviewer Explanation / Justification |
| :--- | :--- |
| `activeTab` | "Required only when the user explicitly triggers a screenshot capture (via click or keyboard shortcut) to inspect the current tab's dimensions and capture visible slices." |
| `scripting` | "Required to inject the scrolling helper and sticky header suppressor into the active tab to perform vertical slice scrolling." |
| `storage` | "Used solely to store user preferences (e.g. scroll delay timing, default export format) locally on the user's device." |
| `unlimitedStorage` | "Required because high-resolution Retina/4K full-page screenshots can produce large multi-megabyte image drafts that exceed standard 5MB local quota." |
| `downloads` | "Required to save the exported PNG, JPG, WebP, or PDF files to the user's local Downloads folder when they click 'Download'." |

---

## 4. Host Permissions Justification
- **Host Permissions**: `<all_urls>` (Optional)
- **Justification**: "Full-page screenshot capturing must operate on arbitrary web pages that the user navigates to and chooses to capture."


---

## 5. Official Store Visual Assets Catalog

All graphics have been generated and saved to the `store/` folder, ready for direct upload to the Chrome Web Store Developer Console:

### A. Promotional Tiles & Marquee Banners
- **Small Promo Tile (440 × 280 px)**: [store/promo_small_440x280.png](file:///Users/nishant/Documents/gravity_work/GhostShot/store/promo_small_440x280.png)
- **Large Promo Tile (920 × 680 px)**: [store/promo_large_920x680.png](file:///Users/nishant/Documents/gravity_work/GhostShot/store/promo_large_920x680.png)
- **Marquee Banner (1400 × 560 px)**: [store/promo_marquee_1400x560.png](file:///Users/nishant/Documents/gravity_work/GhostShot/store/promo_marquee_1400x560.png)

### B. High-Resolution Store Showcase Screenshots (1280 × 800 px)
1. **Screenshot 1 — 4 Powerful Capture Modes**: [store/screenshot1_action_popup_1280x800.png](file:///Users/nishant/Documents/gravity_work/GhostShot/store/screenshot1_action_popup_1280x800.png)
   - *Caption*: "1-Click Full Page, Selection, Viewport & Scroll Container Capture."
2. **Screenshot 2 — Ultra-Long Page Viewer & Minimap**: [store/screenshot2_long_screenshot_viewer_1280x800.png](file:///Users/nishant/Documents/gravity_work/GhostShot/store/screenshot2_long_screenshot_viewer_1280x800.png)
   - *Caption*: "Stitches 15,000+ px pages with zero memory limits and real-time minimap radar."
3. **Screenshot 3 — 100% Free Annotation Studio**: [store/screenshot3_free_annotation_studio_1280x800.png](file:///Users/nishant/Documents/gravity_work/GhostShot/store/screenshot3_free_annotation_studio_1280x800.png)
   - *Caption*: "Crop, 1-2-3 Step Badges, Privacy Redaction Blur & Mockups with zero subscriptions."
4. **Screenshot 4 — Single Continuous Long Page PDF**: [store/screenshot4_continuous_pdf_export_1280x800.png](file:///Users/nishant/Documents/gravity_work/GhostShot/store/screenshot4_continuous_pdf_export_1280x800.png)
   - *Caption*: "Export 1 seamless endless PDF page without forced splitting or smart A4 split."
5. **Screenshot 5 — 100% Local On-Device Privacy**: [store/screenshot5_privacy_settings_1280x800.png](file:///Users/nishant/Documents/gravity_work/GhostShot/store/screenshot5_privacy_settings_1280x800.png)
   - *Caption*: "Zero tracking, zero analytics, and customizable capture heuristics."

### C. Native FigCraft Design Files
- Master Showcase Project: [design/GhostShot_Store_Showcase.figcraft](file:///Users/nishant/Documents/gravity_work/GhostShot/design/GhostShot_Store_Showcase.figcraft)
- Design Artboard HTML Canvas: [design/ghostshot_design_artboard.html](file:///Users/nishant/Documents/gravity_work/GhostShot/design/ghostshot_design_artboard.html)
