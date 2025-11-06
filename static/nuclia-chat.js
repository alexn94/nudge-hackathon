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
            <div style="background: white; color: #1a1a1a; padding: 1rem 1.25rem; display: flex; justify-content: space-between; align-items: center; border-bottom: 1px solid #e5e7eb;">
                <div style="display: flex; align-items: center; gap: 0.75rem;">
                    <!-- Hamburger Menu -->
                    <button style="background: none; border: none; color: #6b7280; cursor: pointer; padding: 0.25rem; display: flex; align-items: center;">
                        <svg xmlns="http://www.w3.org/2000/svg" fill="none" viewBox="0 0 24 24" stroke-width="2" stroke="currentColor" style="width: 24px; height: 24px;">
                            <path stroke-linecap="round" stroke-linejoin="round" d="M3.75 6.75h16.5M3.75 12h16.5m-16.5 5.25h16.5"></path>
                        </svg>
                    </button>
                    <!-- Star Icon (larger) -->
                    <svg width="32" height="32" viewBox="0 0 26 26" fill="none" xmlns="http://www.w3.org/2000/svg">
                        <path fill-rule="evenodd" clip-rule="evenodd" d="M9.875 5.1875C10.2238 5.1875 10.5304 5.41873 10.6262 5.75412L11.4733 8.71891C11.844 10.0166 12.8584 11.031 14.1561 11.4017L17.1209 12.2488C17.4563 12.3446 17.6875 12.6512 17.6875 13C17.6875 13.3488 17.4563 13.6554 17.1209 13.7512L14.1561 14.5983C12.8584 14.969 11.844 15.9834 11.4733 17.2811L10.6262 20.2459C10.5304 20.5813 10.2238 20.8125 9.875 20.8125C9.52619 20.8125 9.21964 20.5813 9.12381 20.2459L8.27673 17.2811C7.90596 15.9834 6.89159 14.969 5.5939 14.5983L2.62912 13.7512C2.29373 13.6554 2.0625 13.3488 2.0625 13C2.0625 12.6512 2.29373 12.3446 2.62912 12.2488L5.59391 11.4017C6.89159 11.031 7.90596 10.0166 8.27673 8.7189L9.12381 5.75412C9.21964 5.41873 9.52619 5.1875 9.875 5.1875Z" fill="url(#paint0_linear)"/>
                        <path fill-rule="evenodd" clip-rule="evenodd" d="M19.25 2.0625C19.6085 2.0625 19.921 2.30648 20.0079 2.65427L20.2776 3.73287C20.5225 4.71256 21.2874 5.4775 22.2671 5.72242L23.3457 5.99208C23.6935 6.07902 23.9375 6.39151 23.9375 6.75C23.9375 7.10849 23.6935 7.42098 23.3457 7.50792L22.2671 7.77758C21.2874 8.0225 20.5225 8.78744 20.2776 9.76712L20.0079 10.8457C19.921 11.1935 19.6085 11.4375 19.25 11.4375C18.8915 11.4375 18.579 11.1935 18.4921 10.8457L18.2224 9.76713C17.9775 8.78744 17.2126 8.0225 16.2329 7.77758L15.1543 7.50792C14.8065 7.42098 14.5625 7.10849 14.5625 6.75C14.5625 6.39151 14.8065 6.07902 15.1543 5.99208L16.2329 5.72242C17.2126 5.4775 17.9775 4.71256 18.2224 3.73288L18.4921 2.65427C18.579 2.30648 18.8915 2.0625 19.25 2.0625Z" fill="url(#paint1_linear)"/>
                        <path fill-rule="evenodd" clip-rule="evenodd" d="M17.6875 16.125C18.0238 16.125 18.3223 16.3402 18.4287 16.6592L18.8393 17.8912C18.9949 18.3578 19.361 18.7239 19.8275 18.8794L21.0596 19.2901C21.3786 19.3964 21.5938 19.695 21.5938 20.0312C21.5938 20.3675 21.3786 20.6661 21.0596 20.7724L19.8275 21.1831C19.361 21.3386 18.9949 21.7047 18.8393 22.1713L18.4287 23.4033C18.3223 23.7223 18.0238 23.9375 17.6875 23.9375C17.3512 23.9375 17.0527 23.7223 16.9463 23.4033L16.5357 22.1713C16.3801 21.7047 16.014 21.3386 15.5475 21.1831L14.3154 20.7724C13.9964 20.6661 13.7812 20.3675 13.7812 20.0312C13.7812 19.695 13.9964 19.3964 14.3154 19.2901L15.5475 18.8794C16.014 18.7239 16.3801 18.3578 16.5357 17.8912L16.9463 16.6592C17.0527 16.3402 17.3512 16.125 17.6875 16.125Z" fill="url(#paint2_linear)"/>
                        <defs>
                            <linearGradient id="paint0_linear" x1="2.0625" y1="23.9375" x2="24.2793" y2="2.0625" gradientUnits="userSpaceOnUse">
                                <stop stop-color="#0928FF"/>
                                <stop offset="1" stop-color="#FDAD00"/>
                            </linearGradient>
                            <linearGradient id="paint1_linear" x1="2.0625" y1="23.9375" x2="24.2793" y2="2.0625" gradientUnits="userSpaceOnUse">
                                <stop stop-color="#0928FF"/>
                                <stop offset="1" stop-color="#FDAD00"/>
                            </linearGradient>
                            <linearGradient id="paint2_linear" x1="2.0625" y1="23.9375" x2="24.2793" y2="2.0625" gradientUnits="userSpaceOnUse">
                                <stop stop-color="#0928FF"/>
                                <stop offset="1" stop-color="#FDAD00"/>
                            </linearGradient>
                        </defs>
                    </svg>
                    <!-- Nuri AI Text -->
                    <div style="font-weight: 700; font-size: 1.1rem; color: #1a1a1a;">Nuri AI</div>
                </div>
                <div style="display: flex; align-items: center; gap: 0.5rem;">
                    <!-- Open In New Icon -->
                    <button style="background: none; border: none; color: #6b7280; cursor: pointer; padding: 0.25rem; display: flex; align-items: center;">
                        <svg xmlns="http://www.w3.org/2000/svg" fill="none" viewBox="0 0 24 24" stroke-width="2" stroke="currentColor" style="width: 20px; height: 20px;">
                            <path stroke-linecap="round" stroke-linejoin="round" d="M13.5 6H5.25A2.25 2.25 0 003 8.25v10.5A2.25 2.25 0 005.25 21h10.5A2.25 2.25 0 0018 18.75V10.5m-10.5 6L21 3m0 0h-5.25M21 3v5.25"></path>
                        </svg>
                    </button>
                    <!-- Minimize Button -->
                    <button id="nuclia-minimize" style="background: none; border: none; color: #6b7280; cursor: pointer; padding: 0.25rem; display: flex; align-items: center;">
                        <svg xmlns="http://www.w3.org/2000/svg" fill="none" viewBox="0 0 24 24" stroke-width="2" stroke="currentColor" style="width: 20px; height: 20px;">
                            <path stroke-linecap="round" stroke-linejoin="round" d="M19.5 12h-15"></path>
                        </svg>
                    </button>
                </div>
            </div>
            
            <!-- Nuri Plus Banner -->
            <div style="background: #0928ff; color: white; padding: 0.875rem 1.25rem; display: flex; align-items: center; gap: 0.75rem;">
                <!-- Small Star Icon -->
                <svg width="20" height="20" viewBox="0 0 26 26" fill="none" xmlns="http://www.w3.org/2000/svg" style="flex-shrink: 0;">
                    <path fill-rule="evenodd" clip-rule="evenodd" d="M9.875 5.1875C10.2238 5.1875 10.5304 5.41873 10.6262 5.75412L11.4733 8.71891C11.844 10.0166 12.8584 11.031 14.1561 11.4017L17.1209 12.2488C17.4563 12.3446 17.6875 12.6512 17.6875 13C17.6875 13.3488 17.4563 13.6554 17.1209 13.7512L14.1561 14.5983C12.8584 14.969 11.844 15.9834 11.4733 17.2811L10.6262 20.2459C10.5304 20.5813 10.2238 20.8125 9.875 20.8125C9.52619 20.8125 9.21964 20.5813 9.12381 20.2459L8.27673 17.2811C7.90596 15.9834 6.89159 14.969 5.5939 14.5983L2.62912 13.7512C2.29373 13.6554 2.0625 13.3488 2.0625 13C2.0625 12.6512 2.29373 12.3446 2.62912 12.2488L5.59391 11.4017C6.89159 11.031 7.90596 10.0166 8.27673 8.7189L9.12381 5.75412C9.21964 5.41873 9.52619 5.1875 9.875 5.1875Z" fill="white"/>
                    <path fill-rule="evenodd" clip-rule="evenodd" d="M19.25 2.0625C19.6085 2.0625 19.921 2.30648 20.0079 2.65427L20.2776 3.73287C20.5225 4.71256 21.2874 5.4775 22.2671 5.72242L23.3457 5.99208C23.6935 6.07902 23.9375 6.39151 23.9375 6.75C23.9375 7.10849 23.6935 7.42098 23.3457 7.50792L22.2671 7.77758C21.2874 8.0225 20.5225 8.78744 20.2776 9.76712L20.0079 10.8457C19.921 11.1935 19.6085 11.4375 19.25 11.4375C18.8915 11.4375 18.579 11.1935 18.4921 10.8457L18.2224 9.76713C17.9775 8.78744 17.2126 8.0225 16.2329 7.77758L15.1543 7.50792C14.8065 7.42098 14.5625 7.10849 14.5625 6.75C14.5625 6.39151 14.8065 6.07902 15.1543 5.99208L16.2329 5.72242C17.2126 5.4775 17.9775 4.71256 18.2224 3.73288L18.4921 2.65427C18.579 2.30648 18.8915 2.0625 19.25 2.0625Z" fill="white"/>
                    <path fill-rule="evenodd" clip-rule="evenodd" d="M17.6875 16.125C18.0238 16.125 18.3223 16.3402 18.4287 16.6592L18.8393 17.8912C18.9949 18.3578 19.361 18.7239 19.8275 18.8794L21.0596 19.2901C21.3786 19.3964 21.5938 19.695 21.5938 20.0312C21.5938 20.3675 21.3786 20.6661 21.0596 20.7724L19.8275 21.1831C19.361 21.3386 18.9949 21.7047 18.8393 22.1713L18.4287 23.4033C18.3223 23.7223 18.0238 23.9375 17.6875 23.9375C17.3512 23.9375 17.0527 23.7223 16.9463 23.4033L16.5357 22.1713C16.3801 21.7047 16.014 21.3386 15.5475 21.1831L14.3154 20.7724C13.9964 20.6661 13.7812 20.3675 13.7812 20.0312C13.7812 19.695 13.9964 19.3964 14.3154 19.2901L15.5475 18.8794C16.014 18.7239 16.3801 18.3578 16.5357 17.8912L16.9463 16.6592C17.0527 16.3402 17.3512 16.125 17.6875 16.125Z" fill="white"/>
                </svg>
                <!-- Text -->
                <div style="flex: 1; line-height: 1.3;">
                    <div style="font-size: 0.8rem; font-weight: 600;">Unlock Nuri Plus - Get Personalized</div>
                    <div style="font-size: 0.8rem; font-weight: 600;">Insights for FREE!</div>
                </div>
            </div>
            
            <!-- Messages Area -->
            <div id="nuclia-messages" style="flex: 1; padding: 1.5rem; overflow-y: auto; background: #f8fafc; display: flex; flex-direction: column; gap: 1rem;">
                <!-- Messages will be added here -->
            </div>
            
            <!-- Input Area -->
            <div style="padding: 1rem; background: white; border-top: 1px solid #e2e8f0; display: flex; gap: 0.75rem; align-items: end;">
                <textarea id="nuclia-input" placeholder="Ask me anything..." style="flex: 1; padding: 0.75rem 1rem; border: 1px solid #e2e8f0; border-radius: 0.75rem; outline: none; font-size: 1rem; font-family: inherit; resize: none; max-height: 120px; transition: all 200ms;" rows="1"></textarea>
                <button id="nuclia-send" style="padding: 0.75rem 1.25rem; background: linear-gradient(135deg, rgb(160, 160, 160) 0%, rgb(180, 180, 180) 100%); color: white; border: none; border-radius: 0.75rem; font-weight: 700; cursor: pointer; white-space: nowrap; transition: all 200ms; display: flex; align-items: center; gap: 0.5rem; height: 44px;">
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
    const openChatBtn = document.getElementById('nuclia-open-chat');
    const minimizeBtn = document.getElementById('nuclia-minimize');
    const closePreviewBtn = document.getElementById('nuclia-close-preview');
    const messagesDiv = document.getElementById('nuclia-messages');
    const input = document.getElementById('nuclia-input');
    const sendBtn = document.getElementById('nuclia-send');
    const previewText = document.getElementById('nuclia-preview-text');
    
    let isWindowOpen = false;
    
    // Simple Markdown to HTML converter
    function markdownToHtml(text) {
        if (!text) return '';
        
        let html = text;
        
        // Headers (###, ##, #)
        html = html.replace(/^### (.*$)/gim, '<h3>$1</h3>');
        html = html.replace(/^## (.*$)/gim, '<h2>$1</h2>');
        html = html.replace(/^# (.*$)/gim, '<h1>$1</h1>');
        
        // Bold (**text** or __text__)
        html = html.replace(/\*\*(.+?)\*\*/g, '<strong>$1</strong>');
        html = html.replace(/__(.+?)__/g, '<strong>$1</strong>');
        
        // Italic (*text* or _text_)
        html = html.replace(/\*(.+?)\*/g, '<em>$1</em>');
        html = html.replace(/_(.+?)_/g, '<em>$1</em>');
        
        // Inline code (`code`)
        html = html.replace(/`(.+?)`/g, '<code style="background: #f1f5f9; padding: 0.125rem 0.375rem; border-radius: 0.25rem; font-family: monospace; font-size: 0.9em;">$1</code>');
        
        // Links [text](url)
        html = html.replace(/\[([^\]]+)\]\(([^\)]+)\)/g, '<a href="$2" target="_blank" style="color: #ff6b35; text-decoration: underline;">$1</a>');
        
        // Unordered lists (- item or * item)
        html = html.replace(/^[\*\-] (.+)$/gim, '<li>$1</li>');
        html = html.replace(/(<li>.*<\/li>)/s, '<ul style="margin: 0.5rem 0; padding-left: 1.5rem;">$1</ul>');
        
        // Ordered lists (1. item)
        html = html.replace(/^\d+\. (.+)$/gim, '<li>$1</li>');
        
        // Line breaks
        html = html.replace(/\n\n/g, '<br><br>');
        html = html.replace(/\n/g, '<br>');
        
        return html;
    }
    
    // Add message to chat
    function addMessage(text, isBot = true, citations = null, suggestedQuestions = null) {
        const messageDiv = document.createElement('div');
        messageDiv.style.display = 'flex';
        messageDiv.style.flexDirection = 'column';
        messageDiv.style.alignItems = isBot ? 'center' : 'flex-end';
        messageDiv.style.animation = 'slideIn 0.3s ease-out';
        messageDiv.style.gap = '1rem';
        messageDiv.style.width = '100%';
        
        const bubble = document.createElement('div');
        bubble.style.padding = '0.875rem 1.125rem';
        bubble.style.borderRadius = '1rem';
        bubble.style.wordWrap = 'break-word';
        bubble.style.fontSize = '1rem';
        bubble.style.lineHeight = '1.5';
        bubble.style.whiteSpace = 'pre-wrap';
        bubble.style.maxWidth = isBot ? '85%' : 'fit-content';
        
        if (isBot) {
            bubble.style.background = 'white';
            bubble.style.color = '#1e293b';
            bubble.style.boxShadow = '0 2px 8px rgba(0,0,0,0.08)';
            bubble.style.border = '1px solid #e2e8f0';
        } else {
            bubble.style.background = 'linear-gradient(135deg, rgb(160, 160, 160) 0%, rgb(180, 180, 180) 100%)';
            bubble.style.color = 'white';
            bubble.style.boxShadow = '0 4px 12px rgba(0,0,0,0.15)';
        }
        
        // Use markdown formatting for bot messages, plain text for user
        if (isBot) {
            bubble.innerHTML = markdownToHtml(text);
        } else {
            bubble.textContent = text;
        }
        messageDiv.appendChild(bubble);
        
        // Add citations if available
        if (isBot && citations && citations.length > 0) {
            const citationsDiv = document.createElement('div');
            citationsDiv.className = 'citations';
            
            citations.forEach((citation, index) => {
                const citationItem = document.createElement('div');
                citationItem.className = 'citation';
                citationItem.innerHTML = `<strong>${index + 1}. ${citation.title}</strong>`;
                
                // Show first paragraph as preview
                if (citation.paragraphs && citation.paragraphs.length > 0) {
                    const preview = document.createElement('div');
                    preview.style.marginTop = '0.5rem';
                    preview.style.fontSize = '0.875rem';
                    preview.textContent = citation.paragraphs[0].text;
                    citationItem.appendChild(preview);
                }
                
                citationsDiv.appendChild(citationItem);
            });
            
            messageDiv.appendChild(citationsDiv);
        }
        
        // Add suggested questions buttons if available
        if (isBot && suggestedQuestions && suggestedQuestions.length > 0) {
            const questionsDiv = document.createElement('div');
            questionsDiv.className = 'suggested-questions';
            // Add explicit inline styles to ensure gap works
            questionsDiv.style.display = 'flex';
            questionsDiv.style.flexDirection = 'column';
            questionsDiv.style.gap = '1rem';
            questionsDiv.style.width = '85%';
            questionsDiv.style.marginTop = '1rem';
            questionsDiv.style.alignItems = 'flex-start';
            questionsDiv.style.alignSelf = 'flex-start';
            
            suggestedQuestions.forEach((question) => {
                const questionBtn = document.createElement('button');
                questionBtn.className = 'suggested-question';
                questionBtn.textContent = question;
                // Add explicit inline styles for font size
                questionBtn.style.fontSize = '0.875rem';
                questionBtn.style.padding = '0.625rem 0.875rem';
                questionBtn.style.border = '1px solid #e5e7eb';
                questionBtn.style.borderRadius = '0.75rem';
                questionBtn.style.textAlign = 'left';
                questionBtn.style.width = '100%';
                
                questionBtn.addEventListener('click', () => {
                    // Send the question as user message
                    const inputField = document.getElementById('nuclia-input');
                    const sendButton = document.getElementById('nuclia-send');
                    if (inputField && sendButton) {
                        inputField.value = question;
                        sendButton.click();
                    }
                });
                
                questionsDiv.appendChild(questionBtn);
            });
            
            messageDiv.appendChild(questionsDiv);
        }
        
        messagesDiv.appendChild(messageDiv);
        messagesDiv.scrollTop = messagesDiv.scrollHeight;
    }
    
    // Show typing indicator
    function showTyping() {
        const typingDiv = document.createElement('div');
        typingDiv.id = 'typing-indicator';
        typingDiv.className = 'typing-indicator';
        typingDiv.innerHTML = '<span></span><span></span><span></span>';
        
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
                
                // Add message to chat window with suggested questions
                addMessage(data.message, true, null, data.suggested_questions || []);
                
                // Show chat window automatically
                previewCard.style.display = 'flex';
                chatWindow.style.display = 'flex';
                isWindowOpen = true;
                
                console.log('💬 Chat window opened with initial message and', (data.suggested_questions || []).length, 'suggested questions');
            }
        } catch (error) {
            console.error('❌ Nuri init error:', error);
        }
    }, 500);
});
