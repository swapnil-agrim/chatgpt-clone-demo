"""Stdlib HTTP server for the chat console: serves the static SPA and (later goals) the JSON +
SSE API. ThreadingHTTPServer so streaming one client never blocks another.
"""
import json
import mimetypes
import os
from http.server import BaseHTTPRequestHandler, ThreadingHTTPServer
from urllib.parse import urlparse

from storage import Storage

STATIC_DIR = os.path.join(os.path.dirname(os.path.abspath(__file__)), "static")


class Handler(BaseHTTPRequestHandler):
    protocol_version = "HTTP/1.1"

    def log_message(self, *args):
        pass  # quiet test runs

    @property
    def store(self):
        return self.server.store

    @property
    def static_dir(self):
        return self.server.static_dir

    # --- routing ---
    def do_GET(self):
        path = urlparse(self.path).path
        if path == "/":
            return self._send_file(os.path.join(self.static_dir, "index.html"), "text/html; charset=utf-8")
        if path.startswith("/static/"):
            return self._serve_static(path[len("/static/"):])
        return self._error(404, "not found")

    # --- helpers ---
    def _serve_static(self, rel):
        rel = rel.lstrip("/")
        full = os.path.normpath(os.path.join(self.static_dir, rel))
        if not full.startswith(self.static_dir) or not os.path.isfile(full):
            return self._error(404, "not found")
        ctype = mimetypes.guess_type(full)[0] or "application/octet-stream"
        return self._send_file(full, ctype)

    def _send_file(self, full, ctype):
        try:
            with open(full, "rb") as f:
                body = f.read()
        except OSError:
            return self._error(404, "not found")
        self.send_response(200)
        self.send_header("Content-Type", ctype)
        self.send_header("Content-Length", str(len(body)))
        self.end_headers()
        self.wfile.write(body)

    def _send_json(self, obj, status=200):
        body = json.dumps(obj).encode()
        self.send_response(status)
        self.send_header("Content-Type", "application/json")
        self.send_header("Content-Length", str(len(body)))
        self.end_headers()
        self.wfile.write(body)

    def _error(self, status, message):
        self._send_json({"error": message}, status=status)


def create_server(port=0, host="127.0.0.1", static_dir=STATIC_DIR, db_path="chat.db"):
    srv = ThreadingHTTPServer((host, port), Handler)
    srv.store = Storage(db_path)
    srv.static_dir = os.path.abspath(static_dir)
    return srv


def main():
    host = os.environ.get("HOST", "127.0.0.1")
    port = int(os.environ.get("PORT", "8000"))
    srv = create_server(port=port, host=host, db_path=os.environ.get("CHAT_DB", "chat.db"))
    print(f"chatgpt-clone-demo serving on http://{host}:{srv.server_address[1]}")
    try:
        srv.serve_forever()
    except KeyboardInterrupt:
        srv.shutdown()


if __name__ == "__main__":
    main()
