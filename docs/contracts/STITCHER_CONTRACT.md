# 📜 Component Contract: OmniStitcher

> **Module**: `extension/src/capture/stitcher.js`  
> **Global Identifier**: `window.OmniStitcher`  
> **Component Owner**: Graphics & Canvas Stitcher Engine Specialist  
> **OpenDots Reference**: `RFC-011`

---

## 1. Component Purpose & Scope
The `OmniStitcher` takes the vertical slice screenshots captured by Chrome's `captureVisibleTab` and stitches them onto HTML5 2D Canvas buffers. It guarantees zero browser memory crashes via multi-tile virtualization (clamping tiles to $\le 16,384\text{px}$) and eliminates duplicate seams via 9-parameter sub-rectangle source and destination blitting.

---

## 2. Mathematical Coordinate & Blitting Contract

### Multi-Tile Buffer Partitioning
To prevent the Chrome/Skia 16,384px canvas allocation crash:
$$\text{MAX\_CANVAS\_DIMENSION} = 16384\text{ px}$$
$$\text{totalWidthPx} = \lceil \text{dimensions.totalWidth} \times \text{dpr} \rceil$$
$$\text{totalHeightPx} = \lceil \text{dimensions.totalHeight} \times \text{dpr} \rceil$$
$$\text{numTiles} = \lceil \text{totalHeightPx} / \text{tileHeightPx} \rceil$$

### 9-Parameter Sub-Rectangle Blitting
Each captured slice provides:
- **Source Crop**: $(sx, sy, sw, sh)$ — specifies the sub-rectangle within the viewport image to extract.
- **Destination Crop**: $(dx, dy, dw, dh)$ — specifies the document location to place the extracted pixels.

For each tile $t$ covering $[\text{tileTop}, \text{tileBottom}]$:
```javascript
const sliceTop = item.destY;
const sliceBottom = item.destY + item.destHeight;
const tileTop = currentTileY;
const tileBottom = currentTileY + currentTileH;

if (sliceBottom > tileTop && sliceTop < tileBottom) {
  const dyInTile = item.destY - tileTop;
  ctx.drawImage(
    item.img,
    item.sourceX, item.sourceY, item.sourceWidth, item.sourceHeight,
    item.destX, dyInTile, item.destWidth, item.destHeight
  );
}
```

---

## 3. Invariants & Output Contract
1. **Physical Pixel Accuracy**: All coordinates inside the canvas context must be scaled by `devicePixelRatio` (DPR) to preserve 4K/Retina crispness.
2. **Context Configuration**: Canvas context must be created with `{ willReadFrequently: true }` to optimize data retrieval for PNG exports and Minimap rendering.
3. **Zero Distortion**: No slice image may be stretched or compressed; $sw \equiv dw$ and $sh \equiv dh$.
