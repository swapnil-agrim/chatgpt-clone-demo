"""LLM adapter — the only module that knows whether we're talking to Claude or a mock.

`stream_reply(messages)` yields text chunks. With ANTHROPIC_API_KEY set it streams from Claude;
otherwise it streams a deterministic mock reply token-by-token, so the app runs with zero config.
"""
import os

DEFAULT_MODEL = "claude-3-5-haiku-latest"


def active_backend(api_key=None):
    return "anthropic" if (api_key or os.environ.get("ANTHROPIC_API_KEY")) else "mock"


def stream_reply(messages, api_key=None, model=DEFAULT_MODEL):
    if active_backend(api_key) == "anthropic":
        yield from _anthropic_stream(messages, api_key or os.environ["ANTHROPIC_API_KEY"], model)
    else:
        yield from _mock_stream(messages)


def _last_user(messages):
    for m in reversed(messages):
        if m.get("role") == "user":
            return m.get("content", "")
    return ""


def _mock_stream(messages):
    prompt = _last_user(messages).strip()
    reply = (
        f"You said: \"{prompt}\". "
        "This is a mock reply from the local LLM adapter — set ANTHROPIC_API_KEY to stream real "
        "Claude responses instead."
    )
    for word in reply.split(" "):
        yield word + " "


def _anthropic_stream(messages, api_key, model):
    """Stream from Claude. Imported lazily so the mock path needs no SDK installed."""
    import anthropic

    client = anthropic.Anthropic(api_key=api_key)
    chat = [{"role": m["role"], "content": m["content"]} for m in messages if m.get("role") in ("user", "assistant")]
    with client.messages.stream(model=model, max_tokens=1024, messages=chat) as stream:
        for text in stream.text_stream:
            yield text
