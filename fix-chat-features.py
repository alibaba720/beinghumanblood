import re

with open('index.html', 'r', encoding='utf-8') as f:
    h = f.read()

# 1. Fix the sendChatMessage function (Bulletproof Regex)
old_func_pattern = r"window\.sendChatMessage = async function\(\) \{.*?input\.value = '';"
new_func = """window.sendChatMessage = async function() {
    const input = document.getElementById('chatInput');
    const text = input.value.trim();
    const user = firebase.auth().currentUser;
    
    if (!text || !user) return;

    // BULLETPROOF RESTRICTION: Block 5 or more digits
    // Remove spaces, dashes, brackets before checking
    const cleanText = text.replace(/[^0-9]/g, ''); // Extract only numbers
    if (cleanText.length >= 5) {
      alert("⚠️ Baraye meharbani chat mein phone number share na karein.");
      return;
    }

    input.value = ''; // Clear input immediately"""

if "window.sendChatMessage" in h:
    h = re.sub(old_func_pattern, new_func, h, flags=re.DOTALL)
    print("✅ Number restriction fixed.")

# 2. Add Tick mark and Timestamp to Messages UI
old_ui = """        if (isMe) {
          msgDiv.style.alignSelf = 'flex-end';
          msgDiv.style.background = '#dcf8c6';
          msgDiv.style.borderBottomRightRadius = '0';
        } else {"""

new_ui = """        // Format time
        let timeString = '';
        if (msg.createdAt) {
            const date = msg.createdAt.toDate();
            timeString = date.toLocaleTimeString([], {hour: '2-digit', minute:'2-digit'});
        }

        if (isMe) {
          msgDiv.style.alignSelf = 'flex-end';
          msgDiv.style.background = '#dcf8c6';
          msgDiv.style.borderBottomRightRadius = '0';
          msgDiv.style.cursor = 'pointer';
          
          // Add click event for timestamp
          msgDiv.onclick = function() {
              const date = msg.createdAt ? msg.createdAt.toDate().toLocaleString() : 'Just now';
              alert(`Sent at: ${date}`);
          };

          const textSpan = document.createElement('span');
          textSpan.textContent = msg.text + " ";
          msgDiv.appendChild(textSpan);

          const metaSpan = document.createElement('span');
          metaSpan.style.fontSize = '10px';
          metaSpan.style.color = '#888';
          metaSpan.style.float = 'right';
          metaSpan.style.marginTop = '5px';
          metaSpan.innerHTML = `${timeString} <span style="color:#34b7f1;">✓✓</span>`;
          msgDiv.appendChild(metaSpan);

        } else {"""

if old_ui in h and "✓✓" not in h:
    h = h.replace(old_ui, new_ui)
    # Modify the else block to not append text twice
    h = h.replace("""          msgDiv.appendChild(nameSpan);
        }
        
        const textNode = document.createTextNode(msg.text);
        msgDiv.appendChild(textNode);
        msgBox.appendChild(msgDiv);""", 
    """          msgDiv.appendChild(nameSpan);
          
          const textSpan = document.createElement('span');
          textSpan.textContent = msg.text + " ";
          msgDiv.appendChild(textSpan);
          
          const metaSpan = document.createElement('span');
          metaSpan.style.fontSize = '10px';
          metaSpan.style.color = '#888';
          metaSpan.style.float = 'right';
          metaSpan.style.marginTop = '5px';
          metaSpan.innerHTML = `${timeString}`;
          msgDiv.appendChild(metaSpan);

          // Add click event for received messages too
          msgDiv.onclick = function() {
              const date = msg.createdAt ? msg.createdAt.toDate().toLocaleString() : 'Just now';
              alert(`Sent at: ${date}`);
          };
        }
        
        msgBox.appendChild(msgDiv);""")
    print("✅ Timestamps and Ticks added.")

with open('index.html', 'w', encoding='utf-8') as f:
    f.write(h)

print("Done: Chat features updated!")
