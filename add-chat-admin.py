import re

with open('admin.html', 'r', encoding='utf-8') as f:
    h = f.read()

# 1. Add "Add to Chat" button in the member card UI
old_btn = """<select class="action-select" onchange="updateRole('${m.id}', this.value)">
                    <option value="" disabled selected>Change Role</option>
                    <option value="donor">Make Donor</option>
                    <option value="moderator">Make Moderator</option>
                    <option value="admin">Make Admin</option>
                    <option value="banned" style="color:#e74c3c; font-weight:bold;">Ban User</option>
                  </select>"""

new_btn = """<div style="display:flex; flex-direction:column; gap:5px; margin-top:5px;">
                  <select class="action-select" onchange="updateRole('${m.id}', this.value)">
                    <option value="" disabled selected>Change Role</option>
                    <option value="donor">Make Donor</option>
                    <option value="moderator">Make Moderator</option>
                    <option value="admin">Make Admin</option>
                    <option value="banned" style="color:#e74c3c; font-weight:bold;">Ban User</option>
                  </select>
                  <button onclick="toggleChatAccess('${m.id}', ${m.isChatMember || false})" style="padding:6px; border-radius:6px; border:1px solid #ccc; font-size:12px; font-weight:bold; cursor:pointer; background:${m.isChatMember ? '#f8d7da' : '#d4edda'}; color:${m.isChatMember ? '#721c24' : '#155724'}; width: 100%;">
                    ${m.isChatMember ? 'Remove from Chat' : 'Add to Chat'}
                  </button>
                </div>"""

if old_btn in h and 'toggleChatAccess' not in h:
    h = h.replace(old_btn, new_btn)

# 2. Add the JS function to handle Chat Access
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

with open('admin.html', 'w', encoding='utf-8') as f:
    f.write(h)

print("Done: Admin Chat Control added successfully!")
