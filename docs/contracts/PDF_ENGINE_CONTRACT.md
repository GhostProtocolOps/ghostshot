# 📜 Component Contract: OmniPDFEngine

> **Module**: `extension/src/capture/pdf_engine.js`  
> **Global Identifier**: `window.OmniPDFEngine`  
> **Component Owner**: Rust & Client-Side Engine Specialist  
> **OpenDots Reference**: `RFC-012`

---

## 1. Component Purpose & Scope
The `OmniPDFEngine` generates publication-quality PDF documents from stitched canvas captures 100% on-device in browser memory. It features two user-selected modes:
1. **Single Continuous Long Page PDF**: Exactly 1 continuous PDF page matching the full height of the web page with zero page splits.
2. **Smart Whitespace Multi-Page PDF**: Paginated A4, US Letter, or US Legal PDF pages that automatically scan canvas scanlines to avoid cutting through text lines.

---

## 2. API Contract Specification

### `generateContinuousPDF(session: StitchedSession): Promise<Uint8Array>`
- **Output**: Pure binary PDF buffer (`Uint8Array`) with MIME `application/pdf`.
- **Page Dimensions**:
  $$\text{ptWidth} = \text{session.dimensions.totalWidth} \times 0.75$$
  $$\text{ptHeight} = \text{session.dimensions.totalHeight} \times 0.75$$
- **Invariants**:
  - `Pages.Count === 1`
  - Zero pagination breaks.
  - JPEG image stream embedded with `/Filter /DCTDecode`.
  - Hyperlinks mapped to PDF `/Annots [ << /Type /Annot /Subtype /Link /A << /S /URI /URI (url) >> >> ]`.

---

### `generateMultiPagePDF(session: StitchedSession, pageSize: "A4" | "Letter" | "Legal"): Promise<Uint8Array>`
- **Whitespace Split Heuristic**:
  - For each target page boundary, scans vertical scanlines within a $\pm 100\text{px}$ window to identify continuous horizontal bands of whitespace or background color.
  - Snaps page split coordinate to the clean whitespace band, ensuring paragraphs and headers are never sliced in half.
