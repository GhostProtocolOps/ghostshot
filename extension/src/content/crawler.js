/**
 * GhostShot - Recursive Shadow DOM & Sticky Element Crawler
 * Traverses both light DOM and open Shadow DOM trees to discover fixed/sticky elements
 * and cleanly suppresses them during scroll slices.
 */

window.OmniCrawler = (function() {
  const modifiedElements = [];

  function isPositioned(style) {
    return style.position === "fixed" || style.position === "sticky";
  }

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
    const fixedHeaders = [];
    const stickyElements = [];
    const fixedOthers = [];
    const viewportHeight = window.innerHeight;
    const viewportWidth = window.innerWidth;

    walkDom(document.body, (el) => {
      if (el === document.body || el === document.documentElement) return;
      
      let style;
      try {
        style = window.getComputedStyle(el);
      } catch (e) {
        return;
      }

      if (!style) return;

      if (style.position === "sticky") {
        stickyElements.push(el);
      } else if (style.position === "fixed") {
        const rect = el.getBoundingClientRect();
        
        // Skip invisible or zero-dimension elements
        if (rect.width === 0 && rect.height === 0) return;

        // Header detection: Element near top of viewport that is not full-screen
        const isNearTop = rect.top <= 40;
        const isNotFullScreen = rect.height < (viewportHeight * 0.7);
        
        if (isNearTop && isNotFullScreen) {
          fixedHeaders.push(el);
        } else {
          fixedOthers.push(el);
        }
      }
    });

    return { fixedHeaders, stickyElements, fixedOthers };
  }

  function hideFixedElements(elements) {
    elements.forEach((el) => {
      // Store original styles to restore later
      modifiedElements.push({
        element: el,
        originalVisibility: el.style.visibility,
        originalOverflow: el.style.overflow
      });

      el.style.setProperty("visibility", "hidden", "important");
      el.style.setProperty("overflow", "hidden", "important");
    });
  }

  function restoreElements() {
    while (modifiedElements.length > 0) {
      const item = modifiedElements.pop();
      if (item.element) {
        item.element.style.visibility = item.originalVisibility;
        item.element.style.overflow = item.originalOverflow;
      }
    }
  }

  return {
    findFixedAndStickyElements,
    hideFixedElements,
    restoreElements
  };
})();
