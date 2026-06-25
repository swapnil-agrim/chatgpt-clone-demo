"""Goal: LLM adapter with streaming + mock fallback."""
import llm


def test_mock_backend_when_no_key(monkeypatch):
    monkeypatch.delenv("ANTHROPIC_API_KEY", raising=False)
    assert llm.active_backend() == "mock"


def test_anthropic_backend_when_key_present():
    assert llm.active_backend(api_key="sk-test-123") == "anthropic"


def test_mock_stream_yields_chunks(monkeypatch):
    monkeypatch.delenv("ANTHROPIC_API_KEY", raising=False)
    chunks = list(llm.stream_reply([{"role": "user", "content": "hello there"}]))
    assert len(chunks) >= 2 and "".join(chunks).strip()


def test_key_present_routes_to_anthropic_stream(monkeypatch):
    monkeypatch.setattr(llm, "_anthropic_stream", lambda messages, api_key, model: iter(["A", "B"]))
    assert list(llm.stream_reply([{"role": "user", "content": "x"}], api_key="sk-test-123")) == ["A", "B"]
