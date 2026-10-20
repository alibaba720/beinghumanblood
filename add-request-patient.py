with open('index.html', 'r', encoding='utf-8') as f:
    h = f.read()

# 1. Add Request Modal HTML (before existing modal)
html_modal = """
<!-- REQUEST BLOOD MODAL -->
<div class="modal-overlay" id="requestModal" onclick="if(event.target===this)closeReqModal()">
  <div class="modal">
    <button class="modal-close" onclick="closeReqModal()">✕</button>
    <h2>🩸 Request Blood</h2>
    <p id="reqContext" style="color:var(--primary);font-weight:700;margin-bottom:15px;background:#fff5e0;padding:10px;border-radius:8px;text-align:center;"></p>
    
    <label style="margin-top:10px;">Patient ka Naam *</label>
    <input type="text" id="reqName" placeholder="Mareez ka naam" style="width:100%;padding:12px;margin-bottom:10px;border:2px solid #ead5c0;border-radius:8px;">

    <label>Hospital ka Naam *</label>
    <input type="text" id="reqHospital" placeholder="Hospital / Clinic" style="width:100%;padding:12px;margin-bottom:10px;border:2px solid #ead5c0;border-radius:8px;">

    <label>Area / Address *</label>
    <input type="text" id="reqArea" placeholder="Area (e.g. Cantt, Johar Town)" style="width:100%;padding:12px;margin-bottom:10px;border:2px solid #ead5c0;border-radius:8px;">

    <label>Urgency (Kitna urgent hai?)</label>
    <select id="reqUrgency" style="width:100%;padding:12px;margin-bottom:15px;border:2px solid #ead5c0;border-radius:8px;">
      <option value="Normal">Normal</option>
      <option value="Urgent">Urgent (Critical)</option>
    </select>

    <button onclick="submitReq()" id="reqSubmitBtn">Submit Request</button>
    <div id="reqMsg" class="msg"></div>
    
    <div id="waOwnerBox" style="display:none; margin-top:15px; text-align:center; padding-top:15px; border-top:1px dashed #ccc;">
      <p style="color:#27ae60;font-weight:bold;margin-bottom:5px;">✅ Request Save Ho Gayi!</p>
      <p style="font-size:12px;color:#666;margin-bottom:12px;">Ab Owner (Ali Hassan) ko alert bhejein taake wo foran donors ko call kar sakein.</p>
      <a id="waOwnerLink" href="#" target="_blank" style="display:inline-block;background:#25D366;color:white;padding:12px 20px;border-radius:8px;text-decoration:none;font-weight:bold;width:100%;">📱 Alert Owner on WhatsApp</a>
    </div>
  </div>
</div>
"""
h = h.replace('<!-- MODAL -->', html_modal + '\n<!-- MODAL -->')

# 2. Modify searchDonors function to add Request button
old_search_success = """        box.innerHTML = `
          <div class="big">
            <div class="num">${snap.size}</div>
            <div class="lbl">${blood} • ${city} — ${t.donorsFound}</div>
          </div>
        `;"""

new_search_success = """        box.innerHTML = `
          <div class="big">
            <div class="num">${snap.size}</div>
            <div class="lbl">${blood} • ${city} — ${t.donorsFound}</div>
          </div>
          <button onclick="openReqModal('${blood}', '${city}')" style="width:100%;padding:14px;margin-top:15px;background:linear-gradient(135deg,#27ae60,#2ecc71);color:white;border:none;border-radius:10px;font-weight:bold;font-size:15px;cursor:pointer;box-shadow:0 4px 10px rgba(39,174,96,0.3);">
            🩸 REQUEST BLOOD NOW
          </button>
        `;"""
h = h.replace(old_search_success, new_search_success)

# 3. Add Logic for Request Modal in the JS block
js_logic = """
  // ==========================================
  // REQUEST BLOOD SYSTEM
  // ==========================================
  let currentReqBlood = '';
  let currentReqCity = '';

  window.openReqModal = function(blood, city) {
    currentReqBlood = blood;
    currentReqCity = city;
    document.getElementById('reqContext').textContent = `Blood Needed: ${blood} in ${city}`;
    document.getElementById('requestModal').classList.add('show');
    document.getElementById('reqMsg').style.display = 'none';
    document.getElementById('waOwnerBox').style.display = 'none';
    document.getElementById('reqSubmitBtn').style.display = 'block';
  };

  window.closeReqModal = function() {
    document.getElementById('requestModal').classList.remove('show');
  };

  window.submitReq = async function() {
    const name = document.getElementById('reqName').value.trim();
    const hospital = document.getElementById('reqHospital').value.trim();
    const area = document.getElementById('reqArea').value.trim();
    const urgency = document.getElementById('reqUrgency').value;
    const btn = document.getElementById('reqSubmitBtn');
    const msgEl = document.getElementById('reqMsg');

    if (!name || !hospital || !area) {
      msgEl.textContent = 'Patient, Hospital aur Area lazmi bharein!';
      msgEl.className = 'msg error';
      msgEl.style.display = 'block';
      return;
    }

    btn.disabled = true;
    btn.textContent = 'Saving...';

    try {
      // 1. Save to Firestore
      await db.collection('requests').add({
        patientName: name,
        hospital: hospital,
        area: area,
        urgency: urgency,
        blood: currentReqBlood,
        city: currentReqCity,
        language: currentLang,
        status: 'pending',
        createdAt: firebase.firestore.FieldValue.serverTimestamp()
      });

      // 2. Prepare WhatsApp link for Owner
      const waText = encodeURIComponent(`🚨 *URGENT BLOOD REQUEST* 🚨\\n\\nBlood: ${currentReqBlood}\\nCity: ${currentReqCity}\\nPatient: ${name}\\nHospital: ${hospital}\\nArea: ${area}\\nUrgency: ${urgency}\\n\\nPlease check site or call donors!`);
      const waLink = `https://wa.me/923016631720?text=${waText}`; // Owner's number

      document.getElementById('waOwnerLink').href = waLink;
      document.getElementById('waOwnerBox').style.display = 'block';
      btn.style.display = 'none';
      msgEl.style.display = 'none';
      
      // Clear inputs
      document.getElementById('reqName').value = '';
      document.getElementById('reqHospital').value = '';
      document.getElementById('reqArea').value = '';

    } catch (e) {
      msgEl.textContent = 'Error: ' + e.message;
      msgEl.className = 'msg error';
      msgEl.style.display = 'block';
      btn.disabled = false;
      btn.textContent = 'Submit Request';
    }
  };
"""

# Insert JS logic inside waitForFirebase (before the closing of the callback)
h = h.replace('window.goToProfile = function() {', js_logic + '\n  window.goToProfile = function() {')

with open('index.html', 'w', encoding='utf-8') as f:
    f.write(h)

print("Done")
