# chatgpt-clone-demo

A minimal, ChatGPT-style streaming chat console — built as the end-to-end test workload for the
[LoopSmith](https://github.com/swapnil-agrim/loopsmith) goal-based SDLC pipeline. Every feature is a
GitHub issue (`sdlc:goal`) driven through LoopSmith's 7-phase loop, with status mirrored to a GitHub
Projects board (Backlog -> In Progress -> QC -> Done / Blocked).

## Stack
Python 3 stdlib only (`http.server`, `sqlite3`) + vanilla JS/CSS. Claude streaming when
`ANTHROPIC_API_KEY` is set, mock token-stream otherwise. SSE streaming, SQLite persistence.

## Run

No dependencies for mock mode — just Python 3:

```bash
./run.sh                 # or: python3 server.py
# open http://127.0.0.1:8000
```

Starts in **mock mode** (zero config). For real Claude replies:

```bash
pip install anthropic
export ANTHROPIC_API_KEY=sk-ant-...
./run.sh
```

Env overrides: `HOST` (default `127.0.0.1`), `PORT` (`8000`), `CHAT_DB` (`chat.db`).

## Test

```bash
python3 -m pytest -q
```
