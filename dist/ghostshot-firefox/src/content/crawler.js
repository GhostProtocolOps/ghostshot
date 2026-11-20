/**
 * GhostShot - Recursive Shadow DOM & Sticky/Fixed Element Crawler
 * Traverses both light DOM and open Shadow DOM trees to discover fixed/sticky elements
 * and cleanly suppresses them during scroll slices to guarantee 100% GoFullPage visual parity.
 * Supports zero-height container anchors (e.g. #top-nav-bar containing absolute #pagetop)
 * and dynamic scroll-triggered header suppression.
 */

window.OmniCrawler = (function () {
  // Map keyed by Element preserving pre-capture styles for idempotent restore
  const originalStylesMap = new Map();

  function walkDom(root, callback) {
    if (!root) return;
    callback(root);

    // If element contains an open shadow root, traverse it
    if (root.shadowRoot) {
      const shadowChildren = root.shadowRoot.children || [];
      for (let i = 0; i < shadowChildren.length; i++) {
        walkDom(shadowChildren[i], callback);
      }
    }

    // Traverse standard children
    const children = root.children || [];
    for (let i = 0; i < children.length; i++) {
      walkDom(children[i], callback);
    }
  }

  function isRenderedFixed(el, style) {
    if (style.position !== "fixed") return false;
    if (style.display === "none") return false;

    // 1. Direct bounding box dimensions
    const rect = el.getBoundingClientRect();
    if (rect.width > 0 && rect.height > 0) return true;

    // 2. Client rects (for inline wrappers or zero-dimension wrappers)
    if (el.getClientRects && el.getClientRects().length > 0) return true;

    // 3. Overflow or scroll dimensions
    if (el.scrollWidth > 0 || el.scrollHeight > 0) return true;

    // 4. Zero-height/zero-width container with non-empty children
    // (e.g. #top-nav-bar has height: 0, but child #pagetop has height: 56)
    if (el.childElementCount > 0) return true;

    return false;
  }

  function isSticky(el, style) {
    const pos = style.position;
    if (pos !== "sticky" && pos !== "-webkit-sticky") return false;
    if (style.display === "none") return false;
    return true;
  }

  function findFixedAndStickyElements() {
    const fixedElements = [];
    const stickyElements = [];

    walkDom(document.body, (el) => {
      if (!el || el === document.body || el === document.documentElement) return;
      if (el.id === "ghostshot-hud-root") return; // Keep HUD visible

      let style;
      try {
        style = window.getComputedStyle(el);
      } catch (e) {
        return;
      }

      if (!style) return;

      if (isRenderedFixed(el, style)) {
        fixedElements.push(el);
      } else if (isSticky(el, style)) {
        stickyElements.push(el);
      }
    });

    return { fixedElements, stickyElements };
  }

  /**
   * Normalizes sticky elements to static positioning during capture.
   * This preserves their exact natural position in the document flow,
   * but prevents them from adhering to the viewport and repeating across scroll slices.
   */
  function normalizeStickyElements(elements) {
    if (!elements || !Array.isArray(elements)) return;
    elements.forEach((el) => {
      if (!el || !el.style) return;
      if (!originalStylesMap.has(el)) {
        originalStylesMap.set(el, {
          type: "sticky",
          position: el.style.position || "",
          top: el.style.top || ""
        });
      }

      el.style.setProperty("position", "static", "important");
      el.style.setProperty("top", "auto", "important");
    });
  }

  /**
   * Hides all fixed elements (headers, subnavs, sidebars, floating widgets).
   * Called on slices > 0 because all fixed elements were already captured in slice 0.
   * Employs display: none !important (removing out-of-flow subtree from rendering)
   * with visibility: hidden and opacity: 0 fail-safes.
   */
  function hideFixedElements(elements) {
    if (!elements || !Array.isArray(elements)) return;
    elements.forEach((el) => {
      if (!el || !el.style) return;
      if (!originalStylesMap.has(el)) {
        originalStylesMap.set(el, {
          type: "fixed",
          display: el.style.display || "",
          visibility: el.style.visibility || "",
          opacity: el.style.opacity || ""
        });
      }

      el.style.setProperty("display", "none", "important");
      el.style.setProperty("visibility", "hidden", "important");
      el.style.setProperty("opacity", "0", "important");
    });
  }

  function restoreElements() {
    for (const [el, orig] of originalStylesMap.entries()) {
      if (!el || !el.style) continue;

      if (orig.type === "sticky") {
        if (orig.position) {
          el.style.position = orig.position;
        } else {
          el.style.removeProperty("position");
        }
        if (orig.top) {
          el.style.top = orig.top;
        } else {
          el.style.removeProperty("top");
        }
      } else if (orig.type === "fixed") {
        if (orig.display) {
          el.style.display = orig.display;
        } else {
          el.style.removeProperty("display");
        }
        if (orig.visibility) {
          el.style.visibility = orig.visibility;
        } else {
          el.style.removeProperty("visibility");
        }
        if (orig.opacity) {
          el.style.opacity = orig.opacity;
        } else {
          el.style.removeProperty("opacity");
        }
      }
    }
    originalStylesMap.clear();
  }

  return {
    findFixedAndStickyElements,
    normalizeStickyElements,
    hideFixedElements,
    restoreElements
  };
})();
