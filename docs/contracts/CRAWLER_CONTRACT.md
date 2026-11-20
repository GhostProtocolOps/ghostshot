# 📜 Component Contract: OmniCrawler

> **Module**: `extension/src/content/crawler.js`  
> **Global Identifier**: `window.OmniCrawler`  
> **Component Owner**: Senior Frontend DOM & CSS Engineer  
> **OpenDots Reference**: `RFC-009`

---

## 1. Component Purpose & Scope
The `OmniCrawler` is responsible for recursively inspecting document hierarchy—including Light DOM elements and open Shadow Roots—to discover elements with CSS positioning constraints (`position: fixed`, `position: sticky`, `position: -webkit-sticky`). It normalizes sticky elements into natural document flow and selectively suppresses fixed chrome on vertical slices $> 0$ to achieve 1:1 visual parity with GoFullPage.

---

## 2. API Contract Specification

### `findFixedAndStickyElements(): { fixedElements: HTMLElement[], stickyElements: HTMLElement[] }`
- **Preconditions**:
  - `document.body` must be loaded and non-null.
- **Behavior**:
  - Recursively walks all child nodes of `document.body`.
  - For each element with an open `shadowRoot`, recursively traverses `shadowRoot.children`.
  - Bypasses `ghostshot-hud-root` to keep the progress UI visible.
  - Resolves computed style via `window.getComputedStyle(el)`.
  - Inspects `el.getBoundingClientRect()`. Filters out elements with `width <= 0 || height <= 0`.
- **Outputs**:
  - `fixedElements`: Array of elements resolving to `position === 'fixed'`.
  - `stickyElements`: Array of elements resolving to `position === 'sticky' || position === '-webkit-sticky'`.
- **Postconditions**:
  - Zero DOM mutations. Pure inspection.

---

### `normalizeStickyElements(elements: HTMLElement[]): void`
- **Preconditions**:
  - `elements` is an array of sticky DOM elements discovered via `findFixedAndStickyElements()`.
- **Behavior**:
  - Caches original `position` and `top` properties in an internal restoration stack:
    ```javascript
    modifiedElements.push({
      element: el,
      type: "sticky",
      originalPosition: el.style.position || "",
      originalTop: el.style.top || ""
    });
    ```
  - Applies atomic overrides:
    ```javascript
    el.style.setProperty("position", "static", "important");
    el.style.setProperty("top", "auto", "important");
    ```
- **Postconditions**:
  - Sticky headers and toolbars remain anchored in their natural layout coordinates in document flow.
  - Sticky elements do not follow the viewport during vertical scrolls.

---

### `hideFixedElements(elements: HTMLElement[]): void`
- **Preconditions**:
  - Must ONLY be called on slice index $> 0$ (after Slice 0 has captured the natural initial viewport view).
- **Behavior**:
  - Caches original `visibility` and `opacity` properties.
  - Applies atomic overrides:
    ```javascript
    el.style.setProperty("visibility", "hidden", "important");
    el.style.setProperty("opacity", "0", "important");
    ```
- **Postconditions**:
  - Fixed headers (`#top-nav-bar`, `#subtopnav`), floating sidebars (`#sidenav`), and chat widgets are invisible during slices $1..N$.
  - Layout space is preserved (elements are NOT set to `display: none`, avoiding document height reflows).

---

### `restoreElements(): void`
- **Behavior**:
  - Pops all records from `modifiedElements` in LIFO order.
  - If original property was non-empty, sets property back to original value.
  - If original property was empty (inherited from stylesheet), removes the inline property via `removeProperty()`.
- **Postconditions**:
  - `document.body` is restored to 100% of its pristine pre-capture visual and functional state.
  - Zero leftover inline styles.

---

## 3. Invariants & Guardrails
1. **Never Mutate Light DOM Hierarchy**: Elements must never be detached, appended, or reparented.
2. **Never Use `display: none`**: Fixed elements must use `visibility: hidden !important` to prevent layout collapse and artificial page shrinkage.
3. **Always Restore**: In the event of user cancellation (<kbd>Esc</kbd>) or capture failure, `restoreElements()` must execute in a `finally` block.
