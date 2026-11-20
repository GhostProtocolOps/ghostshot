#!/usr/bin/env python3
"""
Codex MCP Server Bridge
Exposes locally installed OpenAI Codex CLI (authenticated via your ChatGPT Pro account)
to Antigravity and its autonomous agents with Full Access.
"""

import sys
import os
import json
import subprocess
import tempfile
import traceback

CODEX_PATH = os.environ.get("CODEX_PATH", "/usr/local/bin/codex")

def log(msg: str):
    """Logs to stderr to prevent corrupting stdout JSON-RPC stream."""
    sys.stderr.write(f"[codex-mcp] {msg}\n")
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
                "name": "codex-bridge",
                "version": "1.3.0"
            }
        }
    }

def handle_tools_list(msg_id):
    tools = [
        {
            "name": "codex_ask",
            "description": "Consult the locally installed OpenAI Codex CLI with Full Access (equivalent to /permissions -> Full Access -> Yes). Supports models ('o3-mini', 'o1', 'gpt-4o') and live web search.",
            "inputSchema": {
                "type": "object",
                "properties": {
                    "prompt": {
                        "type": "string",
                        "description": "The specific question, problem description, or code generation task."
                    },
                    "model": {
                        "type": "string",
                        "description": "OpenAI model to use (e.g. 'o3-mini', 'o1', 'gpt-4o'). Defaults to CLI default."
                    },
                    "reasoning_effort": {
                        "type": "string",
                        "enum": ["low", "medium", "high"],
                        "description": "Reasoning effort level for reasoning models like o3-mini or o1."
                    },
                    "enable_search": {
                        "type": "boolean",
                        "description": "Enable live web search via Codex's native web search capabilities."
                    },
                    "working_dir": {
                        "type": "string",
                        "description": "Working directory context for Codex (defaults to current project root)."
                    },
                    "full_access": {
                        "type": "boolean",
                        "description": "Run with full filesystem and execution permissions (defaults to true)."
                    }
                },
                "required": ["prompt"]
            }
        },
        {
            "name": "codex_reason",
            "description": "Deep reasoning tool using OpenAI's frontier reasoning models (e.g. o3-mini or o1 at high effort) with Full Access.",
            "inputSchema": {
                "type": "object",
                "properties": {
                    "problem_statement": {
                        "type": "string",
                        "description": "Detailed description of the hard problem, code context, constraints, and edge cases to analyze."
                    },
                    "model": {
                        "type": "string",
                        "description": "Reasoning model to use (default: 'o3-mini')."
                    },
                    "enable_search": {
                        "type": "boolean",
                        "description": "Enable live web search for real-time documentation or external context."
                    },
                    "working_dir": {
                        "type": "string",
                        "description": "Working directory context."
                    }
                },
                "required": ["problem_statement"]
            }
        },
        {
            "name": "codex_review",
            "description": "Run a non-interactive automated code review on the project repository or git changes using the local Codex CLI.",
            "inputSchema": {
                "type": "object",
                "properties": {
                    "working_dir": {
                        "type": "string",
                        "description": "Working directory of the repository to review."
                    }
                }
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

def run_codex_exec(prompt, model=None, reasoning_effort=None, enable_search=False, working_dir=None, full_access=True, timeout=360):
    with tempfile.NamedTemporaryFile(mode="r+", delete=False, suffix=".txt") as tf:
        temp_out = tf.name

    try:
        cmd = [
            CODEX_PATH,
            "exec",
            "--color", "never",
            "--skip-git-repo-check",
            "--ephemeral"
        ]

        # Full Access: equivalent to /permissions -> Full Access -> Yes
        if full_access:
            cmd.append("--dangerously-bypass-approvals-and-sandbox")
        else:
            cmd.extend(["-s", "read-only"])

        cmd.extend(["-o", temp_out])

        if enable_search:
            cmd.append("--search")
        if model:
            cmd.extend(["-m", model])
        if reasoning_effort:
            cmd.extend(["-c", f'model_reasoning_effort="{reasoning_effort}"'])
        if working_dir and os.path.isdir(working_dir):
            cmd.extend(["-C", working_dir])

        cmd.append(prompt)

        env = os.environ.copy()
        if "/usr/local/bin" not in env.get("PATH", ""):
            env["PATH"] = f"/usr/local/bin:{env.get('PATH', '')}"

        log(f"Calling Codex: model={model or 'default'}, full_access={full_access}")
        proc = subprocess.run(
            cmd,
            stdin=subprocess.DEVNULL,
            capture_output=True,
            text=True,
            timeout=timeout,
            env=env
        )

        output_text = ""
        if os.path.exists(temp_out):
            with open(temp_out, "r", encoding="utf-8", errors="replace") as f:
                output_text = f.read().strip()

        if not output_text:
            output_text = proc.stdout.strip()

        if proc.returncode != 0 and not output_text:
            err_msg = proc.stderr.strip() or f"Codex exited with code {proc.returncode}"
            return {"content": [{"type": "text", "text": f"Codex Execution Error:\n{err_msg}"}], "isError": True}

        return {
            "content": [{"type": "text", "text": output_text or "(No output received from Codex)"}],
            "isError": False
        }
    except subprocess.TimeoutExpired:
        return {"content": [{"type": "text", "text": f"Error: Codex execution timed out after {timeout} seconds."}], "isError": True}
    except Exception as e:
        return {"content": [{"type": "text", "text": f"Error running Codex: {str(e)}\n{traceback.format_exc()}"}], "isError": True}
    finally:
        if os.path.exists(temp_out):
            try:
                os.remove(temp_out)
            except OSError:
                pass

def handle_tools_call(msg_id, params):
    tool_name = params.get("name")
    arguments = params.get("arguments", {})

    if tool_name == "codex_ask":
        prompt = arguments.get("prompt", "")
        model = arguments.get("model")
        reasoning_effort = arguments.get("reasoning_effort")
        enable_search = arguments.get("enable_search", False)
        working_dir = arguments.get("working_dir")
        full_access = arguments.get("full_access", True)
        result = run_codex_exec(prompt, model, reasoning_effort, enable_search, working_dir, full_access)

    elif tool_name == "codex_reason":
        problem = arguments.get("problem_statement", "")
        model = arguments.get("model", "o3-mini")
        enable_search = arguments.get("enable_search", False)
        working_dir = arguments.get("working_dir")
        prompt = (
            "You are acting as an expert reasoning engine. Analyze this problem deeply, "
            "verify all edge cases, evaluate trade-offs, and provide the optimal solution:\n\n"
            f"{problem}"
        )
        result = run_codex_exec(prompt, model=model, reasoning_effort="high", enable_search=enable_search, working_dir=working_dir, full_access=True, timeout=480)

    elif tool_name == "codex_review":
        working_dir = arguments.get("working_dir")
        cmd = [CODEX_PATH, "exec", "review"]
        if working_dir and os.path.isdir(working_dir):
            cmd.extend(["-C", working_dir])
        env = os.environ.copy()
        if "/usr/local/bin" not in env.get("PATH", ""):
            env["PATH"] = f"/usr/local/bin:{env.get('PATH', '')}"
        try:
            proc = subprocess.run(cmd, stdin=subprocess.DEVNULL, capture_output=True, text=True, timeout=360, env=env)
            out = proc.stdout.strip() or proc.stderr.strip()
            result = {
                "content": [{"type": "text", "text": out or "Code review completed with no output."}],
                "isError": proc.returncode != 0
            }
        except Exception as e:
            result = {"content": [{"type": "text", "text": f"Error running review: {str(e)}"}], "isError": True}
    else:
        return {
            "jsonrpc": "2.0",
            "id": msg_id,
            "error": {
                "code": -32601,
                "message": f"Unknown tool: {tool_name}"
            }
        }

    return {
        "jsonrpc": "2.0",
        "id": msg_id,
        "result": result
    }

def main():
    log("Starting Codex MCP Bridge server (v1.3.0 with Full Access)...")
    while True:
        line = sys.stdin.readline()
        if not line:
            break
        line = line.strip()
        if not line:
            continue

        try:
            req = json.loads(line)
        except json.JSONDecodeError as e:
            log(f"Malformed JSON: {e}")
            continue

        msg_id = req.get("id")
        method = req.get("method")

        if method == "notifications/initialized":
            log("Client initialized.")
            continue

        if not method:
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
                    "error": {
                        "code": -32601,
                        "message": f"Method '{method}' not implemented."
                    }
                }

        if response is not None:
            sys.stdout.write(json.dumps(response) + "\n")
            sys.stdout.flush()

if __name__ == "__main__":
    main()
