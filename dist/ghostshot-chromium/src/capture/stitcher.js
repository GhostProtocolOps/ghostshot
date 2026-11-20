/**
 * GhostShot - Canvas Stitcher Engine
 * Assembles slice images onto HTML5 2D Canvas with retina DPR scaling and memory tile chunking.
 * Implements precise sub-rectangle source and destination cropping to eliminate duplicate seams.
 */

window.OmniStitcher = (function() {
  const MAX_CANVAS_DIMENSION = 16384; // Safe boundary across Chromium and WebKit

  async function loadImage(src) {
    return new Promise((resolve, reject) => {
      const img = new Image();
      img.onload = () => resolve(img);
      img.onerror = (e) => reject(new Error("Failed to load slice image"));
      img.src = src;
    });
  }

  async function stitchSlices(session) {
    const { slices, dimensions, dpr } = session;
    const scale = dpr || 1.0;

    const totalWidthPx = Math.ceil(dimensions.totalWidth * scale);
    const totalHeightPx = Math.ceil(dimensions.totalHeight * scale);

    // If height exceeds safe canvas limit, partition into tiles
    const isMultiTiled = totalHeightPx > MAX_CANVAS_DIMENSION;
    const tileHeightPx = isMultiTiled ? MAX_CANVAS_DIMENSION : totalHeightPx;
    const numTiles = Math.ceil(totalHeightPx / tileHeightPx);

    const canvasTiles = [];

    // Preload all slice images
    const loadedImages = await Promise.all(
      slices.map(async (slice) => {
        const img = await loadImage(slice.dataUrl);
        return {
          img,
          // Support both legacy slice format and precision sub-rectangle format
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
    MAX_CANVAS_DIMENSION
  };
})();
