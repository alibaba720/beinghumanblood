with open('index.html', 'r', encoding='utf-8') as f:
    index = f.read()

with open('profile.html', 'r', encoding='utf-8') as f:
    profile = f.read()

# 1. Add button to index.html header
old_header = """      <button class="icon-btn" onclick="toggleLangMenu()" title="Language">🌐</button>
      <button class="icon-btn" onclick="openDonorReqModal()" title="Blood Requests" style="position:relative;">🔔<span id="reqDot" style="display:none;position:absolute;top:6px;right:6px;width:10px;height:10px;background:#e74c3c;border-radius:50%;border:1px solid white;"></span></button>"""
new_header = """      <button class="icon-btn" id="adminPanelBtn" onclick="window.location.href='admin.html'" title="Admin Panel" style="display:none; background:#FFD700; color:#5a0000; font-size:20px;">👑</button>
      <button class="icon-btn" onclick="toggleLangMenu()" title="Language">🌐</button>
      <button class="icon-btn" onclick="openDonorReqModal()" title="Blood Requests" style="position:relative;">🔔<span id="reqDot" style="display:none;position:absolute;top:6px;right:6px;width:10px;height:10px;background:#e74c3c;border-radius:50%;border:1px solid white;"></span></button>"""

if old_header in index and 'id="adminPanelBtn"' not in index:
    index = index.replace(old_header, new_header)

# 2. Show button in index.html if owner/admin
old_role_check = """        if (d.role === 'owner' || d.role === 'admin') {
          document.getElementById('founderName').textContent = d.name || 'Ali Hassan';
          document.getElementById('founderAvatar').textContent = (d.name || 'A').charAt(0).toUpperCase();
        }"""
new_role_check = """        if (d.role === 'owner' || d.role === 'admin') {
          const adminBtn = document.getElementById('adminPanelBtn');
          if (adminBtn) adminBtn.style.display = 'flex';
          document.getElementById('founderName').textContent = d.name || 'Ali Hassan';
          document.getElementById('founderAvatar').textContent = (d.name || 'A').charAt(0).toUpperCase();
        }"""

if old_role_check in index and 'adminPanelBtn.style.display' not in index:
    index = index.replace(old_role_check, new_role_check)

# 3. Add button in profile.html
old_profile_btns = """        <div class="btn-row">
          <button onclick="goToHome()">Home Kholo</button>
          <button class="btn-secondary" onclick="goToProfile()">Edit Profile</button>
          <button class="btn-secondary" onclick="logout()">Logout</button>
        </div>"""
# Note: profile.html might not have goToHome in the same way, let's look for the specific button structure
old_profile_btns_actual = """        <button onclick="saveProfile()" id="saveBtn">Save Karo</button>
        <button class="btn-secondary" onclick="goBack()">Wapas Jao</button>"""
new_profile_btns_actual = """        <button onclick="saveProfile()" id="saveBtn">Save Karo</button>
        <button class="btn-secondary" onclick="goBack()">Wapas Jao</button>
        <button class="btn-secondary" id="adminBtnProfile" onclick="window.location.href='admin.html'" style="display:none; background:#FFD700 !important; color:#5a0000 !important; border-color:#FFD700 !important; margin-top:10px;">👑 Open Admin Panel</button>"""

if old_profile_btns_actual in profile and 'id="adminBtnProfile"' not in profile:
    profile = profile.replace(old_profile_btns_actual, new_profile_btns_actual)

# 4. Show button in profile.html if owner/admin
old_profile_role = """        const roleEl = document.getElementById('p_role');
        roleEl.textContent = currentRole;
        roleEl.className = 'role-display role-' + currentRole;"""
new_profile_role = """        const roleEl = document.getElementById('p_role');
        roleEl.textContent = currentRole;
        roleEl.className = 'role-display role-' + currentRole;
        
        if (currentRole === 'owner' || currentRole === 'admin') {
            const adminBtn = document.getElementById('adminBtnProfile');
            if (adminBtn) adminBtn.style.display = 'block';
        }"""
if old_profile_role in profile and 'adminBtnProfile.style.display' not in profile:
    profile = profile.replace(old_profile_role, new_profile_role)

with open('index.html', 'w', encoding='utf-8') as f: f.write(index)
with open('profile.html', 'w', encoding='utf-8') as f: f.write(profile)

print("Done: Admin buttons added")
