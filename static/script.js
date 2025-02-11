async function sendMessage() {
    let userInput = document.getElementById("userInput").value.trim();
    if (userInput === "") return;

    addMessage(userInput, "user-message");

    let chatBox = document.getElementById("chatBox");
    let typingMessage = document.createElement("div");
    typingMessage.className = "bot-message typing";
    typingMessage.textContent = "Typing...";
    chatBox.appendChild(typingMessage);
    chatBox.scrollTop = chatBox.scrollHeight;

    try {
        let response = await fetch("/chat", {
            method: "POST",
            headers: { "Content-Type": "application/json" },
            body: JSON.stringify({ message: userInput })
        });

        let data = await response.json();
        chatBox.removeChild(typingMessage);

        // Use typing effect for bot response
        addTypingEffect(data.response, "bot-message");
    } catch (error) {
        chatBox.removeChild(typingMessage);
        addMessage("Error: Could not connect to the chatbot server.", "bot-message");
        console.error("Error:", error);
    }

    document.getElementById("userInput").value = "";
}

function addMessage(text, className) {
    let chatBox = document.getElementById("chatBox");
    let messageDiv = document.createElement("div");
    messageDiv.className = className;
    messageDiv.textContent = text;
    chatBox.appendChild(messageDiv);
    chatBox.scrollTop = chatBox.scrollHeight;
}

// ✅ Typing effect for bot responses
function addTypingEffect(text, className) {
    let chatBox = document.getElementById("chatBox");
    let messageDiv = document.createElement("div");
    messageDiv.className = className;
    chatBox.appendChild(messageDiv);
    chatBox.scrollTop = chatBox.scrollHeight;

    let i = 0;
    function typeWriter() {
        if (i < text.length) {
            messageDiv.textContent += text.charAt(i);
            i++;
            setTimeout(typeWriter, 30); // Adjust speed (lower = faster)
            chatBox.scrollTop = chatBox.scrollHeight; // Auto-scroll while typing
        }
    }
    typeWriter();
}
