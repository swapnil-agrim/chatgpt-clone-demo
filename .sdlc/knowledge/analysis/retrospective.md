# Retrospective — chatgpt-clone-demo (fresh re-run, LoopSmith 0.5.0 + #8/#9)

Second full run, on a reset repo, with the upgraded plugin (GitHub PM scaffolding + audit trail + QC).

## Loop / process
- **8 goals → 7 done, 1 parked.** "Deploy to a public host" (#16) parked at the irreversible gate;
  backlog then drained. Park-and-continue verified again.
- **Audit trail (new):** each phase recorded via `loop.py note` lands as an issue comment — the issue
  timeline is now a readable build log (Research/Plan, Implement/Review, 🔒 Critical Insights).
- **QC stage (new):** `loop.py qc` moves the card to a QC column at review; board flow is
  Backlog → In Progress → QC → Done (Blocked for parked).
- **TDD per goal** kept green throughout; full suite 24 passing.

## Technical (unchanged, re-confirmed)
- SSE over stdlib `http.server`: `Connection: close` + `close_connection` + flush per frame; client
  reads with `fetch().body.getReader()` (not EventSource). JSON-encode each `data:` frame.
- Mock-LLM fallback behind one adapter → zero-config run + hermetic tests.
- Render user/LLM text with `textContent` (XSS).

## LoopSmith findings
- 🔒 **Board sync is fail-open and that matters:** mid/post-run, the `gh project` API entered a
  sustained "unknown owner type" error state. The loop kept going correctly (issues = source of truth
  all transitioned right); the Projects board just fell slightly behind (2 of 8 cards stale). A small
  **retry/backoff around the project ops** in `GitHubSource` would keep the board in sync through
  transient gh API blips — recommended v0.5.x improvement.
- The built-in "Status" field still can't be deleted (v0.5.1 cleanup already queued).

See [[architecture]] for how the app fits together.
