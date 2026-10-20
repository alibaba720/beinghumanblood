with open('index.html', 'r', encoding='utf-8') as f:
    h = f.read()

# 1. Add HTML for Waiting state in Request Modal
old_wa_box = """    <div id="waOwnerBox" style="display:none; margin-top:15px; text-align:center; padding-top:15px; border-top:1px dashed #ccc;">"""
new_wa_box = """    <div id="waitingBox" style="display:none; text-align:center; padding:20px;">
      <div style="font-size:30px; margin-bottom:10px;">⏳</div>
      <h3 style="color:#8B0000; margin-bottom:5px;">Waiting for Donor...</h3>
      <p style="font-size:12px;color:#666;">Jab koi donor accept karega, uski details yahan aapko mil jayengi. Is page ko band na karein.</p>
    </div>

    <div id="donorFoundBox" style="display:none; background:#d4edda; padding:15px; border-radius:10px; margin-top:15px; border-left:4px solid #27ae60; text-align:center;">
      <h3 style="color:#155724; margin-bottom:5px;">✅ Donor Mil Gaya!</h3>
      <p id="donorFoundName" style="font-weight:bold; font-size:16px; color:#8B0000; margin-bottom:5px;"></p>
      <p id="donorFoundPhone" style="font-size:15px;"></p>
      <p style="font-size:12px; color:#666; margin-top:10px;">Baraye meharbani foran rabta karein.</p>
    </div>

    <div id="waOwnerBox" style="display:none; margin-top:15px; text-align:center; padding-top:15px; border-top:1px dashed #ccc;">"""
h = h.replace(old_wa_box, new_wa_box)

# 2. Store currentUserData in auth state
auth_state_old = """      const doc = await db.collection('users').doc(user.uid).get();
      if (doc.exists) {
        const d = doc.data();"""
auth_state_new = """      const doc = await db.collection('users').doc(user.uid).get();
      if (doc.exists) {
        const d = doc.data();
        window.currentUserData = d;"""
h = h.replace(auth_state_old, auth_state_new)

# 3. Update submitReq for live tracking
old_submit = """      // 1. Save to Firestore
      await db.collection('requests').add({
        patientName: name,
        patientPhone: phone,
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
      document.getElementById('reqPhone').value = '';
      document.getElementById('reqHospital').value = '';
      document.getElementById('reqArea').value = '';"""

new_submit = """      // 1. Save to Firestore
      const docRef = await db.collection('requests').add({
        patientName: name,
        patientPhone: phone,
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
      const waText = encodeURIComponent(`🚨 *URGENT BLOOD REQUEST* 🚨\\n\\nBlood: ${currentReqBlood}\\nCity: ${currentReqCity}\\nPatient: ${name}\\nPhone: ${phone}\\nHospital: ${hospital}\\nArea: ${area}\\n\\nPlease check site!`);
      const waLink = `https://wa.me/923016631720?text=${waText}`;

      document.getElementById('waOwnerLink').href = waLink;
      document.getElementById('waOwnerBox').style.display = 'block';
      btn.style.display = 'none';
      msgEl.style.display = 'none';
      
      // Clear inputs
      document.getElementById('reqName').value = '';
      document.getElementById('reqPhone').value = '';
      document.getElementById('reqHospital').value = '';
      document.getElementById('reqArea').value = '';

      // Show Waiting Box
      document.getElementById('waitingBox').style.display = 'block';
      document.getElementById('donorFoundBox').style.display = 'none';

      // 3. Listen for donor acceptance
      docRef.onSnapshot((doc) => {
        if (doc.exists) {
          const data = doc.data();
          if (data.status === 'accepted') {
            document.getElementById('waitingBox').style.display = 'none';
            document.getElementById('donorFoundBox').style.display = 'block';
            document.getElementById('donorFoundName').textContent = `Donor: ${data.donorName}`;
            document.getElementById('donorFoundPhone').innerHTML = `Phone: <a href="tel:${data.donorPhone}" style="color:#8B0000; font-weight:bold; text-decoration:none;">${data.donorPhone}</a>`;
            document.getElementById('waOwnerBox').style.display = 'none'; // Hide owner alert once accepted
          }
        }
      });"""
h = h.replace(old_submit, new_submit)


# 4. Update acceptRequest to save donor info and notify owner
old_accept = """  window.acceptRequest = async function(reqId, pName, pPhone) {
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
  };"""

new_accept = """  window.acceptRequest = async function(reqId, pName, pPhone) {
    if (!window.currentUserData) return alert("Please login again.");
    
    try {
      await db.collection('requests').doc(reqId).update({ 
        status: 'accepted',
        acceptedBy: firebase.auth().currentUser.uid,
        donorName: window.currentUserData.name,
        donorPhone: window.currentUserData.phone,
        acceptedAt: firebase.firestore.FieldValue.serverTimestamp()
      });
      
      // Alert donor with patient details
      alert(`Shukriya! Aap ne madad ka waada kiya.\\n\\nPatient: ${pName}\\nPhone: ${pPhone}\\n\\nBaraye meharbani foran rabta karein.`);
      
      // Owner alert link for donor
      const waText = encodeURIComponent(`✅ *DONOR ACCEPTED* ✅\\n\\nDonor: ${window.currentUserData.name}\\nPhone: ${window.currentUserData.phone}\\nPatient: ${pName}\\n\\nMain hospital ja raha hoon.`);
      const waOwnerLink = `https://wa.me/923016631720?text=${waText}`;
      
      // Show Owner Alert option
      if(confirm("Owner ko WhatsApp par alert bhejein taake unhe pata chale aap ja rahe hain?")) {
        window.open(waOwnerLink, '_blank');
      }

      closeDonorReqModal();
      checkForRequests(); // Refresh dot
    } catch (e) {
      alert("Error: " + e.message);
    }
  };"""
h = h.replace(old_accept, new_accept)

with open('index.html', 'w', encoding='utf-8') as f:
    f.write(h)

print("Done")
