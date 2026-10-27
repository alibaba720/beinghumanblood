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

      // Calculate 7 days ago
      const sevenDaysAgo = new Date();
      sevenDaysAgo.setDate(sevenDaysAgo.getDate() - 7);

      // Fetch latest 200 messages ordered by newest first
      chatUnsubscribe = db.collection('chat_messages')
        .orderBy('createdAt', 'desc')
        .limit(200)
        .onSnapshot(snapshot => {
          msgBox.innerHTML = '';
          
          let validMessages = [];
          snapshot.forEach(doc => {
            const msg = doc.data();
            // Only keep messages from last 7 days
            if (msg.createdAt && msg.createdAt.toDate() >= sevenDaysAgo) {
              validMessages.push(msg);
            }
          });

          if (validMessages.length === 0) {
            msgBox.innerHTML = '<div style="text-align:center; color:#888; font-size:12px; margin-top:10px;">No messages in last 7 days. Say Salam!</div>';
            return;
          }

          // Reverse to show oldest first (top to bottom)
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
                
                if (date.toDateString() === today.toDateString()) {
                    msgDateStr = 'Today';
                } else if (date.toDateString() === yesterday.toDateString()) {
                    msgDateStr = 'Yesterday';
                } else {
                    msgDateStr = date.toLocaleDateString();
                }
                timeString = date.toLocaleTimeString([], {hour: '2-digit', minute:'2-digit'});
                fullDateString = date.toLocaleString();
            }

            // Add Date Separator (Today / Yesterday)
            if (msgDateStr !== lastDateStr) {
                lastDateStr = msgDateStr;
                const sep = document.createElement('div');
                sep.style.textAlign = 'center';
                sep.style.margin = '12px 0';
                sep.innerHTML = `<span style="background: #e1f3fb; color: #5c7a8a; font-size: 11px; padding: 5px 14px; border-radius: 8px; font-weight: 600; box-shadow: 0 1px 1px rgba(0,0,0,0.1);">${msgDateStr}</span>`;
                msgBox.appendChild(sep);
            }

            const isMe = msg.uid === user.uid;
            const msgDiv = document.createElement('div');
            msgDiv.style.maxWidth = '80%';
            msgDiv.style.padding = '6px 10px 6px 10px';
            msgDiv.style.borderRadius = '8px';
            msgDiv.style.fontSize = '14px';
            msgDiv.style.lineHeight = '1.4';
            msgDiv.style.wordWrap = 'break-word';
            msgDiv.style.boxShadow = '0 1px 1px rgba(0,0,0,0.1)';
            msgDiv.style.cursor = 'pointer';
            msgDiv.style.display = 'flex';
            msgDiv.style.flexDirection = 'column';

            msgDiv.onclick = function() {
                alert("Sent at: " + fullDateString);
            };

            if (isMe) {
                msgDiv.style.alignSelf = 'flex-end';
                msgDiv.style.background = '#dcf8c6';
                msgDiv.style.borderTopRightRadius = '0'; 
                
                msgDiv.innerHTML = `
                  <div style="word-break: break-word; margin-bottom: 12px;">${msg.text}</div>
                  <div style="position: absolute; bottom: 4px; right: 8px; font-size: 10px; color: #888; display: flex; align-items: center; gap: 3px;">
                    ${timeString} <span style="color: #34b7f1; font-weight: bold;">✓✓</span>
                  </div>
                `;
            } else {
                msgDiv.style.alignSelf = 'flex-start';
                msgDiv.style.background = '#ffffff';
                msgDiv.style.borderTopLeftRadius = '0';
                
                msgDiv.innerHTML = `
                  <div style="font-size: 11px; color: #8B0000; font-weight: bold; margin-bottom: 3px;">${msg.senderName || 'User'}</div>
                  <div style="word-break: break-word; margin-bottom: 12px;">${msg.text}</div>
                  <div style="position: absolute; bottom: 4px; right: 8px; font-size: 10px; color: #888;">
                    ${timeString}
                  </div>
                `;
            }
            
            // Important for absolute positioning of time
            msgDiv.style.position = 'relative'; 
            msgBox.appendChild(msgDiv);
          });
          
          msgBox.scrollTop = msgBox.scrollHeight;
        });
    }"""

if "function loadChatMessages" in h:
    h = re.sub(pattern, new_func, h, flags=re.DOTALL)
    with open('index.html', 'w', encoding='utf-8') as f:
        f.write(h)
    print("Done: WhatsApp style chat with 7-day limit added.")
else:
    print("Error: Function not found.")
