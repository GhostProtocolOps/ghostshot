# Privacy Policy for OmniSnap

**Last Updated**: November 2026

OmniSnap ("we", "our", or "the extension") is committed to protecting your privacy. This Privacy Policy explains our practices regarding data collection and usage.

---

## 1. Single Purpose
OmniSnap exists solely to capture full-page web screenshots, provide on-device annotation tools, and export image/PDF files locally to the user's machine.

---

## 2. Zero Data Collection & Zero Telemetry
- **No Personal Data Collected**: OmniSnap does not collect, log, store, or transmit any personally identifiable information (PII).
- **No Browsing History Collected**: We do not monitor, record, or transmit URLs or web content you visit.
- **Zero Third-Party Tracking**: Unlike other screenshot extensions, OmniSnap contains **no Google Analytics, no telemetry, no advertising trackers, and no third-party tracking scripts**.

---

## 3. Local-Only Processing
All screenshot slicing, canvas stitching, and image annotations occur **100% locally in your browser memory**:
- Captured images are temporarily stored in local browser memory (`IndexedDB` / `chrome.storage.local`) on your device.
- You can clear all stored snapshots at any time with one click in the extension Options page.
- Image files are saved directly to your local file system via standard browser downloads when you choose to export them.

---

## 4. Permissions Justification
OmniSnap requests only the minimal permissions required to capture and edit screenshots:
- `activeTab`: Used only when you explicitly invoke the extension to access the current tab and trigger the capture.
- `scripting`: Required to inject the scrolling and coordinate calculation scripts into the active page.
- `storage` / `unlimitedStorage`: Used strictly to save your local extension preferences (e.g. delay settings) and temporary local snapshot drafts.
- `downloads`: Used only when you click "Download Image" or "Download PDF" to save the file to your computer.

---

## 5. Contact
If you have questions about this Privacy Policy, please open an issue in the project repository.
