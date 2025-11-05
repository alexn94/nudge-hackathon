// Nuri AI Chat Widget - BrokerChooser Premium Edition
console.log('🤖 Nuri AI initializing...');

document.addEventListener('DOMContentLoaded', function() {
    console.log('✅ DOM ready, setting up Nuri chat...');
    
    // HIDE ORIGINAL BROKERCHOOSER CHAT
    setTimeout(function() {
        const originalChats = document.querySelectorAll('[data-page*="AssistantModal"]');
        originalChats.forEach(el => {
            el.style.display = 'none';
        });
    }, 100);
    
    // Create complete chat widget HTML
    const chatHTML = `
        <!-- Chat Preview Card -->
        <div id="nuclia-preview-card" style="display: none; position: fixed; bottom: 1rem; right: 1rem; z-index: 10000; max-width: 18rem; width: 100%; gap: 0.5rem; flex-direction: row-reverse;">
            <button id="nuclia-close-preview" style="display: flex; align-items: center; justify-content: center; border-radius: 0.5rem; transition: all 200ms; font-weight: 600; cursor: pointer; padding: 0.75rem 0.875rem; font-size: 1rem; color: rgb(71 85 105); background-color: white; border: none; box-shadow: 0 4px 6px -1px rgba(0,0,0,0.1); height: 2rem; width: 2rem; flex-shrink: 0;">
                <svg xmlns="http://www.w3.org/2000/svg" fill="none" viewBox="0 0 24 24" stroke-width="1.5" stroke="currentColor" style="width: 1rem; height: 1rem; stroke: rgb(2 6 23);">
                    <path stroke-linecap="round" stroke-linejoin="round" d="M6 18 18 6M6 6l12 12"></path>
                </svg>
            </button>
            
            <button id="nuclia-open-chat" type="button" style="display: flex; width: 100%; flex-direction: column; gap: 0.5rem; overflow: clip; border-radius: 0.5rem; background-color: white; box-shadow: 0 4px 6px -1px rgba(0,0,0,0.1); border: none; cursor: pointer; padding: 0; text-align: left; transition: all 200ms;">
                <div style="background: linear-gradient(135deg, #ff6b35 0%, #f97316 100%); display: flex; width: 100%; align-items: center; justify-content: space-between; padding: 0.5rem;">
                    <span style="padding: 0 0.5rem; font-size: 0.75rem; line-height: 1; font-weight: 600; color: white;">Nuri AI</span>
                    <svg width="16" height="16" viewBox="0 0 16 16" fill="none" xmlns="http://www.w3.org/2000/svg" style="margin: 0.5rem; width: 1rem; height: 1rem;">
                        <path d="M6.63636 7.60045L13.6543 14.6184C13.7172 14.6835 13.7924 14.7355 13.8756 14.7712C13.9588 14.8069 14.0483 14.8257 14.1388 14.8265C14.2293 14.8273 14.3191 14.8101 14.4029 14.7758C14.4867 14.7415 14.5628 14.6909 14.6269 14.6269C14.6909 14.5628 14.7415 14.4867 14.7758 14.4029C14.8101 14.3191 14.8273 14.2293 14.8265 14.1388C14.8257 14.0483 14.8069 13.9588 14.7712 13.8756C14.7355 13.7924 14.6835 13.7172 14.6184 13.6543L7.60045 6.63636H9.36364C9.54447 6.63636 9.71789 6.56453 9.84576 6.43666C9.97362 6.3088 10.0455 6.13537 10.0455 5.95455C10.0455 5.77372 9.97362 5.60029 9.84576 5.47243C9.71789 5.34456 9.54447 5.27273 9.36364 5.27273H5.95455C5.77372 5.27273 5.60029 5.34456 5.47243 5.47243C5.34456 5.60029 5.27273 5.77372 5.27273 5.95455V9.36364C5.27273 9.54447 5.34456 9.71789 5.47243 9.84575C5.60029 9.97362 5.77372 10.0455 5.95455 10.0455C6.13538 10.0455 6.3088 9.97362 6.43666 9.84575C6.56453 9.71789 6.63636 9.54447 6.63636 9.36364V7.60045Z" fill="white"></path>
                    </svg>
                </div>
                <div style="display: flex; flex-direction: column; gap: 0.25rem; padding: 0 0.5rem 0.5rem 0.5rem; text-align: start;">
                    <span style="font-size: 0.625rem; font-weight: normal; color: rgb(100 116 139);">New message</span>
                    <p id="nuclia-preview-text" style="display: -webkit-box; -webkit-line-clamp: 2; -webkit-box-orient: vertical; overflow: hidden; font-size: 0.75rem; font-weight: normal; color: rgb(2 6 23); margin: 0; line-height: 1.4;">Loading...</p>
                </div>
            </button>
        </div>
        
        <!-- Full Chat Window -->
        <div id="nuclia-chat-window" style="display: none; position: fixed; bottom: 1rem; right: 1rem; width: 400px; max-width: calc(100vw - 2rem); height: 600px; max-height: calc(100vh - 2rem); background: white; border-radius: 1rem; box-shadow: 0 20px 25px -5px rgba(0,0,0,0.1), 0 10px 10px -5px rgba(0,0,0,0.04); z-index: 10001; flex-direction: column; overflow: hidden; animation: slideIn 0.3s ease-out;">
            <!-- Header -->
            <div style="background: linear-gradient(135deg, #1a1a1a 0%, #000000 100%); color: white; padding: 1.25rem; display: flex; justify-content: space-between; align-items: center; border-bottom: 3px solid #ff6b35;">
                <div>
                    <div style="font-weight: 700; font-size: 1.2rem; margin-bottom: 0.25rem;">Nuri AI</div>
                    <div style="font-size: 0.85rem; opacity: 0.8; display: flex; align-items: center; gap: 0.5rem;">
                        <span style="display: inline-block; width: 8px; height: 8px; background: #10b981; border-radius: 50%; animation: pulse 2s ease-in-out infinite;"></span>
                        Online
                    </div>
                </div>
                <button id="nuclia-minimize" style="background: rgba(255,255,255,0.1); border: none; color: white; font-size: 1.5rem; cursor: pointer; width: 36px; height: 36px; border-radius: 0.5rem; display: flex; align-items: center; justify-content: center; transition: all 200ms;">
                    <svg xmlns="http://www.w3.org/2000/svg" fill="none" viewBox="0 0 24 24" stroke-width="2" stroke="currentColor" style="width: 20px; height: 20px;">
                        <path stroke-linecap="round" stroke-linejoin="round" d="M19.5 12h-15"></path>
                    </svg>
                </button>
            </div>
            
            <!-- Messages Area -->
            <div id="nuclia-messages" style="flex: 1; padding: 1.5rem; overflow-y: auto; background: #f8fafc; display: flex; flex-direction: column; gap: 1rem;">
                <!-- Messages will be added here -->
            </div>
            
            <!-- Input Area -->
            <div style="padding: 1rem; background: white; border-top: 1px solid #e2e8f0; display: flex; gap: 0.75rem; align-items: end;">
                <textarea id="nuclia-input" placeholder="Ask me anything..." style="flex: 1; padding: 0.75rem 1rem; border: 1px solid #e2e8f0; border-radius: 0.75rem; outline: none; font-size: 0.95rem; font-family: inherit; resize: none; max-height: 120px; transition: all 200ms;" rows="1"></textarea>
                <button id="nuclia-send" style="padding: 0.75rem 1.25rem; background: #ff6b35; color: white; border: none; border-radius: 0.75rem; font-weight: 700; cursor: pointer; white-space: nowrap; transition: all 200ms; display: flex; align-items: center; gap: 0.5rem; height: 44px;">
                    <span>Send</span>
                    <svg xmlns="http://www.w3.org/2000/svg" fill="none" viewBox="0 0 24 24" stroke-width="2" stroke="currentColor" style="width: 18px; height: 18px;">
                        <path stroke-linecap="round" stroke-linejoin="round" d="M6 12 3.269 3.125A59.769 59.769 0 0 1 21.485 12 59.768 59.768 0 0 1 3.27 20.875L5.999 12Zm0 0h7.5"></path>
                    </svg>
                </button>
            </div>
        </div>
        
        <style>
            @keyframes slideIn {
                from { transform: translateY(20px); opacity: 0; }
                to { transform: translateY(0); opacity: 1; }
            }
            @keyframes pulse {
                0%, 100% { opacity: 1; }
                50% { opacity: 0.5; }
            }
            #nuclia-minimize:hover { background: rgba(255,255,255,0.2); }
            #nuclia-send:hover { background: #e55a2b; transform: translateY(-1px); }
            #nuclia-send:active { transform: translateY(0); }
            #nuclia-input:focus { border-color: #ff6b35; }
            #nuclia-open-chat:hover { box-shadow: 0 10px 15px -3px rgba(0,0,0,0.1); transform: translateY(-2px); }
        </style>
    `;
    
    document.body.insertAdjacentHTML('beforeend', chatHTML);
    
    // Get elements
    const previewCard = document.getElementById('nuclia-preview-card');
    const chatWindow = document.getElementById('nuclia-chat-window');
    const messagesDiv = document.getElementById('nuclia-messages');
    const input = document.getElementById('nuclia-input');
    const sendBtn = document.getElementById('nuclia-send');
    const previewText = document.getElementById('nuclia-preview-text');
    const openChatBtn = document.getElementById('nuclia-open-chat');
    const minimizeBtn = document.getElementById('nuclia-minimize');
    const closePreviewBtn = document.getElementById('nuclia-close-preview');
    
    let isWindowOpen = false;
    
    // Add message to chat
    function addMessage(text, isBot = true, citations = null) {
        const messageDiv = document.createElement('div');
        messageDiv.style.display = 'flex';
        messageDiv.style.flexDirection = 'column';
        messageDiv.style.alignItems = isBot ? 'flex-start' : 'flex-end';
        messageDiv.style.animation = 'slideIn 0.3s ease-out';
        messageDiv.style.gap = '0.5rem';
        messageDiv.style.maxWidth = '85%';
        
        const bubble = document.createElement('div');
        bubble.style.padding = '0.875rem 1.125rem';
        bubble.style.borderRadius = '1rem';
        bubble.style.wordWrap = 'break-word';
        bubble.style.fontSize = '0.95rem';
        bubble.style.lineHeight = '1.5';
        bubble.style.whiteSpace = 'pre-wrap';
        
        if (isBot) {
            bubble.style.background = 'white';
            bubble.style.color = '#1e293b';
            bubble.style.boxShadow = '0 2px 8px rgba(0,0,0,0.08)';
            bubble.style.border = '1px solid #e2e8f0';
        } else {
            bubble.style.background = 'linear-gradient(135deg, #ff6b35 0%, #f97316 100%)';
            bubble.style.color = 'white';
            bubble.style.boxShadow = '0 4px 12px rgba(255,107,53,0.3)';
        }
        
        bubble.textContent = text;
        messageDiv.appendChild(bubble);
        
        // Add citations if available
        if (isBot && citations && citations.length > 0) {
            const citationsDiv = document.createElement('div');
            citationsDiv.style.display = 'flex';
            citationsDiv.style.flexDirection = 'column';
            citationsDiv.style.gap = '0.5rem';
            citationsDiv.style.marginTop = '0.5rem';
            citationsDiv.style.fontSize = '0.85rem';
            
            const citationsTitle = document.createElement('div');
            citationsTitle.style.fontWeight = '600';
            citationsTitle.style.color = '#64748b';
            citationsTitle.style.fontSize = '0.8rem';
            citationsTitle.textContent = '📚 Sources:';
            citationsDiv.appendChild(citationsTitle);
            
            citations.forEach((citation, index) => {
                const citationItem = document.createElement('div');
                citationItem.style.background = '#f8fafc';
                citationItem.style.border = '1px solid #e2e8f0';
                citationItem.style.borderRadius = '0.5rem';
                citationItem.style.padding = '0.625rem 0.875rem';
                citationItem.style.cursor = 'pointer';
                citationItem.style.transition = 'all 200ms';
                
                const citationTitle = document.createElement('div');
                citationTitle.style.fontWeight = '600';
                citationTitle.style.color = '#1e293b';
                citationTitle.style.marginBottom = '0.25rem';
                citationTitle.textContent = `${index + 1}. ${citation.title}`;
                citationItem.appendChild(citationTitle);
                
                // Show first paragraph as preview
                if (citation.paragraphs && citation.paragraphs.length > 0) {
                    const preview = document.createElement('div');
                    preview.style.color = '#64748b';
                    preview.style.fontSize = '0.8rem';
                    preview.style.overflow = 'hidden';
                    preview.style.textOverflow = 'ellipsis';
                    preview.style.display = '-webkit-box';
                    preview.style.webkitLineClamp = '2';
                    preview.style.webkitBoxOrient = 'vertical';
                    preview.textContent = citation.paragraphs[0].text;
                    citationItem.appendChild(preview);
                    
                    // Add expand functionality
                    let expanded = false;
                    citationItem.addEventListener('click', () => {
                        expanded = !expanded;
                        if (expanded) {
                            preview.style.webkitLineClamp = 'unset';
                            preview.style.display = 'block';
                            citationItem.style.background = '#eff6ff';
                        } else {
                            preview.style.webkitLineClamp = '2';
                            preview.style.display = '-webkit-box';
                            citationItem.style.background = '#f8fafc';
                        }
                    });
                    
                    citationItem.addEventListener('mouseenter', () => {
                        citationItem.style.borderColor = '#cbd5e1';
                        citationItem.style.boxShadow = '0 2px 4px rgba(0,0,0,0.05)';
                    });
                    
                    citationItem.addEventListener('mouseleave', () => {
                        citationItem.style.borderColor = '#e2e8f0';
                        citationItem.style.boxShadow = 'none';
                    });
                }
                
                citationsDiv.appendChild(citationItem);
            });
            
            messageDiv.appendChild(citationsDiv);
        }
        
        messagesDiv.appendChild(messageDiv);
        messagesDiv.scrollTop = messagesDiv.scrollHeight;
    }
    
    // Show typing indicator
    function showTyping() {
        const typingDiv = document.createElement('div');
        typingDiv.id = 'typing-indicator';
        typingDiv.style.display = 'flex';
        typingDiv.style.alignItems = 'center';
        typingDiv.style.gap = '0.5rem';
        typingDiv.style.padding = '0.875rem 1.125rem';
        typingDiv.style.background = 'white';
        typingDiv.style.borderRadius = '1rem';
        typingDiv.style.maxWidth = '120px';
        typingDiv.style.boxShadow = '0 2px 8px rgba(0,0,0,0.08)';
        typingDiv.innerHTML = `
            <div style="display: flex; gap: 0.3rem;">
                <div style="width: 8px; height: 8px; background: #94a3b8; border-radius: 50%; animation: bounce 1.4s ease-in-out 0s infinite;"></div>
                <div style="width: 8px; height: 8px; background: #94a3b8; border-radius: 50%; animation: bounce 1.4s ease-in-out 0.2s infinite;"></div>
                <div style="width: 8px; height: 8px; background: #94a3b8; border-radius: 50%; animation: bounce 1.4s ease-in-out 0.4s infinite;"></div>
            </div>
        `;
        
        const style = document.createElement('style');
        style.textContent = '@keyframes bounce { 0%, 60%, 100% { transform: translateY(0); } 30% { transform: translateY(-10px); } }';
        document.head.appendChild(style);
        
        messagesDiv.appendChild(typingDiv);
        messagesDiv.scrollTop = messagesDiv.scrollHeight;
    }
    
    function hideTyping() {
        const typing = document.getElementById('typing-indicator');
        if (typing) typing.remove();
    }
    
    // Send message
    async function sendMessage() {
        const message = input.value.trim();
        if (!message) return;
        
        addMessage(message, false);
        input.value = '';
        input.style.height = 'auto';
        
        showTyping();
        
        try {
            const response = await fetch('/api/chat', {
                method: 'POST',
                headers: {'Content-Type': 'application/json; charset=utf-8'},
                body: JSON.stringify({message: message})
            });
            
            const data = await response.json();
            hideTyping();
            
            if (data.success && data.message) {
                addMessage(data.message, true, data.citations || null);
            } else {
                addMessage('Sorry, an error occurred. Please try again!', true);
            }
        } catch (error) {
            console.error('Chat error:', error);
            hideTyping();
            addMessage('Failed to connect. Please check your internet connection!', true);
        }
    }
    
    // Event handlers
    sendBtn.addEventListener('click', sendMessage);
    input.addEventListener('keydown', function(e) {
        if (e.key === 'Enter' && !e.shiftKey) {
            e.preventDefault();
            sendMessage();
        }
    });
    
    // Auto-resize textarea
    input.addEventListener('input', function() {
        this.style.height = 'auto';
        this.style.height = Math.min(this.scrollHeight, 120) + 'px';
    });
    
    // Open chat window
    openChatBtn.addEventListener('click', function() {
        previewCard.style.display = 'none';
        chatWindow.style.display = 'flex';
        isWindowOpen = true;
        input.focus();
    });
    
    // Minimize chat
    minimizeBtn.addEventListener('click', function() {
        chatWindow.style.display = 'none';
        previewCard.style.display = 'flex';
        isWindowOpen = false;
    });
    
    // Close preview
    closePreviewBtn.addEventListener('click', function() {
        previewCard.style.display = 'none';
    });
    
    // Initialize chat
    setTimeout(async function() {
        console.log('🚀 Initializing Nuri chat...');
        
        try {
            const response = await fetch('/api/init-chat', {
                method: 'POST',
                headers: {'Content-Type': 'application/json; charset=utf-8'}
            });
            
            const data = await response.json();
            console.log('✅ Nuri response received');
            
            if (data.success && data.message) {
                // Update preview
                const preview = data.message.substring(0, 100) + (data.message.length > 100 ? '...' : '');
                previewText.textContent = preview;
                
                // Add message to chat window
                addMessage(data.message, true);
                
                // Show chat window automatically
                previewCard.style.display = 'flex';
                chatWindow.style.display = 'flex';
                isWindowOpen = true;
                
                console.log('💬 Chat window opened with initial message');
            }
        } catch (error) {
            console.error('❌ Nuri init error:', error);
        }
    }, 500);
});
