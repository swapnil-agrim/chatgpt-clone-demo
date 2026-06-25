# chatgpt-clone-demo

A minimal, ChatGPT-style streaming chat console — built as the end-to-end test workload for the
[LoopSmith](https://github.com/swapnil-agrim/loopsmith) goal-based SDLC pipeline. Every feature is a
GitHub issue (`sdlc:goal`) driven through LoopSmith's 7-phase loop, with status mirrored to a GitHub
Projects board (Backlog -> In Progress -> QC -> Done / Blocked).

## Stack
Python 3 stdlib only (`http.server`, `sqlite3`) + vanilla JS/CSS. Claude streaming when
`ANTHROPIC_API_KEY` is set, mock token-stream otherwise. SSE streaming, SQLite persistence.

## Run
> Built incrementally by the SDLC loop — run instructions land with the polish goal.
