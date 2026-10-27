import os

# 1. Create chat.html (Dedicated Chat Page)
chat_html = """<!DOCTYPE html>
<html lang="en">
<head>
<meta charset="UTF-8">
<meta name="viewport" content="width=device-width, initial-scale=1.0, maximum-scale=1.0, user-scalable=no">
<title>BH Chats</title>
<link rel="manifest" href="manifest-chat.json">
<link href="https://fonts.googleapis.com/css2?family=Inter:wght@400;500;600;700&display=swap" rel="stylesheet">
<style>
  * { margin: 0; padding: 0; box-sizing: border-box; font-family: 'Inter', sans-serif; }
  body { background: #efeae2; height: 100vh; display: flex; flex-direction: column; overflow: hidden; }
  
  .header { background: #8B0000; color: white; padding: 15px; display: flex; justify-content: space-between; align-items: center; box-shadow: 0 2px 5px rgba(0,0,0,0.2); z-index: 10; }
  .header h3 { margin: 0; font-size: 18px; font-weight: 700; }
  .close-btn { background: none; border: none; color: white; font-size: 24px; cursor: pointer; padding: 0 10px; }

  #chatMessages { flex: 1; overflow-y: auto; padding: 15px; display: flex; flex-direction: column; gap: 10px; }
  
  .msg-bubble { max-width: 80%; padding: 6px 10px; border-radius: 8px; font-size: 14px; line-height: 1.4; word-wrap: break-word; box-shadow: 0 1px 1px rgba(0,0,0,0.1); cursor: pointer; display: flex; flex-direction: column; position: relative; }
  .msg-me { align-self: flex-end; background: #dcf8c6; border-top-right-radius: 0; }
  .msg-other { align-self: flex-start; background: #ffffff; border-top-left-radius: 0; }
  
  .msg-text { word-break: break-word; margin-bottom: 12px; }
  .msg-meta { position: absolute; bottom: 4px; right: 8px; font-size: 10px; color: #888; display: flex; align-items: center; gap: 3px; }
  .sender-name { font-size: 11px; color: #8B0000; font-weight: bold; margin-bottom: 3px; cursor: pointer; text-decoration: underline; }
  
  .date-sep { text-align: center; margin: 12px 0; }
  .date-sep span { background: #e1f3fb; color: #5c7a8a; font-size: 11px; padding: 5px 14px; border-radius: 8px; font-weight: 600; box-shadow: 0 1px 1px rgba(0,0,0,0.1); }

  .input-area { padding: 10px; background: #f0f0f0; display: flex; gap: 10px; align-items: center; border-top: 1px solid #ddd; }
  #chatInput { flex: 1; padding: 12px 15px; border-radius: 25px; border: 1px solid #ccc; outline: none; font-size: 15px; }
  .send-btn { background: #27ae60; color: white; border: none; border-radius: 50%; width: 45px; height: 45px; cursor: pointer; display: flex; justify-content: center; align-items: center; font-size: 18px; flex-shrink: 0; }
</style>
</head>
<body>

<div class="header">
  <h3>🩸 BH Chats</h3>
  <button class="close-btn" onclick="window.close()">✕</button>
</div>

<div id="chatMessages">
  <div style="text-align:center; color:#888; font-size:12px; margin-top:20px;">Loading messages...</div>
</div>

<div class="input-area">
  <input type="text" id="chatInput" placeholder="Type a message..." onkeypress="if(event.key==='Enter') sendChatMessage()">
  <button class="send-btn" onclick="sendChatMessage()">➤</button>
</div>

<script src="firebase/firebase-app-compat.js"></script>
<script src="firebase/firebase-auth-compat.js"></script>
<script src="firebase/firebase-firestore-compat.js"></script>
<script>
  const firebaseConfig = {
    apiKey: "AIzaSyAp8lKgJuBKpHdXF4pXHr7U3aXwtZUKv_4",
    authDomain: "beinghuman-blood-pk.firebaseapp.com",
    projectId: "beinghuman-blood-pk",
    storageBucket: "beinghuman-blood-pk.firebasestorage.app",
    messagingSenderId: "46427863084",
    appId: "1:46427863084:web:fff219fd6e17fd83e23989"
  };
  if (!firebase.apps.length) firebase.initializeApp(firebaseConfig);
  const auth = firebase.auth();
  const db = firebase.firestore();

  let currentUserData = null;

  auth.onAuthStateChanged(async function(user) {
    if (!user) {
      window.location.href = 'login.html';
      return;
    }
    
    const doc = await db.collection('users').doc(user.uid).get();
    if (doc.exists) {
      currentUserData = doc.data();
      if (!currentUserData.isChatMember && currentUserData.role !== 'owner' && currentUserData.role !== 'admin') {
        alert("Aap chat member nahi hain.");
        window.location.href = 'index.html';
        return;
      }
      loadChatMessages();
    }
  });

  function loadChatMessages() {
    const msgBox = document.getElementById('chatMessages');
    const user = firebase.auth().currentUser;

    const sevenDaysAgo = new Date();
    sevenDaysAgo.setDate(sevenDaysAgo.getDate() - 7);

    db.collection('chat_messages').orderBy('createdAt', 'desc').limit(200).onSnapshot(snapshot => {
      msgBox.innerHTML = '';
      let validMessages = [];
      snapshot.forEach(doc => {
        const msg = doc.data();
        if (msg.createdAt && msg.createdAt.toDate() >= sevenDaysAgo) validMessages.push(msg);
      });

      if (validMessages.length === 0) {
        msgBox.innerHTML = '<div style="text-align:center; color:#888; font-size:12px; margin-top:20px;">No messages in last 7 days.</div>';
        return;
      }

      validMessages.reverse();
      let lastDateStr = '';

      validMessages.forEach(msg => {
        let msgDateStr = 'Today';
        let timeString = '';
        let fullDateString = 'Just now';
        
        if (msg.createdAt) {
            const date = msg.createdAt.toDate();
            const today = new Date();
            const yesterday = new Date(today);
            yesterday.setDate(yesterday.getDate() - 1);
            
            if (date.toDateString() === today.toDateString()) msgDateStr = 'Today';
            else if (date.toDateString() === yesterday.toDateString()) msgDateStr = 'Yesterday';
            else msgDateStr = date.toLocaleDateString();
            
            timeString = date.toLocaleTimeString([], {hour: '2-digit', minute:'2-digit'});
            fullDateString = date.toLocaleString();
        }

        if (msgDateStr !== lastDateStr) {
            lastDateStr = msgDateStr;
            const sep = document.createElement('div');
            sep.className = 'date-sep';
            sep.innerHTML = `<span>${msgDateStr}</span>`;
            msgBox.appendChild(sep);
        }

        const isMe = msg.uid === user.uid;
        const msgDiv = document.createElement('div');
        msgDiv.className = `msg-bubble ${isMe ? 'msg-me' : 'msg-other'}`;
        msgDiv.onclick = function() { alert("Sent at: " + fullDateString); };

        if (isMe) {
            msgDiv.innerHTML = `
              <div class="msg-text">${msg.text}</div>
              <div class="msg-meta">${timeString} <span style="color: #34b7f1; font-weight: bold;">✓✓</span></div>
            `;
        } else {
            msgDiv.innerHTML = `
              <div class="sender-name" onclick="event.stopPropagation(); openAdminChatMenu('${msg.uid}', '${msg.senderName}')">${msg.senderName || 'User'}</div>
              <div class="msg-text">${msg.text}</div>
              <div class="msg-meta">${timeString}</div>
            `;
        }
        msgBox.appendChild(msgDiv);
      });
      msgBox.scrollTop = msgBox.scrollHeight;
    });
  }

  async function sendChatMessage() {
    const input = document.getElementById('chatInput');
    const text = input.value.trim();
    const user = firebase.auth().currentUser;
    if (!text || !user || !currentUserData) return;

    if (currentUserData.isMuted && currentUserData.muteExpiry) {
        if (currentUserData.muteExpiry.toDate() > new Date()) {
            alert("⚠️ Aapko mute kar diya gaya hai.");
            return;
        }
    }

    if (currentUserData.role !== 'owner') {
        const cleanText = text.replace(/[^0-9]/g, '');
        if (cleanText.length >= 5) {
          alert("⚠️ Number share na karein.");
          return;
        }
    }

    input.value = '';
    try {
      await db.collection('chat_messages').add({
        uid: user.uid,
        senderName: currentUserData.name,
        text: text,
        createdAt: firebase.firestore.FieldValue.serverTimestamp()
      });
    } catch(e) { alert("Error: " + e.message); }
  }

  // Admin Menu Logic
  let selectedChatUid = null;
  let selectedChatName = null;

  function openAdminChatMenu(uid, name) {
    if (!currentUserData || (currentUserData.role !== 'owner' && currentUserData.role !== 'admin')) return;
    if (uid === firebase.auth().currentUser.uid) return;
    
    selectedChatUid = uid;
    selectedChatName = name;
    
    const action = prompt(`Action for ${name}:\\n1. Visit Profile\\n2. Mute Member\\n3. Remove from Chat\\nEnter number (1, 2, or 3):`);
    
    if (action === '1') {
        db.collection('users').doc(uid).get().then(doc => {
            if (doc.exists) {
                const d = doc.data();
                alert(`Name: ${d.name}\\nPhone: ${d.phone}\\nCity: ${d.city}\\nBlood: ${d.blood}\\nRole: ${d.role}`);
            }
        });
    } else if (action === '2') {
        const hours = prompt(`Mute ${name} for how many hours?`, "24");
        if (hours && !isNaN(hours)) {
            const expiry = new Date();
            expiry.setHours(expiry.getHours() + parseInt(hours));
            db.collection('users').doc(uid).update({ isMuted: true, muteExpiry: firebase.firestore.Timestamp.fromDate(expiry) });
            db.collection('donors').doc(uid).update({ isMuted: true, muteExpiry: firebase.firestore.Timestamp.fromDate(expiry) }).catch(()=>{});
            alert(`User muted for ${hours} hours.`);
        }
    } else if (action === '3') {
        if (confirm(`Remove ${name} from chat?`)) {
            db.collection('users').doc(uid).update({ isChatMember: false });
            db.collection('donors').doc(uid).update({ isChatMember: false }).catch(()=>{});
            alert("User removed.");
        }
    }
  }
</script>
</body>
</html>"""

with open('chat.html', 'w', encoding='utf-8') as f:
    f.write(chat_html)

# 2. Update manifest-chat.json to point to chat.html
manifest_chat = """{
  "name": "BH Chats",
  "short_name": "BH Chats",
  "start_url": "/chat.html",
  "display": "standalone",
  "background_color": "#8B0000",
  "theme_color": "#8B0000",
  "icons": [
    {
      "src": "https://cdn-icons-png.flaticon.com/512/149/149071.png",
      "sizes": "512x512",
      "type": "image/png"
    }
  ]
}"""
with open('manifest-chat.json', 'w', encoding='utf-8') as f:
    f.write(manifest_chat)

print("Done: Dedicated chat.html created and manifest updated!")
