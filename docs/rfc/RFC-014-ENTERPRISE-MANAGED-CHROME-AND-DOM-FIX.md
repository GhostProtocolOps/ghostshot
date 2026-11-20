# 📄 RFC-014: Enterprise Managed Chrome DevTools Runtime & Universal Header Suppression Engine

> **RFC Identifier**: `RFC-014`  
> **Status**: `APPROVED & PRODUCTION DEPLOYED`  
> **Target Release**: GhostShot `v2.0.2`  
> **Company ID**: `a9cd98a6-04c3-417e-90cc-5b8135819d6f` (*GhostShot Systems*)  
> **Database References**:  
> - `gravity_sql.review_audit_runs`: `e3d4b791-8845-4209-915f-c96b718814df`  
> - `gravity_jsonb.code_review_findings`: Multiple Findings (Senior DOM Architect & Orchestration Engineer)  
> - `gravity_vector.architectural_embeddings`: 384-dimensional pgvector embedding  
> - `Paperclip Issues`: `GHO-27`, `GHO-28`, `GHO-29`, `GHO-30`, `GHO-31`

---

## 1. Context & Motivation

When testing full-page screen capture on modern complex responsive web pages (specifically W3Schools documentation layouts containing zero-height header wrappers, subnav containers, and left sidebar drawers), visual duplication occurred where the top navigation chrome repeated across every vertical scroll slice. 

Extensive root cause analysis proved:
1. Containers with `position: fixed` frequently collapse to `height: 0px` (or `width: 0px`) while wrapping rendered child elements with `position: absolute`.
2. Traditional heuristic filters (`rect.width > 0 && rect.height > 0`) discarded these containers, leaving their absolute children anchored to the viewport.
3. The option "Hide Sticky Navbars" must be default-active across all entry vectors (Popup, Options, Keyboard Shortcuts, and API calls) and backed by an idempotent style suppression engine.

---

## 2. Technical Architecture & Algorithm

### 2.1 The `isRenderedFixed` Multi-Axis Evaluator
```javascript
function isRenderedFixed(el, style) {
  if (style.position !== "fixed") return false;
  if (style.display === "none") return false;

  // 1. Direct bounding box dimensions
  const rect = el.getBoundingClientRect();
  if (rect.width > 0 && rect.height > 0) return true;

  // 2. Client rects for inline wrappers
  if (el.getClientRects && el.getClientRects().length > 0) return true;

  // 3. Overflow or scroll dimensions
  if (el.scrollWidth > 0 || el.scrollHeight > 0) return true;

  // 4. Zero-height/zero-width container with non-empty children
  // (e.g. #top-nav-bar has height: 0, but child #pagetop has height: 56)
  if (el.childElementCount > 0) return true;

  return false;
}
```

### 2.2 Idempotent WeakMap Style Caching
Dynamic re-discovery on every scroll slice (`sliceIndex > 0`) prevents scroll-injected headers from bypassing detection. An internal `originalStylesMap = new Map()` ensures original inline styles are recorded exactly once and never overwritten by subsequent suppression passes.

### 2.3 Force Suppression Without Layout Shift
Because `position: fixed` elements are out of normal document flow:
$$\Delta \text{Layout}(\text{body}) = 0$$
Applying `display: none !important; visibility: hidden !important; opacity: 0 !important;` completely removes the fixed subtree from the paint pipeline without causing document reflow.

---

## 3. Managed Chrome DevTools Profile Supervisor

Integrated into the AI enterprise toolchain:
* **Script**: `scripts/chrome_managed_profile.py`
* **Transport**: Chrome DevTools MCP with `--autoConnect`, `--enable-automation`, `--categoryExtensions`, and `--categoryInput`.
* **Supervision**: Live process, target, and service worker inspection.
