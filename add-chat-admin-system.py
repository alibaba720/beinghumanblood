import re

# ==========================================
# 1. UPDATE ADMIN.HTML
# ==========================================
with open('admin.html', 'r', encoding='utf-8') as f:
    admin = f.read()

# Add Mute button below Add to Chat
old_btn = """<button onclick="toggleChatAccess('${m.id}', ${m.isChatMember || false})" style="padding:8px; border-radius:6px; border:1px solid #ccc; font-size:12px; font-weight:bold; cursor:pointer; background:${m.isChatMember ? '#f8d7da' : '#d4edda'}; color:${m.isChatMember ? '#721c24' : '#155724'}; width:100%;">"""
new_btn = """<button onclick="toggleChatAccess('${m.id}', ${m.isChatMember || false})" style="padding:8px; border-radius:6px; border:1px solid #ccc; font-size:12px; font-weight:bold; cursor:pointer; background:${m.isChatMember ? '#f8d7da' : '#d4edda'}; color:${m.isChatMember ? '#721c24' : '#155724'}; width:100%;">
                  ${m.isChatMember ? 'Remove from Chat' : 'Add to Chat'}
                </button>
                <button onclick="muteMember('${m.id}', '${m.name}', ${m.isMuted || false})" style="padding:8px; border-radius:6px; border:1px solid #ccc; font-size:12px; font-weight:bold; cursor:pointer; background:${m.isMuted ? '#fff3cd' : '#f8f9fa'}; color:${m.isMuted ? '#856404' : '#333'}; width:100%; margin-top:5px;">
                  ${m.isMuted ? 'Unmute User' : 'Mute Chat'}
                </button>"""
# Remove the old closing button tag to prevent duplicates
admin = admin.replace(old_btn + "\n                  ${m.isChatMember ? 'Remove from Chat' : 'Add to Chat'}\n                </button>", new_btn)

# Add muteMember function in admin.html JS
if 'window.muteMember' not in admin:
    mute_js = """
    window.muteMember = async function(uid, name, isMuted) {
      if (isMuted) {
        if(!confirm(`Unmute ${name}?`)) return;
        try {
          await db.collection('users').doc(uid).update({ isMuted: false, muteExpiry: null });
          await db.collection('donors').doc(uid).update({ isMuted: false, muteExpiry: null }).catch(()=>{});
          alert("User unmuted successfully.");
          loadMembers();
        } catch(e) { alert(e.message); }
      } else {
        const hours = prompt(`Mute ${name} for how many hours? (Enter number e.g., 24)`, "24");
        if (hours && !isNaN(hours)) {
          const expiry = new Date();
          expiry.setHours(expiry.getHours() + parseInt(hours));
          try {
            await db.collection('users').doc(uid).update({ isMuted: true, muteExpiry: firebase.firestore.Timestamp.fromDate(expiry) });
            await db.collection('donors').doc(uid).update({ isMuted: true, muteExpiry: firebase.firestore.Timestamp.fromDate(expiry) }).catch(()=>{});
            alert(`User muted for ${hours} hours.`);
            loadMembers();
          } catch(e) { alert(e.message); }
        }
      }
    };
    """
    admin = admin.replace('window.switchTab = function(tab, event) {', mute_js + '\n    window.switchTab = function(tab, event) {')

with open('admin.html', 'w', encoding='utf-8') as f:
    f.write(admin)
    print("Admin Panel updated.")


# ==========================================
# 2. UPDATE INDEX.HTML
# ==========================================
with open('index.html', 'r', encoding='utf-8') as f:
    index = f.read()

# A. Update sendChatMessage (Owner Bypass & Mute Check)
old_send = """    if (!text || !user) return;

    // BULLETPROOF RESTRICTION: Block 5 or more digits
    // Remove spaces, dashes, brackets before checking
    const cleanText = text.replace(/[^0-9]/g, ''); // Extract only numbers
    if (cleanText.length >= 5) {
      alert("⚠️ Baraye meharbani chat mein phone number share na karein.");
      return;
    }

    input.value = ''; // Clear input immediately"""

new_send = """    if (!text || !user) return;

    const userDoc = await db.collection('users').doc(user.uid).get();
    const uData = userDoc.data();

    // 1. Check if Muted
    if (uData.isMuted && uData.muteExpiry) {
        const expiry = uData.muteExpiry.toDate();
        if (expiry > new Date()) {
            alert("⚠️ Aapko chat se mute kar diya gaya hai. Waqt khatam hone tak intezar karein.");
            return;
        }
    }

    // 2. Number Restriction (Owner is exempt)
    if (uData.role !== 'owner') {
        const cleanText = text.replace(/[^0-9]/g, '');
        if (cleanText.length >= 5) {
          alert("⚠️ Baraye meharbani chat mein phone number share na karein.");
          return;
        }
    }

    input.value = ''; // Clear input immediately"""

if "if (!text || !user) return;" in index and "if (uData.role !== 'owner')" not in index:
    index = index.replace(old_send, new_send)

# B. Update loadChatMessages (Clickable Names for Admins)
old_name = """              <div style="font-size: 11px; color: #8B0000; font-weight: bold; margin-bottom: 3px;">${msg.senderName || 'User'}</div>"""
new_name = """              <div style="font-size: 11px; color: #8B0000; font-weight: bold; margin-bottom: 3px; cursor: pointer; text-decoration: underline;" onclick="event.stopPropagation(); openAdminChatMenu('${msg.uid}', '${msg.senderName}')">${msg.senderName || 'User'}</div>"""

if old_name in index:
    index = index.replace(old_name, new_name)

# C. Add Admin Chat Menu UI & Logic
if 'id="adminChatMenu"' not in index:
    # Add UI Modal
    admin_menu_html = """
<!-- ADMIN CHAT ACTION MENU -->
<div class="modal-overlay" id="adminChatMenu" onclick="if(event.target===this)closeAdminMenu()">
  <div class="modal" style="max-width: 300px; padding: 20px;">
    <h3 id="acmName" style="color:#8B0000; margin-bottom:15px; font-size:16px; border-bottom:1px solid #eee; padding-bottom:10px;">User Actions</h3>
    <button onclick="visitChatProfile()" style="width:100%; padding:12px; margin-bottom:10px; background:#3498db; color:white; border:none; border-radius:8px; font-weight:bold;">👤 Visit Profile</button>
    <button onclick="muteChatUser()" style="width:100%; padding:12px; margin-bottom:10px; background:#f39c12; color:white; border:none; border-radius:8px; font-weight:bold;">🔇 Mute Member</button>
    <button onclick="removeChatUser()" style="width:100%; padding:12px; margin-bottom:10px; background:#e74c3c; color:white; border:none; border-radius:8px; font-weight:bold;">❌ Remove from Chat</button>
    <button onclick="closeAdminMenu()" style="width:100%; padding:12px; background:#eee; color:#333; border:none; border-radius:8px; font-weight:bold;">Cancel</button>
  </div>
</div>
"""
    index = index.replace('<!-- MODAL -->', admin_menu_html + '\n<!-- MODAL -->')

    # Add Logic
    admin_menu_js = """
  let selectedChatUid = null;
  let selectedChatName = null;

  window.openAdminChatMenu = function(uid, name) {
    const user = firebase.auth().currentUser;
    if (!user || !window.currentUserData) return;
    
    // Only admins/owners can see this menu
    if (window.currentUserData.role !== 'owner' && window.currentUserData.role !== 'admin') return;

    // Don't show menu for self
    if (uid === user.uid) return;

    selectedChatUid = uid;
    selectedChatName = name;
    document.getElementById('acmName').textContent = name;
    document.getElementById('adminChatMenu').classList.add('show');
  };

  window.closeAdminMenu = function() {
    document.getElementById('adminChatMenu').classList.remove('show');
  };

  window.visitChatProfile = async function() {
    if (!selectedChatUid) return;
    try {
        const doc = await db.collection('users').doc(selectedChatUid).get();
        if (doc.exists) {
            const d = doc.data();
            alert(`Name: ${d.name}\\nPhone: ${d.phone}\\nCity: ${d.city}\\nBlood: ${d.blood}\\nRole: ${d.role}`);
        }
    } catch(e) { alert(e.message); }
    closeAdminMenu();
  };

  window.muteChatUser = async function() {
    if (!selectedChatUid) return;
    const hours = prompt(`Mute ${selectedChatName} for how many hours? (e.g., 24)`, "24");
    if (hours && !isNaN(hours)) {
        const expiry = new Date();
        expiry.setHours(expiry.getHours() + parseInt(hours));
        try {
            await db.collection('users').doc(selectedChatUid).update({ isMuted: true, muteExpiry: firebase.firestore.Timestamp.fromDate(expiry) });
            await db.collection('donors').doc(selectedChatUid).update({ isMuted: true, muteExpiry: firebase.firestore.Timestamp.fromDate(expiry) }).catch(()=>{});
            alert(`User muted for ${hours} hours.`);
        } catch(e) { alert(e.message); }
    }
    closeAdminMenu();
  };

  window.removeChatUser = async function() {
    if (!selectedChatUid) return;
    if (!confirm(`Remove ${selectedChatName} from chat?`)) return;
    try {
        await db.collection('users').doc(selectedChatUid).update({ isChatMember: false });
        await db.collection('donors').doc(selectedChatUid).update({ isChatMember: false }).catch(()=>{});
        alert("User removed from Chat.");
    } catch(e) { alert(e.message); }
    closeAdminMenu();
  };
"""
    if 'window.openAdminChatMenu' not in index:
        index = index.replace('window.openChatModal = function() {', admin_menu_js + '\n  window.openChatModal = function() {')

with open('index.html', 'w', encoding='utf-8') as f:
    f.write(index)
    print("Index.html updated.")

print("Done: Full chat admin system applied!")
