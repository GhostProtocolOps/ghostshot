/**
 * GhostShot - Floating Capture HUD & Full-Page Orchestrator
 * In-page animated circular progress ring and live slice counter with Esc/Cancel support.
 * Coordinates DOM crawling, scroll sweeps, fixed/sticky element management,
 * and mathematical terminal slice clamping for seamless GoFullPage parity.
 */

window.OmniHUD = (function() {
  let hudContainer = null;
  let progressCircle = null;
  let statusText = null;
  let onCancelCallback = null;

  const CIRCUMFERENCE = 2 * Math.PI * 16; // 100.53

  function createHUD(onCancel) {
    onCancelCallback = onCancel;
    if (document.getElementById("ghostshot-hud-root")) return;

    hudContainer = document.createElement("div");
    hudContainer.id = "ghostshot-hud-root";
    hudContainer.innerHTML = `
      <div class="ghostshot-hud-capsule">
        <div class="ghostshot-hud-ring">
          <svg width="40" height="40" viewBox="0 0 40 40">
            <circle cx="20" cy="20" r="16" class="ghostshot-hud-track"></circle>
            <circle cx="20" cy="20" r="16" class="ghostshot-hud-fill" id="ghostshot-hud-circle" transform="rotate(-90 20 20)"></circle>
          </svg>
          <span class="ghostshot-hud-pct" id="ghostshot-hud-pct">0%</span>
        </div>
        <div class="ghostshot-hud-info">
          <div class="ghostshot-hud-title">Capturing Full Page...</div>
          <div class="ghostshot-hud-sub" id="ghostshot-hud-status">Initializing capture engine</div>
        </div>
        <button class="ghostshot-hud-cancel" id="ghostshot-hud-btn-cancel">Cancel (Esc)</button>
      </div>
    `;

    document.body.appendChild(hudContainer);
    progressCircle = document.getElementById("ghostshot-hud-circle");
    statusText = document.getElementById("ghostshot-hud-status");

    document.getElementById("ghostshot-hud-btn-cancel").addEventListener("click", () => {
      destroyHUD();
      if (onCancelCallback) onCancelCallback();
    });

    window.addEventListener("keydown", handleKeyDown);
  }

  function handleKeyDown(e) {
    if (e.key === "Escape") {
      destroyHUD();
      if (onCancelCallback) onCancelCallback();
    }
  }

  function updateProgress(currentSlice, totalSlices) {
    if (!hudContainer) return;
    const fraction = Math.min(1.0, currentSlice / Math.max(1, totalSlices));
    const dashOffset = CIRCUMFERENCE * (1 - fraction);
    if (progressCircle) {
      progressCircle.style.strokeDashoffset = dashOffset;
    }
    const pctLabel = document.getElementById("ghostshot-hud-pct");
    if (pctLabel) {
      pctLabel.textContent = Math.round(fraction * 100) + "%";
    }
    if (statusText) {
      statusText.textContent = `Slice ${currentSlice} of ~${totalSlices} • Stitching`;
    }
  }

  function destroyHUD() {
    window.removeEventListener("keydown", handleKeyDown);
    if (hudContainer) {
      hudContainer.remove();
      hudContainer = null;
    }
  }

  return {
    createHUD,
    updateProgress,
    destroyHUD
  };
})();

// Content script capture orchestrator:
chrome.runtime.onMessage.addListener((request, sender, sendResponse) => {
  if (request.action === "INIT_PAGE_CAPTURE") {
    executeFullPageCapture(request.options)
      .then((payload) => {
        chrome.runtime.sendMessage({ action: "FINISH_CAPTURE", payload });
        sendResponse({ success: true });
      })
      .catch((err) => {
        console.error("GhostShot capture error:", err);
        sendResponse({ success: false, error: err.message });
      });
    return true; // Keep sendResponse open
  }
});

async function executeFullPageCapture(options) {
  const scrollEngine = window.OmniScrollEngine;
  const crawler = window.OmniCrawler;
  const hud = window.OmniHUD;

  let isAborted = false;
  hud.createHUD(() => {
    isAborted = true;
    crawler.restoreElements();
    scrollEngine.restoreScroll();
  });

  const container = scrollEngine.findScrollableContainer();
  scrollEngine.disableSmoothScrolling(container.element);
  scrollEngine.hideScrollbars();

  // Page Warmup (sweep page to trigger lazy loaded images and responsive DOM)
  await scrollEngine.warmupPage(container);

  // Discover fixed and sticky elements across DOM & open Shadow DOM
  const { fixedElements, stickyElements } = crawler.findFixedAndStickyElements();

  // Normalize sticky elements immediately to static flow so they render in-place
  // without adhering to viewport during subsequent scroll slices
  crawler.normalizeStickyElements(stickyElements);

  // Re-read dimensions after warmup
  const windowHeight = container.clientHeight;
  const windowWidth = container.clientWidth;
  const totalHeight = container.scrollHeight;
  const totalWidth = container.scrollWidth;
  const dpr = window.devicePixelRatio || 1;

  const maxScrollY = Math.max(0, totalHeight - windowHeight);
  const totalSlices = Math.max(1, Math.ceil(totalHeight / windowHeight));

  const slices = [];
  let capturedY = 0;
  let sliceIndex = 0;

  while (capturedY < totalHeight && !isAborted) {
    hud.updateProgress(sliceIndex + 1, totalSlices);

    // Calculate exact target scroll coordinate, clamped to document bounds
    const targetScrollY = Math.min(capturedY, maxScrollY);
    await scrollEngine.scrollToCoordinate(container, 0, targetScrollY);

    // Allow browser painting and dynamic layout settling
    if (options && options.delay > 0) {
      await new Promise((r) => setTimeout(r, options.delay * 1000));
    } else {
      await new Promise((r) => setTimeout(r, 60));
    }

    // After slice 0, hide all fixed elements (headers, sidebars, subnavs)
    // to prevent duplicate repeating bars across the document
    if (sliceIndex > 0 && fixedElements.length > 0) {
      crawler.hideFixedElements(fixedElements);
      // Brief tick for style recalibration
      await new Promise((r) => setTimeout(r, 20));
    }

    // Capture visible tab slice via background service worker
    const response = await new Promise((resolve) => {
      chrome.runtime.sendMessage({ action: "CAPTURE_VISIBLE_SLICE" }, resolve);
    });

    if (response && response.success && response.dataUrl) {
      const actualScrollY = container.type === "window" ? window.scrollY : container.element.scrollTop;

      // Portion from actualScrollY to capturedY was already captured in earlier slices
      const sourceY = Math.max(0, capturedY - actualScrollY);
      const sliceHeight = Math.max(1, Math.min(totalHeight, actualScrollY + windowHeight) - capturedY);

      slices.push({
        index: sliceIndex,
        dataUrl: response.dataUrl,
        sourceX: 0,
        sourceY: sourceY,
        sourceWidth: windowWidth,
        sourceHeight: sliceHeight,
        destX: 0,
        destY: capturedY,
        destWidth: windowWidth,
        destHeight: sliceHeight,
        y: capturedY,
        height: sliceHeight,
        width: windowWidth
      });

      capturedY += sliceHeight;
    } else {
      console.warn("GhostShot: capture slice returned empty response", response);
      capturedY += windowHeight;
    }

    sliceIndex++;

    if (targetScrollY >= maxScrollY && capturedY >= totalHeight) {
      break;
    }
  }

  // Harvest hyperlinks for PDF export
  const links = scrollEngine.harvestLinks();

  // Cleanup & restore DOM
  hud.destroyHUD();
  crawler.restoreElements();
  scrollEngine.restoreScroll(container);

  if (isAborted) {
    throw new Error("Capture cancelled by user");
  }

  return {
    url: window.location.href,
    title: document.title,
    dimensions: {
      totalWidth,
      totalHeight,
      windowWidth,
      windowHeight
    },
    dpr,
    slices,
    links
  };
}
