"""Goal: polish — title autogen, run script, README run steps."""
import json
import os


def test_first_message_autogenerates_title(client):
    _, b = client.request("POST", "/api/conversations",
                          body=json.dumps({"title": "New chat"}), headers={"Content-Type": "application/json"})
    cid = json.loads(b)["id"]
    client.request("POST", f"/api/conversations/{cid}/messages",
                   body=json.dumps({"content": "What is the capital of France?"}),
                   headers={"Content-Type": "application/json"})
    _, detail = client.request("GET", f"/api/conversations/{cid}")
    title = json.loads(detail)["conversation"]["title"]
    assert title != "New chat" and "capital" in title.lower()


def test_run_script_exists_and_executable():
    assert os.path.isfile("run.sh") and os.access("run.sh", os.X_OK)


def test_readme_documents_how_to_run():
    txt = open("README.md").read().lower()
    assert "run.sh" in txt or "python3 server.py" in txt
