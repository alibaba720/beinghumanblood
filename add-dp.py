import re

# 1. UPDATE PROFILE.HTML
with open('profile.html', 'r', encoding='utf-8') as f: profile = f.read()

# Add DP UI
dp_html = """
    <!-- DP UPLOAD -->
    <div style="text-align:center; margin-bottom: 20px;">
      <div style="position:relative; display:inline-block;">
        <img id="dpPreview" src="https://cdn-icons-png.flaticon.com/512/149/149071.png" style="width:100px; height:100px; border-radius:50%; object-fit:cover; border:3px solid #8B0000;">
        <label for="dpInput" style="position:absolute; bottom:0; right:0; background:#8B0000; color:white; width:32px; height:32px; border-radius:50%; display:flex; align-items:center; justify-content:center; cursor:pointer; border:2px solid white; font-size:14px;">📷</label>
        <input type="file" id="dpInput" accept="image/*" style="display:none" onchange="uploadDP(this)">
      </div>
      <p style="font-size:11px; color:#888; margin-top:5px;">Apni photo lagayein (DP)</p>
    </div>
"""
if 'id="dpPreview"' not in profile:
    profile = profile.replace('<label>Poora Naam</label>', dp_html + '\n    <label>Poora Naam</label>')

# Add DP JS
dp_js = """
  const IMGBB_API_KEY = "YOUR_API_KEY_HERE";
  
  window.uploadDP = async function(input) {
    if (!input.files || !input.files[0]) return;
    const file = input.files[0];
    const formData = new FormData();
    formData.append('image', file);
    
    const preview = document.getElementById('dpPreview');
    preview.style.opacity = '0.5';
    
    try {
      const res = await fetch(`https://api.imgbb.com/1/upload?key=${IMGBB_API_KEY}`, {
        method: 'POST',
        body: formData
      });
      const data = await res.json();
      if (data.success) {
        const url = data.data.url;
        await db.collection('users').doc(currentUser.uid).update({ dpUrl: url });
        await db.collection('donors').doc(currentUser.uid).update({ dpUrl: url }).catch(()=>{});
        preview.src = url;
        alert("✅ Photo upload ho gayi!");
      } else {
        alert("Upload error: " + data.error.message);
      }
    } catch(e) {
      alert("Network error: " + e.message);
    }
    preview.style.opacity = '1';
  };
"""
if 'uploadDP' not in profile:
    profile = profile.replace('window.saveProfile = async function() {', dp_js + '\n  window.saveProfile = async function() {')
    # Load existing DP
    profile = profile.replace("document.getElementById('p_name').value = d.name || '';", 
        "document.getElementById('p_name').value = d.name || '';\n        if(d.dpUrl) document.getElementById('dpPreview').src = d.dpUrl;")

with open('profile.html', 'w', encoding='utf-8') as f: f.write(profile)


# 2. UPDATE INDEX.HTML
with open('index.html', 'r', encoding='utf-8') as f: index = f.read()

old_user_btn = '<button class="user-btn" onclick="goToProfile()">👤 <span id="userName">User</span></button>'
new_user_btn = '<button class="user-btn" onclick="goToProfile()" style="display:flex; align-items:center; gap:5px; padding-left:5px;"><img id="headerDP" src="" style="width:28px; height:28px; border-radius:50%; object-fit:cover; display:none; border:2px solid rgba(255,255,255,0.5);"> <span id="userName">User</span></button>'
if old_user_btn in index:
    index = index.replace(old_user_btn, new_user_btn)

old_auth = "document.getElementById('userName').textContent = (d.name || 'User').split(' ')[0];"
new_auth = """document.getElementById('userName').textContent = (d.name || 'User').split(' ')[0];
        if (d.dpUrl) {
          const dpImg = document.getElementById('headerDP');
          dpImg.src = d.dpUrl;
          dpImg.style.display = 'inline-block';
        }"""
if 'headerDP' in index and 'dpImg.src = d.dpUrl' not in index:
    index = index.replace(old_auth, new_auth)

with open('index.html', 'w', encoding='utf-8') as f: f.write(index)


# 3. UPDATE ADMIN.HTML
with open('admin.html', 'r', encoding='utf-8') as f: admin = f.read()

old_member_card = """          <div class="member-card">
            <div class="member-info">
              <h4>${m.name} <span class="role-badge role-${m.role}">${m.role}</span></h4>
              <p>🩸 ${m.blood} • 📍 ${m.city}</p>
              <p>📞 <a href="tel:${m.phone}" style="color:#8B0000;text-decoration:none;">${m.phone}</a></p>
            </div>"""

new_member_card = """          <div class="member-card">
            <div style="display:flex; align-items:center; gap:10px;">
              <img src="${m.dpUrl || 'https://cdn-icons-png.flaticon.com/512/149/149071.png'}" style="width:45px; height:45px; border-radius:50%; object-fit:cover; border:2px solid #eee;">
              <div class="member-info">
                <h4>${m.name} <span class="role-badge role-${m.role}">${m.role}</span></h4>
                <p>🩸 ${m.blood} • 📍 ${m.city}</p>
                <p>📞 <a href="tel:${m.phone}" style="color:#8B0000;text-decoration:none;">${m.phone}</a></p>
              </div>
            </div>"""
if old_member_card in admin:
    admin = admin.replace(old_member_card, new_member_card)

with open('admin.html', 'w', encoding='utf-8') as f: f.write(admin)

print("Done")
