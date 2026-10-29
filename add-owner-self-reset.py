with open('admin.html', 'r', encoding='utf-8') as f:
    h = f.read()

# 1. Add button in the Header
old_header = """  <a href="index.html" class="back-btn">← Back to Site</a>"""
new_header = """  <div style="display:flex; gap:10px;">
    <button onclick="changeMyPassword()" class="back-btn" style="background:#f39c12; color:white;">🔑 My Password</button>
    <a href="index.html" class="back-btn">← Back to Site</a>
  </div>"""

if old_header in h and 'changeMyPassword' not in h:
    h = h.replace(old_header, new_header)

# 2. Add the JS function to change password
reset_self_js = """
    window.changeMyPassword = async function() {
      const newPass = prompt("Enter your NEW password (min 6 characters):");
      if (!newPass) return;
      if (newPass.length < 6) return alert("Password must be at least 6 characters.");
      
      try {
        const user = firebase.auth().currentUser;
        const res = await fetch('/api/reset-password', {
          method: 'POST',
          headers: { 'Content-Type': 'application/json' },
          body: JSON.stringify({ uid: user.uid, newPassword: newPass })
        });
        const data = await res.json();
        
        if (data.success) {
          alert("✅ Mubarak ho! Aapka password successfully change ho gaya hai.\\n\\nNaya Password yaad rakhna!");
        } else {
          alert("❌ Error: " + data.error);
        }
      } catch(e) {
        alert("❌ Network error: " + e.message);
      }
    };
"""

if 'window.changeMyPassword' not in h:
    h = h.replace('window.switchTab = function(tab, event) {', reset_self_js + '\n    window.switchTab = function(tab, event) {')

with open('admin.html', 'w', encoding='utf-8') as f:
    f.write(h)

print("Done: Owner self-reset button added to Admin Panel Header.")
