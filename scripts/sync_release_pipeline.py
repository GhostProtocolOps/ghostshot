#!/usr/bin/env python3
import urllib.request
import json
import uuid

# 1. Paperclip updates
company_id = 'a9cd98a6-04c3-417e-90cc-5b8135819d6f'
project_id = 'a6acefb0-c4ac-42e5-b0f5-980e1a11c081'
engine_id = '93ca1e2a-59ea-4dab-90c9-85555b9682b6'

new_issues = [
    {
        'title': 'Git Repository Release: Push v2.0.0 with GoFullPage Parity Fixes',
        'description': 'Committed and pushed commit 67727c3 and release tag v2.0.0 to https://github.com/GhostProtocolOps/ghostshot.git.',
        'priority': 'critical',
        'status': 'done',
        'assigneeAgentId': engine_id
    },
    {
        'title': 'Chrome Web Store Developer Pipeline: Package v2.0.0 ZIP & Upload Pipeline',
        'description': 'Verified dist/ghostshot-chrome-brave-edge.zip (53.25 KB, SHA256 2b993ce8...), created scripts/upload_cws.py for automated/manual CWS updates.',
        'priority': 'critical',
        'status': 'done',
        'assigneeAgentId': engine_id
    },
    {
        'title': 'Chrome DevTools MCP Managed Profile Integration & Automated Extension Testing',
        'description': 'Integrated Chrome DevTools MCP with extension automation. Reloaded pjmebjdolmjagkldnddeifdpbbfogggn, triggered full page capture on W3Schools AWS page, verified stitched 1440x2868px canvas with zero seams.',
        'priority': 'critical',
        'status': 'done',
        'assigneeAgentId': engine_id
    }
]

for iss in new_issues:
    payload = {
        'companyId': company_id,
        'projectId': project_id,
        'title': iss['title'],
        'description': iss['description'],
        'priority': iss['priority'],
        'status': iss['status'],
        'assigneeAgentId': iss['assigneeAgentId']
    }
    try:
        req = urllib.request.Request(
            f'http://127.0.0.1:3100/api/companies/{company_id}/issues',
            data=json.dumps(payload).encode(),
            headers={'Content-Type': 'application/json'},
            method='POST'
        )
        with urllib.request.urlopen(req) as resp:
            data = json.loads(resp.read().decode())
            print(f'✅ Paperclip issue created: {data.get("identifier", "OK")} - {data.get("title")}')
    except Exception as e:
        print('Paperclip create error:', e)

# 2. OpenDots RFC-006
space_id = 'f88253c3-a18c-4c1a-83eb-bfd806bb6385'
rfc006 = {
    'title': 'RFC-006: Chrome DevTools MCP Managed Profile Extension Automation & CWS Deployment Runbook',
    'content': '''# RFC-006: Chrome DevTools MCP Managed Profile Extension Automation & CWS Deployment Runbook

## 1. Chrome DevTools MCP Automation Architecture
GhostShot integrates directly with Chrome DevTools MCP for end-to-end automated UI testing and extension lifecycle management:
- **Managed Profile Path**: Dedicated Chrome profile with `--categoryExtensions`, `--experimentalIncludeAllPages`, and `--categoryInput`.
- **Extension Discovery & Reload**:
  - `list_extensions`: Discovers installed extension ID `pjmebjdolmjagkldnddeifdpbbfogggn`.
  - `reload_extension`: Invalidate cached scripts and loads freshly compiled dist bundle without browser restart.
  - `trigger_extension_action`: Dispatches extension action popup.
  - `evaluate_script`: Programmatically verifies canvas tiles, pixel dimensions, and DOM suppression states.

## 2. Chrome Web Store Deployment Pipeline
- **Package Location**: `dist/ghostshot-chrome-brave-edge.zip`
- **Integrity**: 53.25 KB, 35 files, SHA-256 `2b993ce85f51d569171385d4ab59a0b0bfa33a48939edc4b6dee31fb138cb229`.
- **Automated CLI**: `scripts/upload_cws.py` supports direct OAuth2 token exchange with Google Web Store API endpoint `https://www.googleapis.com/upload/chromewebstore/v1.1/items/{itemId}`.
- **Manual Console**: 1-click package replacement via `https://chrome.google.com/webstore/devconsole` under Developer Mode.

## 3. GitHub Git Release
- Remote: `https://github.com/GhostProtocolOps/ghostshot.git`
- Branch: `main` (commit `67727c3`)
- Tag: `v2.0.0`'''
}

try:
    req = urllib.request.Request(
        f'http://127.0.0.1:4310/api/spaces/{space_id}/pages',
        data=json.dumps(rfc006).encode(),
        headers={'Content-Type': 'application/json'},
        method='POST'
    )
    with urllib.request.urlopen(req) as resp:
        data = json.loads(resp.read().decode())
        print(f'✅ OpenDots page created: {data.get("title")}')
except Exception as e:
    print('OpenDots create error:', e)
