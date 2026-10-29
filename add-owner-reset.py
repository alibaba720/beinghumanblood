with open('admin.html', 'r', encoding='utf-8') as f:
    h = f.read()

# 1. Update global variable for currentUserRole
old_auth = """        const d = doc.data();
        if (d.role !== 'owner' && d.role !== 'admin') {"""
new_auth = """        const d = doc.data();
        window.currentUserRole = d.role;
        if (d.role !== 'owner' && d.role !== 'admin') {"""
if old_auth in h:
    h = h.replace(old_auth, new_auth)

# 2. Add Reset Password Button in the member card
old_btn = """                <button onclick="muteMember('${m.id}', '${m.name}', ${m.isMuted || false})" style="padding:8px; border-radius:6px; border:1px solid #ccc; font-size:12px; font-weight:bold; cursor:pointer; background:${m.isMuted ? '#fff3cd' : '#f8f9fa'}; color:${m.isMuted ? '#856404' : '#333'}; width:100%; margin-top:5px;">
                  ${m.isMuted ? 'Unmute User' : 'Mute Chat'}
                </button>"""
                
new_btn = """                <button onclick="muteMember('${m.id}', '${m.name}', ${m.isMuted || false})" style="padding:8px; border-radius:6px; border:1px solid #ccc; font-size:12px; font-weight:bold; cursor:pointer; background:${m.isMuted ? '#fff3cd' : '#f8f9fa'}; color:${m.isMuted ? '#856404' : '#333'}; width:100%; margin-top:5px;">
                  ${m.isMuted ? 'Unmute User' : 'Mute Chat'}
                </button>
                ${window.currentUserRole === 'owner' && m.role !== 'owner' ? `
                <button onclick="resetUserPassword('${m.id}', '${m.name}')" style="padding:8px; border-radius:6px; border:1px solid #ccc; font-size:12px; font-weight:bold; cursor:pointer; background:#e3f2fd; color:#0d47a1; width:100%; margin-top:5px;">
                  🔑 Reset Password
                </button>
                ` : ''}"""

if old_btn in h and 'resetUserPassword' not in h:
    h = h.replace(old_btn, new_btn)

# 3. Add resetUserPassword JS function
reset_js = """
    window.resetUserPassword = async function(uid, name) {
      const newPass = prompt(`Enter new password for ${name} (min 6 characters):`);
      if (!newPass) return;
      if (newPass.length < 6) return alert("Password must be at least 6 characters.");
      
      try {
        const res = await fetch('/api/reset-password', {
          method: 'POST',
          headers: { 'Content-Type': 'application/json' },
          body: JSON.stringify({ uid: uid, newPassword: newPass })
        });
        const data = await res.json();
        
        if (data.success) {
          alert(`✅ Password successfully reset for ${name}!\\n\\nNew Password: ${newPass}`);
        } else {
          alert("❌ Error: " + data.error);
        }
      } catch(e) {
        alert("❌ Network error: " + e.message);
      }
    };
"""

if 'window.resetUserPassword' not in h:
    h = h.replace('window.switchTab = function(tab, event) {', reset_js + '\n    window.switchTab = function(tab, event) {')

with open('admin.html', 'w', encoding='utf-8') as f:
    f.write(h)

print("Done: Owner-only password reset button added to Admin Panel.")
