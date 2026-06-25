# Architecture — chatgpt-clone-demo

A three-module, stdlib-only ChatGPT-style console. No framework, no build step.

## Layers
- **`storage.py`** — `Storage(db_path)` over SQLite. `conversations(id,title,created_at)`,
  `messages(id,conversation_id,role,content,created_at)`. CRUD + `set_title`. `check_same_thread=False`
  + a write lock for the threaded server.
- **`llm.py`** — adapter. `stream_reply(messages) -> iterator[str]`. Claude (`anthropic`, streaming)
  when `ANTHROPIC_API_KEY` set, else a mock token-stream. `active_backend()` drives the UI banner.
- **`server.py`** — `ThreadingHTTPServer`. Serves the SPA + the API.

## HTTP surface
- `GET /`, `GET /static/*` — SPA.
- `GET /api/meta` — `{backend}` for the mock-mode banner.
- `GET/POST /api/conversations`, `GET /api/conversations/{id}` — backlog CRUD.
- `POST /api/conversations/{id}/messages` — persist user turn → **stream** reply over SSE → persist
  full reply (+ auto-title on first turn). 404 unknown conv, 400 empty, SSE `error` event on failure.

## Frontend (`static/`)
- `index.html` two panes: `#sidebar` (list + New chat + banner), `#chat` (messages + composer).
- `app.js` — list/create/select conversations; stream replies via `fetch().body.getReader()`,
  appending tokens with `textContent`.

See [[retrospective]] for lessons.
