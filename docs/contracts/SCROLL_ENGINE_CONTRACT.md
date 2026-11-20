# 📜 Component Contract: OmniScrollEngine

> **Module**: `extension/src/content/scroll_engine.js`  
> **Global Identifier**: `window.OmniScrollEngine`  
> **Component Owner**: Chief Systems Architect & Viewport Engineer  
> **OpenDots Reference**: `RFC-010`

---

## 1. Component Purpose & Scope
The `OmniScrollEngine` manages viewport scroll coordinates, identifies dynamic scroll containers (SPAs, Notion, Slack, overflow-y divs), suppresses native smooth scrolling physics for deterministic frame alignment, injects scrollbar suppression rules, and harvests clickable anchor hyperlinks.

---

## 2. API Contract Specification

### `findScrollableContainer(): ScrollContainerDescriptor`
```typescript
interface ScrollContainerDescriptor {
  type: "window" | "element";
  element: Window | HTMLElement;
  scrollWidth: number;
  scrollHeight: number;
  clientWidth: number;
  clientHeight: number;
}
```
- **Detection Algorithm**:
  1. Inspects `Math.max(document.body.scrollHeight, document.documentElement.scrollHeight)`.
  2. If document height exceeds `window.innerHeight + 10px`, selects `window`.
  3. Otherwise, iterates over `<div, main, section, article>` elements, evaluating `getComputedStyle(el).overflowY === 'scroll' || 'auto'`, selecting the element with the maximum `scrollHeight`.
  4. Fallback: returns `window`.

---

### `disableSmoothScrolling(target: Window | HTMLElement): void`
- Sets `scroll-behavior: auto !important` on `document.documentElement`, `document.body`, and `target` to eliminate asynchronous CSS scroll animations during automated capture passes.

---

### `hideScrollbars(): void`
- Injects a dedicated `<style id="ghostshot-hide-scrollbars">` tag into `document.head` disabling `::-webkit-scrollbar` and setting `scrollbar-width: none !important`. Prevents scrollbar bars from being baked into stitched screenshot canvas edges.

---

### `scrollToCoordinate(container: ScrollContainerDescriptor, x: number, y: number): Promise<void>`
- Dispatches instantaneous scroll:
  - If `type === 'window'`: `window.scrollTo(x, y)` followed by `window.dispatchEvent(new CustomEvent("scroll"))`.
  - If `type === 'element'`: `container.element.scrollTop = y` followed by element scroll event.
- Delays `20ms` to guarantee browser paint buffer settles.

---

### `warmupPage(container: ScrollContainerDescriptor): Promise<void>`
- Saves original `scrollX` and `scrollY`.
- Executes a swift vertical sweep down to $\min(\text{scrollHeight}, 6000\text{px})$ and returns to $(0, 0)$.
- **Purpose**: Triggers `IntersectionObserver` callbacks, lazy-loaded images, and responsive DOM components before slice capture starts.

---

### `harvestLinks(): ClickableLinkDescriptor[]`
- Scans `document.querySelectorAll("a[href]")`.
- Computes absolute document-relative coordinates:
  $$x = \text{rect.left} + \text{scrollX}, \quad y = \text{rect.top} + \text{scrollY}$$
- Filters out non-visible links (`width <= 0 || height <= 0`).
- Returns structured link array for downstream PDF link annotation embedding.
