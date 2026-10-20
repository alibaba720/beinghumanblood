with open('admin.html', 'r', encoding='utf-8') as f:
    h = f.read()

# 1. Add Search UI inside Members tab
old_members_html = """  <div id="members" class="section">
    <div id="membersList"><div class="empty-msg">Loading members...</div></div>
  </div>"""

new_members_html = """  <div id="members" class="section">
    <div style="background:white; padding:15px; border-radius:12px; margin-bottom:15px; box-shadow:0 2px 8px rgba(0,0,0,0.06);">
      <h3 style="margin-bottom:10px; color:#8B0000; font-size:15px;">🔍 Search Donors</h3>
      <div style="display:flex; gap:10px; margin-bottom:10px;">
        <select id="adminSearchBlood" style="flex:1; padding:10px; border:1px solid #ccc; border-radius:8px; font-family:inherit;">
          <option value="">All Blood</option>
          <option value="A+">A+</option><option value="A-">A-</option>
          <option value="B+">B+</option><option value="B-">B-</option>
          <option value="AB+">AB+</option><option value="AB-">AB-</option>
          <option value="O+">O+</option><option value="O-">O-</option>
        </select>
        <input type="text" id="adminSearchCity" placeholder="City (e.g. Daska)" style="flex:1; padding:10px; border:1px solid #ccc; border-radius:8px; font-family:inherit;">
      </div>
      <button onclick="filterAdminMembers()" style="width:100%; padding:10px; background:#8B0000; color:white; border:none; border-radius:8px; font-weight:bold; cursor:pointer;">Search</button>
    </div>
    <div id="membersList"><div class="empty-msg">Loading members...</div></div>
  </div>"""

if old_members_html in h:
    h = h.replace(old_members_html, new_members_html)

# 2. Update loadMembers logic to store globally and add search function
old_load_members = """    async function loadMembers() {
      const list = document.getElementById('membersList');
      try {
        const snap = await db.collection('users').get();
        
        if (snap.empty) {
          list.innerHTML = '<div class="empty-msg">Koi member nahi mila.</div>';
          return;
        }

        let members = [];
        snap.forEach(doc => members.push({ id: doc.id, ...doc.data() }));
        
        const roleOrder = { owner: 1, admin: 2, moderator: 3, donor: 4 };
        members.sort((a, b) => (roleOrder[a.role] || 4) - (roleOrder[b.role] || 4));

        let html = '';
        members.forEach(m => {
          html += `
            <div class="member-card">
              <div class="member-info">
                <h4>${m.name} <span class="role-badge role-${m.role}">${m.role}</span></h4>
                <p>🩸 ${m.blood} • 📍 ${m.city}</p>
                <p>📞 <a href="tel:${m.phone}" style="color:#8B0000;text-decoration:none;">${m.phone}</a></p>
              </div>
              <div>
                ${m.role !== 'owner' ? `
                  <select class="action-select" onchange="updateRole('${m.id}', this.value)">
                    <option value="" disabled selected>Change Role</option>
                    <option value="donor">Make Donor</option>
                    <option value="moderator">Make Moderator</option>
                    <option value="admin">Make Admin</option>
                  </select>
                ` : '<div style="font-size:12px;font-weight:bold;color:#d35400;">Protected</div>'}
              </div>
            </div>
          `;
        });
        list.innerHTML = html;
      } catch (e) {
        list.innerHTML = '<div class="empty-msg" style="color:red;">Error: ' + e.message + '</div>';
      }
    }"""

new_load_members = """    let allMembersList = [];

    async function loadMembers() {
      const list = document.getElementById('membersList');
      try {
        const snap = await db.collection('users').get();
        
        if (snap.empty) {
          list.innerHTML = '<div class="empty-msg">Koi member nahi mila.</div>';
          return;
        }

        allMembersList = [];
        snap.forEach(doc => allMembersList.push({ id: doc.id, ...doc.data() }));
        
        const roleOrder = { owner: 1, admin: 2, moderator: 3, donor: 4 };
        allMembersList.sort((a, b) => (roleOrder[a.role] || 4) - (roleOrder[b.role] || 4));

        renderMembers(allMembersList);
      } catch (e) {
        list.innerHTML = '<div class="empty-msg" style="color:red;">Error: ' + e.message + '</div>';
      }
    }

    function renderMembers(members) {
      const list = document.getElementById('membersList');
      if (members.length === 0) {
        list.innerHTML = '<div class="empty-msg">Koi member nahi mila is search par.</div>';
        return;
      }

      let html = '';
      members.forEach(m => {
        html += `
          <div class="member-card">
            <div class="member-info">
              <h4>${m.name} <span class="role-badge role-${m.role}">${m.role}</span></h4>
              <p>🩸 ${m.blood} • 📍 ${m.city}</p>
              <p>📞 <a href="tel:${m.phone}" style="color:#8B0000;text-decoration:none;">${m.phone}</a></p>
            </div>
            <div>
              ${m.role !== 'owner' ? `
                <select class="action-select" onchange="updateRole('${m.id}', this.value)">
                  <option value="" disabled selected>Change Role</option>
                  <option value="donor">Make Donor</option>
                  <option value="moderator">Make Moderator</option>
                  <option value="admin">Make Admin</option>
                </select>
              ` : '<div style="font-size:12px;font-weight:bold;color:#d35400;">Protected</div>'}
            </div>
          </div>
        `;
      });
      list.innerHTML = html;
    }

    window.filterAdminMembers = function() {
      const blood = document.getElementById('adminSearchBlood').value;
      const city = document.getElementById('adminSearchCity').value.trim().toLowerCase();

      if (!blood && !city) {
        renderMembers(allMembersList);
        return;
      }

      const filtered = allMembersList.filter(m => {
        const matchBlood = blood ? m.blood === blood : true;
        const matchCity = city ? (m.city && m.city.toLowerCase().includes(city)) : true;
        return matchBlood && matchCity;
      });

      renderMembers(filtered);
    };"""

if old_load_members in h:
    h = h.replace(old_load_members, new_load_members)

with open('admin.html', 'w', encoding='utf-8') as f:
    f.write(h)

print("Done")
