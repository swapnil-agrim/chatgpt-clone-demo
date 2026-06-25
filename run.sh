#!/usr/bin/env bash
# Start the chatgpt-clone-demo server.
#   ANTHROPIC_API_KEY set  -> streams real Claude replies
#   unset                  -> built-in mock token-stream (zero config)
# Override HOST / PORT / CHAT_DB via env if needed.
set -euo pipefail
cd "$(dirname "$0")"
exec python3 server.py
