"""Goal: streaming chat over SSE."""
import json


def _new_conv(client):
    _, b = client.request("POST", "/api/conversations",
                          body=json.dumps({"title": "t"}), headers={"Content-Type": "application/json"})
    return json.loads(b)["id"]


def test_stream_yields_chunks_and_persists_both_messages(client):
    cid = _new_conv(client)
    resp, body = client.request("POST", f"/api/conversations/{cid}/messages",
                                body=json.dumps({"content": "hello there"}), headers={"Content-Type": "application/json"})
    assert resp.status == 200
    assert "text/event-stream" in resp.getheader("Content-Type", "")
    assert len([ln for ln in body.splitlines() if ln.startswith("data:")]) >= 2
    _, detail = client.request("GET", f"/api/conversations/{cid}")
    msgs = json.loads(detail)["messages"]
    assert [m["role"] for m in msgs] == ["user", "assistant"]
    assert msgs[0]["content"] == "hello there" and msgs[1]["content"].strip()


def test_stream_unknown_conversation_404(client):
    resp, _ = client.request("POST", "/api/conversations/99999/messages",
                             body=json.dumps({"content": "x"}), headers={"Content-Type": "application/json"})
    assert resp.status == 404
