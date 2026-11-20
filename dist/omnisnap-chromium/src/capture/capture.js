/**
 * OmniSnap - Capture Viewer Controller
 * Displays the full stitched screenshot immediately after capture with zoom, pan, and 1-click actions.
 * Supports Single Continuous Long Page PDF (1 page - no split) and multi-page smart splits.
 */

document.addEventListener("DOMContentLoaded", async () => {
  const urlParams = new URLSearchParams(window.location.search);
  const sessionId = urlParams.get("sessionId");

  let currentSession = null;
  let currentZoom = 1.0;
  let stitchedSession = null;

  const canvasWrapper = document.getElementById("canvas-wrapper");
  const minimapCanvas = document.getElementById("minimap-canvas");
  const minimapLens = document.getElementById("minimap-lens");
  const viewerMain = document.getElementById("viewer-main");
  const pdfFormatSelect = document.getElementById("pdf-format-select");
  const downloadImgLabel = document.getElementById("download-img-label");

  // Load user default format settings from storage
  chrome.storage.local.get(["pdf_format", "fmt", "pdf_smart_page", "pdf_insert_links"], (res) => {
    if (res.pdf_format && pdfFormatSelect) {
      pdfFormatSelect.value = res.pdf_format;
    }
    if (res.fmt && downloadImgLabel) {
      downloadImgLabel.textContent = `Download ${res.fmt.toUpperCase()}`;
    }
  });

  // Save format preference on dropdown change
  if (pdfFormatSelect) {
    pdfFormatSelect.addEventListener("change", () => {
      chrome.storage.local.set({ pdf_format: pdfFormatSelect.value });
    });
  }

  // Load session from background service worker
  chrome.runtime.sendMessage({ action: "GET_SESSION_DATA", sessionId }, async (res) => {
    if (res && res.session) {
      currentSession = res.session;
      document.getElementById("display-title").textContent = currentSession.title || "Full Page Capture";
      document.getElementById("display-meta").textContent = 
        `${currentSession.dimensions.totalWidth} × ${currentSession.dimensions.totalHeight} px • ${currentSession.url}`;

      // Stitch captured slices onto canvas tiles
      stitchedSession = await window.OmniStitcher.stitchSlices(currentSession);
      canvasWrapper.innerHTML = ""; // Clear initial elements

      // Append all canvas tiles seamlessly
      stitchedSession.canvasTiles.forEach((tile, idx) => {
        tile.canvas.className = "viewer-tile-canvas";
        tile.canvas.id = `viewer-tile-${idx}`;
        canvasWrapper.appendChild(tile.canvas);
      });

      // Render minimap thumbnail from tiles
      renderMinimap(stitchedSession);

      // Initial Fit Zoom
      fitToWidth();
    } else {
      document.getElementById("display-meta").textContent = "No active capture session found.";
    }
  });

  function renderMinimap(stitched) {
    minimapCanvas.width = 88;
    minimapCanvas.height = 148;
    const mmCtx = minimapCanvas.getContext("2d");
    mmCtx.clearRect(0, 0, 88, 148);

    const totalH = stitched.totalHeightPx;
    let renderedY = 0;

    for (const tile of stitched.canvasTiles) {
      const tileHFrac = tile.height / totalH;
      const mmTileH = tileHFrac * 148;
      mmCtx.drawImage(tile.canvas, 0, 0, tile.width, tile.height, 0, renderedY, 88, mmTileH);
      renderedY += mmTileH;
    }
  }

  // 1. Edit in Studio (Free Annotations, Shapes, Text, Privacy Blur)
  document.getElementById("btn-edit-studio").addEventListener("click", () => {
    window.location.href = `../studio/studio.html?sessionId=${sessionId}`;
  });

  // 2. 1-Click Copy Image to Clipboard
  document.getElementById("btn-copy-image").addEventListener("click", async () => {
    if (!stitchedSession) return;
    const btn = document.getElementById("btn-copy-image");
    const originalText = btn.innerHTML;

    try {
      const exportCanvas = getCompositeCanvas(stitchedSession);
      exportCanvas.toBlob(async (blob) => {
        try {
          await navigator.clipboard.write([
            new ClipboardItem({ "image/png": blob })
          ]);
          btn.innerHTML = "✓ Copied!";
          btn.style.background = "#059669";
          setTimeout(() => {
            btn.innerHTML = originalText;
            btn.style.background = "#10B981";
          }, 2000);
        } catch (e) {
          alert("Clipboard copy failed: " + e.message);
        }
      }, "image/png");
    } catch (e) {
      alert("Copy image error: " + e.message);
    }
  });

  // 3. Download Image (PNG or JPG according to setting)
  document.getElementById("btn-download-image").addEventListener("click", () => {
    if (!stitchedSession) return;
    chrome.storage.local.get(["fmt"], (res) => {
      const fmt = res.fmt || "png";
      const mime = fmt === "jpg" ? "image/jpeg" : "image/png";
      const ext = fmt === "jpg" ? "jpg" : "png";
      const filename = `OmniSnap_${sanitizeFilename(currentSession ? currentSession.title : "screenshot")}.${ext}`;

      const exportCanvas = getCompositeCanvas(stitchedSession);
      exportCanvas.toBlob((blob) => {
        const url = URL.createObjectURL(blob);
        const a = document.createElement("a");
        a.href = url;
        a.download = filename;
        document.body.appendChild(a);
        a.click();
        a.remove();
        URL.revokeObjectURL(url);
      }, mime, 0.94);
    });
  });

  // 4. Download PDF (1 Continuous Long Page or Multi-Page Smart Split)
  document.getElementById("btn-download-pdf").addEventListener("click", async () => {
    if (!stitchedSession) return;
    const btn = document.getElementById("btn-download-pdf");
    const originalText = btn.innerHTML;
    btn.innerHTML = "Generating PDF...";
    btn.style.opacity = "0.7";

    const formatMode = pdfFormatSelect ? pdfFormatSelect.value : "full";

    try {
      const links = currentSession ? currentSession.links : [];
      let pdfBlob;

      if (formatMode === "full") {
        // 1 Continuous Long Page matching full screenshot height (User's preferred setting!)
        pdfBlob = await window.OmniPDF.generateContinuousPDF(stitchedSession.canvasTiles, links);
      } else {
        // Multi-page split (A4, Letter, Legal) with smart whitespace split
        pdfBlob = await window.OmniPDF.generateMultiPagePDF(stitchedSession.canvasTiles, {
          format: formatMode,
          smartSplit: true,
          margin: 20,
          links
        });
      }

      const filename = `OmniSnap_${sanitizeFilename(currentSession ? currentSession.title : "capture")}.pdf`;
      const url = URL.createObjectURL(pdfBlob);
      const a = document.createElement("a");
      a.href = url;
      a.download = filename;
      document.body.appendChild(a);
      a.click();
      a.remove();
      URL.revokeObjectURL(url);
    } catch (e) {
      alert("PDF generation failed: " + e.message);
    } finally {
      btn.innerHTML = originalText;
      btn.style.opacity = "1";
    }
  });

  // 5. Options / Settings Gear
  document.getElementById("btn-settings").addEventListener("click", () => {
    if (chrome.runtime.openOptionsPage) {
      chrome.runtime.openOptionsPage();
    } else {
      window.open("../options/options.html", "_blank");
    }
  });

  // 6. Recent Captures / History
  document.getElementById("btn-history").addEventListener("click", () => {
    alert("OmniSnap Local Session History: All captures are stored securely on-device. Zero telemetry.");
  });

  // 7. Discard / Trash
  document.getElementById("btn-trash").addEventListener("click", () => {
    if (confirm("Discard this screenshot session?")) {
      window.close();
    }
  });

  // Helper to create single composite canvas from tiles when exporting image
  function getCompositeCanvas(stitched) {
    if (stitched.canvasTiles.length === 1) {
      return stitched.canvasTiles[0].canvas;
    }
    const c = document.createElement("canvas");
    c.width = stitched.totalWidthPx;
    c.height = stitched.totalHeightPx;
    const ctx = c.getContext("2d");
    let dy = 0;
    for (const t of stitched.canvasTiles) {
      ctx.drawImage(t.canvas, 0, dy);
      dy += t.height;
    }
    return c;
  }

  // Zoom controls
  document.getElementById("zoom-in").addEventListener("click", () => setZoom(currentZoom + 0.15));
  document.getElementById("zoom-out").addEventListener("click", () => setZoom(Math.max(0.08, currentZoom - 0.15)));
  document.getElementById("zoom-fit").addEventListener("click", fitToWidth);
  document.getElementById("zoom-actual").addEventListener("click", () => setZoom(1.0));

  function setZoom(val) {
    currentZoom = val;
    canvasWrapper.style.transform = `scale(${currentZoom})`;
    document.getElementById("zoom-level").textContent = Math.round(currentZoom * 100) + "%";
    updateMinimapLens();
  }

  function fitToWidth() {
    const vWidth = viewerMain.clientWidth - 80;
    const cWidth = (stitchedSession ? stitchedSession.totalWidthPx : 1200);
    const scale = Math.min(vWidth / cWidth, 1.0);
    setZoom(scale);
  }

  // Update minimap indicator on scroll
  viewerMain.addEventListener("scroll", updateMinimapLens);

  function updateMinimapLens() {
    if (!stitchedSession || !stitchedSession.totalHeightPx) return;
    const totalH = stitchedSession.totalHeightPx * currentZoom;
    const scrollFrac = viewerMain.scrollTop / (viewerMain.scrollHeight - viewerMain.clientHeight || 1);
    const lensHeight = Math.max(16, (viewerMain.clientHeight / (totalH || 1)) * 148);
    const maxTop = 148 - lensHeight;
    minimapLens.style.height = `${lensHeight}px`;
    minimapLens.style.top = `${scrollFrac * maxTop}px`;
  }

  function sanitizeFilename(name) {
    return (name || "capture").replace(/[^a-zA-Z0-9_-]/g, "_").substring(0, 40);
  }
});
