---
name: multi-bridge
description: Unified multi-model routing bridge connecting APInex free models (Qwen, GPT-6 Luna, Gemini 4, Kimi K3), direct official DeepSeek V3/R1, and local Codex CLI with intelligent 429 circuit breaking.
---

# Multi-Bridge Skill

This skill allows Antigravity to route prompts across multiple AI providers and models automatically or directly.

## Available Tools

1. **`auto_route_task`**:
   - `prompt`: The coding, reasoning, or text task.
   - `task_type`: `"coding"` (Qwen), `"reasoning"` (DeepSeek V4 Pro), `"schema"` (GPT-6 Luna), `"long_context"` (Gemini 4 / Kimi), or `"general"` (Gemini 3.8 Flash).
   - `allow_paid_fallback`: Boolean (default `false`). If `true`, permits falling back to official DeepSeek API if all free tier models are rate-limited.

2. **Direct Model Tools**:
   - `ask_qwen`: Query Alibaba Qwen (`free/qwen-3.8-max`).
   - `ask_gpt`: Query OpenAI GPT architecture (`free/gpt-6-luna`).
   - `ask_gemini`: Query Google Gemini (`free/gemini-4-hydrogen` or `free/gemini-3.8-flash`).
   - `ask_kimi`: Query Moonshot Kimi (`free/kimi-k3`).
   - `ask_deepseek_free`: Query DeepSeek via APInex (`free/deepseek-v4-pro-0813` or `free/deepseek-v4.1-flash`).
   - `ask_deepseek_direct`: Query official Direct DeepSeek API (`deepseek-chat` or `deepseek-reasoner`).

3. **Consensus Tool**:
   - `compare_models`: Send a single prompt to multiple models (e.g. Qwen + GPT + DeepSeek) and compare their responses side-by-side.
