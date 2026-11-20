/**
 * GhostShot - Recursive Shadow DOM & Sticky/Fixed Element Crawler
 * Traverses both light DOM and open Shadow DOM trees to discover fixed/sticky elements
 * and cleanly suppresses them during scroll slices to guarantee 100% GoFullPage visual parity.
 */

window.OmniCrawler = (function () {
  const modifiedElements = [];

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

      const position = style.position;
      if (position === "fixed") {
        const rect = el.getBoundingClientRect();
        // Include any fixed element with non-zero dimensions
        if (rect.width > 0 && rect.height > 0) {
          fixedElements.push(el);
        }
      } else if (position === "sticky" || position === "-webkit-sticky") {
        const rect = el.getBoundingClientRect();
        if (rect.width > 0 && rect.height > 0) {
          stickyElements.push(el);
        }
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
      modifiedElements.push({
        element: el,
        type: "sticky",
        originalPosition: el.style.position || "",
        originalTop: el.style.top || ""
      });

      el.style.setProperty("position", "static", "important");
      el.style.setProperty("top", "auto", "important");
    });
  }

  /**
   * Hides all fixed elements (headers, subnavs, sidebars, floating widgets).
   * Called on slices > 0 because all fixed elements were already captured in slice 0.
   */
  function hideFixedElements(elements) {
    if (!elements || !Array.isArray(elements)) return;
    elements.forEach((el) => {
      if (!el || !el.style) return;
      // Don't re-add if already modified
      if (modifiedElements.some((m) => m.element === el && m.type === "fixed")) return;

      modifiedElements.push({
        element: el,
        type: "fixed",
        originalVisibility: el.style.visibility || "",
        originalOpacity: el.style.opacity || ""
      });

      el.style.setProperty("visibility", "hidden", "important");
      el.style.setProperty("opacity", "0", "important");
    });
  }

  function restoreElements() {
    while (modifiedElements.length > 0) {
      const item = modifiedElements.pop();
      if (!item || !item.element || !item.element.style) continue;

      if (item.type === "sticky") {
        if (item.originalPosition) {
          item.element.style.position = item.originalPosition;
        } else {
          item.element.style.removeProperty("position");
        }
        if (item.originalTop) {
          item.element.style.top = item.originalTop;
        } else {
          item.element.style.removeProperty("top");
        }
      } else if (item.type === "fixed") {
        if (item.originalVisibility) {
          item.element.style.visibility = item.originalVisibility;
        } else {
          item.element.style.removeProperty("visibility");
        }
        if (item.originalOpacity) {
          item.element.style.opacity = item.originalOpacity;
        } else {
          item.element.style.removeProperty("opacity");
        }
      }
    }
  }

  return {
    findFixedAndStickyElements,
    normalizeStickyElements,
    hideFixedElements,
    restoreElements
  };
})();
