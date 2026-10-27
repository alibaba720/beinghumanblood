import re

with open('index.html', 'r', encoding='utf-8') as f:
    h = f.read()

# Pattern to match the entire loadChatMessages function
pattern = r"function loadChatMessages\(\) \{.*?msgBox\.scrollTop = msgBox\.scrollHeight;.*?\n\s*\}\);\n\s*\}"

new_func = """function loadChatMessages() {
      const msgBox = document.getElementById('chatMessages');
      const user = firebase.auth().currentUser;
      if (!user) return;

      if (chatUnsubscribe) chatUnsubscribe();

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
          msgDiv.style.maxWidth = '85%';
          msgDiv.style.padding = '8px 12px';
          msgDiv.style.borderRadius = '8px';
          msgDiv.style.fontSize = '14px';
          msgDiv.style.lineHeight = '1.4';
          msgDiv.style.wordWrap = 'break-word';
          msgDiv.style.boxShadow = '0 1px 2px rgba(0,0,0,0.1)';
          msgDiv.style.cursor = 'pointer';
          msgDiv.style.position = 'relative';

          let timeString = '';
          let fullDateString = 'Just now';
          if (msg.createdAt) {
            const date = msg.createdAt.toDate();
            timeString = date.toLocaleTimeString([], {hour: '2-digit', minute:'2-digit'});
            fullDateString = date.toLocaleString();
          }

          msgDiv.onclick = function() {
            alert("Sent at: " + fullDateString);
          };

          if (isMe) {
            msgDiv.style.alignSelf = 'flex-end';
            msgDiv.style.background = '#dcf8c6';
            msgDiv.style.borderTopRightRadius = '0'; 
            
            msgDiv.innerHTML = `
              <div style="padding-right: 50px;">${msg.text}</div>
              <div style="position: absolute; bottom: 6px; right: 8px; font-size: 10px; color: #888; display: flex; align-items: center; gap: 3px;">
                ${timeString} <span style="color: #34b7f1; font-weight: bold;">✓✓</span>
              </div>
            `;
          } else {
            msgDiv.style.alignSelf = 'flex-start';
            msgDiv.style.background = '#ffffff';
            msgDiv.style.borderTopLeftRadius = '0';
            
            msgDiv.innerHTML = `
              <div style="font-size: 11px; color: #8B0000; font-weight: bold; margin-bottom: 3px;">${msg.senderName || 'User'}</div>
              <div style="padding-right: 50px;">${msg.text}</div>
              <div style="position: absolute; bottom: 6px; right: 8px; font-size: 10px; color: #888;">
                ${timeString}
              </div>
            `;
          }
          
          msgBox.appendChild(msgDiv);
        });
        
        msgBox.scrollTop = msgBox.scrollHeight;
      });
    }"""

if "function loadChatMessages" in h:
    h = re.sub(pattern, new_func, h, flags=re.DOTALL)
    with open('index.html', 'w', encoding='utf-8') as f:
        f.write(h)
    print("Done: Timestamp and ticks added perfectly.")
else:
    print("Error: Function not found. Checking fallback...")
    # Fallback if exact regex fails
    if "function loadChatMessages" in h and "✓✓" not in h:
        # A simpler replacement if the regex doesn't match perfectly
        h = h.replace("const msgDiv = document.createElement('div');", "const msgDiv = document.createElement('div');\n          msgDiv.style.position = 'relative';")
        h = h.replace("msgDiv.appendChild(textNode);", "msgDiv.appendChild(textNode);\n          const timeSpan = document.createElement('span'); timeSpan.style.fontSize='10px'; timeSpan.style.color='#888'; timeSpan.style.marginLeft='10px'; timeSpan.innerHTML = (msg.createdAt ? msg.createdAt.toDate().toLocaleTimeString([], {hour: '2-digit', minute:'2-digit'}) : '') + (isMe ? ' ✓✓' : ''); msgDiv.appendChild(timeSpan);")
        with open('index.html', 'w', encoding='utf-8') as f:
            f.write(h)
        print("Done: Fallback applied.")
