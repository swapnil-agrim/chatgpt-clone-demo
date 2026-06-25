"""SQLite persistence for conversations and messages. Stdlib only.

One Storage wraps one DB file. check_same_thread=False so the threaded http.server can share it;
a single lock serialises writes (the demo is low-concurrency).
"""
import sqlite3
import threading
from datetime import datetime, timezone


def _now():
    return datetime.now(timezone.utc).isoformat()


class Storage:
    def __init__(self, db_path):
        self._db = sqlite3.connect(db_path, check_same_thread=False)
        self._db.row_factory = sqlite3.Row
        self._lock = threading.Lock()
        self._init_schema()

    def _init_schema(self):
        with self._lock:
            self._db.executescript(
                """
                CREATE TABLE IF NOT EXISTS conversations (
                    id INTEGER PRIMARY KEY AUTOINCREMENT,
                    title TEXT NOT NULL,
                    created_at TEXT NOT NULL
                );
                CREATE TABLE IF NOT EXISTS messages (
                    id INTEGER PRIMARY KEY AUTOINCREMENT,
                    conversation_id INTEGER NOT NULL,
                    role TEXT NOT NULL,
                    content TEXT NOT NULL,
                    created_at TEXT NOT NULL,
                    FOREIGN KEY (conversation_id) REFERENCES conversations(id)
                );
                """
            )
            self._db.commit()

    # --- conversations ---
    def create_conversation(self, title="New chat"):
        with self._lock:
            cur = self._db.execute(
                "INSERT INTO conversations (title, created_at) VALUES (?, ?)", (title, _now())
            )
            self._db.commit()
            return cur.lastrowid

    def list_conversations(self):
        rows = self._db.execute(
            "SELECT id, title, created_at FROM conversations ORDER BY id DESC"
        ).fetchall()
        return [dict(r) for r in rows]

    def get_conversation(self, conversation_id):
        row = self._db.execute(
            "SELECT id, title, created_at FROM conversations WHERE id = ?", (conversation_id,)
        ).fetchone()
        return dict(row) if row else None

    def set_title(self, conversation_id, title):
        with self._lock:
            self._db.execute(
                "UPDATE conversations SET title = ? WHERE id = ?", (title, conversation_id)
            )
            self._db.commit()

    # --- messages ---
    def add_message(self, conversation_id, role, content):
        with self._lock:
            cur = self._db.execute(
                "INSERT INTO messages (conversation_id, role, content, created_at) VALUES (?, ?, ?, ?)",
                (conversation_id, role, content, _now()),
            )
            self._db.commit()
            return cur.lastrowid

    def get_messages(self, conversation_id):
        rows = self._db.execute(
            "SELECT id, conversation_id, role, content, created_at FROM messages "
            "WHERE conversation_id = ? ORDER BY id ASC",
            (conversation_id,),
        ).fetchall()
        return [dict(r) for r in rows]
