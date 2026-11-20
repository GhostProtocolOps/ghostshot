---
name: codex-bridge
description: Delegate deep reasoning, code generation, and automated code review to the locally installed OpenAI Codex CLI across all its supported models (o3-mini, o1, gpt-4o).
---

# Codex Bridge Skill

This skill allows Antigravity to collaborate with the user's local `codex` CLI using their ChatGPT Pro account.

## Available Tools & Models

1. **`codex_reason`**:
   - Triggers deep reasoning mode using OpenAI frontier reasoning models (e.g. `o3-mini`, `o1` with high reasoning effort).
   - Ideal for algorithmic problems, concurrency, hard debugging, and architectural trade-offs.

2. **`codex_ask`**:
   - General-purpose tool to invoke Codex.
   - Allows explicit model selection (`model: "o3-mini"`, `"o1"`, `"gpt-4o"`, etc.).
   - Supports `reasoning_effort`: `"low"`, `"medium"`, `"high"`.
   - Supports `write_access`: Boolean to allow or restrict direct file modifications.

3. **`codex_review`**:
   - Executes `codex exec review` to run non-interactive code review across the repository or unstaged git changes.
