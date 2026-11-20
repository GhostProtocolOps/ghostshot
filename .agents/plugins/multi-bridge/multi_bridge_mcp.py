#!/usr/bin/env python3
"""
Multi-Model Unified AI Bridge MCP Server (v2.1.0)
Features:
1. Intelligent Auto-Routing (auto_route_task) with task-based model selection.
2. 429 Circuit-Breaker: Graceful fallback between free models without draining paid balance.
3. Protected Paid Fallback: Only uses direct DeepSeek API ($50 pool) when explicitly permitted.
4. Direct Model Tools: ask_qwen, ask_gpt, ask_gemini, ask_kimi, ask_deepseek_direct, ask_deepseek_free.
5. Multi-Model Consensus: compare_models for cross-checking responses side-by-side.

Zero external dependencies (pure Python standard library).
"""

import sys
import os
import json
import urllib.request
import urllib.error
import time
import traceback

# In-memory circuit breaker cooldowns: {model_name: timestamp_when_available}
COOLDOWNS = {}

def get_env_var(name, default=""):
    val = os.environ.get(name)
    if val:
        return val
    candidates = [
        os.path.join(os.getcwd(), ".env"),
        os.path.expanduser("~/.gemini/config/.env"),
        os.path.expanduser("~/.env"),
        "/Users/nishant/Documents/gravity_work/gravity_1/.env"
    ]
    for env_path in candidates:
        if os.path.exists(env_path):
            try:
                with open(env_path, "r", encoding="utf-8") as f:
                    for line in f:
                        line = line.strip()
                        if line.startswith(f"{name}="):
                            v = line.split("=", 1)[1].strip()
                            if (v.startswith('"') and v.endswith('"')) or (v.startswith("'") and v.endswith("'")):
                                v = v[1:-1]
                            if v:
                                return v
            except Exception:
                pass
    return default

def log(msg: str):
    sys.stderr.write(f"[multi-bridge] {msg}\n")
    sys.stderr.flush()

def make_chat_request(url, api_key, model, prompt, system_prompt=None, max_tokens=1500, temperature=0.7, timeout=60):
    now = time.time()
    if model in COOLDOWNS and now < COOLDOWNS[model]:
        wait_left = int(COOLDOWNS[model] - now)
        return {"content": None, "error": f"CircuitBreakerActive: {model} is on cooldown for {wait_left}s due to recent rate limit."}

    messages = []
    if system_prompt:
        messages.append({"role": "system", "content": system_prompt})
    messages.append({"role": "user", "content": prompt})

    payload = {
        "model": model,
        "messages": messages,
        "max_tokens": max_tokens,
        "temperature": temperature
    }

    req = urllib.request.Request(
        url,
        headers={
            "Authorization": f"Bearer {api_key}",
            "Content-Type": "application/json",
            "User-Agent": "Antigravity-MultiBridge/2.1"
        },
        data=json.dumps(payload).encode("utf-8")
    )

    try:
        with urllib.request.urlopen(req, timeout=timeout) as resp:
            data = json.loads(resp.read().decode("utf-8"))
            content = data["choices"][0]["message"]["content"].strip()
            usage = data.get("usage", {})
            return {"content": content, "usage": usage, "error": None}
    except urllib.error.HTTPError as e:
        body = e.read().decode("utf-8", errors="replace")
        if e.code == 429:
            # Set a 30-second circuit breaker cooldown on this model
            COOLDOWNS[model] = time.time() + 30
            log(f"Model {model} hit HTTP 429. Setting 30s cooldown.")
        return {"content": None, "error": f"HTTP {e.code}: {body}"}
    except Exception as e:
        return {"content": None, "error": str(e)}

def handle_initialize(msg_id):
    return {
        "jsonrpc": "2.0",
        "id": msg_id,
        "result": {
            "protocolVersion": "2024-11-05",
            "capabilities": {"tools": {}},
            "serverInfo": {
                "name": "multi-bridge",
                "version": "2.1.0"
            }
        }
    }

def handle_tools_list(msg_id):
    tools = [
        {
            "name": "auto_route_task",
            "description": "Intelligent multi-model router. Automatically selects the optimal free model based on task type (coding, reasoning, schema, long_context), handles 429 circuit-breakers, and falls back safely.",
            "inputSchema": {
                "type": "object",
                "properties": {
                    "prompt": {"type": "string", "description": "The task, question, or code generation instruction."},
                    "task_type": {
                        "type": "string",
                        "enum": ["coding", "reasoning", "schema", "long_context", "general"],
                        "description": "Category of work: 'coding' (Qwen), 'reasoning' (DeepSeek V4 Pro), 'schema' (GPT-6 Luna), 'long_context' (Gemini 4 / Kimi), 'general' (Gemini 3.8 Flash). Default: coding."
                    },
                    "allow_paid_fallback": {
                        "type": "boolean",
                        "description": "Set to true to allow falling back to official paid DeepSeek API if all free tier models are rate-limited. Default is false to strictly protect your balance."
                    },
                    "system_prompt": {"type": "string", "description": "Optional system prompt persona."}
                },
                "required": ["prompt"]
            }
        },
        {
            "name": "ask_qwen",
            "description": "Direct query to Alibaba Qwen ('free/qwen-3.8-max') via APInex for free. Best for backend logic, algorithm design, and python/ts coding.",
            "inputSchema": {
                "type": "object",
                "properties": {
                    "prompt": {"type": "string", "description": "Coding question or implementation task."},
                    "system_prompt": {"type": "string", "description": "Optional system prompt."}
                },
                "required": ["prompt"]
            }
        },
        {
            "name": "ask_gpt",
            "description": "Direct query to OpenAI GPT architecture ('free/gpt-6-luna') via APInex for free. Best for structured schema generation, JSON parsing, and creative logic.",
            "inputSchema": {
                "type": "object",
                "properties": {
                    "prompt": {"type": "string", "description": "Instruction or prompt."},
                    "system_prompt": {"type": "string", "description": "Optional system prompt."}
                },
                "required": ["prompt"]
            }
        },
        {
            "name": "ask_gemini",
            "description": "Direct query to Google Gemini ('free/gemini-4-hydrogen' or 'free/gemini-3.8-flash') via APInex for free. Best for long context and fast drafts.",
            "inputSchema": {
                "type": "object",
                "properties": {
                    "prompt": {"type": "string", "description": "Prompt or instruction."},
                    "model": {
                        "type": "string",
                        "enum": ["free/gemini-4-hydrogen", "free/gemini-3.8-flash"],
                        "description": "Gemini 4 Hydrogen (frontier) or Gemini 3.8 Flash (ultra-fast)."
                    },
                    "system_prompt": {"type": "string", "description": "Optional system prompt."}
                },
                "required": ["prompt"]
            }
        },
        {
            "name": "ask_kimi",
            "description": "Direct query to Moonshot Kimi ('free/kimi-k3') via APInex for free. Best for massive documentation analysis and research synthesis.",
            "inputSchema": {
                "type": "object",
                "properties": {
                    "prompt": {"type": "string", "description": "Research query or document summary."},
                    "system_prompt": {"type": "string", "description": "Optional system prompt."}
                },
                "required": ["prompt"]
            }
        },
        {
            "name": "ask_deepseek_free",
            "description": "Query DeepSeek via APInex for free ('free/deepseek-v4-pro-0813' or 'free/deepseek-v4.1-flash') without consuming direct account balance.",
            "inputSchema": {
                "type": "object",
                "properties": {
                    "prompt": {"type": "string", "description": "Coding or reasoning prompt."},
                    "model": {
                        "type": "string",
                        "enum": ["free/deepseek-v4-pro-0813", "free/deepseek-v4.1-flash"],
                        "description": "V4 Pro (reasoning) or V4.1 Flash (speed)."
                    },
                    "system_prompt": {"type": "string", "description": "Optional system prompt."}
                },
                "required": ["prompt"]
            }
        },
        {
            "name": "ask_deepseek_direct",
            "description": "Query official Direct DeepSeek API (powered by your $50 balance). Use for production code generation, official DeepSeek-V3, or DeepSeek-R1 reasoning.",
            "inputSchema": {
                "type": "object",
                "properties": {
                    "prompt": {"type": "string", "description": "The coding or reasoning task."},
                    "model": {
                        "type": "string",
                        "enum": ["deepseek-chat", "deepseek-reasoner"],
                        "description": "deepseek-chat (V3 fast coding) or deepseek-reasoner (R1 reasoning chain)."
                    },
                    "system_prompt": {"type": "string", "description": "Optional system prompt persona."}
                },
                "required": ["prompt"]
            }
        },
        {
            "name": "compare_models",
            "description": "Query 2 or 3 models simultaneously (e.g. Qwen, GPT, DeepSeek) and compare their responses side-by-side for consensus.",
            "inputSchema": {
                "type": "object",
                "properties": {
                    "prompt": {"type": "string", "description": "The prompt to compare across models."},
                    "models": {
                        "type": "array",
                        "items": {"type": "string"},
                        "description": "List of models to compare, e.g. ['qwen', 'gpt', 'deepseek', 'gemini']."
                    }
                },
                "required": ["prompt"]
            }
        }
    ]
    return {
        "jsonrpc": "2.0",
        "id": msg_id,
        "result": {"tools": tools}
    }

def handle_auto_route(args, apx_base, apx_key, ds_key):
    prompt = args.get("prompt", "")
    task_type = args.get("task_type", "coding").lower()
    allow_paid = args.get("allow_paid_fallback", False)
    system_prompt = args.get("system_prompt", "You are an elite expert software engineer. Provide concise, clean, production-grade solutions.")

    # Strategy Map: (Primary Free Model, Secondary Free Fallback)
    routes = {
        "coding": ("free/qwen-3.8-max", "free/deepseek-v4.1-flash"),
        "reasoning": ("free/deepseek-v4-pro-0813", "free/qwen-3.8-max"),
        "schema": ("free/gpt-6-luna", "free/qwen-3.8-max"),
        "long_context": ("free/gemini-4-hydrogen", "free/kimi-k3"),
        "general": ("free/gemini-3.8-flash", "free/deepseek-v4.1-flash")
    }

    primary_model, fallback_model = routes.get(task_type, routes["coding"])

    # Attempt 1: Primary Free Model
    log(f"Auto-Routing ({task_type}) -> Primary: {primary_model}")
    res = make_chat_request(apx_base, apx_key, primary_model, prompt, system_prompt)
    if not res["error"]:
        header = f"[Routed to: {primary_model} (Tier 1 Free)]\n\n"
        return {"content": [{"type": "text", "text": header + res["content"]}], "isError": False}

    log(f"Primary {primary_model} failed ({res['error']}). Trying fallback: {fallback_model}")

    # Attempt 2: Secondary Free Model
    time.sleep(1.0)
    res2 = make_chat_request(apx_base, apx_key, fallback_model, prompt, system_prompt)
    if not res2["error"]:
        header = f"[Primary rate-limited. Routed to Fallback: {fallback_model} (Tier 1 Free)]\n\n"
        return {"content": [{"type": "text", "text": header + res2["content"]}], "isError": False}

    # Attempt 3: Paid DeepSeek Fallback (Only if explicitly permitted)
    if allow_paid and ds_key:
        log("Free models unavailable. Engaging Tier 2: Direct DeepSeek API ($50 pool)")
        ds_model = "deepseek-reasoner" if task_type == "reasoning" else "deepseek-chat"
        res3 = make_chat_request("https://api.deepseek.com/chat/completions", ds_key, ds_model, prompt, system_prompt)
        if not res3["error"]:
            header = f"[Tier 1 Exhausted. Routed to Paid Tier 2: {ds_model} (Official DeepSeek API)]\n\n"
            return {"content": [{"type": "text", "text": header + res3["content"]}], "isError": False}
        return {"content": [{"type": "text", "text": f"Error across all tiers. DeepSeek Direct error: {res3['error']}"}], "isError": True}

    msg = (
        f"Free tier models ({primary_model}, {fallback_model}) were temporarily busy or rate-limited.\n"
        "To protect your $50 balance, paid fallback was not engaged.\n"
        "To allow falling back to official DeepSeek, pass `allow_paid_fallback: true`."
    )
    return {"content": [{"type": "text", "text": msg}], "isError": True}

def handle_tools_call(msg_id, params):
    tool_name = params.get("name")
    args = params.get("arguments", {})

    prompt = args.get("prompt", "")
    system_prompt = args.get("system_prompt", "You are an elite expert software engineer. Provide concise, clean, production-grade solutions.")

    ds_key = get_env_var("DEEPSEEK_API_KEY")
    apx_key = get_env_var("APINEX_API_KEY")
    apx_base = get_env_var("APINEX_BASE_URL", "https://api.apinex.bond/v1").rstrip("/") + "/chat/completions"

    if tool_name == "auto_route_task":
        result = handle_auto_route(args, apx_base, apx_key, ds_key)
        return {"jsonrpc": "2.0", "id": msg_id, "result": result}

    elif tool_name == "ask_deepseek_direct":
        if not ds_key:
            return {"jsonrpc": "2.0", "id": msg_id, "result": {"content": [{"type": "text", "text": "Error: DEEPSEEK_API_KEY is missing."}], "isError": True}}
        model = args.get("model", "deepseek-chat")
        res = make_chat_request("https://api.deepseek.com/chat/completions", ds_key, model, prompt, system_prompt)
        if res["error"]:
            return {"jsonrpc": "2.0", "id": msg_id, "result": {"content": [{"type": "text", "text": f"DeepSeek Direct Error: {res['error']}"}], "isError": True}}
        return {"jsonrpc": "2.0", "id": msg_id, "result": {"content": [{"type": "text", "text": res["content"]}], "isError": False}}

    elif tool_name == "ask_qwen":
        res = make_chat_request(apx_base, apx_key, "free/qwen-3.8-max", prompt, system_prompt)
        text = res["content"] if not res["error"] else f"Qwen Error: {res['error']}"
        return {"jsonrpc": "2.0", "id": msg_id, "result": {"content": [{"type": "text", "text": text}], "isError": bool(res["error"])}}

    elif tool_name == "ask_gpt":
        res = make_chat_request(apx_base, apx_key, "free/gpt-6-luna", prompt, system_prompt)
        text = res["content"] if not res["error"] else f"GPT Error: {res['error']}"
        return {"jsonrpc": "2.0", "id": msg_id, "result": {"content": [{"type": "text", "text": text}], "isError": bool(res["error"])}}

    elif tool_name == "ask_gemini":
        model = args.get("model", "free/gemini-4-hydrogen")
        res = make_chat_request(apx_base, apx_key, model, prompt, system_prompt)
        text = res["content"] if not res["error"] else f"Gemini Error: {res['error']}"
        return {"jsonrpc": "2.0", "id": msg_id, "result": {"content": [{"type": "text", "text": text}], "isError": bool(res["error"])}}

    elif tool_name == "ask_kimi":
        res = make_chat_request(apx_base, apx_key, "free/kimi-k3", prompt, system_prompt)
        text = res["content"] if not res["error"] else f"Kimi Error: {res['error']}"
        return {"jsonrpc": "2.0", "id": msg_id, "result": {"content": [{"type": "text", "text": text}], "isError": bool(res["error"])}}

    elif tool_name == "ask_deepseek_free":
        model = args.get("model", "free/deepseek-v4-pro-0813")
        res = make_chat_request(apx_base, apx_key, model, prompt, system_prompt)
        text = res["content"] if not res["error"] else f"DeepSeek Free Error: {res['error']}"
        return {"jsonrpc": "2.0", "id": msg_id, "result": {"content": [{"type": "text", "text": text}], "isError": bool(res["error"])}}

    elif tool_name == "compare_models":
        selected = args.get("models", ["qwen", "gpt", "deepseek"])
        outputs = []
        model_map = {
            "qwen": (apx_base, apx_key, "free/qwen-3.8-max", "Alibaba Qwen 3.8 Max"),
            "gpt": (apx_base, apx_key, "free/gpt-6-luna", "OpenAI GPT-6 Luna"),
            "gemini": (apx_base, apx_key, "free/gemini-4-hydrogen", "Google Gemini 4 Hydrogen"),
            "deepseek": ("https://api.deepseek.com/chat/completions", ds_key, "deepseek-chat", "Official DeepSeek V3"),
            "kimi": (apx_base, apx_key, "free/kimi-k3", "Moonshot Kimi K3")
        }

        for name in selected:
            key_name = name.lower()
            if key_name in model_map:
                url, k, m, label = model_map[key_name]
                r = make_chat_request(url, k, m, prompt, system_prompt, max_tokens=600, timeout=40)
                ans = r["content"] if not r["error"] else f"(Error: {r['error']})"
                outputs.append(f"### {label}\n{ans}")
                time.sleep(1.0)

        final_text = "\n\n---\n\n".join(outputs) if outputs else "No valid models selected for comparison."
        return {"jsonrpc": "2.0", "id": msg_id, "result": {"content": [{"type": "text", "text": final_text}], "isError": False}}

    return {
        "jsonrpc": "2.0",
        "id": msg_id,
        "error": {"code": -32601, "message": f"Unknown tool: {tool_name}"}
    }

def main():
    log("Starting Multi-Model AI Bridge MCP Server (v2.1.0 with Auto-Router)...")
    while True:
        line = sys.stdin.readline()
        if not line:
            break
        line = line.strip()
        if not line:
            continue

        try:
            req = json.loads(line)
        except json.JSONDecodeError:
            continue

        msg_id = req.get("id")
        method = req.get("method")

        if method == "notifications/initialized":
            continue

        response = None
        if method == "initialize":
            response = handle_initialize(msg_id)
        elif method == "tools/list":
            response = handle_tools_list(msg_id)
        elif method == "tools/call":
            response = handle_tools_call(msg_id, req.get("params", {}))
        elif method == "ping":
            response = {"jsonrpc": "2.0", "id": msg_id, "result": {}}
        else:
            if msg_id is not None:
                response = {
                    "jsonrpc": "2.0",
                    "id": msg_id,
                    "error": {"code": -32601, "message": f"Method '{method}' not implemented."}
                }

        if response is not None:
            sys.stdout.write(json.dumps(response) + "\n")
            sys.stdout.flush()

if __name__ == "__main__":
    main()
