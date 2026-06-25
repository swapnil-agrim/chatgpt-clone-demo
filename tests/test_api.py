"""Goal: Conversations REST API."""
import json


def test_list_empty(client):
    resp, body = client.request("GET", "/api/conversations")
    assert resp.status == 200 and json.loads(body) == []


def test_create_then_list_and_get_detail(client):
    resp, body = client.request("POST", "/api/conversations",
                                body=json.dumps({"title": "Hello"}), headers={"Content-Type": "application/json"})
    assert resp.status in (200, 201)
    cid = json.loads(body)["id"]
    assert json.loads(body)["title"] == "Hello"
    _, listing = client.request("GET", "/api/conversations")
    assert any(c["id"] == cid for c in json.loads(listing))
    resp, detail = client.request("GET", f"/api/conversations/{cid}")
    d = json.loads(detail)
    assert resp.status == 200 and d["conversation"]["id"] == cid and d["messages"] == []


def test_create_without_body_gets_default_title(client):
    resp, body = client.request("POST", "/api/conversations")
    assert resp.status in (200, 201) and json.loads(body)["title"]


def test_get_unknown_conversation_404(client):
    resp, _ = client.request("GET", "/api/conversations/99999")
    assert resp.status == 404
