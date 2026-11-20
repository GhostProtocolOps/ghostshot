/**
 * GhostShot - Canvas Stitcher Engine
 * Assembles slice images onto HTML5 2D Canvas with retina DPR scaling and memory tile chunking.
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
      slices.map(async (slice) => ({
        img: await loadImage(slice.dataUrl),
        y: slice.y * scale,
        height: slice.height * scale,
        width: slice.width * scale
      }))
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
        const sliceTop = item.y;
        const sliceBottom = item.y + item.height;
        const tileTop = currentTileY;
        const tileBottom = currentTileY + currentTileH;

        // Check if slice overlaps with current tile
        if (sliceBottom > tileTop && sliceTop < tileBottom) {
          const dy = sliceTop - tileTop;
          ctx.drawImage(item.img, 0, dy);
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
