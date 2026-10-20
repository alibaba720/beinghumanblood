with open('index.html', 'r', encoding='utf-8') as f:
    h = f.read()

# 1. Add Bell Icon to Header
old_header_actions = """<div class="header-actions">
      <button class="icon-btn" onclick="toggleLangMenu()" title="Language">🌐</button>"""
new_header_actions = """<div class="header-actions">
      <button class="icon-btn" onclick="toggleLangMenu()" title="Language">🌐</button>
      <button class="icon-btn" onclick="openDonorReqModal()" title="Blood Requests" style="position:relative;">🔔<span id="reqDot" style="display:none;position:absolute;top:6px;right:6px;width:10px;height:10px;background:#e74c3c;border-radius:50%;border:1px solid white;"></span></button>"""
h = h.replace(old_header_actions, new_header_actions)

# 2. Add Patient Phone field to Patient Request Form
old_patient_form = """    <label style="margin-top:10px;">Patient ka Naam *</label>
    <input type="text" id="reqName" placeholder="Mareez ka naam" style="width:100%;padding:12px;margin-bottom:10px;border:2px solid #ead5c0;border-radius:8px;">"""
new_patient_form = """    <label style="margin-top:10px;">Patient ka Naam *</label>
    <input type="text" id="reqName" placeholder="Mareez ka naam" style="width:100%;padding:12px;margin-bottom:10px;border:2px solid #ead5c0;border-radius:8px;">

    <label>Patient ka Phone Number *</label>
    <input type="tel" id="reqPhone" placeholder="03xxxxxxxxx" style="width:100%;padding:12px;margin-bottom:10px;border:2px solid #ead5c0;border-radius:8px;">"""
h = h.replace(old_patient_form, new_patient_form)

# 3. Update submitReq to include phone
old_submit_req = """    const name = document.getElementById('reqName').value.trim();
    const hospital = document.getElementById('reqHospital').value.trim();"""
new_submit_req = """    const name = document.getElementById('reqName').value.trim();
    const phone = document.getElementById('reqPhone').value.trim();
    const hospital = document.getElementById('reqHospital').value.trim();"""
h = h.replace(old_submit_req, new_submit_req)

h = h.replace("""    if (!name || !hospital || !area) {
      msgEl.textContent = 'Patient, Hospital aur Area lazmi bharein!';""", """    if (!name || !phone || !hospital || !area) {
      msgEl.textContent = 'Patient, Phone, Hospital aur Area lazmi bharein!';""")

h = h.replace("""        patientName: name,
        hospital: hospital,""", """        patientName: name,
        patientPhone: phone,
        hospital: hospital,""")

h = h.replace("""      document.getElementById('reqName').value = '';
      document.getElementById('reqHospital').value = '';""", """      document.getElementById('reqName').value = '';
      document.getElementById('reqPhone').value = '';
      document.getElementById('reqHospital').value = '';""")

# 4. Add Donor Requests Modal HTML
donor_modal_html = """
<!-- DONOR REQUESTS MODAL -->
<div class="modal-overlay" id="donorReqModal" onclick="if(event.target===this)closeDonorReqModal()">
  <div class="modal">
    <button class="modal-close" onclick="closeDonorReqModal()">✕</button>
    <h2>🔔 Blood Requests</h2>
    <p style="color:#666;font-size:13px;margin-bottom:15px;">Aap ke shehar aur blood group ki requests:</p>
    <div id="donorReqList" style="max-height: 60vh; overflow-y: auto;"></div>
  </div>
</div>
"""
h = h.replace('<!-- MODAL -->', donor_modal_html + '\n<!-- MODAL -->')

# 5. Add Donor JS Logic
donor_js = """
  let currentUserCity = '';
  let currentUserBlood = '';
  let activeRequests = [];

  async function checkForRequests() {
    if (!currentUserCity || !currentUserBlood) return;
    try {
      const snap = await db.collection('requests')
        .where('city', '==', currentUserCity)
        .where('blood', '==', currentUserBlood)
        .where('status', '==', 'pending')
        .get();
      
      activeRequests = [];
      snap.forEach(doc => activeRequests.push({ id: doc.id, ...doc.data() }));
      
      const dot = document.getElementById('reqDot');
      if (activeRequests.length > 0 && document.getElementById('userName').textContent !== 'Login') {
        dot.style.display = 'block';
      } else {
        dot.style.display = 'none';
      }
    } catch (e) { console.error("Error fetching requests:", e); }
  }

  window.openDonorReqModal = function() {
    if (document.getElementById('userName').textContent === 'Login') {
      window.location.href = 'login.html';
      return;
    }
    document.getElementById('donorReqModal').classList.add('show');
    renderDonorRequests();
  };

  window.closeDonorReqModal = function() {
    document.getElementById('donorReqModal').classList.remove('show');
  };

  window.renderDonorRequests = function() {
    const list = document.getElementById('donorReqList');
    if (activeRequests.length === 0) {
      list.innerHTML = '<div style="text-align:center;padding:20px;color:#999;">Filhal koi request nahi hai. Shukriya!</div>';
      return;
    }
    
    list.innerHTML = activeRequests.map(r => `
      <div style="background:#fff8f0;border:1px solid #ead5c0;border-radius:10px;padding:15px;margin-bottom:10px;">
        <div style="font-weight:bold;color:#8B0000;font-size:16px;margin-bottom:5px;">${r.patientName}</div>
        <div style="font-size:13px;color:#555;margin-bottom:3px;">📍 ${r.hospital}, ${r.area}</div>
        <div style="font-size:13px;color:#555;margin-bottom:10px;">🚨 Urgency: ${r.urgency}</div>
        <button onclick="acceptRequest('${r.id}', '${r.patientName}', '${r.patientPhone}')" style="width:100%;padding:10px;background:#27ae60;color:white;border:none;border-radius:8px;font-weight:bold;cursor:pointer;">✅ Accept Request</button>
      </div>
    `).join('');
  };

  window.acceptRequest = async function(reqId, pName, pPhone) {
    try {
      await db.collection('requests').doc(reqId).update({ 
        status: 'accepted',
        acceptedBy: firebase.auth().currentUser.uid,
        acceptedAt: firebase.firestore.FieldValue.serverTimestamp()
      });
      
      alert(`Shukriya! Aap ne madad ka waada kiya.\\n\\nPatient: ${pName}\\nPhone: ${pPhone}\\n\\nBaraye meharbani foran rabta karein.`);
      closeDonorReqModal();
      checkForRequests(); // Refresh dot
    } catch (e) {
      alert("Error: " + e.message);
    }
  };
"""

# Inject donor JS logic inside the auth state block so we have user data
auth_state_old = """        const d = doc.data();
        document.getElementById('userName').textContent = (d.name || 'User').split(' ')[0];
        if (d.role === 'owner' || d.role === 'admin') {
          document.getElementById('founderName').textContent = d.name || 'Ali Hassan';
          document.getElementById('founderAvatar').textContent = (d.name || 'A').charAt(0).toUpperCase();
        }"""

auth_state_new = """        const d = doc.data();
        document.getElementById('userName').textContent = (d.name || 'User').split(' ')[0];
        
        // Set global vars for donor requests
        currentUserCity = d.city || '';
        currentUserBlood = d.blood || '';
        
        // Check for pending requests
        checkForRequests();

        if (d.role === 'owner' || d.role === 'admin') {
          document.getElementById('founderName').textContent = d.name || 'Ali Hassan';
          document.getElementById('founderAvatar').textContent = (d.name || 'A').charAt(0).toUpperCase();
        }"""
h = h.replace(auth_state_old, auth_state_new)

# Inject JS
h = h.replace('window.openReqModal = function(blood, city) {', donor_js + '\n  window.openReqModal = function(blood, city) {')

with open('index.html', 'w', encoding='utf-8') as f:
    f.write(h)

print("Done")
