// Frontend (goal: conversation list + create + select). Streaming send arrives next goal.
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

// XSS-safe message rendering — textContent only, never innerHTML with model/user data.
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

newChatBtn.addEventListener("click", newChat);
composer.addEventListener("submit", (e) => e.preventDefault()); // streaming send wired next goal

loadConversations().then(() => showEmptyHint());
