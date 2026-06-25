"""Goal: error handling + edge cases."""
import json
import llm


def _new_conv(client):
    _, b = client.request("POST", "/api/conversations",
                          body=json.dumps({"title": "t"}), headers={"Content-Type": "application/json"})
    return json.loads(b)["id"]


def test_empty_message_400_and_not_persisted(client):
    cid = _new_conv(client)
    resp, _ = client.request("POST", f"/api/conversations/{cid}/messages",
                             body=json.dumps({"content": "   "}), headers={"Content-Type": "application/json"})
    assert resp.status == 400
    _, detail = client.request("GET", f"/api/conversations/{cid}")
    assert json.loads(detail)["messages"] == []


def test_unknown_conversation_post_404(client):
    resp, _ = client.request("POST", "/api/conversations/4242/messages",
                             body=json.dumps({"content": "hi"}), headers={"Content-Type": "application/json"})
    assert resp.status == 404


def test_sse_emits_error_event_when_llm_raises(client, monkeypatch):
    cid = _new_conv(client)

    def boom(history):
        yield "partial "
        raise RuntimeError("model exploded")

    monkeypatch.setattr(llm, "stream_reply", boom)
    resp, body = client.request("POST", f"/api/conversations/{cid}/messages",
                                body=json.dumps({"content": "hi"}), headers={"Content-Type": "application/json"})
    assert resp.status == 200 and "event: error" in body


def test_meta_reports_mock_backend(client, monkeypatch):
    monkeypatch.delenv("ANTHROPIC_API_KEY", raising=False)
    resp, body = client.request("GET", "/api/meta")
    assert resp.status == 200 and json.loads(body)["backend"] == "mock"
