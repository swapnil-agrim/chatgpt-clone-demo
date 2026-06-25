// Frontend: conversation list + create + select + live SSE streaming.
const messagesEl = document.getElementById("messages");
const promptEl = document.getElementById("prompt");
const listEl = document.getElementById("conversations");
const newChatBtn = document.getElementById("new-chat");
const composer = document.getElementById("composer");

let currentId = null;

async function api(method, path, body) {
  const opts = { method, headers: {} };
  if (body !== undefined) { opts.headers["Content-Type"] = "application/json"; opts.body = JSON.stringify(body); }
  const res = await fetch(path, opts);
  if (!res.ok) throw new Error(`${method} ${path} -> ${res.status}`);
  return res.json();
}

function showEmptyHint() {
  messagesEl.replaceChildren();
  const hint = document.createElement("div");
  hint.id = "empty-hint";
  hint.textContent = "Start a new conversation.";
  messagesEl.appendChild(hint);
}

// XSS-safe — textContent only, never innerHTML with model/user data.
function addMessageEl(role, content) {
  const hint = document.getElementById("empty-hint");
  if (hint) hint.remove();
  const wrap = document.createElement("div");
  wrap.className = `msg ${role}`;
  const r = document.createElement("div");
  r.className = "role";
  r.textContent = role === "user" ? "You" : "Assistant";
  const c = document.createElement("div");
  c.className = "content";
  c.textContent = content;
  wrap.append(r, c);
  messagesEl.appendChild(wrap);
  messagesEl.scrollTop = messagesEl.scrollHeight;
  return c;
}

function renderConversations(items) {
  listEl.replaceChildren();
  for (const conv of items) {
    const li = document.createElement("li");
    li.textContent = conv.title;
    li.dataset.id = conv.id;
    if (conv.id === currentId) li.classList.add("active");
    li.addEventListener("click", () => selectConversation(conv.id));
    listEl.appendChild(li);
  }
}

async function loadConversations() {
  renderConversations(await api("GET", "/api/conversations"));
}

async function selectConversation(id) {
  currentId = id;
  const data = await api("GET", `/api/conversations/${id}`);
  messagesEl.replaceChildren();
  if (!data.messages.length) showEmptyHint();
  for (const m of data.messages) addMessageEl(m.role, m.content);
  [...listEl.children].forEach((li) => li.classList.toggle("active", Number(li.dataset.id) === id));
}

async function newChat() {
  const conv = await api("POST", "/api/conversations", { title: "New chat" });
  currentId = conv.id;
  await loadConversations();
  showEmptyHint();
}

function handleFrame(frame, target) {
  let event = "message", data = "";
  for (const line of frame.split("\n")) {
    if (line.startsWith("event:")) event = line.slice(6).trim();
    else if (line.startsWith("data:")) data += line.slice(5).trim();
  }
  if (event === "done") return;
  if (event === "error") { target.textContent += "\n[stream error]"; return; }
  try {
    const obj = JSON.parse(data);
    if (obj.text) { target.textContent += obj.text; messagesEl.scrollTop = messagesEl.scrollHeight; }
  } catch (_) { /* ignore */ }
}

async function sendMessage(text) {
  if (!currentId) {
    const conv = await api("POST", "/api/conversations", { title: text.slice(0, 40) || "New chat" });
    currentId = conv.id;
    await loadConversations();
  }
  addMessageEl("user", text);
  const target = addMessageEl("assistant", "");
  const res = await fetch(`/api/conversations/${currentId}/messages`, {
    method: "POST", headers: { "Content-Type": "application/json" }, body: JSON.stringify({ content: text }),
  });
  if (!res.ok) { target.textContent = "[error: " + res.status + "]"; return; }
  const reader = res.body.getReader();
  const decoder = new TextDecoder();
  let buf = "";
  for (;;) {
    const { done, value } = await reader.read();
    if (done) break;
    buf += decoder.decode(value, { stream: true });
    let i;
    while ((i = buf.indexOf("\n\n")) >= 0) { handleFrame(buf.slice(0, i), target); buf = buf.slice(i + 2); }
  }
  await loadConversations();
}

newChatBtn.addEventListener("click", newChat);
composer.addEventListener("submit", async (e) => {
  e.preventDefault();
  const text = promptEl.value.trim();
  if (!text) return;
  promptEl.value = ""; promptEl.style.height = "auto";
  try { await sendMessage(text); } catch (err) { console.error(err); }
});

async function showBackendBanner() {
  try {
    const meta = await api("GET", "/api/meta");
    if (meta.backend === "mock") {
      const b = document.getElementById("backend-banner");
      b.textContent = "Mock mode — set ANTHROPIC_API_KEY to stream real Claude replies.";
      b.hidden = false;
    }
  } catch (_) { /* non-fatal */ }
}

loadConversations().then(() => showEmptyHint());
showBackendBanner();
