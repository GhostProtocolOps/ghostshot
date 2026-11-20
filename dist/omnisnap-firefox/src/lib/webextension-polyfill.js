/**
 * Universal WebExtension API Bridge
 * Normalizes differences between chrome.* (Chromium, Brave, Edge), browser.* (Firefox), and Safari WebExtensions.
 */
(function(global) {
  if (typeof global.browser === "undefined") {
    if (typeof global.chrome !== "undefined") {
      global.browser = global.chrome;
    }
  }
  
  // Ensure promise-based tab queries and captures where standard callbacks were legacy
  if (global.browser && !global.browser.tabs.queryAsync) {
    global.browser.tabs.queryAsync = function(queryInfo) {
      return new Promise((resolve, reject) => {
        try {
          global.browser.tabs.query(queryInfo, (tabs) => {
            if (global.chrome && global.chrome.runtime.lastError) {
              reject(global.chrome.runtime.lastError);
            } else {
              resolve(tabs);
            }
          });
        } catch (e) {
          reject(e);
        }
      });
    };
  }

  if (global.browser && !global.browser.tabs.captureVisibleTabAsync) {
    global.browser.tabs.captureVisibleTabAsync = function(windowId, options) {
      return new Promise((resolve, reject) => {
        try {
          global.browser.tabs.captureVisibleTab(windowId, options, (dataUrl) => {
            if (global.chrome && global.chrome.runtime.lastError) {
              reject(global.chrome.runtime.lastError);
            } else {
              resolve(dataUrl);
            }
          });
        } catch (e) {
          reject(e);
        }
      });
    };
  }
})(typeof globalThis !== "undefined" ? globalThis : typeof self !== "undefined" ? self : window);
