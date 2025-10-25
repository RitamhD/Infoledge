// Chat Toggle function: toggle chat container expand/collapse
document.getElementById("chat-toggle").addEventListener("click", () => {
  const chatContainer = document.getElementById("chat-container");
  const toggleBtn = document.getElementById("chat-toggle");
  const isExpanded = chatContainer.classList.toggle("expanded");

  // Update accessibility attributes
  chatContainer.setAttribute('aria-hidden', !isExpanded);
  toggleBtn.setAttribute('aria-expanded', isExpanded);
  toggleBtn.setAttribute('aria-label', isExpanded ? "Close chat" : "Open chat");
  toggleBtn.title = isExpanded ? "Close chat" : "Open chat";
  toggleBtn.textContent = isExpanded ? "Close" : "ask AI";

  if (isExpanded) {
    document.getElementById("user-input").focus();
  }

  document.addEventListener("click", (e) => {
    if (chatContainer.classList.contains("expanded") && !chatContainer.contains(e.target) && !toggleBtn.contains(e.target)) {
      chatContainer.classList.remove("expanded");
      chatContainer.setAttribute('aria-hidden', true);
      toggleBtn.setAttribute('aria-expanded', false);
      toggleBtn.setAttribute('aria-label', "Open chat");
      toggleBtn.title = "Open chat";
      toggleBtn.textContent = "ask AI";
    }
  })

});

// Append a message to the chatbox
function appendMessage(text, sender) {
  const chatBox = document.getElementById('chatbox');
  const messageDiv = document.createElement("div");
  messageDiv.className = `message ${sender}`;
  messageDiv.textContent = text;
  chatBox.appendChild(messageDiv);
  chatBox.scrollTop = chatBox.scrollHeight;
}

// Show greeting message on initial page load
document.addEventListener("DOMContentLoaded", () => {
  appendMessage("Hey, how can I help you today?", "bot");
});

// Send button click handler with streaming response
document.getElementById("send").addEventListener("click", async () => {
  const input = document.getElementById("user-input");
  const message = input.value.trim();
  if (!message) return;

  // Show user message immediately
  appendMessage(message, "user");

  // Clear and focus input box
  input.value = "";
  input.focus();

  // Prepare bot message container for streaming content
  const botMessageDiv = document.createElement("div");
  botMessageDiv.className = "message bot";
  document.getElementById("chatbox").appendChild(botMessageDiv);
  botMessageDiv.textContent = ""; // start empty
  document.getElementById("chatbox").scrollTop = document.getElementById("chatbox").scrollHeight;

  try {
    // Start streaming response from backend
    const response = await fetch("/stream-chat", {
      method: "POST",
      headers: {
        "Content-Type": "application/json"
      },
      body: JSON.stringify({ message })
    });

    if (!response.body) {
      // If backend doesn't support streaming, fallback to full text
      const fullText = await response.text();
      botMessageDiv.textContent = fullText;
      return;
    }

    // Read response body as stream
    const reader = response.body.getReader();
    const decoder = new TextDecoder();
    let done = false;
    let accumulatedText = "";

    while (!done) {
      const { value, done: doneReading } = await reader.read();
      if (value) {
        const chunk = decoder.decode(value, { stream: true });
        accumulatedText += chunk;
        botMessageDiv.innerHTML = DOMPurify.sanitize(marked.parse(accumulatedText));
        document.getElementById("chatbox").scrollTop = document.getElementById("chatbox").scrollHeight;
      }
      done = doneReading;
    }
  } catch (error) {
    appendMessage("Error streaming response: " + error.message, "bot");
  }
});


// Auto send message
document.getElementById("user-input").addEventListener('keypress', function(event) {
  if (event.key === "Enter") {
    event.preventDefault();
    document.getElementById("send").click();
  }
});
