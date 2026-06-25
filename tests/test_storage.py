"""Goal: SQLite storage layer."""
import storage


def _store(tmp_path):
    return storage.Storage(str(tmp_path / "chat.db"))


def test_create_and_get_conversation(tmp_path):
    s = _store(tmp_path)
    cid = s.create_conversation("My first chat")
    conv = s.get_conversation(cid)
    assert conv["id"] == cid and conv["title"] == "My first chat" and conv["created_at"]


def test_list_conversations_empty_then_populated(tmp_path):
    s = _store(tmp_path)
    assert s.list_conversations() == []
    a = s.create_conversation("A")
    b = s.create_conversation("B")
    ids = [c["id"] for c in s.list_conversations()]
    assert a in ids and b in ids


def test_add_and_get_messages(tmp_path):
    s = _store(tmp_path)
    cid = s.create_conversation("chat")
    s.add_message(cid, "user", "hello")
    s.add_message(cid, "assistant", "hi there")
    assert [(m["role"], m["content"]) for m in s.get_messages(cid)] == [("user", "hello"), ("assistant", "hi there")]


def test_get_unknown_conversation_is_none(tmp_path):
    s = _store(tmp_path)
    assert s.get_conversation(999) is None
    assert s.get_messages(999) == []
