/**
 * GhostShot - Background Service Worker
 * Orchestrates multi-slice captures, tab communication, keyboard shortcuts, and Studio opening.
 */

const activeSessions = new Map();

// Listen for keyboard command shortcuts
chrome.commands.onCommand.addListener(async (command) => {
  const [tab] = await chrome.tabs.query({ active: true, currentWindow: true });
  if (!tab || !tab.id) return;

  if (command === "_execute_action" || command === "capture_full") {
    startCapture(tab.id, { mode: "full", delay: 0, hideSticky: true });
  } else if (command === "capture_viewport") {
    startCapture(tab.id, { mode: "viewport", delay: 0 });
  } else if (command === "capture_selected") {
    startCapture(tab.id, { mode: "selected", delay: 0 });
  }
});

// Message listener from popup and content scripts
chrome.runtime.onMessage.addListener((request, sender, sendResponse) => {
  const tabId = sender.tab ? sender.tab.id : request.tabId;

  switch (request.action) {
    case "START_CAPTURE": {
      startCapture(request.tabId, request.options)
        .then((res) => sendResponse({ success: true, session: res }))
        .catch((err) => sendResponse({ success: false, error: err.message }));
      return true; // Keep sendResponse open for async
    }

    case "CAPTURE_VISIBLE_SLICE": {
      // Capture the current visible screen slice
      chrome.tabs.captureVisibleTab(null, { format: "png" }, (dataUrl) => {
        if (chrome.runtime.lastError) {
          sendResponse({ success: false, error: chrome.runtime.lastError.message });
        } else {
          sendResponse({ success: true, dataUrl });
        }
      });
      return true;
    }

    case "FINISH_CAPTURE": {
      handleCaptureComplete(tabId, request.payload)
        .then((res) => sendResponse({ success: true, ...res }))
        .catch((err) => sendResponse({ success: false, error: err.message }));
      return true;
    }

    case "ABORT_CAPTURE": {
      activeSessions.delete(tabId);
      sendResponse({ success: true });
      break;
    }

    case "GET_SESSION_DATA": {
      const session = activeSessions.get(request.sessionId);
      sendResponse({ session: session || null });
      break;
    }
  }
});

async function startCapture(tabId, options) {
  // Ensure content scripts are injected
  try {
    await chrome.scripting.executeScript({
      target: { tabId },
      files: [
        "src/content/crawler.js",
        "src/content/scroll_engine.js",
        "src/content/hud.js"
      ]
    });
  } catch (e) {
    console.warn("Content scripts may already be present or restricted URL:", e);
  }

  // Send message to initiate page capture
  return new Promise((resolve, reject) => {
    chrome.tabs.sendMessage(tabId, { action: "INIT_PAGE_CAPTURE", options }, (response) => {
      if (chrome.runtime.lastError) {
        reject(chrome.runtime.lastError);
      } else {
        resolve(response);
      }
    });
  });
}

async function handleCaptureComplete(tabId, payload) {
  const sessionId = "omni_" + Date.now() + "_" + Math.random().toString(36).substring(2, 9);
  
  // Save captured payload into memory cache
  activeSessions.set(sessionId, {
    sessionId,
    url: payload.url,
    title: payload.title,
    dimensions: payload.dimensions,
    slices: payload.slices,
    links: payload.links || [],
    dpr: payload.dpr || 1.0,
    timestamp: Date.now()
  });

  // Open the Capture Viewer page immediately after capture!
  const captureUrl = chrome.runtime.getURL(`src/capture/capture.html?sessionId=${sessionId}`);
  const newTab = await chrome.tabs.create({ url: captureUrl });
  return { sessionId, tabId: newTab.id };
}

// Lifecycle listeners
chrome.runtime.onInstalled.addListener((details) => {
  if (details.reason === "install") {
    console.log("GhostShot installed successfully!");
  }
});
