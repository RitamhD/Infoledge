<<<<<<< HEAD
// ------------------------------
// Chat Toggle (Open / Close)
// ------------------------------
document.getElementById("chat-toggle").addEventListener("click", (e) => {
  e.stopPropagation();
  const chatContainer = document.getElementById("chat-container");
  const toggleBtn = document.getElementById("chat-toggle");
  const isExpanded = chatContainer.classList.toggle("expanded");
  const img = toggleBtn.querySelector("img");

  // Accessibility attributes
  chatContainer.setAttribute("aria-hidden", !isExpanded);
  toggleBtn.setAttribute("aria-expanded", isExpanded);
  toggleBtn.setAttribute("aria-label", isExpanded ? "Close chat" : "Open chat");
  toggleBtn.title = isExpanded ? "Close chat" : "Open chat";

  if (img) {
    img.src = isExpanded
      ? "static/resources/close_bot.png"
      : "static/resources/bot.png";
  }

  if (isExpanded) document.getElementById("user-input").focus();

  // Close chat on clicking outside
  document.addEventListener("click", (evt) => {
    if (
      chatContainer.classList.contains("expanded") &&
      !chatContainer.contains(evt.target) &&
      !toggleBtn.contains(evt.target)
    ) {
      chatContainer.classList.remove("expanded");
      chatContainer.setAttribute("aria-hidden", true);
      toggleBtn.setAttribute("aria-expanded", false);
      toggleBtn.setAttribute("aria-label", "Open chat");
      toggleBtn.title = "Open chat";
      if (img) img.src = "static/resources/bot.png";
    }
  });
});

// ------------------------------
// Append Message Utility
// ------------------------------
function appendMessage(text, sender) {
  const chatBox = document.getElementById("chatbox");
  const messageDiv = document.createElement("div");
  messageDiv.className = `message ${sender}`;

  if (sender === "bot") {
    const img = document.createElement("img");
    img.src = "static/resources/bot.png";
    img.alt = "Bot";
    img.className = "bot-avatar";
    messageDiv.appendChild(img);
  }

  const textSpan = document.createElement("span");
  textSpan.textContent = text;
  messageDiv.appendChild(textSpan);

=======
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
>>>>>>> 5f0416db394212f08a47de8aa1e66ce78c310935
  chatBox.appendChild(messageDiv);
  chatBox.scrollTop = chatBox.scrollHeight;
}

<<<<<<< HEAD
// ------------------------------
// Initial Greeting
// ------------------------------
=======
// Show greeting message on initial page load
>>>>>>> 5f0416db394212f08a47de8aa1e66ce78c310935
document.addEventListener("DOMContentLoaded", () => {
  appendMessage("Hey, how can I help you today?", "bot");
});

<<<<<<< HEAD
// ------------------------------
// Send Message + Stream Response
// ------------------------------
async function sendMessage() {
  const input = document.getElementById("user-input");
  const chatBox = document.getElementById("chatbox");
  const message = input.value.trim();
  if (!message) return;

  appendMessage(message, "user"); // show user msg
  input.value = "";
  input.focus();

  // Create bot message container
  const botMessageDiv = document.createElement("div");
  botMessageDiv.className = "message bot";

  const botImg = document.createElement("img");
  botImg.src = "static/resources/bot.png";
  botImg.alt = "Bot";
  botImg.className = "bot-avatar";

  const botTextSpan = document.createElement("span");
  const loadingDiv = document.createElement("div");
  loadingDiv.className = "loading-dots";
  loadingDiv.innerHTML = "Thinking " + "<span></span><span></span><span></span>";

  botMessageDiv.appendChild(botImg);
  botMessageDiv.appendChild(botTextSpan);
  botMessageDiv.appendChild(loadingDiv);
  chatBox.appendChild(botMessageDiv);
  chatBox.scrollTop = chatBox.scrollHeight;

  try {
    const response = await fetch("/stream-chat", {
      method: "POST",
      headers: { "Content-Type": "application/json" },
      body: JSON.stringify({ message }),
    });

    if (!response.body) {
      const fullText = await response.text();
      botTextSpan.textContent = fullText;
      loadingDiv.remove();
      return;
    }

    const reader = response.body.getReader();
    const decoder = new TextDecoder();
    let accumulatedText = "";
    let done = false;
=======
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
>>>>>>> 5f0416db394212f08a47de8aa1e66ce78c310935

    while (!done) {
      const { value, done: doneReading } = await reader.read();
      if (value) {
        const chunk = decoder.decode(value, { stream: true });
        accumulatedText += chunk;
<<<<<<< HEAD
        botTextSpan.innerHTML = DOMPurify.sanitize(marked.parse(accumulatedText));
        chatBox.scrollTop = chatBox.scrollHeight;
      }
      done = doneReading;
    }

    loadingDiv.remove();
  } catch (error) {
    appendMessage(`Error: ${error.message}`, "bot");
  }
}

// ------------------------------
// Button & Enter Key Handlers
// ------------------------------
document.getElementById("send").addEventListener("click", sendMessage);
document
  .getElementById("user-input")
  .addEventListener("keypress", (e) => {
    if (e.key === "Enter") {
      e.preventDefault();
      sendMessage();
    }
  });
=======
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
>>>>>>> 5f0416db394212f08a47de8aa1e66ce78c310935
