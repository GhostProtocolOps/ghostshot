/**
 * OmniSnap - Production Multi-Page & Continuous Long Screenshot PDF Engine
 * Reverse-engineered & upgraded from GoFullPage:
 * - Supports "1 Continuous Long Page" (Single seamless page matching full screenshot height - No split!)
 * - Supports standard multi-page formats (A4, US Letter, Legal) with smart whitespace splitting
 * - Supports multi-tile canvas assemblies (>16,384px height) without browser memory crash
 * - Clickable hyperlink transformation per page
 * - Zero-dependency, pure client-side PDF 1.4 binary stream generator
 */

window.OmniPDF = (function () {
  const PAGE_FORMATS = {
    full: { label: "1 Continuous Long Page (No Split)" },
    a4: { width: 595.28, height: 841.89, label: "A4 Portrait (210 × 297 mm)" },
    letter: { width: 612.0, height: 792.0, label: "US Letter Portrait (8.5 × 11 in)" },
    legal: { width: 612.0, height: 1008.0, label: "US Legal Portrait (8.5 × 14 in)" },
    "a4-landscape": { width: 841.89, height: 595.28, label: "A4 Landscape" },
    "letter-landscape": { width: 792.0, height: 612.0, label: "US Letter Landscape" }
  };

  /**
   * Smart Whitespace Scanline Detector
   * Analyzes the bottom scan range of a slice to find an empty horizontal gap
   * between paragraphs or lines of text, preventing awkward text-cutting across pages.
   */
  function findCleanSplitY(ctx, width, targetHeight, scanRange = 80) {
    if (targetHeight <= scanRange) return targetHeight;

    const startY = Math.max(0, targetHeight - scanRange);
    let imgData;
    try {
      imgData = ctx.getImageData(0, startY, width, scanRange);
    } catch (e) {
      return targetHeight;
    }

    const data = imgData.data;
    let bestY = targetHeight;

    for (let row = scanRange - 1; row >= 0; row--) {
      let isUniform = true;
      const baseIdx = (row * width) * 4;
      const r0 = data[baseIdx];
      const g0 = data[baseIdx + 1];
      const b0 = data[baseIdx + 2];

      for (let col = 4; col < width; col += 4) {
        const idx = (row * width + col) * 4;
        const diff = Math.abs(data[idx] - r0) + Math.abs(data[idx + 1] - g0) + Math.abs(data[idx + 2] - b0);
        if (diff > 15) {
          isUniform = false;
          break;
        }
      }

      if (isUniform) {
        bestY = startY + row;
        break;
      }
    }

    return bestY > startY + 10 ? bestY : targetHeight;
  }

  /**
   * Generates a Single Continuous Long Page PDF (1 Page - Matches entire screenshot height)
   */
  async function generateContinuousPDF(canvasOrTiles, links = []) {
    let tiles = [];
    if (Array.isArray(canvasOrTiles)) {
      tiles = canvasOrTiles.map((t) => (t.canvas ? t.canvas : t));
    } else if (canvasOrTiles && canvasOrTiles.canvasTiles) {
      tiles = canvasOrTiles.canvasTiles.map((t) => t.canvas);
    } else {
      tiles = [canvasOrTiles];
    }

    const totalWidthPx = tiles[0].width;
    let totalHeightPx = 0;
    for (const t of tiles) {
      totalHeightPx += t.height;
    }

    // Convert pixels to PDF points (at 72 DPI, 1 px = 0.75 pt)
    const ptWidth = Math.round(totalWidthPx * 0.75);
    const ptHeight = Math.round(totalHeightPx * 0.75);

    const paper = { width: ptWidth, height: ptHeight };

    // Prepare tile image data
    const tileImages = [];
    let currentYPt = 0;

    for (let i = 0; i < tiles.length; i++) {
      const tileCanvas = tiles[i];
      const tileHeightPt = Math.round(tileCanvas.height * 0.75);
      const dataUrl = tileCanvas.toDataURL("image/jpeg", 0.92);

      // In PDF coordinates (origin at bottom-left):
      const pdfY = ptHeight - currentYPt - tileHeightPt;

      tileImages.push({
        id: i + 1,
        dataUrl,
        xPt: 0,
        yPt: pdfY,
        widthPt: ptWidth,
        heightPt: tileHeightPt,
        pixelWidth: tileCanvas.width,
        pixelHeight: tileCanvas.height
      });

      currentYPt += tileHeightPt;
    }

    const pageLinks = (links || []).map((l) => ({
      url: l.href || l.url,
      x: (l.x || 0) * 0.75,
      y: (l.y || 0) * 0.75,
      w: (l.width || 0) * 0.75,
      h: (l.height || 0) * 0.75
    }));

    return buildContinuousPDFBinary(tileImages, pageLinks, paper);
  }

  /**
   * Generates Multi-Page PDF (A4, US Letter, Legal) with smart whitespace page splitting
   */
  async function generateMultiPagePDF(canvasOrTiles, options = {}) {
    const formatKey = options.format || "a4";
    const paper = PAGE_FORMATS[formatKey] || PAGE_FORMATS.a4;
    const margin = options.margin !== undefined ? options.margin : 20;
    const smartSplit = options.smartSplit !== false;
    const links = options.links || [];

    // Normalize input to a single canvas for slicing
    let fullCanvas;
    if (Array.isArray(canvasOrTiles)) {
      if (canvasOrTiles.length === 1) {
        fullCanvas = canvasOrTiles[0].canvas || canvasOrTiles[0];
      } else {
        fullCanvas = document.createElement("canvas");
        fullCanvas.width = canvasOrTiles[0].width;
        fullCanvas.height = canvasOrTiles.reduce((acc, t) => acc + (t.height || t.canvas.height), 0);
        const fctx = fullCanvas.getContext("2d");
        let dy = 0;
        for (const t of canvasOrTiles) {
          const c = t.canvas || t;
          fctx.drawImage(c, 0, dy);
          dy += c.height;
        }
      }
    } else if (canvasOrTiles && canvasOrTiles.canvasTiles) {
      return generateMultiPagePDF(canvasOrTiles.canvasTiles, options);
    } else {
      fullCanvas = canvasOrTiles;
    }

    const canvasWidth = fullCanvas.width;
    const canvasHeight = fullCanvas.height;

    const printableWidth = paper.width - (margin * 2);
    const printableHeight = paper.height - (margin * 2);

    const scale = printableWidth / canvasWidth;
    const maxSliceHeightPx = printableHeight / scale;

    const pages = [];
    let currentY = 0;
    let pageNum = 1;

    const ctx = fullCanvas.getContext("2d", { willReadFrequently: true });

    while (currentY < canvasHeight) {
      const remainingHeight = canvasHeight - currentY;
      let sliceHeight = Math.min(maxSliceHeightPx, remainingHeight);

      if (smartSplit && remainingHeight > maxSliceHeightPx) {
        const adjustedSplit = findCleanSplitY(ctx, canvasWidth, currentY + sliceHeight, 80);
        sliceHeight = adjustedSplit - currentY;
      }

      const pageCanvas = document.createElement("canvas");
      pageCanvas.width = canvasWidth;
      pageCanvas.height = sliceHeight;

      const pCtx = pageCanvas.getContext("2d");
      pCtx.drawImage(
        fullCanvas,
        0, currentY, canvasWidth, sliceHeight,
        0, 0, canvasWidth, sliceHeight
      );

      const sliceHeightPt = sliceHeight * scale;
      const imgDataUrl = pageCanvas.toDataURL("image/jpeg", 0.92);

      const pageYStart = currentY;
      const pageYEnd = currentY + sliceHeight;

      const pageLinks = (links || [])
        .filter((l) => l.y >= pageYStart && l.y < pageYEnd)
        .map((l) => ({
          url: l.href || l.url,
          x: margin + (l.x * scale),
          y: (l.y - pageYStart) * scale,
          w: l.width * scale,
          h: l.height * scale
        }));

      pages.push({
        pageNum,
        imgDataUrl,
        sliceHeightPt,
        printableWidth,
        links: pageLinks
      });

      currentY += sliceHeight;
      pageNum++;
    }

    return buildMultiPagePDFBinary(pages, paper, margin);
  }

  /**
   * PDF 1.4 Binary Builder for Single Continuous Page (with multi-tile image support)
   */
  function buildContinuousPDFBinary(tileImages, pageLinks, paper) {
    const objects = [];
    const xrefOffsets = [];
    let byteOffset = 0;

    function addObj(content) {
      const objId = objects.length + 1;
      xrefOffsets.push(byteOffset);
      const str = `${objId} 0 obj\n${content}\nendobj\n`;
      byteOffset += str.length;
      objects.push(str);
      return objId;
    }

    const header = "%PDF-1.4\n%âãÏÓ\n";
    byteOffset += header.length;

    // Obj 1: Catalog
    addObj("<< /Type /Catalog /Pages 2 0 R >>");

    // Placeholder Obj 2: Pages root
    objects.push("");
    xrefOffsets.push(byteOffset);
    byteOffset += 100;

    const xObjectMap = [];
    const imageObjIds = [];

    // Add Image XObjects
    for (const img of tileImages) {
      const base64Data = img.dataUrl.split(",")[1];
      const binaryImg = atob(base64Data);
      const imgLen = binaryImg.length;
      const imgObjId = objects.length + 1;
      xrefOffsets.push(byteOffset);

      const imgHeader = `<< /Type /XObject /Subtype /Image /Width ${img.pixelWidth} /Height ${img.pixelHeight} /ColorSpace /DeviceRGB /BitsPerComponent 8 /Filter /DCTDecode /Length ${imgLen} >>\nstream\n`;
      const imgTrailer = "\nendstream\nendobj\n";
      byteOffset += `${imgObjId} 0 obj\n${imgHeader}`.length + imgLen + imgTrailer.length;

      objects.push({ isBinary: true, objId: imgObjId, header: `${imgObjId} 0 obj\n${imgHeader}`, data: binaryImg, trailer: imgTrailer });
      xObjectMap.push(`/Im${img.id} ${imgObjId} 0 R`);
      imageObjIds.push(imgObjId);
    }

    // Build Page Content Stream (places each tile image at its exact vertical offset)
    let contentStream = "q\n";
    for (const img of tileImages) {
      contentStream += `${img.widthPt.toFixed(2)} 0 0 ${img.heightPt.toFixed(2)} ${img.xPt.toFixed(2)} ${img.yPt.toFixed(2)} cm\n/Im${img.id} Do\n`;
    }
    contentStream += "Q\n";

    const contentObjId = addObj(`<< /Length ${contentStream.length} >>\nstream\n${contentStream}endstream`);

    // Add Annotation Links
    const annotIds = [];
    for (const link of pageLinks) {
      const pdfY = paper.height - (link.y + link.h);
      const annotId = addObj(`<< /Type /Annot /Subtype /Link /Rect [${link.x.toFixed(2)} ${pdfY.toFixed(2)} ${(link.x + link.w).toFixed(2)} ${(pdfY + link.h).toFixed(2)}] /Border [0 0 0] /A << /S /URI /URI (${escapePdfString(link.url)}) >> >>`);
      annotIds.push(`${annotId} 0 R`);
    }

    const annotStr = annotIds.length > 0 ? `/Annots [${annotIds.join(" ")}]` : "";
    const pageId = addObj(`<< /Type /Page /Parent 2 0 R /MediaBox [0 0 ${paper.width.toFixed(2)} ${paper.height.toFixed(2)}] /Contents ${contentObjId} 0 R /Resources << /XObject << ${xObjectMap.join(" ")} >> >> ${annotStr} >>`);

    // Obj 2: Pages root
    objects[1] = `2 0 obj\n<< /Type /Pages /Kids [${pageId} 0 R] /Count 1 >>\nendobj\n`;

    return finalizePDF(header, objects);
  }

  /**
   * PDF 1.4 Binary Builder for Standard Multi-Page Formats
   */
  function buildMultiPagePDFBinary(pages, paper, margin) {
    const objects = [];
    const xrefOffsets = [];
    let byteOffset = 0;

    function addObj(content) {
      const objId = objects.length + 1;
      xrefOffsets.push(byteOffset);
      const str = `${objId} 0 obj\n${content}\nendobj\n`;
      byteOffset += str.length;
      objects.push(str);
      return objId;
    }

    const header = "%PDF-1.4\n%âãÏÓ\n";
    byteOffset += header.length;

    addObj("<< /Type /Catalog /Pages 2 0 R >>");

    // Placeholder Obj 2
    objects.push("");
    xrefOffsets.push(byteOffset);
    byteOffset += 100;

    const pageObjIds = [];

    for (const page of pages) {
      const base64Data = page.imgDataUrl.split(",")[1];
      const binaryImg = atob(base64Data);
      const imgLen = binaryImg.length;

      const imgObjId = objects.length + 1;
      xrefOffsets.push(byteOffset);
      const imgHeader = `<< /Type /XObject /Subtype /Image /Width ${Math.round(page.printableWidth / 0.75)} /Height ${Math.round(page.sliceHeightPt / 0.75)} /ColorSpace /DeviceRGB /BitsPerComponent 8 /Filter /DCTDecode /Length ${imgLen} >>\nstream\n`;
      const imgTrailer = "\nendstream\nendobj\n";
      byteOffset += `${imgObjId} 0 obj\n${imgHeader}`.length + imgLen + imgTrailer.length;
      objects.push({ isBinary: true, objId: imgObjId, header: `${imgObjId} 0 obj\n${imgHeader}`, data: binaryImg, trailer: imgTrailer });

      const contentStream = `q\n${page.printableWidth.toFixed(2)} 0 0 ${page.sliceHeightPt.toFixed(2)} ${margin} ${(paper.height - margin - page.sliceHeightPt).toFixed(2)} cm\n/Im1 Do\nQ\n`;
      const contentObjId = addObj(`<< /Length ${contentStream.length} >>\nstream\n${contentStream}endstream`);

      const annotIds = [];
      for (const link of page.links) {
        const pdfY = paper.height - (link.y + link.h);
        const annotId = addObj(`<< /Type /Annot /Subtype /Link /Rect [${link.x.toFixed(2)} ${pdfY.toFixed(2)} ${(link.x + link.w).toFixed(2)} ${(pdfY + link.h).toFixed(2)}] /Border [0 0 0] /A << /S /URI /URI (${escapePdfString(link.url)}) >> >>`);
        annotIds.push(`${annotId} 0 R`);
      }

      const annotStr = annotIds.length > 0 ? `/Annots [${annotIds.join(" ")}]` : "";
      const pageId = addObj(`<< /Type /Page /Parent 2 0 R /MediaBox [0 0 ${paper.width.toFixed(2)} ${paper.height.toFixed(2)}] /Contents ${contentObjId} 0 R /Resources << /XObject << /Im1 ${imgObjId} 0 R >> >> ${annotStr} >>`);
      pageObjIds.push(`${pageId} 0 R`);
    }

    objects[1] = `2 0 obj\n<< /Type /Pages /Kids [${pageObjIds.join(" ")}] /Count ${pageObjIds.length} >>\nendobj\n`;

    return finalizePDF(header, objects);
  }

  function finalizePDF(header, objects) {
    let currentPos = header.length;
    const finalXref = [];
    const finalParts = [header];

    for (let i = 0; i < objects.length; i++) {
      finalXref.push(currentPos);
      const obj = objects[i];
      if (obj.isBinary) {
        finalParts.push(obj.header);
        finalParts.push(binaryStringToUint8Array(obj.data));
        finalParts.push(obj.trailer);
        currentPos += obj.header.length + obj.data.length + obj.trailer.length;
      } else {
        finalParts.push(obj);
        currentPos += obj.length;
      }
    }

    const startXref = currentPos;
    let xref = `xref\n0 ${finalXref.length + 1}\n0000000000 65535 f \n`;
    for (const offset of finalXref) {
      xref += `${String(offset).padStart(10, "0")} 00000 n \n`;
    }

    const trailer = `trailer\n<< /Size ${finalXref.length + 1} /Root 1 0 R >>\nstartxref\n${startXref}\n%%EOF\n`;
    finalParts.push(xref);
    finalParts.push(trailer);

    return new Blob(finalParts, { type: "application/pdf" });
  }

  function binaryStringToUint8Array(str) {
    const buf = new Uint8Array(str.length);
    for (let i = 0; i < str.length; i++) {
      buf[i] = str.charCodeAt(i) & 0xff;
    }
    return buf;
  }

  function escapePdfString(str) {
    return (str || "").replace(/\\/g, "\\\\").replace(/\(/g, "\\(").replace(/\)/g, "\\)");
  }

  return {
    generateContinuousPDF,
    generateMultiPagePDF,
    PAGE_FORMATS
  };
})();
