/**
 * GhostShot - Next-Gen Scroll Engine & Container Detector
 * Identifies dynamic scroll containers (SPAs, Notion, Slack, overflow-y divs),
 * executes warmup sweeps, dispatches scroll events, and extracts links.
 */

window.OmniScrollEngine = (function() {
  let originalScrollX = 0;
  let originalScrollY = 0;
  let scrollbarStyleTag = null;

  function findScrollableContainer() {
    // 1. Check if window / documentElement / body scrolls
    const docHeight = Math.max(
      document.body ? document.body.scrollHeight : 0,
      document.documentElement ? document.documentElement.scrollHeight : 0
    );

    if (docHeight > window.innerHeight + 10) {
      return {
        type: "window",
        element: window,
        scrollWidth: Math.max(document.body.scrollWidth, document.documentElement.scrollWidth),
        scrollHeight: docHeight,
        clientWidth: window.innerWidth,
        clientHeight: window.innerHeight
      };
    }

    // 2. Otherwise search for an inner scroll container with overflow-y
    const allDivs = document.querySelectorAll("div, main, section, article");
    let bestContainer = null;
    let maxScroll = 0;

    for (let i = 0; i < allDivs.length; i++) {
      const el = allDivs[i];
      if (el.scrollHeight > el.clientHeight + 50) {
        const style = window.getComputedStyle(el);
        if (style.overflowY === "scroll" || style.overflowY === "auto") {
          if (el.scrollHeight > maxScroll) {
            maxScroll = el.scrollHeight;
            bestContainer = el;
          }
        }
      }
    }

    if (bestContainer) {
      return {
        type: "element",
        element: bestContainer,
        scrollWidth: bestContainer.scrollWidth,
        scrollHeight: bestContainer.scrollHeight,
        clientWidth: bestContainer.clientWidth,
        clientHeight: bestContainer.clientHeight
      };
    }

    // Fallback to window
    return {
      type: "window",
      element: window,
      scrollWidth: window.innerWidth,
      scrollHeight: window.innerHeight,
      clientWidth: window.innerWidth,
      clientHeight: window.innerHeight
    };
  }

  function disableSmoothScrolling(targetElement) {
    if (document.documentElement) {
      document.documentElement.style.setProperty("scroll-behavior", "auto", "important");
    }
    if (document.body) {
      document.body.style.setProperty("scroll-behavior", "auto", "important");
    }
    if (targetElement && targetElement !== window) {
      targetElement.style.setProperty("scroll-behavior", "auto", "important");
    }
  }

  function hideScrollbars() {
    if (!scrollbarStyleTag) {
      scrollbarStyleTag = document.createElement("style");
      scrollbarStyleTag.id = "ghostshot-hide-scrollbars";
      scrollbarStyleTag.textContent = `
        ::-webkit-scrollbar { display: none !important; width: 0 !important; height: 0 !important; }
        html, body, * { scrollbar-width: none !important; -ms-overflow-style: none !important; }
      `;
      document.head.appendChild(scrollbarStyleTag);
    }
  }

  function restoreScrollbars() {
    if (scrollbarStyleTag) {
      scrollbarStyleTag.remove();
      scrollbarStyleTag = null;
    }
  }

  async function scrollToCoordinate(container, x, y) {
    if (container.type === "window") {
      window.scrollTo(x, y);
      window.dispatchEvent(new CustomEvent("scroll"));
    } else {
      container.element.scrollLeft = x;
      container.element.scrollTop = y;
      container.element.dispatchEvent(new CustomEvent("scroll"));
    }
    // Tiny delay to let repaint occur
    await new Promise((r) => setTimeout(r, 20));
  }

  async function warmupPage(container) {
    // Save original position
    originalScrollX = container.type === "window" ? window.scrollX : container.element.scrollLeft;
    originalScrollY = container.type === "window" ? window.scrollY : container.element.scrollTop;

    // Fast scroll to bottom then back to top to trigger dynamic content & lazy loaded images
    await scrollToCoordinate(container, 0, Math.min(container.scrollHeight, 6000));
    await new Promise((r) => setTimeout(r, 60));
    await scrollToCoordinate(container, 0, 0);
    await new Promise((r) => setTimeout(r, 60));
  }

  function restoreScroll(container) {
    if (container) {
      scrollToCoordinate(container, originalScrollX, originalScrollY);
    }
    restoreScrollbars();
  }

  function harvestLinks() {
    const links = [];
    const anchorTags = document.querySelectorAll("a[href]");
    const scrollX = window.scrollX;
    const scrollY = window.scrollY;

    for (let i = 0; i < anchorTags.length; i++) {
      const a = anchorTags[i];
      const rect = a.getBoundingClientRect();
      if (rect.width > 0 && rect.height > 0 && a.href) {
        links.push({
          href: a.href,
          x: rect.left + scrollX,
          y: rect.top + scrollY,
          width: rect.width,
          height: rect.height
        });
      }
    }
    return links;
  }

  return {
    findScrollableContainer,
    disableSmoothScrolling,
    hideScrollbars,
    restoreScrollbars,
    scrollToCoordinate,
    warmupPage,
    restoreScroll,
    harvestLinks
  };
})();
