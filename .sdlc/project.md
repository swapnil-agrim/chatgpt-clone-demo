# Project: chatgpt-clone-demo

A ChatGPT-style web chat console: conversation sidebar (past chats, "New chat"), a message thread,
a prompt box, and assistant replies that **stream** token-by-token. This repo is the test workload
for the LoopSmith SDLC pipeline (autonomous `/sdlc-loop`, GitHub-issue backlog + Projects board).

## Stack & conventions
- **Backend:** Python 3 standard library only (`http.server`, `sqlite3`, `json`). No web framework.
- **Frontend:** one static `index.html` + vanilla JS/CSS. No build step.
- **LLM:** the `anthropic` SDK (Claude, streaming) when `ANTHROPIC_API_KEY` is set; otherwise a
  built-in **mock token-stream** so it runs with no key. The adapter is the only LLM-aware module.
- **Streaming:** Server-Sent Events. **Persistence:** `sqlite3` (conversations + messages).
- Render user/LLM text with `textContent` only (never `innerHTML`).

## Verify command
verify: `python3 -m pytest -q`

## Taxonomy
- type: `type:feature`, `type:chore` · area: `area:backend`, `area:frontend`, `area:storage`, `area:llm`, `area:infra`

## Irreversible / expensive actions
- deploy / publish to a public host
- delete or overwrite production data
- spend money / launch paid compute
- migrate data

## North-star pointers
- Simplest thing that genuinely streams from an LLM and persists chats. No auth, no accounts.
- The mock fallback must always work with zero configuration.
