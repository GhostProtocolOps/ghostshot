/**
 * OmniSnap - Options Page Controller
 * Persists user preferences to chrome.storage.local
 */

document.addEventListener("DOMContentLoaded", async () => {
  const elements = {
    pdfFormat: document.getElementById("setting-pdf-format"),
    pdfSmartPage: document.getElementById("setting-pdf-smart-page"),
    pdfInsertLinks: document.getElementById("setting-pdf-insert-links"),
    fmt: document.getElementById("setting-fmt"),
    delay: document.getElementById("setting-delay"),
    stickySuppress: document.getElementById("setting-sticky-suppress"),
    shadowDom: document.getElementById("setting-shadow-dom"),
    fitCopies: document.getElementById("setting-fit-copies"),
    filenameTemplate: document.getElementById("setting-filename-template"),
    saveAs: document.getElementById("setting-save-as"),
    clearCacheBtn: document.getElementById("btn-clear-cache"),
    cacheStatus: document.getElementById("cache-status")
  };

  const DEFAULTS = {
    pdf_format: "full", // Default: 1 Continuous Long Page (No split!)
    pdf_smart_page: true,
    pdf_insert_links: true,
    fmt: "png",
    scrollDelay: 60,
    stickySuppress: true,
    shadowDomEnabled: true,
    fit_copies: true,
    filename_template: "omnisnap-{title}-{date:yyyy-MM-dd-HH_mm_ss}",
    save_as: false
  };

  // Load preferences from storage with fallback to defaults
  chrome.storage.local.get(Object.keys(DEFAULTS), (res) => {
    const config = { ...DEFAULTS, ...res };

    if (elements.pdfFormat) elements.pdfFormat.value = config.pdf_format;
    if (elements.pdfSmartPage) elements.pdfSmartPage.checked = config.pdf_smart_page;
    if (elements.pdfInsertLinks) elements.pdfInsertLinks.checked = config.pdf_insert_links;
    if (elements.fmt) elements.fmt.value = config.fmt;
    if (elements.delay) elements.delay.value = config.scrollDelay;
    if (elements.stickySuppress) elements.stickySuppress.checked = config.stickySuppress;
    if (elements.shadowDom) elements.shadowDom.checked = config.shadowDomEnabled;
    if (elements.fitCopies) elements.fitCopies.checked = config.fit_copies;
    if (elements.filenameTemplate) elements.filenameTemplate.value = config.filename_template;
    if (elements.saveAs) elements.saveAs.checked = config.save_as;
  });

  // Helper to save setting
  function save(key, val) {
    chrome.storage.local.set({ [key]: val });
  }

  // Register change listeners
  elements.pdfFormat.addEventListener("change", () => save("pdf_format", elements.pdfFormat.value));
  elements.pdfSmartPage.addEventListener("change", () => save("pdf_smart_page", elements.pdfSmartPage.checked));
  elements.pdfInsertLinks.addEventListener("change", () => save("pdf_insert_links", elements.pdfInsertLinks.checked));
  elements.fmt.addEventListener("change", () => save("fmt", elements.fmt.value));
  elements.delay.addEventListener("change", () => save("scrollDelay", parseInt(elements.delay.value, 10)));
  elements.stickySuppress.addEventListener("change", () => save("stickySuppress", elements.stickySuppress.checked));
  elements.shadowDom.addEventListener("change", () => save("shadowDomEnabled", elements.shadowDom.checked));
  elements.fitCopies.addEventListener("change", () => save("fit_copies", elements.fitCopies.checked));
  elements.filenameTemplate.addEventListener("input", () => save("filename_template", elements.filenameTemplate.value.trim()));
  elements.saveAs.addEventListener("change", () => save("save_as", elements.saveAs.checked));

  // Clear cache action
  elements.clearCacheBtn.addEventListener("click", () => {
    chrome.storage.local.get(null, (all) => {
      // Preserve core preferences, clear session and cache data
      const preserved = {};
      for (const key of Object.keys(DEFAULTS)) {
        if (key in all) preserved[key] = all[key];
      }
      chrome.storage.local.clear(() => {
        chrome.storage.local.set(preserved, () => {
          elements.cacheStatus.textContent = "Temporary slice cache: 0 MB (Cleared!)";
          alert("Capture cache successfully cleared!");
        });
      });
    });
  });
});
