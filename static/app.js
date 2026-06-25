// Frontend shell (goal: server + static). Conversation list + streaming wired in later goals.
const messagesEl = document.getElementById("messages");
const promptEl = document.getElementById("prompt");

function showEmptyHint() {
  messagesEl.replaceChildren();
  const hint = document.createElement("div");
  hint.id = "empty-hint";
  hint.textContent = "Start a new conversation.";
  messagesEl.appendChild(hint);
}

promptEl.addEventListener("input", () => {
  promptEl.style.height = "auto";
  promptEl.style.height = Math.min(promptEl.scrollHeight, 200) + "px";
});

showEmptyHint();
