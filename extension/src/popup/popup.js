/**
 * GhostShot - Popup Controller
 */

document.addEventListener("DOMContentLoaded", () => {
  let selectedDelay = 0;

  // Delay pills selector
  const delayPills = document.querySelectorAll("#delay-selector .pill-btn");
  delayPills.forEach((btn) => {
    btn.addEventListener("click", () => {
      delayPills.forEach((p) => p.classList.remove("active"));
      btn.classList.add("active");
      selectedDelay = parseInt(btn.dataset.delay, 10);
    });
  });

  // Full Page Capture
  document.getElementById("btn-capture-full").addEventListener("click", async () => {
    await triggerCapture("full");
  });

  // Selected Area Capture
  document.getElementById("btn-capture-selected").addEventListener("click", async () => {
    await triggerCapture("selected");
  });

  // Visible Viewport Capture
  document.getElementById("btn-capture-viewport").addEventListener("click", async () => {
    await triggerCapture("viewport");
  });

  // Options page
  document.getElementById("btn-options").addEventListener("click", () => {
    if (chrome.runtime.openOptionsPage) {
      chrome.runtime.openOptionsPage();
    } else {
      window.open(chrome.runtime.getURL("src/options/options.html"));
    }
  });

  async function triggerCapture(mode) {
    const [tab] = await chrome.tabs.query({ active: true, currentWindow: true });
    if (!tab || !tab.id) return;

    const hideSticky = document.getElementById("toggle-hide-sticky").checked;

    chrome.runtime.sendMessage(
      {
        action: "START_CAPTURE",
        tabId: tab.id,
        options: {
          mode,
          delay: selectedDelay,
          hideSticky
        }
      },
      (response) => {
        // Close popup as the capture proceeds in-page
        window.close();
      }
    );
  }
});
