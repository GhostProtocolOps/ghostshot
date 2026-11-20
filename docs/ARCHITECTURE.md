# GhostShot — System Architecture & Technical Specifications

GhostShot is a modern, high-performance browser extension designed for high-resolution full-page screenshot capture, nested scroll container snapshots, and integrated client-side annotation studio.

---

## 1. High-Level Architecture Overview

GhostShot operates across three isolated browser execution tiers connected via asynchronous messaging channels:

```
┌────────────────────────────────────────────────────────────────────────┐
│                        GhostShot Architecture                           │
└────────────────────────────────────────────────────────────────────────┘
                               │
               ┌───────────────┴───────────────┐
               ▼                               ▼
       [ popup.html / JS ]            [ background worker ]
       • Modern Glassmorphic UI       • Central capture coordinator
       • 4 Capture mode triggers      • Tab stream capture orchestrator
       • Shortcuts & quick settings   • Storage & download dispatch
               │                               │
               │ (chrome.tabs.sendMessage)     │ (chrome.tabs.captureVisibleTab)
               ▼                               ▼
       [ content scripts ]            [ capture / studio tab ]
       • scroll_engine.js             • Multi-tile canvas stitcher
       • crawler.js (containers)      • Built-in annotation studio
       • hud.js (floating progress)   • Client-side PDF 1.4 stream compiler
       • Sticky header suppressor     • Clipboard & lossless export
```

---

## 2. Core Subsystems

### 2.1 Dynamic Scroll Engine & DOM Traversal (`src/content/scroll_engine.js`)
- **Recursive Shadow DOM Walker**: Unlike legacy screenshot tools that only traverse the light DOM, GhostShot traverses open Shadow DOM roots (`element.shadowRoot`) to support modern Web Components (e.g. Lit, Salesforce LWC, YouTube components).
- **Coordinate Clamping**: Accurately computes true scrollable boundaries using `document.scrollingElement.scrollHeight`, `document.documentElement.clientHeight`, and viewport device pixel ratios (DPR).
- **Adaptive Scroll Warmup**: Progressively pre-scrolls dynamic Single Page Applications (SPAs) to trigger lazy-loaded media, virtualized lists, and dynamic DOM mounts before slice ingestion.

### 2.2 Intelligent Sticky / Fixed Header Suppressor
- Detects `position: fixed` and `position: sticky` elements along the viewport edges.
- Temporarily suppresses fixed banners on intermediate scroll slices (`visibility: hidden !important`) and restores original computed styles after capture completes.
- Eliminates duplicated repeating headers across stitched captures.

### 2.3 Nested Scroll Container Snip (`src/content/crawler.js`)
- Automatically identifies scrollable inner elements (`overflow-y: auto / scroll` with `scrollHeight > clientHeight + 50`).
- Allows users to capture independent document widgets (Notion databases, Slack threads, Twitter feeds, code viewers) without scrolling the entire outer page.

### 2.4 Multi-Tile Canvas Partitioning (`src/capture/stitcher.js` & `crates/ghostshot-core`)
- Standard browser canvas implementations crash or produce blank images when canvas dimensions exceed hardware limits (typically 16,384px or 32,768px on WebKit / Blink).
- GhostShot dynamically partitions ultra-tall captures (>20,000px) into a vertical strip of managed canvas tiles, ensuring zero memory overflows on high-DPI Retina screens.

### 2.5 Built-In Annotation Studio (`src/studio/studio.js`)
- **Vector Overlay Layer**: Independent canvas overlay for arrows, rectangles, ellipses, text callouts, freehand curves, and semi-transparent highlighters.
- **Auto-Incrementing Step Badges**: Automated numbered markers (1, 2, 3...) with customizable palette schemes for bug reporting and SOP generation.
- **Privacy Redaction Engine**: Pure client-side Gaussian blur and pixelation filters to obscure passwords, API keys, and sensitive data before export.
- **Mockup Presentation Studio**: Wraps captures in macOS Dark/Light or Windows 11 window frames with custom gradient backdrops and ambient drop shadows.

### 2.6 Native Client-Side PDF Engine (`src/capture/pdf_engine.js`)
- **Single Continuous Long Page PDF**: Generates a single, seamless PDF document matching the exact pixel/point height of the web page without artificial page breaks.
- **Smart Multi-Page A4 / Letter Pagination**: Scans horizontal raster lines for whitespace gaps between text blocks to split multi-page documents without cutting text lines in half.
- **Hyperlink Preservation**: Detects anchor tags (`<a>`) in the original DOM and embeds clickable PDF link annotations (`/Type /Annot /Subtype /Link /A << /S /URI /URI (...) >>`).

---

## 3. Privacy & Security Model

- **Zero Telemetry**: GhostShot contains zero third-party analytics trackers, cookies, or remote reporting endpoints.
- **100% On-Device Processing**: All image assembly, canvas rendering, annotation manipulation, and PDF compilation take place inside the browser's local sandbox memory.
- **No Remote Servers**: No captures or user data ever leave the local machine.
