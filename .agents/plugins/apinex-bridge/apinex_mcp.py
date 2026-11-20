#!/usr/bin/env python3
"""
APInex MCP Server Bridge
Exposes APInex multi-model gateway (45 models with free-tier access) as an MCP tool.
Zero external dependencies (pure Python standard library).
"""

import sys
import os
import json
import urllib.request
import traceback

def get_env_var(name, default=""):
    val = os.environ.get(name)
    if val:
        return val
    # Try reading from workspace .env
    env_file = "/Users/nishant/Documents/gravity_work/GhostShot/.env"
    if os.path.exists(env_file):
        try:
            with open(env_file, "r") as f:
                for line in f:
                    line = line.strip()
                    if line.startswith(f"{name}="):
                        return line.split("=", 1)[1].strip()
        except Exception:
            pass
    return default

def log(msg: str):
    sys.stderr.write(f"[apinex-mcp] {msg}\n")
    sys.stderr.flush()

def handle_initialize(msg_id):
    return {
        "jsonrpc": "2.0",
        "id": msg_id,
        "result": {
            "protocolVersion": "2024-11-05",
            "capabilities": {
                "tools": {}
            },
            "serverInfo": {
                "name": "apinex-bridge",
                "version": "1.0.0"
            }
        }
    }

def handle_tools_list(msg_id):
    tools = [
        {
            "name": "apinex_ask",
            "description": "Send a prompt to any of APInex's 45 models (e.g. 'free/deepseek-v4.1-flash', 'free/gemini-3.8-flash', 'deepseek-v4-pro').",
            "inputSchema": {
                "type": "object",
                "properties": {
                    "prompt": {
                        "type": "string",
                        "description": "Prompt or instruction for the model."
                    },
                    "model": {
                        "type": "string",
                        "description": "Target model ID (defaults to 'free/deepseek-v4.1-flash')."
                    },
                    "max_tokens": {
                        "type": "integer",
                        "description": "Maximum tokens to generate (default: 1024)."
                    }
                },
                "required": ["prompt"]
            }
        },
        {
            "name": "apinex_list_models",
            "description": "List all 40+ active and free models available on your APInex account.",
            "inputSchema": {
                "type": "object",
                "properties": {}
            }
        }
    ]
    return {
        "jsonrpc": "2.0",
        "id": msg_id,
        "result": {
            "tools": tools
        }
    }

def run_apinex_ask(arguments):
    prompt = arguments.get("prompt", "")
    model = arguments.get("model", "free/deepseek-v4.1-flash")
    max_tokens = arguments.get("max_tokens", 1024)

    api_key = get_env_var("APINEX_API_KEY")
    base_url = get_env_var("APINEX_BASE_URL", "https://api.apinex.bond/v1").rstrip("/")

    if not api_key:
        return {"content": [{"type": "text", "text": "Error: APINEX_API_KEY not found in environment or .env file."}], "isError": True}

    url = f"{base_url}/chat/completions"
    payload = {
        "model": model,
        "messages": [{"role": "user", "content": prompt}],
        "max_tokens": max_tokens
    }

    req = urllib.request.Request(
        url,
        headers={"Authorization": f"Bearer {api_key}", "Content-Type": "application/json"},
        data=json.dumps(payload).encode("utf-8")
    )

    try:
        with urllib.request.urlopen(req, timeout=60) as resp:
            data = json.loads(resp.read().decode("utf-8"))
            content = data["choices"][0]["message"]["content"].strip()
            return {"content": [{"type": "text", "text": content}], "isError": False}
    except Exception as e:
        return {"content": [{"type": "text", "text": f"APInex API Error ({model}): {str(e)}"}], "isError": True}

def run_apinex_list_models():
    api_key = get_env_var("APINEX_API_KEY")
    base_url = get_env_var("APINEX_BASE_URL", "https://api.apinex.bond/v1").rstrip("/")

    if not api_key:
        return {"content": [{"type": "text", "text": "Error: APINEX_API_KEY not found."}], "isError": True}

    url = f"{base_url}/models"
    req = urllib.request.Request(
        url,
        headers={"Authorization": f"Bearer {api_key}"}
    )

    try:
        with urllib.request.urlopen(req, timeout=30) as resp:
            data = json.loads(resp.read().decode("utf-8"))
            models = [m.get("id") for m in data.get("data", [])]
            free_models = [m for m in models if "free" in m.lower()]
            text = f"Total Models: {len(models)}\n\nFree Models ({len(free_models)}):\n"
            text += "\n".join(f" - {m}" for m in free_models)
            text += "\n\nAll Other Models:\n"
            text += "\n".join(f" - {m}" for m in models if "free" not in m.lower())
            return {"content": [{"type": "text", "text": text}], "isError": False}
    except Exception as e:
        return {"content": [{"type": "text", "text": f"Error fetching models: {str(e)}"}], "isError": True}

def handle_tools_call(msg_id, params):
    tool_name = params.get("name")
    arguments = params.get("arguments", {})

    if tool_name == "apinex_ask":
        result = run_apinex_ask(arguments)
    elif tool_name == "apinex_list_models":
        result = run_apinex_list_models()
    else:
        return {
            "jsonrpc": "2.0",
            "id": msg_id,
            "error": {"code": -32601, "message": f"Unknown tool: {tool_name}"}
        }

    return {"jsonrpc": "2.0", "id": msg_id, "result": result}

def main():
    log("Starting APInex MCP Bridge server...")
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

        if response is not None:
            sys.stdout.write(json.dumps(response) + "\n")
            sys.stdout.flush()

if __name__ == "__main__":
    main()
