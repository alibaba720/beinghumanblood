with open('index.html', 'r', encoding='utf-8') as f:
    h = f.read()

# 1. Add Chat Button in Header (Hidden by default)
if 'id="chatBtn"' not in h:
    old_header = """<button class="icon-btn" onclick="toggleLangMenu()" title="Language">🌐</button>"""
    new_header = """<button class="icon-btn" id="chatBtn" onclick="openChatModal()" title="Chat" style="display:none; background:#27ae60; color:white; position:relative;">💬<span id="chatDot" style="display:none;position:absolute;top:6px;right:6px;width:10px;height:10px;background:#e74c3c;border-radius:50%;border:1px solid white;"></span></button>
      <button class="icon-btn" onclick="toggleLangMenu()" title="Language">🌐</button>"""
    h = h.replace(old_header, new_header)

# 2. Add Chat Modal UI (WhatsApp Style)
if 'id="chatModal"' not in h:
    chat_ui = """
<!-- CHAT MODAL -->
<div class="modal-overlay" id="chatModal" onclick="if(event.target===this)closeChatModal()">
  <div class="modal" style="height: 85vh; display: flex; flex-direction: column; padding: 0; overflow: hidden; border-radius: 16px;">
    <div style="background: #8B0000; color: white; padding: 15px; display: flex; justify-content: space-between; align-items: center;">
      <h3 style="margin: 0; font-size: 16px;">🩸 BeingHuman Chat</h3>
      <button onclick="closeChatModal()" style="background: none; border: none; color: white; font-size: 20px; cursor: pointer;">✕</button>
    </div>
    <div id="chatMessages" style="flex: 1; overflow-y: auto; padding: 15px; background: #efeae2; display: flex; flex-direction: column; gap: 10px;">
      <div style="text-align:center; color:#888; font-size:12px; margin-top:10px;">Loading messages...</div>
    </div>
    <div style="padding: 10px; background: #f0f0f0; display: flex; gap: 10px; align-items: center;">
      <input type="text" id="chatInput" placeholder="Type a message..." style="flex: 1; padding: 12px 15px; border-radius: 25px; border: 1px solid #ccc; outline: none; margin-bottom: 0; font-size:14px;">
      <button onclick="sendChatMessage()" style="background: #27ae60; color: white; border: none; border-radius: 50%; width: 45px; height: 45px; cursor: pointer; display: flex; justify-content: center; align-items: center; font-size: 18px; flex-shrink:0;">➤</button>
    </div>
  </div>
</div>
"""
    h = h.replace('<!-- MODAL -->', chat_ui + '\n<!-- MODAL -->')

# 3. Add Chat Logic in JS
chat_js = """
  // ==========================================
  // CHAT SYSTEM LOGIC
  // ==========================================
  let chatUnsubscribe = null;

  window.openChatModal = function() {
    document.getElementById('chatModal').classList.add('show');
    document.getElementById('chatDot').style.display = 'none'; // Hide red dot
    loadChatMessages();
  };

  window.closeChatModal = function() {
    document.getElementById('chatModal').classList.remove('show');
    if (chatUnsubscribe) {
      chatUnsubscribe();
      chatUnsubscribe = null;
    }
  };

  function loadChatMessages() {
    const msgBox = document.getElementById('chatMessages');
    const user = firebase.auth().currentUser;
    if (!user) return;

    chatUnsubscribe = db.collection('chat_messages').orderBy('createdAt', 'asc').limit(100).onSnapshot(snapshot => {
      msgBox.innerHTML = '';
      if (snapshot.empty) {
        msgBox.innerHTML = '<div style="text-align:center; color:#888; font-size:12px; margin-top:10px;">No messages yet. Say Salam!</div>';
        return;
      }

      snapshot.forEach(doc => {
        const msg = doc.data();
        const isMe = msg.uid === user.uid;
        
        const msgDiv = document.createElement('div');
        msgDiv.style.maxWidth = '80%';
        msgDiv.style.padding = '8px 12px';
        msgDiv.style.borderRadius = '10px';
        msgDiv.style.fontSize = '14px';
        msgDiv.style.lineHeight = '1.4';
        msgDiv.style.wordWrap = 'break-word';
        msgDiv.style.boxShadow = '0 1px 2px rgba(0,0,0,0.1)';
        
        if (isMe) {
          msgDiv.style.alignSelf = 'flex-end';
          msgDiv.style.background = '#dcf8c6';
          msgDiv.style.borderBottomRightRadius = '0';
        } else {
          msgDiv.style.alignSelf = 'flex-start';
          msgDiv.style.background = '#ffffff';
          msgDiv.style.borderBottomLeftRadius = '0';
          
          const nameSpan = document.createElement('div');
          nameSpan.style.fontSize = '11px';
          nameSpan.style.color = '#8B0000';
          nameSpan.style.fontWeight = 'bold';
          nameSpan.style.marginBottom = '3px';
          nameSpan.textContent = msg.senderName || 'User';
          msgDiv.appendChild(nameSpan);
        }
        
        const textNode = document.createTextNode(msg.text);
        msgDiv.appendChild(textNode);
        msgBox.appendChild(msgDiv);
      });
      
      msgBox.scrollTop = msgBox.scrollHeight; // Auto scroll to bottom
    });
  }

  window.sendChatMessage = async function() {
    const input = document.getElementById('chatInput');
    const text = input.value.trim();
    const user = firebase.auth().currentUser;
    
    if (!text || !user) return;
    
    input.value = ''; // Clear input immediately
    
    try {
      const userDoc = await db.collection('users').doc(user.uid).get();
      const userName = userDoc.exists ? userDoc.data().name : 'User';

      await db.collection('chat_messages').add({
        uid: user.uid,
        senderName: userName,
        text: text,
        createdAt: firebase.firestore.FieldValue.serverTimestamp()
      });
    } catch(e) {
      alert("Error sending message: " + e.message);
    }
  };

  // Handle Enter key for chat
  document.getElementById('chatInput')?.addEventListener('keypress', function (e) {
    if (e.key === 'Enter') {
      sendChatMessage();
    }
  });
"""

if 'window.openChatModal = function()' not in h:
    h = h.replace('window.openReqModal = function(blood, city) {', chat_js + '\n\n  window.openReqModal = function(blood, city) {')

# 4. Show Chat button if user isChatMember
old_auth_check = """      if (doc.exists) {
        const d = doc.data();
        if (d.role === 'banned') {"""
new_auth_check = """      if (doc.exists) {
        const d = doc.data();
        if (d.isChatMember) {
          const chatBtn = document.getElementById('chatBtn');
          if (chatBtn) chatBtn.style.display = 'flex';
        }
        if (d.role === 'banned') {"""

if old_auth_check in h and 'd.isChatMember' not in h:
    h = h.replace(old_auth_check, new_auth_check)

with open('index.html', 'w', encoding='utf-8') as f:
    f.write(h)

print("Done: Chat UI and Logic added successfully!")
