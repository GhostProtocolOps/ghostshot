/**
 * OmniSnap - Floating Capture HUD
 * In-page animated circular progress ring and live slice counter with Esc/Cancel support.
 */

window.OmniHUD = (function() {
  let hudContainer = null;
  let progressCircle = null;
  let statusText = null;
  let onCancelCallback = null;

  const CIRCUMFERENCE = 2 * Math.PI * 16; // 100.53

  function createHUD(onCancel) {
    onCancelCallback = onCancel;
    if (document.getElementById("omnisnap-hud-root")) return;

    hudContainer = document.createElement("div");
    hudContainer.id = "omnisnap-hud-root";
    hudContainer.innerHTML = `
      <div class="omnisnap-hud-capsule">
        <div class="omnisnap-hud-ring">
          <svg width="40" height="40" viewBox="0 0 40 40">
            <circle cx="20" cy="20" r="16" class="omnisnap-hud-track"></circle>
            <circle cx="20" cy="20" r="16" class="omnisnap-hud-fill" id="omnisnap-hud-circle" transform="rotate(-90 20 20)"></circle>
          </svg>
          <span class="omnisnap-hud-pct" id="omnisnap-hud-pct">0%</span>
        </div>
        <div class="omnisnap-hud-info">
          <div class="omnisnap-hud-title">Capturing Full Page...</div>
          <div class="omnisnap-hud-sub" id="omnisnap-hud-status">Initializing capture engine</div>
        </div>
        <button class="omnisnap-hud-cancel" id="omnisnap-hud-btn-cancel">Cancel (Esc)</button>
      </div>
    `;

    document.body.appendChild(hudContainer);
    progressCircle = document.getElementById("omnisnap-hud-circle");
    statusText = document.getElementById("omnisnap-hud-status");

    document.getElementById("omnisnap-hud-btn-cancel").addEventListener("click", () => {
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
    const fraction = Math.min(1.0, currentSlice / totalSlices);
    const dashOffset = CIRCUMFERENCE * (1 - fraction);
    if (progressCircle) {
      progressCircle.style.strokeDashoffset = dashOffset;
    }
    const pctLabel = document.getElementById("omnisnap-hud-pct");
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
        console.error("OmniSnap capture error:", err);
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

  // Page Warmup
  await scrollEngine.warmupPage(container);

  // Discover fixed headers
  const { fixedHeaders } = crawler.findFixedAndStickyElements();

  const windowHeight = container.clientHeight;
  const windowWidth = container.clientWidth;
  const totalHeight = container.scrollHeight;
  const totalWidth = container.scrollWidth;
  const dpr = window.devicePixelRatio || 1;

  // Plan slices
  const slices = [];
  let currY = 0;
  let sliceIndex = 0;
  const totalSlices = Math.ceil(totalHeight / windowHeight);

  while (currY < totalHeight && !isAborted) {
    hud.updateProgress(sliceIndex + 1, totalSlices);

    // Scroll to position
    await scrollEngine.scrollToCoordinate(container, 0, currY);

    // Apply delay if configured
    if (options && options.delay > 0) {
      await new Promise((r) => setTimeout(r, options.delay * 1000));
    } else {
      await new Promise((r) => setTimeout(r, 60));
    }

    // After step 0, hide fixed headers to avoid repeating headers in subsequent slices
    if (sliceIndex > 0 && fixedHeaders.length > 0) {
      crawler.hideFixedElements(fixedHeaders);
    }

    // Call service worker to capture the visible tab
    const response = await new Promise((resolve) => {
      chrome.runtime.sendMessage({ action: "CAPTURE_VISIBLE_SLICE" }, resolve);
    });

    if (response && response.success && response.dataUrl) {
      slices.push({
        index: sliceIndex,
        y: currY,
        height: Math.min(windowHeight, totalHeight - currY),
        width: windowWidth,
        dataUrl: response.dataUrl
      });
    }

    currY += windowHeight;
    sliceIndex++;
  }

  // Harvest hyperlinks for PDF export
  const links = scrollEngine.harvestLinks();

  // Cleanup
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
