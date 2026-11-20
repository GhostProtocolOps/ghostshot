# 📄 RFC-013: Zero-Height Fixed-Container Suppression & Chrome DevTools Managed Profile Integration

> **RFC Identifier**: `RFC-013`  
> **Status**: `APPROVED & IMPLEMENTED`  
> **Author**: Antigravity Multi-Agent Fleet & Review Panel  
> **Target Release**: GhostShot `v2.0.2`  
> **Database References**:  
> - `gravity_sql.review_audit_runs`: `e3d4b791-8845-4209-915f-c96b718814df`  
> - `gravity_jsonb.code_review_findings`: Senior DOM & Browser Rendering Architect  
> - `gravity_vector.architectural_embeddings`: 384-dim normalized vector embeddings  
> - `Paperclip Issues`: `GHO-23`, `GHO-24`, `GHO-25`, `GHO-26`

---

## 1. Executive Summary

During rigorous visual comparison against the GoFullPage reference benchmark on `https://www.w3schools.com/aws/index.php`, a repeating top navigation bar anomaly was diagnosed. While secondary subnav elements (`div#subtopnav`) were successfully hidden, the primary green header (`div#top-nav-bar` containing `div#pagetop`) repeated across every vertical scroll slice (6 times total).

This RFC formalizes:
1. **The Zero-Height Fixed-Container Anomaly**: Root cause analysis of CSS containers where `getBoundingClientRect().height === 0` despite containing rendered absolute descendants.
2. **Idempotent Multi-Slice Suppression Engine**: Upgrading `OmniCrawler` with `Map<Element, StyleState>` caching and dynamic per-slice re-discovery in `OmniHUD`.
3. **Chrome DevTools Managed Profile Integration**: An automated supervisor (`scripts/chrome_managed_profile.py`) enabling `--remote-debugging-port=9222`, `--enable-automation`, and `--enable-extensions` directly within the AI company workflow.

---

## 2. Root Cause Analysis

### 2.1 The CSS Collapsed-Height Trap
On W3Schools, the header hierarchy is constructed as:
```html
<div id="top-nav-bar" class="classic" style="position: fixed; top: 0px; z-index: 100;">
  <div id="pagetop" class="w3-bar notranslate w3-white" style="position: absolute; top: 0px; height: 56px;">
    <!-- Tutorials, References, Exercises, Certificates, Login -->
  </div>
</div>
```
When `window.getComputedStyle(topNavBar)` is evaluated:
- `position`: `"fixed"`
- `getBoundingClientRect()`: `{ x: 0, y: 0, width: 1440, height: 0 }`

Because `height === 0`, previous heuristic `if (rect.width > 0 && rect.height > 0)` discarded `top-nav-bar` from `fixedElements`. And because `#pagetop` resolved to `position: absolute`, it was also discarded. Consequently, `#top-nav-bar` and `#pagetop` remained anchored to the viewport across all scroll slices.

### 2.2 Mathematical Proof of Layout Invariance
Applying `display: none !important` to an element with computed `position: fixed` removes the element and its entire DOM subtree from the render tree. Because fixed elements are out of normal document flow, setting `display: none` produces:
$$\Delta \text{Layout}(\text{body}) = 0$$
No siblings reflow, no scroll heights mutate, and all child elements (including absolute elements) are guaranteed 100% hidden.

---

## 3. Engineering Implementation

### 3.1 `OmniCrawler.isRenderedFixed`
```javascript
function isRenderedFixed(el, style) {
  if (style.position !== "fixed") return false;
  if (style.display === "none") return false;

  // 1. Direct bounding box dimensions
  const rect = el.getBoundingClientRect();
  if (rect.width > 0 && rect.height > 0) return true;

  // 2. Client rects for inline or zero-dimension wrappers
  if (el.getClientRects && el.getClientRects().length > 0) return true;

  // 3. Overflow or scroll dimensions
  if (el.scrollWidth > 0 || el.scrollHeight > 0) return true;

  // 4. Zero-height/zero-width container with non-empty children
  if (el.childElementCount > 0) return true;

  return false;
}
```

### 3.2 Dynamic Re-Discovery in `OmniHUD`
```javascript
// On slices > 0, re-discover fixed elements to catch scroll-injected headers
if (sliceIndex > 0) {
  const { fixedElements: currentFixed } = crawler.findFixedAndStickyElements();
  crawler.hideFixedElements(currentFixed);
  await new Promise((r) => setTimeout(r, 25));
}
```

---

## 4. Managed Chrome Profile Architecture

The AI company now provides automated supervision for Google Chrome:
```
scripts/chrome_managed_profile.py [status | start | stop | json]
```
- **Flags**: `--remote-debugging-port=9222`, `--enable-automation`, `--enable-extensions`, `--load-extension=...`
- **Harness**: Directly connects Chrome DevTools MCP with the real browser profile for continuous automated verification.
