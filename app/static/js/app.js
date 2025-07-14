document.addEventListener('DOMContentLoaded', function() {
    // DOM Elements
    const usernameForm = document.getElementById('usernameForm');
    const redditUsername = document.getElementById('redditUsername');
    const generateBtn = document.getElementById('generateBtn');
    const personaCard = document.querySelector('.persona-card');
    const personaDetails = document.getElementById('personaDetails');
    const saveToFileBtn = document.getElementById('saveToFileBtn');
    const chatCard = document.querySelector('.chat-card');
    const chatMessages = document.getElementById('chatMessages');
    const chatForm = document.getElementById('chatForm');
    const messageInput = document.getElementById('messageInput');
    const personaName = document.getElementById('personaName');
    const welcomeScreen = document.getElementById('welcomeScreen');

    // Store the current persona
    let currentPersona = null;

    // Handle username form submission
    usernameForm.addEventListener('submit', async function(e) {
        e.preventDefault();
        
        const username = redditUsername.value.trim();
        if (!username) return;
        
        // Show loading state
        generateBtn.disabled = true;
        const originalBtnText = generateBtn.innerHTML;
        generateBtn.innerHTML = '<i class="bi bi-arrow-repeat animate-spin mr-2"></i><span>Generating...</span>';
        
        try {
            const response = await fetch('/api/persona', {
                method: 'POST',
                headers: {
                    'Content-Type': 'application/json'
                },
                body: JSON.stringify({ username })
            });
            
            if (!response.ok) {
                const error = await response.json();
                throw new Error(error.detail || 'Failed to generate persona');
            }
            
            const persona = await response.json();
            displayPersona(persona);
            currentPersona = persona;
            
            // Show chat interface and hide welcome screen
            chatCard.classList.remove('hidden');
            if (welcomeScreen) welcomeScreen.classList.add('hidden');
            
            personaName.textContent = persona.name || username;
            
            // Add initial greeting message
            const greeting = `Hello! I'm an AI persona based on Reddit user ${username}'s activity. How can I help you today?`;
            addMessage(greeting, 'persona');
            
        } catch (error) {
            showNotification(error.message, 'error');
            console.error(error);
        } finally {
            generateBtn.disabled = false;
            generateBtn.innerHTML = originalBtnText;
        }
    });

    // Handle chat form submission
    chatForm.addEventListener('submit', async function(e) {
        e.preventDefault();
        
        const message = messageInput.value.trim();
        if (!message || !currentPersona) return;
        
        // Add user message to chat
        addMessage(message, 'user');
        
        // Clear input
        messageInput.value = '';
        
        try {
            // Show typing indicator
            const typingIndicator = addMessage(`
                <div class="typing-indicator">
                    <div class="typing-dot"></div>
                    <div class="typing-dot"></div>
                    <div class="typing-dot"></div>
                </div>
            `, 'persona');
            
            const response = await fetch('/api/chat', {
                method: 'POST',
                headers: {
                    'Content-Type': 'application/json'
                },
                body: JSON.stringify({
                    persona: currentPersona,
                    message: message
                })
            });
            
            if (!response.ok) {
                const error = await response.json();
                throw new Error(error.detail || 'Failed to get response');
            }
            
            const data = await response.json();
            
            // Remove typing indicator
            typingIndicator.remove();
            
            // Add persona response
            addMessage(data.response, 'persona');
            
        } catch (error) {
            showNotification(error.message, 'error');
            console.error(error);
        }
    });
    
    // Handle save to file button click
    saveToFileBtn.addEventListener('click', async function() {
        if (!currentPersona) return;
        
        const originalBtnText = saveToFileBtn.innerHTML;
        saveToFileBtn.innerHTML = '<i class="bi bi-arrow-repeat animate-spin mr-2"></i><span>Saving...</span>';
        saveToFileBtn.disabled = true;
        
        try {
            const response = await fetch('/api/save-persona', {
                method: 'POST',
                headers: {
                    'Content-Type': 'application/json'
                },
                body: JSON.stringify({
                    username: redditUsername.value.trim(),
                    persona: currentPersona
                })
            });
            
            if (!response.ok) {
                const error = await response.json();
                throw new Error(error.detail || 'Failed to save persona');
            }
            
            const data = await response.json();
            
            // Create a download link
            const a = document.createElement('a');
            a.href = data.file_url;
            a.download = data.filename;
            document.body.appendChild(a);
            a.click();
            document.body.removeChild(a);
            
            showNotification('Persona saved successfully!', 'success');
            
        } catch (error) {
            showNotification(error.message, 'error');
            console.error(error);
        } finally {
            saveToFileBtn.disabled = false;
            saveToFileBtn.innerHTML = originalBtnText;
        }
    });

    // Function to display persona details
    function displayPersona(persona) {
        personaCard.classList.remove('hidden');
        
        let html = '<div class="space-y-4">';
        
        // Add each trait to the display
        for (const [key, value] of Object.entries(persona)) {
            if (value && key !== 'raw_data') {
                const formattedKey = key.charAt(0).toUpperCase() + key.slice(1);
                html += `<div class="persona-trait">
                    <span class="trait-label">${formattedKey}</span>
                    <div class="text-gray-300">${value}</div>
                </div>`;
            }
        }
        
        html += '</div>';
        personaDetails.innerHTML = html;
    }

    // Function to add a message to the chat
    function addMessage(content, sender) {
        const messageDiv = document.createElement('div');
        messageDiv.className = `message ${sender}-message fade-in`;
        
        // Add timestamp for persona messages
        if (sender === 'persona') {
            const now = new Date();
            const time = now.toLocaleTimeString([], { hour: '2-digit', minute: '2-digit' });
            messageDiv.innerHTML = `
                ${content}
                <div class="text-xs text-gray-500 mt-1 text-right">${time}</div>
            `;
        } else {
            messageDiv.innerHTML = content;
        }
        
        chatMessages.appendChild(messageDiv);
        
        // Scroll to bottom
        chatMessages.scrollTop = chatMessages.scrollHeight;
        
        return messageDiv;
    }
    
    // Function to show notifications
    function showNotification(message, type = 'info') {
        // Create notification element
        const notification = document.createElement('div');
        notification.className = `fixed top-4 right-4 px-6 py-3 rounded-lg shadow-lg z-50 fade-in`;
        
        // Set styles based on notification type
        if (type === 'error') {
            notification.classList.add('bg-red-600', 'text-white');
            notification.innerHTML = `<i class="bi bi-exclamation-circle mr-2"></i>${message}`;
        } else if (type === 'success') {
            notification.classList.add('bg-green-600', 'text-white');
            notification.innerHTML = `<i class="bi bi-check-circle mr-2"></i>${message}`;
        } else {
            notification.classList.add('bg-blue-600', 'text-white');
            notification.innerHTML = `<i class="bi bi-info-circle mr-2"></i>${message}`;
        }
        
        // Add to DOM
        document.body.appendChild(notification);
        
        // Remove after 4 seconds
        setTimeout(() => {
            notification.style.opacity = '0';
            notification.style.transform = 'translateY(-20px)';
            notification.style.transition = 'opacity 0.5s, transform 0.5s';
            
            setTimeout(() => {
                document.body.removeChild(notification);
            }, 500);
        }, 4000);
    }
});