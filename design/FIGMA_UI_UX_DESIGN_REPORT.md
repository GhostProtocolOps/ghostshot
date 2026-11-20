# GhostShot Pro — Complete Figma UI/UX Design Report

**Design Lead**: AI Multi-Model Fleet (FigCraft & `free/gpt-6-luna`)  
**Design System**: OmniDesign Glassmorphic Dark & Light Design System  
**Resolution Grid**: 4px / 8px spatial grid  
**Target Viewports**: Desktop Browser Extension (360px popup, full-screen Studio 1440px+, HUD overlay)

---

## 1. Visual Hierarchy & Design System Foundations

GhostShot Pro delivers an ultra-clean, modern aesthetic inspired by Raycast, Linear, and macOS Sonoma.

### 1.1 Color Tokens
- **Primary Brand Gradient**: `linear-gradient(135deg, #4F46E5 0%, #06B6D4 100%)` (Electric Indigo to Vivid Cyan).
- **Surface Elevation Layers**:
  - `Canvas Background`: `#0F172A` (Tailwind Slate 900)
  - `Card / Modal Surface`: `#1E293B` (Tailwind Slate 800) with `backdrop-filter: blur(16px)`
  - `Hover / Active State`: `#334155` (Tailwind Slate 700)
  - `Hairline Borders`: `1px solid rgba(255, 255, 255, 0.08)`
- **Typography**: Inter / system UI font stack with high readability at 11px–14px sizes.

---

## 2. Comprehensive Screen Specifications

### Screen 1: Extension Action Popup (`popup.html`)
- **Frame Dimensions**: `360px` width x `470px` height.
- **Top Brand Bar**:
  - Logo icon: Dual-ring camera aperture gradient badge.
  - App Name: `GhostShot Pro` with subtle version pill `v2.0`.
  - Right Icon Actions: History clock icon button, Settings gear icon button.
- **Hero Capture Card (Interactive Grid of 4 Modes)**:
  1. **Full Page Capture** (Primary, Glowing border accent):
     - Icon: `Scroll` / Document with down-arrow.
     - Title: "Full Page"
     - Subtitle: "Auto-scroll entire document or container"
     - Badge: `⌥⇧P`
  2. **Selected Region**:
     - Icon: `Crop` / Crosshair.
     - Title: "Crop Region"
     - Subtitle: "Drag to capture exact pixels"
     - Badge: `⌥⇧S`
  3. **Visible Viewport**:
     - Icon: `Monitor` / Screen.
     - Title: "Visible Area"
     - Subtitle: "Instant snapshot without scrolling"
     - Badge: `⌥⇧V`
  4. **Element Picker**:
     - Icon: `Layers` / Inspect.
     - Title: "DOM Element"
     - Subtitle: "Snap specific div, table, or card"
     - Badge: `⌥⇧E`
- **Capture Controls Strip**:
  - Delay Selector: Pill group (`0s`, `1s`, `2s`, `3s`, `5s`).
  - Toggle: "Hide Fixed Navbars" (Checked by default with switch toggle).
  - Format Dropdown: `PNG (Lossless)`, `JPG (Compressed)`, `WebP`.
- **Footer**:
  - Privacy indicator: Shield icon with text: `"100% On-Device • Zero Telemetry"`.

---

### Screen 2: In-Page Capture HUD (`hud.html` / injected)
- **Frame Dimensions**: Floating capsule `280px` width x `52px` height.
- **Positioning**: Fixed top-center (`top: 24px; left: 50%; transform: translateX(-50%)`), `z-index: 2147483647`.
- **Components**:
  - Circular Progress Indicator: SVG circle with gradient stroke showing real-time percent completion (`0%` to `100%`).
  - Text Info: `"Capturing slice 4 of ~12..."` in crisp bold white text.
  - Stop / Cancel Button: Subtle red-tinted pill button `"Cancel (Esc)"`.
  - Motion: Smooth ease-out entrance, fading completely out before capture synthesis so it never appears in the output image.

---

### Screen 3: Studio Screenshot Editor (`studio.html`)
- **Layout**: Full-screen 3-zone layout (Top Navigation, Center Infinite Canvas, Left/Floating Pro Tools, Right Export Sidebar).
- **Top Navigation Bar**:
  - Back Button: Return to captured list.
  - Snapshot Title & Metadata: Editable title, URL breadcrumb, Dimensions (`3840 x 14200 px`), File size estimate.
  - History Controls: Undo (`⌘Z`), Redo (`⇧⌘Z`), Revert to Original.
  - Canvas Zoom: Slider + Presets (`Fit to Screen`, `50%`, `100%`, `200%`).
  - Quick Action: `"Copy to Clipboard"` prominent button with checkmark animation.
- **Annotation & Pro Editing Toolbar**:
  - **Select & Transform**: Move, resize, and rotate annotations.
  - **Crop & Straighten**: Non-destructive cropping handles.
  - **Arrow**: Sleek directional pointers with adjustable stroke and tip styles.
  - **Shapes**: Rectangle, Rounded Box, Circle/Ellipse, Speech Bubble.
  - **Numbered Step Badges**: Auto-incrementing badges (`1`, `2`, `3`...) for documentation, bug reports, and tutorials.
  - **Highlighter**: Semi-transparent vibrant marker overlay.
  - **Privacy Redaction (Blur & Pixelate)**:
    - Gaussian Blur brush/box with radius slider (5px–40px).
    - Mosaic Pixelate box with block size slider.
  - **Freehand Pen**: Smooth bezier curve drawing engine.
  - **Text Callouts**: Rich font styling, background pills, and drop shadows.
- **Mockup Studio Panel (Instant Dribbble / Twitter / Presentation Ready)**:
  - Frame Selector: macOS Dark (traffic lights), macOS Light, Windows 11 Fluent, None.
  - Canvas Padding: `0px`, `24px`, `48px`, `80px`.
  - Background Wallpaper:
    - Transparent (PNG alpha).
    - Solid minimalist tones.
    - Gorgeous Mesh & Linear Gradients (Indigo Glow, Sunset Flare, Emerald Matrix, Deep Space).
  - Realistic Drop Shadow: Multi-layered soft ambient occlusion shadow.

---

### Screen 4: Export & Sharing Dialog
- **Modal Dimensions**: `480px` width x `420px` height.
- **Format Selection Tabs**:
  - `PNG` (Lossless, retina 2x preserved).
  - `JPG` (Quality slider: 75% to 100%).
  - `WebP` (Modern high compression).
  - `PDF Smart Multi-Page` (Splits into A4, Letter, Legal pages without cutting lines of text in half; preserves clickable web hyperlinks!).
  - `PDF Continuous` (Single long sheet).
- **Filename Builder**:
  - Live preview: `GhostShot_google_com_2026-11-20_0515.png`
  - Token chips: `[Domain]`, `[Page Title]`, `[Date]`, `[Time]`.
- **Primary Buttons**:
  - Primary: `"Download Image"` (Large gradient CTA).
  - Secondary: `"Copy to Clipboard"` (Clipboard API with PNG blob).

---

### Screen 5: Options & Preferences Dashboard (`options.html`)
- **Card-based Settings**:
  - **Capture Engine**:
    - Scroll Delay slider (20ms – 500ms for lazy load heavy pages).
    - Auto-detect SPA scroll containers (Notion, Slack, Twitter/X).
    - Shadow DOM recursive inspection toggle.
  - **Shortcuts & Commands**:
    - Configurable keyboard hotkeys for all 4 capture modes.
  - **Storage & Privacy**:
    - Local capture history toggle (IndexedDB).
    - Storage quota meter (e.g. `24.5 MB used`).
    - Clear cache button.
    - Zero external network requests confirmation guarantee.
