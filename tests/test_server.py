"""Goal: HTTP server + static two-pane shell."""


def test_root_serves_two_pane_html(client):
    resp, body = client.request("GET", "/")
    assert resp.status == 200
    assert "text/html" in resp.getheader("Content-Type", "")
    assert 'id="sidebar"' in body and 'id="chat"' in body
    assert "New chat" in body


def test_static_css_served_with_type(client):
    resp, body = client.request("GET", "/static/styles.css")
    assert resp.status == 200
    assert "text/css" in resp.getheader("Content-Type", "")
    assert len(body) > 0


def test_unknown_path_404(client):
    resp, _ = client.request("GET", "/nope/not/here")
    assert resp.status == 404
