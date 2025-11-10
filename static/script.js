// static/script.js

document.addEventListener('DOMContentLoaded', () => {
    const chatForm = document.getElementById('chat-form');
    const chatBox = document.getElementById('chat-box');
    const userInput = document.getElementById('user-input');
    
    // URL do endpoint Flask (sempre o servidor Flask)
    const API_URL = '/chat'; 

    function appendMessage(text, type) {
        const messageDiv = document.createElement('div');
        messageDiv.classList.add('message', type);
        
        const paragraph = document.createElement('p');
        paragraph.textContent = text;
        
        messageDiv.appendChild(paragraph);
        chatBox.appendChild(messageDiv);
        chatBox.scrollTop = chatBox.scrollHeight;
        
        return messageDiv;
    }

    chatForm.addEventListener('submit', async (e) => {
        e.preventDefault();
        const message = userInput.value.trim();
        
        if (!message) return;

        // 1. Exibe a mensagem do usuário
        appendMessage(message, 'outgoing');
        userInput.value = '';

        // 2. Exibe o indicador de 'digitando...'
        const loadingMessage = appendMessage('Gênio do Futebol está pensando...', 'incoming');
        loadingMessage.querySelector('p').classList.add('loading');

        try {
            // 3. Envia a mensagem para o Flask
            const response = await fetch(API_URL, {
                method: 'POST',
                headers: {
                    'Content-Type': 'application/json',
                },
                body: JSON.stringify({ message: message }),
            });

            if (!response.ok) {
                // Tenta ler o erro do servidor
                const errorData = await response.json(); 
                throw new Error(errorData.error || `Erro HTTP: ${response.status}`);
            }

            const data = await response.json();
            const geminiResponse = data.response;

            // 4. Remove o 'digitando...' e exibe a resposta do Gemini
            loadingMessage.remove();
            appendMessage(geminiResponse, 'incoming');

        } catch (error) {
            console.error('Erro ao chamar o backend:', error);
            loadingMessage.remove();
            appendMessage(`Desculpe, falha na comunicação. Erro: ${error.message}`, 'incoming');
        }
    });
});