// Role selector functionality
document.addEventListener('DOMContentLoaded', function() {
    const roleBtns = document.querySelectorAll('.role-btn');
    const roleInput = document.getElementById('role');
    
    if (roleBtns.length > 0 && roleInput) {
        roleBtns.forEach(btn => {
            btn.addEventListener('click', function() {
                // Clear form when switching roles
                const usernameInput = document.getElementById('usernameInput');
                const emailInput = document.getElementById('emailInput');
                const passwordInput = document.getElementById('passwordInput');
                const otpCode = document.getElementById('otpCode');
                const otpGroup = document.getElementById('otpGroup');
                const sendOtpBtn = document.getElementById('sendOtpBtn');
                const resendOtpBtn = document.getElementById('resendOtpBtn');
                const submitBtn = document.getElementById('submitBtn');
                
                if (usernameInput) usernameInput.value = '';
                if (emailInput) emailInput.value = '';
                if (passwordInput) passwordInput.value = '';
                if (otpCode) otpCode.value = '';
                
                // Reset OTP state
                if (otpGroup) otpGroup.style.display = 'none';
                if (sendOtpBtn) {
                    sendOtpBtn.innerHTML = '<i class="fas fa-paper-plane"></i> Send OTP';
                    sendOtpBtn.disabled = false;
                    sendOtpBtn.classList.remove('verified');
                }
                if (resendOtpBtn) resendOtpBtn.style.display = 'none';
                if (submitBtn) {
                    submitBtn.disabled = true;
                    submitBtn.innerHTML = '<i class="fas fa-lock"></i> Verify Email First';
                    submitBtn.style.background = '#9ca3af';
                }
                
                // Update role
                roleBtns.forEach(b => b.classList.remove('active'));
                this.classList.add('active');
                roleInput.value = this.getAttribute('data-role');
            });
        });
    }
    
    // Name validation - only letters and spaces
    const nameInput = document.getElementById('nameInput');
    if (nameInput) {
        nameInput.addEventListener('input', function() {
            this.value = this.value.replace(/[^A-Za-z\s]/g, '');
        });
    }
    
    // Username validation - only letters
    const usernameInput = document.getElementById('usernameInput');
    if (usernameInput) {
        usernameInput.addEventListener('input', function() {
            this.value = this.value.replace(/[^A-Za-z]/g, '');
        });
    }
    
    // Email - NO RESTRICTIONS, allows numbers
    console.log('Email input allows all characters including numbers');
});


// Chatbot functionality
function sendChatMessage() {
    const input = document.getElementById('chatbotInput');
    const message = input.value.trim();
    
    if (!message) return;
    
    // Add user message
    addChatMessage(message, 'user');
    input.value = '';
    
    // Simulate AI response
    setTimeout(() => {
        const response = getChatbotResponse(message);
        addChatMessage(response, 'bot');
    }, 800);
}

function sendQuickMessage(message) {
    addChatMessage(message, 'user');
    
    setTimeout(() => {
        const response = getChatbotResponse(message);
        addChatMessage(response, 'bot');
    }, 800);
}

function addChatMessage(text, sender) {
    const messagesContainer = document.getElementById('chatbotMessages');
    
    const messageDiv = document.createElement('div');
    messageDiv.className = `chat-message ${sender}`;
    
    const avatar = document.createElement('div');
    avatar.className = 'message-avatar';
    avatar.innerHTML = sender === 'bot' ? '<i class="fas fa-robot"></i>' : '<i class="fas fa-user"></i>';
    
    const content = document.createElement('div');
    content.className = 'message-content';
    content.innerHTML = `<p>${text}</p>`;
    
    messageDiv.appendChild(avatar);
    messageDiv.appendChild(content);
    
    messagesContainer.appendChild(messageDiv);
    messagesContainer.scrollTop = messagesContainer.scrollHeight;
}

function getChatbotResponse(message) {
    const lowerMessage = message.toLowerCase();
    
    // Category help
    if (lowerMessage.includes('category') || lowerMessage.includes('choose')) {
        return 'Choose the category that best matches your issue:<br><br>🔧 <strong>Plumbing</strong> - Leaks, pipes, drains, water issues<br>⚡ <strong>Electrical</strong> - Wiring, outlets, lights, power problems<br>🔨 <strong>Carpentry</strong> - Furniture, doors, wood repairs<br>🧹 <strong>Cleaning</strong> - Deep cleaning, maintenance<br>❄️ <strong>HVAC</strong> - AC, heating, ventilation<br>🎨 <strong>Painting</strong> - Interior/exterior painting<br>🛠️ <strong>General</strong> - Other repairs';
    }
    
    // Pricing info
    if (lowerMessage.includes('price') || lowerMessage.includes('pricing') || lowerMessage.includes('cost')) {
        return 'Our AI calculates fair prices based on:<br><br>• <strong>Urgency</strong>: Low ₹300-500, Medium ₹400-700, High ₹1000-1400<br>• <strong>Category complexity</strong><br>• <strong>Location</strong><br>• <strong>Market rates</strong><br><br>You\'ll see the estimated price after submitting your request!';
    }
    
    // Urgency help
    if (lowerMessage.includes('urgency') || lowerMessage.includes('priority')) {
        return '<strong>Urgency Levels:</strong><br><br>🟢 <strong>Low Priority</strong> - Can wait a few days (₹300-500)<br>🟡 <strong>Medium Priority</strong> - Within 1-2 days (₹400-700)<br>🔴 <strong>High Priority</strong> - Urgent/Emergency (₹1000-1400)<br><br>Choose based on how quickly you need the service!';
    }
    
    // Photo/video help
    if (lowerMessage.includes('photo') || lowerMessage.includes('video') || lowerMessage.includes('upload')) {
        return 'Adding photos or videos helps workers understand your issue better!<br><br>• Drag & drop files or click to browse<br>• Supports JPG, PNG, MP4, MOV<br>• Max 50MB per file<br>• Multiple files allowed<br><br>This is optional but highly recommended for accurate quotes!';
    }
    
    // Tracking help
    if (lowerMessage.includes('track') || lowerMessage.includes('status') || lowerMessage.includes('progress')) {
        return 'After submitting your request:<br><br>1️⃣ <strong>Submitted</strong> - Request received<br>2️⃣ <strong>Assigned</strong> - Worker matched by AI<br>3️⃣ <strong>In Progress</strong> - Worker is on the job<br>4️⃣ <strong>Completed</strong> - Job finished<br><br>You can track everything from your dashboard!';
    }
    
    // Worker info
    if (lowerMessage.includes('worker') || lowerMessage.includes('professional')) {
        return 'Our AI matches you with verified professionals based on:<br><br>✓ Skills & specialization<br>✓ Technical rating<br>✓ Location proximity<br>✓ Availability<br>✓ Past performance<br><br>All workers are background-checked and highly rated!';
    }
    
    // Payment help
    if (lowerMessage.includes('payment') || lowerMessage.includes('pay')) {
        return 'Payment is simple and secure:<br><br>• Get price estimate upfront<br>• Payment held securely<br>• Released only after job completion<br>• All prices in Indian Rupees (₹)<br>• Multiple payment methods accepted<br><br>You\'re protected by our satisfaction guarantee!';
    }
    
    // General help
    if (lowerMessage.includes('help') || lowerMessage.includes('how')) {
        return 'I can help you with:<br><br>• Choosing the right category<br>• Understanding pricing<br>• Selecting urgency level<br>• Uploading photos/videos<br>• Tracking your request<br>• Worker information<br>• Payment details<br><br>Just ask me anything!';
    }
    
    // Default response
    return 'I\'m here to help! You can ask me about:<br><br>• Service categories<br>• Pricing information<br>• Urgency levels<br>• Photo/video uploads<br>• Tracking your request<br>• Worker matching<br><br>What would you like to know?';
}

// Allow Enter key to send message
document.addEventListener('DOMContentLoaded', function() {
    const chatInput = document.getElementById('chatbotInput');
    if (chatInput) {
        chatInput.addEventListener('keypress', function(e) {
            if (e.key === 'Enter') {
                sendChatMessage();
            }
        });
    }
});
