"""Shared fixture: a live server on an ephemeral port, backed by a temp DB."""
import threading
import http.client
import pytest
import server


@pytest.fixture
def live_server(tmp_path):
    srv = server.create_server(port=0, static_dir="static", db_path=str(tmp_path / "t.db"))
    port = srv.server_address[1]
    t = threading.Thread(target=srv.serve_forever, daemon=True)
    t.start()
    try:
        yield port
    finally:
        srv.shutdown()


class Client:
    def __init__(self, port):
        self.port = port

    def request(self, method, path, body=None, headers=None):
        conn = http.client.HTTPConnection("localhost", self.port, timeout=10)
        conn.request(method, path, body=body, headers=headers or {})
        resp = conn.getresponse()
        data = resp.read().decode()
        return resp, data


@pytest.fixture
def client(live_server):
    return Client(live_server)
