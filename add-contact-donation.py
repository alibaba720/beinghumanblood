with open('index.html', 'r', encoding='utf-8') as f:
    h = f.read()

# 1. Add CSS for Donation and Contact
new_css = """
/* DONATION SECTION */
.donation-box {
  background: linear-gradient(135deg, #fff, #fdf4ea);
  border: 2px dashed #FFD700;
  border-radius: 16px;
  padding: 30px 20px;
  text-align: center;
  box-shadow: 0 4px 15px rgba(0,0,0,0.05);
}
.donation-box h2 { color: #8B0000; font-size: 22px; margin-bottom: 10px; }
.donation-box p { font-size: 14px; color: #666; margin-bottom: 15px; line-height: 1.6; }
.donation-badge {
  display: inline-block;
  background: #FFD700;
  color: #5a0000;
  padding: 8px 20px;
  border-radius: 20px;
  font-weight: 800;
  font-size: 12px;
  text-transform: uppercase;
  letter-spacing: 1px;
}

/* CONTACT SECTION */
.contact-box {
  background: white;
  border-radius: 16px;
  padding: 25px 20px;
  box-shadow: 0 4px 15px rgba(0,0,0,0.05);
}
.contact-box label {
  display: block; margin-bottom: 5px; font-weight: 600; font-size: 13px; color: #333;
}
.contact-box input, .contact-box textarea {
  width: 100%; padding: 12px; margin-bottom: 15px; border: 2px solid #eee; border-radius: 8px; font-size: 14px; font-family: inherit;
}
.contact-box input:focus, .contact-box textarea:focus {
  outline: none; border-color: #8B0000;
}
.contact-box button {
  width: 100%; padding: 14px; background: #8B0000; color: white; border: none; border-radius: 8px; font-weight: bold; font-size: 15px; cursor: pointer;
}
</style>
"""
if "/* DONATION SECTION */" not in h:
    h = h.replace('</style>', new_css)

# 2. Add HTML Sections before Footer
new_html = """
<!-- DONATION SECTION -->
<section class="section">
  <div class="donation-box">
    <div style="font-size: 40px; margin-bottom: 10px;">💖</div>
    <h2>BeingHuman Foundation</h2>
    <p>InshaAllah hum jald hi ghareeb mareezon aur ambulance ki madad ke liye donation system shuru kar rahe hain taake kisi ki jaan paison ki wajah se na jaye.</p>
    <div class="donation-badge">Coming Soon</div>
  </div>
</section>

<!-- CONTACT SECTION -->
<section class="section">
  <div class="section-head">
    <h2 class="section-title">📬 Contact Us</h2>
    <p class="section-sub">Koi sawal ya mashwara hai? Humse rabta karein.</p>
  </div>
  <div class="contact-box">
    <label>Apka Naam *</label>
    <input type="text" id="ctName" placeholder="Ahmed Khan">
    
    <label>WhatsApp Number *</label>
    <input type="tel" id="ctPhone" placeholder="03xxxxxxxxx">
    
    <label>Apna Message likhein *</label>
    <textarea id="ctMessage" rows="4" placeholder="Apna sawal ya mashwara yahan likhein..."></textarea>
    
    <button onclick="submitContact()" id="ctBtn">Send Message</button>
  </div>
</section>

<!-- FOOTER -->"""

if "<!-- DONATION SECTION -->" not in h:
    h = h.replace('<!-- FOOTER -->', new_html)

# 3. Add JS Logic for Contact Form
new_js = """
  // ==========================================
  // CONTACT FORM LOGIC
  // ==========================================
  window.submitContact = async function() {
    const name = document.getElementById('ctName').value.trim();
    const phone = document.getElementById('ctPhone').value.trim();
    const message = document.getElementById('ctMessage').value.trim();
    const btn = document.getElementById('ctBtn');

    if (!name || !phone || !message) {
      alert("Baraye meharbani saare fields bharein!");
      return;
    }

    btn.disabled = true;
    btn.textContent = 'Sending...';

    try {
      // Save to Firestore
      await db.collection('messages').add({
        name: name,
        phone: phone,
        message: message,
        createdAt: firebase.firestore.FieldValue.serverTimestamp()
      });

      // Prepare WhatsApp message for Owner
      const waText = encodeURIComponent(`📬 *Naya Message (BeingHuman Blood)*\\n\\nNaam: ${name}\\nPhone: ${phone}\\n\\nMessage: ${message}`);
      const waLink = `https://wa.me/923016631720?text=${waText}`;
      
      alert("✅ Message Owner ko bhej diya gaya hai!");
      
      // Open WhatsApp
      window.open(waLink, '_blank');

      // Clear form
      document.getElementById('ctName').value = '';
      document.getElementById('ctPhone').value = '';
      document.getElementById('ctMessage').value = '';

    } catch (e) {
      alert("Error: " + e.message);
    }

    btn.disabled = false;
    btn.textContent = 'Send Message';
  };
"""

if "window.submitContact" not in h:
    h = h.replace('window.openReqModal = function(blood, city) {', new_js + '\n\n  window.openReqModal = function(blood, city) {')

with open('index.html', 'w', encoding='utf-8') as f:
    f.write(h)

print("Done: Donation and Contact sections added.")
