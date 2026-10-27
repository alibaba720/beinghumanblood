with open('admin.html', 'r', encoding='utf-8') as f:
    h = f.read()

# Find the exact block and add the button after the select tag
old_block = """<option value="banned" style="color:#e74c3c; font-weight:bold;">Ban User</option>
                  </select>"""
                  
new_block = """<option value="banned" style="color:#e74c3c; font-weight:bold;">Ban User</option>
                  </select>
                  <button onclick="toggleChatAccess('${m.id}', ${m.isChatMember || false})" style="padding:6px; border-radius:6px; border:1px solid #ccc; font-size:12px; font-weight:bold; cursor:pointer; background:${m.isChatMember ? '#f8d7da' : '#d4edda'}; color:${m.isChatMember ? '#721c24' : '#155724'}; width: 100%; margin-top:5px;">
                    ${m.isChatMember ? 'Remove from Chat' : 'Add to Chat'}
                  </button>"""

if old_block in h and 'toggleChatAccess' not in h:
    h = h.replace(old_block, new_block)
    print("Button added to UI.")

# Add the JS function
js_func = """
    window.toggleChatAccess = async function(uid, currentStatus) {
      if (!confirm(`Kya aap waqai is user ko ${currentStatus ? 'Chat se remove' : 'Chat mein add'} karna chahte hain?`)) return;
      try {
        const newStatus = !currentStatus;
        await db.collection('users').doc(uid).update({ isChatMember: newStatus });
        await db.collection('donors').doc(uid).update({ isChatMember: newStatus }).catch(()=>{});
        alert(newStatus ? "✅ User added to Chat!" : "❌ User removed from Chat!");
        loadMembers(); // Refresh list
      } catch(e) {
        alert("Error: " + e.message);
      }
    };
"""

if 'window.toggleChatAccess' not in h:
    h = h.replace('window.switchTab = function(tab, event) {', js_func + '\n    window.switchTab = function(tab, event) {')
    print("Function added to JS.")

with open('admin.html', 'w', encoding='utf-8') as f:
    f.write(h)

print("Done: Chat control fixed!")
