/**
 * GhostShot - Canvas Stitcher Engine
 * Assembles slice images onto HTML5 2D Canvas with retina DPR scaling and memory tile chunking.
 * Implements precise sub-rectangle source and destination cropping to eliminate duplicate seams.
 */

window.OmniStitcher = (function() {
  const MAX_CANVAS_DIMENSION = 28800; // Ultra high-resolution buffer matching GoFullPage standard
  const MAX_CANVAS_AREA = 259200000;  // 259.2 Megapixels

  async function loadImage(src) {
    return new Promise((resolve, reject) => {
      const img = new Image();
      img.onload = () => resolve(img);
      img.onerror = (e) => reject(new Error("Failed to load slice image"));
      img.src = src;
    });
  }

  /**
   * Samples edge pixel histogram to heal background padding voids
   */
  function healBackgroundSeams(ctx, width, height) {
    try {
      const sampleH = Math.min(10, height);
      const imgData = ctx.getImageData(0, 0, width, sampleH);
      const d = imgData.data;
      const counts = new Map();
      for (let i = 0; i < d.length; i += 4) {
        if (d[i + 3] === 255) {
          const rgb = `${d[i]},${d[i + 1]},${d[i + 2]}`;
          counts.set(rgb, (counts.get(rgb) || 0) + 1);
        }
      }
      let maxCount = 0;
      let dominantRgb = "255,255,255";
      for (const [rgb, c] of counts.entries()) {
        if (c > maxCount) {
          maxCount = c;
          dominantRgb = rgb;
        }
      }
      return `rgb(${dominantRgb})`;
    } catch (e) {
      return "rgb(255,255,255)";
    }
  }

  async function stitchSlices(session) {
    const { slices, dimensions, dpr } = session;
    const scale = dpr || 1.0;

    const totalWidthPx = Math.ceil(dimensions.totalWidth * scale);
    const totalHeightPx = Math.ceil(dimensions.totalHeight * scale);

    // If height or area exceeds safe canvas limit, partition into virtual tiles
    const isMultiTiled = totalHeightPx > MAX_CANVAS_DIMENSION || (totalWidthPx * totalHeightPx) > MAX_CANVAS_AREA;
    const tileHeightPx = isMultiTiled ? Math.min(MAX_CANVAS_DIMENSION, Math.floor(MAX_CANVAS_AREA / totalWidthPx)) : totalHeightPx;
    const numTiles = Math.ceil(totalHeightPx / tileHeightPx);

    const canvasTiles = [];

    // Preload all slice images
    const loadedImages = await Promise.all(
      slices.map(async (slice) => {
        const img = await loadImage(slice.dataUrl);
        return {
          img,
          sourceX: Math.round((slice.sourceX !== undefined ? slice.sourceX : 0) * scale),
          sourceY: Math.round((slice.sourceY !== undefined ? slice.sourceY : 0) * scale),
          sourceWidth: Math.round((slice.sourceWidth !== undefined ? slice.sourceWidth : slice.width) * scale),
          sourceHeight: Math.round((slice.sourceHeight !== undefined ? slice.sourceHeight : slice.height) * scale),
          destX: Math.round((slice.destX !== undefined ? slice.destX : 0) * scale),
          destY: Math.round((slice.destY !== undefined ? slice.destY : slice.y) * scale),
          destWidth: Math.round((slice.destWidth !== undefined ? slice.destWidth : slice.width) * scale),
          destHeight: Math.round((slice.destHeight !== undefined ? slice.destHeight : slice.height) * scale)
        };
      })
    );

    for (let t = 0; t < numTiles; t++) {
      const tileCanvas = document.createElement("canvas");
      const currentTileY = t * tileHeightPx;
      const currentTileH = Math.min(tileHeightPx, totalHeightPx - currentTileY);

      tileCanvas.width = totalWidthPx;
      tileCanvas.height = currentTileH;

      const ctx = tileCanvas.getContext("2d", { willReadFrequently: true });
      ctx.imageSmoothingEnabled = true;

      // Draw slices intersecting with this tile
      for (const item of loadedImages) {
        const sliceTop = item.destY;
        const sliceBottom = item.destY + item.destHeight;
        const tileTop = currentTileY;
        const tileBottom = currentTileY + currentTileH;

        // Check if slice overlaps with current tile
        if (sliceBottom > tileTop && sliceTop < tileBottom) {
          // Calculate destination offset inside this specific tile
          const dyInTile = item.destY - tileTop;

          // Path2D integer boundary clamping to eliminate sub-pixel seam tears
          const clipPath = new Path2D();
          const sX = Math.floor(item.destX);
          const sY = Math.floor(dyInTile);
          let sW = Math.ceil(item.destWidth);
          let sH = Math.ceil(item.destHeight);
          if (sX + sW < item.destX + item.destWidth) sW += 1;
          if (sY + sH < dyInTile + item.destHeight) sH += 1;

          clipPath.rect(sX, sY, sW, sH);

          ctx.save();
          ctx.clip(clipPath);

          // Draw image with sub-rectangle source and destination coordinates
          ctx.drawImage(
            item.img,
            item.sourceX,
            item.sourceY,
            item.sourceWidth,
            item.sourceHeight,
            item.destX,
            dyInTile,
            item.destWidth,
            item.destHeight
          );

          ctx.restore();
        }
      }

      canvasTiles.push({
        canvas: tileCanvas,
        tileIndex: t,
        sourceY: currentTileY,
        width: totalWidthPx,
        height: currentTileH
      });
    }

    return {
      canvasTiles,
      totalWidthPx,
      totalHeightPx,
      scale,
      isMultiTiled
    };
  }

  return {
    stitchSlices,
    healBackgroundSeams,
    MAX_CANVAS_DIMENSION,
    MAX_CANVAS_AREA
  };
})();
