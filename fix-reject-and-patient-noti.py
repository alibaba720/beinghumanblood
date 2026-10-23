with open('index.html', 'r', encoding='utf-8') as f:
    index = f.read()

with open('admin.html', 'r', encoding='utf-8') as f:
    admin = f.read()

# ==========================================
# 1. INDEX.HTML FIXES (Donor Reject + Patient Noti + Waiting Screen)
# ==========================================

# 1a. Update Donor UI to add Reject Button
old_donor_btn = """<button onclick="acceptRequest('${r.id}', '${r.patientName}', '${r.patientPhone}')" style="width:100%;padding:10px;background:#27ae60;color:white;border:none;border-radius:8px;font-weight:bold;cursor:pointer;">✅ Accept Request</button>"""
new_donor_btn = """<div style="display:flex; gap:10px; margin-top:10px;">
          <button onclick="acceptRequest('${r.id}', '${r.patientName}', '${r.patientPhone}')" style="flex:1;padding:10px;background:#27ae60;color:white;border:none;border-radius:8px;font-weight:bold;cursor:pointer;">✅ Accept</button>
          <button onclick="rejectRequest('${r.id}')" style="flex:1;padding:10px;background:#e74c3c;color:white;border:none;border-radius:8px;font-weight:bold;cursor:pointer;">❌ Reject</button>
        </div>"""
if old_donor_btn in index:
    index = index.replace(old_donor_btn, new_donor_btn)

# 1b. Add Reject Logic in JS
reject_js = """
  window.rejectRequest = async function(reqId) {
    if(!confirm("Kya aap waqai is request ko reject karna chahte hain? (Patient ko aap ka number nahi jayega)")) return;
    try {
      await db.collection('requests').doc(reqId).update({ 
        status: 'rejected',
        rejectedBy: window.currentUserData ? window.currentUserData.name : 'Donor',
        rejectedAt: firebase.firestore.FieldValue.serverTimestamp()
      });
      alert("Request Rejected. Shukriya.");
      closeDonorReqModal();
      checkForRequests();
    } catch(e) {
      alert("Error: " + e.message);
    }
  };
"""
if "window.rejectRequest =" not in index:
    index = index.replace('window.acceptRequest = async function', reject_js + '\n  window.acceptRequest = async function')

# 1c. Update Patient Waiting Screen UI
old_waiting = """    <div id="waitingBox" style="display:none; text-align:center; padding:20px;">
      <div style="font-size:30px; margin-bottom:10px;">⏳</div>
      <h3 style="color:#8B0000; margin-bottom:5px;">Waiting for Donor...</h3>
      <p style="font-size:12px;color:#666;">Jab koi donor accept karega, uski details yahan aapko mil jayengi. Is page ko band na karein.</p>
    </div>"""
new_waiting = """    <div id="waitingBox" style="display:none; text-align:center; padding:20px;">
      <div style="font-size:40px; margin-bottom:10px;">⏳</div>
      <h3 style="color:#8B0000; margin-bottom:10px; font-size:18px;">Thora Intzar Karein...</h3>
      <p style="font-size:14px;color:#444; line-height:1.6; margin-bottom:15px;">Aapki request donors ko bhej di gayi hai. Madad aa rahi hai. Aap is page ko band kar sakte hain, hum aapko notification bhejenge.</p>
      <div style="background:#fff5e0; padding:15px; border-radius:10px; border:1px dashed #f39c12;">
        <p style="font-size:13px; color:#8B0000; font-weight:bold; margin-bottom:5px;">Zyada urgent hai?</p>
        <p style="font-size:12px; color:#666; margin-bottom:10px;">Owner se foran rabta karein</p>
        <a href="https://wa.me/923016631720?text=Salam,%20mujhe%20URGENT%20blood%20chahiye." target="_blank" style="display:inline-block; background:#25D366; color:white; padding:10px 20px; border-radius:8px; text-decoration:none; font-weight:bold; font-size:14px;">📱 WhatsApp Owner</a>
      </div>
    </div>"""
if old_waiting in index:
    index = index.replace(old_waiting, new_waiting)

# 1d. Update submitReq to request FCM token for patient & save in request
old_submit = """      // 1. Save to Firestore
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
      });"""
new_submit = """      // Try getting FCM token for Patient
      let patientToken = "";
      try {
        if ('serviceWorker' in navigator && 'PushManager' in window && Notification.permission === 'granted') {
           const reg = await navigator.serviceWorker.register('/firebase-messaging-sw.js');
           const msg = firebase.messaging();
           patientToken = await msg.getToken({ vapidKey: "BKajJKv3dIDBFvOdrVIPGug4O5ITYBs_kDaKW9Y_IPrKe1L2XcmDITqY--LaKBydvkppKc52JGTjQGSxrSyagcA", serviceWorkerRegistration: reg });
        } else if ('Notification' in window && Notification.permission !== 'denied') {
           await Notification.requestPermission();
        }
      } catch(e) { console.log("Patient token error: ", e); }

      // 1. Save to Firestore
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
        patientFcmToken: patientToken || "",
        createdAt: firebase.firestore.FieldValue.serverTimestamp()
      });"""
if old_submit in index:
    index = index.replace(old_submit, new_submit)

# 1e. Send notification to Patient when Donor accepts
old_accept_alert = """      // Alert donor with patient details
      alert(`Shukriya! Aap ne madad ka waada kiya.\\n\\nPatient: ${pName}\\nPhone: ${pPhone}\\n\\nBaraye meharbani foran rabta karein.`);"""
new_accept_alert = """      // Send Push Notification to Patient
      try {
        const reqDoc = await db.collection('requests').doc(reqId).get();
        if (reqDoc.exists && reqDoc.data().patientFcmToken) {
          fetch('/api/send-notification', {
            method: 'POST',
            headers: { 'Content-Type': 'application/json' },
            body: JSON.stringify({
              token: reqDoc.data().patientFcmToken,
              title: '✅ Donor Mil Gaya!',
              body: `Donor: ${window.currentUserData.name}, Phone: ${window.currentUserData.phone}. Wo aapki madad ke liye nikal chuke hain.`
            })
          }).catch(e => console.log(e));
        }
      } catch(e) { console.log(e); }

      // Alert donor with patient details
      alert(`Shukriya! Aap ne madad ka waada kiya.\\n\\nPatient: ${pName}\\nPhone: ${pPhone}\\n\\nBaraye meharbani foran rabta karein.`);"""
if old_accept_alert in index:
    index = index.replace(old_accept_alert, new_accept_alert)


# ==========================================
# 2. ADMIN.HTML FIXES (Show Rejected)
# ==========================================
old_admin_req = """              ${isAccepted ? `
                <div class="donor-box">
                  <b>✅ Donor Accepted:</b><br>
                  Name: ${r.donorName}<br>
                  Phone: <a href="tel:${r.donorPhone}">${r.donorPhone}</a>
                </div>
              ` : '<div style="font-size:11px;color:#999;margin-top:8px;">Waiting for donor to accept...</div>'}"""
new_admin_req = """              ${isAccepted ? `
                <div class="donor-box">
                  <b>✅ Donor Accepted:</b><br>
                  Name: ${r.donorName}<br>
                  Phone: <a href="tel:${r.donorPhone}">${r.donorPhone}</a>
                </div>
              ` : r.status === 'rejected' ? `
                <div class="donor-box" style="background:#f8d7da; border-color:#e74c3c; color:#721c24;">
                  <b>❌ Request Rejected By:</b> ${r.rejectedBy || 'Donor'}
                </div>
              ` : '<div style="font-size:11px;color:#999;margin-top:8px;">Waiting for donor to accept...</div>'}"""
if old_admin_req in admin:
    admin = admin.replace(old_admin_req, new_admin_req)

with open('index.html', 'w', encoding='utf-8') as f:
    f.write(index)
with open('admin.html', 'w', encoding='utf-8') as f:
    f.write(admin)

print("Done: Reject button, patient waiting UI, patient FCM noti, and admin view fixed.")
