# 🏛️ AI Company Architecture & Execution Playbook

> **Scope**: Universal Enterprise Agent Framework  
> **Integrations**: Paperclip, Chrome DevTools MCP, OpenDots, REA, Craft Suite, PostgreSQL 4-DB Federation, Multi-Bridge Consensus (Qwen, GPT, DeepSeek, Codex), ECC Memory Vault.

---

## 1. Core Operating Doctrine: The 5 Institutional Tiers

When a mandate is assigned, the AI Company never writes speculative code in a single turn. It executes across 5 synchronized tiers:

### Tier 1: Governance & Task Ingestion (Paperclip)
* **Principle**: Work must be owned by designated agents, not an anonymous prompt loop.
* **Roles**:
  - `Lead Architect`: Scope, strategy, release tagging, and cross-agent coordination.
  - `Engine Specialist`: Low-level algorithm implementations, memory safety, math clamping.
  - `Compliance & Security Officer`: Least-privilege manifests, store policies, privacy audits.
  - `QA & Test Automation Specialist`: Live CDP script evaluation, headless browser assertions.
* **Mechanism**: Every charge is broken into structured epics/tickets with explicit priority (`critical`, `high`, `medium`), acceptance criteria, and status tracking (`todo` &rarr; `in_progress` &rarr; `done`).

### Tier 2: Forensic Ground-Truthing & Reverse Engineering (REA & Craft Suite)
* **Principle**: Never guess how complex systems work; decompile reference implementations to uncover ground truth.
* **Mechanism**:
  - Extract and unpack reference targets (extensions, binaries, web bundles).
  - Use **REA** and **Craft Suite** to analyze AST signatures and extract core math algorithms.
  - Audit competitor blindspots (e.g. GoFullPage's Shadow DOM blindness, zero-height container drops, hard PDF page splits) and adopt strengths (28,800px virtual canvas, Path2D seam clamping, dynamic style injection).

### Tier 3: Multi-Model Adversarial Consensus (Multi-Bridge & Codex)
* **Principle**: No single frontier model is infallible. Multi-model consensus prevents hallucinations and regression blindspots.
* **Mechanism**:
  - Run `compare_models` across **Alibaba Qwen 3.8 Max** and **OpenAI GPT-6 Luna**.
  - Delegate deep reasoning to **DeepSeek Reasoner (R1)** or **Codex CLI (`o3-mini`)**.
  - Cross-check AST diffs for cross-browser regressions (Chromium, WebKit, Gecko).

### Tier 4: Live Runtime CDP Verification (Chrome DevTools MCP)
* **Principle**: Theoretical passes in unit tests are insufficient; assertions must pass inside the live browser runtime.
* **Mechanism**:
  - Maintain a supervisor daemon (`scripts/chrome_managed_profile.py`) monitoring Google Chrome on port 9222.
  - Hot-reload extensions live via `reload_extension`.
  - Execute CDP script evaluation directly inside target production pages (e.g. W3Schools AWS tutorial).
  - Verify exact DOM suppression (`display: none !important; visibility: hidden !important;`) and post-capture restoration.

### Tier 5: 4-Database Knowledge Federation & Release Staging
* **Principle**: Institutional memory must survive across sessions, crashes, and agent restarts.
* **Federated Storage**:
  1. `gravity_1`: Relational entity catalog and architectural parity matrix.
  2. `gravity_sql`: Review audit runs, timestamps, and pass/fail metrics.
  3. `gravity_jsonb`: Structured AST deconstructions and multi-model consensus telemetry.
  4. `gravity_vector`: 384-dimensional pgvector semantic embeddings for architectural retrieval.
* **Release Artifacts**:
  - Automated least-privilege linter (`audit_manifest_permissions.py`).
  - Non-destructive packaging (`package_browsers.sh`).
  - Staging distribution zips and auditing platform review locks (CWS Developer Console).

---

## 2. Universal Failure Modes & Hard-Learned Heuristics

1. **Zero-Height Container Anchors**:
   - Modern frameworks frequently wrap content in collapsed parent `div`s with `height: 0` containing `absolute` children.
   - *Heuristic*: A fixed element is active if `childElementCount > 0`, `clientRects.length > 0`, or `scrollWidth/scrollHeight > 0`. Never rely solely on `rect.height > 0`.
2. **Dynamic UI Binding vs. Hardcoding**:
   - Never hardcode version strings in user-facing templates (`popup.html`).
   - *Heuristic*: Always bind UI labels to `chrome.runtime.getManifest().version` at runtime with an updated fallback.
3. **Filesystem-Aware Packaging**:
   - Destructive build scripts (`rm -rf dist`) destroy directory inodes and trigger browser extension unmounting upon restart.
   - *Heuristic*: Use safe copying/rsync to preserve directory identity, and instruct developers to load from the permanent repository root (`extension/`).
4. **Platform-Level Review Gates**:
   - External platforms (Chrome Web Store, App Store) lock binary uploads during active review.
   - *Heuristic*: Always verify store status via CDP before attempting uploads; stage packages for automated release once the review gate clears.
