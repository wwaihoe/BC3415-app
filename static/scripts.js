function sendMessage() {
    const userInput = document.getElementById('user-input');
    const chatMessages = document.getElementById('chat-messages');

    if (userInput.value.trim() === '') return;

    // Add user message to chat
    const userMessage = document.createElement('div');
    userMessage.className = 'message user-message';
    userMessage.textContent = userInput.value;
    chatMessages.appendChild(userMessage);

    // Send message to server
    fetch('/chat', {
        method: 'POST',
        headers: {
            'Content-Type': 'application/json',
        },
        body: JSON.stringify({ message: userInput.value }),
    })
    .then(response => response.json())
    .then(data => {
        // Add bot message to chat
        const botMessage = document.createElement('div');
        botMessage.className = 'message bot-message';
        botMessage.textContent = data.response;
        chatMessages.appendChild(botMessage);

        // Scroll to bottom of chat
        chatMessages.scrollTop = chatMessages.scrollHeight;
    });

    // Clear input
    userInput.value = '';
}

// Allow sending message with Enter key
document.getElementById('user-input').addEventListener('keypress', function(e) {
    if (e.key === 'Enter') {
        sendMessage();
    }
});


function querySentiment() {
    const sentimentInput = document.getElementById('sentiment-input');
    fetch('/sentimentanalysisquery', {
        method: 'POST',
        headers: {
            'Content-Type': 'application/json',
        },
        body: JSON.stringify({ text: sentimentInput.value }),
    })
    .then(response => response.json())
    .then(data => {
        const sentimentOutput = document.getElementById('sentiment-output');
        textOutput = "Polarity: " + data.polarity + "\r\nSubjectivity: " + data.subjectivity;
        sentimentOutput.textContent = textOutput;
    });
}