/**
 * OmniSnap Studio - Interactive Annotation & Mockup Controller
 */

document.addEventListener("DOMContentLoaded", async () => {
  const urlParams = new URLSearchParams(window.location.search);
  const sessionId = urlParams.get("sessionId");

  let currentSession = null;
  let currentZoom = 1.0;
  let activeTool = "select";
  let activeColor = "#EF4444";
  let activeStrokeWidth = 4;
  let badgeStepCounter = 1;

  const baseCanvas = document.getElementById("base-canvas");
  const annotationCanvas = document.getElementById("annotation-canvas");
  const baseCtx = baseCanvas.getContext("2d");
  const annotCtx = annotationCanvas.getContext("2d");

  // Fetch session data from background worker
  chrome.runtime.sendMessage({ action: "GET_SESSION_DATA", sessionId }, async (res) => {
    if (res && res.session) {
      currentSession = res.session;
      document.getElementById("display-title").textContent = currentSession.title || "Full Page Capture";
      document.getElementById("window-url-display").textContent = currentSession.url || "https://example.com";
      document.getElementById("export-filename").value = `OmniSnap_${sanitizeFilename(currentSession.title || "capture")}.png`;

      // Stitch captured slices using the stitcher engine
      const stitched = await window.OmniStitcher.stitchSlices(currentSession);
      const firstTile = stitched.canvasTiles[0];

      baseCanvas.width = firstTile.width;
      baseCanvas.height = firstTile.height;
      annotationCanvas.width = firstTile.width;
      annotationCanvas.height = firstTile.height;

      baseCtx.drawImage(firstTile.canvas, 0, 0);

      document.getElementById("display-meta").textContent = 
        `${firstTile.width} × ${firstTile.height} px • ${stitched.scale}x Retina DPR`;

      // Auto-fit initial zoom
      fitToScreen();
    } else {
      document.getElementById("display-meta").textContent = "No capture session found.";
    }
  });

  // Tool Switching
  const toolBtns = document.querySelectorAll(".tool-btn");
  toolBtns.forEach((btn) => {
    btn.addEventListener("click", () => {
      toolBtns.forEach((b) => b.classList.remove("active"));
      btn.classList.add("active");
      activeTool = btn.dataset.tool;
    });
  });

  // Palette color switching
  const swatches = document.querySelectorAll(".swatch");
  swatches.forEach((swatch) => {
    swatch.addEventListener("click", () => {
      swatches.forEach((s) => s.classList.remove("active"));
      swatch.classList.add("active");
      activeColor = swatch.dataset.color;
    });
  });

  // Stroke width switching
  const strokeBtns = document.querySelectorAll(".stroke-btn");
  strokeBtns.forEach((btn) => {
    btn.addEventListener("click", () => {
      strokeBtns.forEach((b) => b.classList.remove("active"));
      btn.classList.add("active");
      activeStrokeWidth = parseInt(btn.dataset.width, 10);
    });
  });

  // Mockup Studio Controls
  const mockupWrapper = document.getElementById("mockup-wrapper");
  const mockupWindow = document.getElementById("mockup-window");
  const windowHeader = document.getElementById("window-header");

  document.getElementById("mockup-bg").addEventListener("change", (e) => {
    mockupWrapper.className = `mockup-wrapper ${e.target.value}`;
  });

  document.getElementById("mockup-padding").addEventListener("change", (e) => {
    mockupWrapper.style.padding = `${e.target.value}px`;
  });

  document.getElementById("mockup-shadow").addEventListener("change", (e) => {
    if (e.target.checked) {
      mockupWindow.classList.add("has-shadow");
    } else {
      mockupWindow.classList.remove("has-shadow");
    }
  });

  document.getElementById("mockup-frame").addEventListener("change", (e) => {
    const val = e.target.value;
    if (val === "none") {
      windowHeader.style.display = "none";
    } else if (val === "macos-dark") {
      windowHeader.style.display = "flex";
      windowHeader.className = "window-header";
    } else if (val === "macos-light") {
      windowHeader.style.display = "flex";
      windowHeader.className = "window-header light";
    }
  });

  // Zoom controls
  document.getElementById("btn-zoom-in").addEventListener("click", () => setZoom(currentZoom + 0.15));
  document.getElementById("btn-zoom-out").addEventListener("click", () => setZoom(Math.max(0.1, currentZoom - 0.15)));
  document.getElementById("btn-zoom-fit").addEventListener("click", fitToScreen);

  function setZoom(val) {
    currentZoom = val;
    mockupWrapper.style.transform = `scale(${currentZoom})`;
    document.getElementById("label-zoom").textContent = Math.round(currentZoom * 100) + "%";
  }

  function fitToScreen() {
    const viewport = document.getElementById("canvas-viewport");
    const vWidth = viewport.clientWidth - 80;
    const vHeight = viewport.clientHeight - 80;
    const cWidth = baseCanvas.width || 1200;
    const cHeight = baseCanvas.height || 800;

    const scale = Math.min(vWidth / cWidth, vHeight / cHeight, 1.0);
    setZoom(scale);
  }

  // Interactive Drawing on Annotation Canvas
  let isDrawing = false;
  let startX = 0;
  let startY = 0;

  annotationCanvas.addEventListener("mousedown", (e) => {
    const rect = annotationCanvas.getBoundingClientRect();
    startX = (e.clientX - rect.left) * (annotationCanvas.width / rect.width);
    startY = (e.clientY - rect.top) * (annotationCanvas.height / rect.height);
    isDrawing = true;

    if (activeTool === "badge") {
      // Draw numbered step badge
      annotCtx.save();
      annotCtx.beginPath();
      annotCtx.arc(startX, startY, 16, 0, 2 * Math.PI);
      annotCtx.fillStyle = activeColor;
      annotCtx.fill();
      annotCtx.fillStyle = "#FFFFFF";
      annotCtx.font = "bold 14px -apple-system, sans-serif";
      annotCtx.textAlign = "center";
      annotCtx.textBaseline = "middle";
      annotCtx.fillText(String(badgeStepCounter++), startX, startY);
      annotCtx.restore();
      isDrawing = false;
    }
  });

  annotationCanvas.addEventListener("mouseup", (e) => {
    if (!isDrawing) return;
    isDrawing = false;

    const rect = annotationCanvas.getBoundingClientRect();
    const endX = (e.clientX - rect.left) * (annotationCanvas.width / rect.width);
    const endY = (e.clientY - rect.top) * (annotationCanvas.height / rect.height);

    annotCtx.save();
    annotCtx.strokeStyle = activeColor;
    annotCtx.lineWidth = activeStrokeWidth;
    annotCtx.fillStyle = activeColor;

    if (activeTool === "rect") {
      annotCtx.strokeRect(startX, startY, endX - startX, endY - startY);
    } else if (activeTool === "circle") {
      annotCtx.beginPath();
      const r = Math.hypot(endX - startX, endY - startY) / 2;
      annotCtx.arc((startX + endX) / 2, (startY + endY) / 2, r, 0, 2 * Math.PI);
      annotCtx.stroke();
    } else if (activeTool === "arrow") {
      drawArrow(annotCtx, startX, startY, endX, endY, activeStrokeWidth);
    } else if (activeTool === "blur") {
      // Privacy Redaction: Blur/Pixelate the region on the base canvas
      applyPrivacyRedaction(baseCtx, startX, startY, endX - startX, endY - startY);
    }
    annotCtx.restore();
  });

  function drawArrow(ctx, fromX, fromY, toX, toY, width) {
    const headlen = 16;
    const angle = Math.atan2(toY - fromY, toX - fromX);
    ctx.lineWidth = width;
    ctx.beginPath();
    ctx.moveTo(fromX, fromY);
    ctx.lineTo(toX, toY);
    ctx.stroke();

    // Arrowhead
    ctx.beginPath();
    ctx.moveTo(toX, toY);
    ctx.lineTo(toX - headlen * Math.cos(angle - Math.PI / 6), toY - headlen * Math.sin(angle - Math.PI / 6));
    ctx.lineTo(toX - headlen * Math.cos(angle + Math.PI / 6), toY - headlen * Math.sin(angle + Math.PI / 6));
    ctx.closePath();
    ctx.fill();
  }

  function applyPrivacyRedaction(ctx, x, y, w, h) {
    const rx = Math.min(x, x + w);
    const ry = Math.min(y, y + h);
    const rw = Math.abs(w);
    const rh = Math.abs(h);
    if (rw === 0 || rh === 0) return;

    const imgData = ctx.getImageData(rx, ry, rw, rh);
    const data = imgData.data;
    const blockSize = 10;

    // Pixelate algorithm
    for (let py = 0; py < rh; py += blockSize) {
      for (let px = 0; px < rw; px += blockSize) {
        const pIndex = (py * rw + px) * 4;
        const r = data[pIndex];
        const g = data[pIndex + 1];
        const b = data[pIndex + 2];

        for (let dy = 0; dy < blockSize && py + dy < rh; dy++) {
          for (let dx = 0; dx < blockSize && px + dx < rw; dx++) {
            const idx = ((py + dy) * rw + (px + dx)) * 4;
            data[idx] = r;
            data[idx + 1] = g;
            data[idx + 2] = b;
          }
        }
      }
    }
    ctx.putImageData(imgData, rx, ry);
  }

  // 1-Click Copy Image to Clipboard
  document.getElementById("btn-copy-clipboard").addEventListener("click", copyCompositeToClipboard);
  document.getElementById("modal-btn-copy").addEventListener("click", copyCompositeToClipboard);

  async function copyCompositeToClipboard() {
    const merged = getMergedCanvas();
    merged.toBlob(async (blob) => {
      try {
        await navigator.clipboard.write([
          new ClipboardItem({ "image/png": blob })
        ]);
        alert("Screenshot copied to clipboard!");
      } catch (e) {
        alert("Clipboard copy failed: " + e.message);
      }
    }, "image/png");
  }

  function getMergedCanvas() {
    const merged = document.createElement("canvas");
    merged.width = baseCanvas.width;
    merged.height = baseCanvas.height;
    const mCtx = merged.getContext("2d");
    mCtx.drawImage(baseCanvas, 0, 0);
    mCtx.drawImage(annotationCanvas, 0, 0);
    return merged;
  }

  // Export Modal Handlers
  const exportModal = document.getElementById("export-modal");
  document.getElementById("btn-open-export").addEventListener("click", () => {
    exportModal.classList.remove("hidden");
  });
  document.getElementById("btn-close-modal").addEventListener("click", () => {
    exportModal.classList.add("hidden");
  });

  document.getElementById("modal-btn-download").addEventListener("click", async () => {
    let filename = document.getElementById("export-filename").value || "OmniSnap_Capture.png";
    const activeTab = document.querySelector(".format-tabs .tab-btn.active");
    const fmt = activeTab ? activeTab.dataset.fmt : "png";
    const merged = getMergedCanvas();

    if (fmt === "pdf") {
      filename = filename.replace(/\.[a-zA-Z0-9]+$/, ".pdf");
      const pdfBlob = await window.OmniPDF.generateMultiPagePDF(merged, {
        format: "a4",
        smartSplit: true,
        margin: 20,
        links: currentSession ? currentSession.links : []
      });
      const url = URL.createObjectURL(pdfBlob);
      const a = document.createElement("a");
      a.href = url;
      a.download = filename;
      document.body.appendChild(a);
      a.click();
      a.remove();
      URL.revokeObjectURL(url);
      exportModal.classList.add("hidden");
      return;
    }

    const mime = fmt === "jpg" ? "image/jpeg" : fmt === "webp" ? "image/webp" : "image/png";
    merged.toBlob((blob) => {
      const url = URL.createObjectURL(blob);
      const a = document.createElement("a");
      a.href = url;
      a.download = filename;
      document.body.appendChild(a);
      a.click();
      a.remove();
      URL.revokeObjectURL(url);
      exportModal.classList.add("hidden");
    }, mime, 0.92);
  });

  function sanitizeFilename(name) {
    return name.replace(/[^a-zA-Z0-9_-]/g, "_").substring(0, 40);
  }
});
