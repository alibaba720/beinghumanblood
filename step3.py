with open('login.html', 'r', encoding='utf-8') as f:
    h = f.read()

html_code = """
<div class="modal-overlay" id="forgotModal" onclick="if(event.target===this)closeForgotModal()">
  <div class="modal" style="max-width: 400px; padding: 25px; border-radius: 16px;">
    <button class="modal-close" onclick="closeForgotModal()">✕</button>
    <h2 style="color:#8B0000; margin-bottom: 15px; font-size: 20px;">Reset Password</h2>
    <div id="fpStep1">
      <label>WhatsApp Number</label>
      <input type="tel" id="fp_phone" placeholder="03xxxxxxxxx" style="width:100%; padding:12px; margin-bottom:15px; border:2px solid #ead5c0; border-radius:8px;">
      <button onclick="getSecretQuestion()" style="width:100%; padding:12px; background:#8B0000; color:white; border:none; border-radius:8px; font-weight:bold;">Next</button>
      <div id="fp_msg1" style="color:red; font-size:13px; margin-top:10px; text-align:center;"></div>
    </div>
    <div id="fpStep2" style="display:none;">
      <p style="font-size:14px; margin-bottom:10px;"><b>Secret Question:</b> <span id="fp_question_text" style="color:#8B0000;"></span></p>
      <label>Secret Answer</label>
      <input type="text" id="fp_answer" placeholder="Answer" style="width:100%; padding:12px; margin-bottom:15px; border:2px solid #ead5c0; border-radius:8px;">
      <label>New Password</label>
      <input type="password" id="fp_newpass" placeholder="New Password (6+ chars)" style="width:100%; padding:12px; margin-bottom:15px; border:2px solid #ead5c0; border-radius:8px;">
      <button onclick="submitPasswordReset()" style="width:100%; padding:12px; background:#27ae60; color:white; border:none; border-radius:8px; font-weight:bold;">Reset Password</button>
      <div id="fp_msg2" style="color:red; font-size:13px; margin-top:10px; text-align:center;"></div>
    </div>
    <div style="text-align: center; margin-top: 20px; border-top: 1px solid #eee; padding-top: 15px;">
      <p style="font-size:12px; color:#666; margin-bottom:10px;">Secret answer bhool gaye? Owner se rabta karein.</p>
      <a href="https://wa.me/923016631720?text=Salam" target="_blank" style="display:inline-block; background:#25D366; color:white; padding:10px 20px; border-radius:8px; text-decoration:none; font-weight:bold; font-size:13px;">📱 WhatsApp Owner</a>
    </div>
  </div>
</div>
<script>
  let fp_uid = "";
  function openForgotModal() { document.getElementById('forgotModal').classList.add('show'); }
  function closeForgotModal() { document.getElementById('forgotModal').classList.remove('show'); }
  async function getSecretQuestion() {
      const phoneRaw = document.getElementById('fp_phone').value.trim();
      const msg = document.getElementById('fp_msg1');
      msg.textContent = "";
      if(!phoneRaw) { msg.textContent = "Number daalein!"; return; }
      let phone = phoneRaw.replace(/\\\\D/g, '');
      if(phone.startsWith('92') && phone.length === 12) phone = '0' + phone.substring(2);
      if(phone.length === 10 && phone.startsWith('3')) phone = '0' + phone;
      try {
        const snap = await db.collection('users').where('phone', '==', phone).limit(1).get();
        if(snap.empty) { msg.textContent = "Number registered nahi hai."; return; }
        const userData = snap.docs[0].data();
        fp_uid = snap.docs[0].id;
        if(!userData.secretQuestion) {
          msg.textContent = "Secret question set nahi tha. Owner se rabta karein.";
          return;
        }
        document.getElementById('fp_question_text').textContent = userData.secretQuestion;
        document.getElementById('fpStep1').style.display = 'none';
        document.getElementById('fpStep2').style.display = 'block';
      } catch(e) { msg.textContent = "Error: " + e.message; }
  }
  async function submitPasswordReset() {
      const answer = document.getElementById('fp_answer').value.trim().toLowerCase();
      const newPass = document.getElementById('fp_newpass').value;
      const msg = document.getElementById('fp_msg2');
      if(!answer || !newPass) { msg.textContent = "Sab fields bharein!"; return; }
      if(newPass.length < 6) { msg.textContent = "Password 6+ characters ka ho!"; return; }
      msg.style.color = "#f39c12";
      msg.textContent = "Processing...";
      try {
        const userDoc = await db.collection('users').doc(fp_uid).get();
        const userData = userDoc.data();
        if(!userData.secretAnswer || userData.secretAnswer.toLowerCase() !== answer) {
          msg.style.color = "red";
          msg.textContent = "Secret answer galat hai!";
          return;
        }
        const res = await fetch('/api/reset-password', {
          method: 'POST',
          headers: { 'Content-Type': 'application/json' },
          body: JSON.stringify({ uid: fp_uid, newPassword: newPass })
        });
        const data = await res.json();
        if(data.success) {
          msg.style.color = "green";
          msg.textContent = "✅ Password reset ho gaya!";
          setTimeout(() => { closeForgotModal(); location.reload(); }, 2000);
        } else {
          msg.style.color = "red";
          msg.textContent = "Error: " + data.error;
        }
      } catch(e) {
        msg.style.color = "red";
        msg.textContent = "API Error: " + e.message;
      }
  }
</script>
"""

if 'id="forgotModal"' not in h:
    h = h.replace('</body>', html_code + '\n</body>')
    with open('login.html', 'w', encoding='utf-8') as f:
        f.write(h)
    print("Done 3: Forgot Password Modal added.")
else:
    print("Error: Already added.")
