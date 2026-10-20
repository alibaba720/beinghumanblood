with open('index.html', 'r', encoding='utf-8') as f:
    h = f.read()

# 1. Add Toast CSS
css_toast = """
/* TOAST NOTIFICATION */
#toastContainer {
  position: fixed;
  top: 20px;
  left: 50%;
  transform: translateX(-50%);
  z-index: 9999;
  display: flex;
  flex-direction: column;
  gap: 10px;
  width: 90%;
  max-width: 400px;
}
.toast-msg {
  background: linear-gradient(135deg, #27ae60, #2ecc71);
  color: white;
  padding: 15px 20px;
  border-radius: 12px;
  box-shadow: 0 10px 30px rgba(39,174,96,0.4);
  font-weight: 600;
  font-size: 14px;
  line-height: 1.5;
  display: flex;
  align-items: center;
  gap: 10px;
  animation: slideDown 0.4s cubic-bezier(0.68, -0.55, 0.265, 1.55);
  border: 2px solid rgba(255,255,255,0.2);
}
@keyframes slideDown {
  from { transform: translateY(-100%); opacity: 0; }
  to { transform: translateY(0); opacity: 1; }
}
@keyframes fadeOut {
  from { opacity: 1; transform: translateY(0); }
  to { opacity: 0; transform: translateY(-20px); }
}
.toast-msg .icon { font-size: 24px; }
"""
if "/* TOAST NOTIFICATION */" not in h:
    h = h.replace('/* MODALS */', css_toast + '\n/* MODALS */')

# 2. Add Toast Container to HTML
if '<div id="toastContainer"></div>' not in h:
    h = h.replace('<body class="lang-en">', '<body class="lang-en">\n<div id="toastContainer"></div>')

# 3. Add Translations
en_msg = '    otherAcceptedMsg: "Allah chose someone else for this noble deed this time. Perhaps next time, He will choose you. ❤️",\n'
rm_msg = '    otherAcceptedMsg: "Allah ne is baar ye naik kaam kisi aur ke zimme laga diya, shayad agli baari Allah ye zimmedari aapko de. ❤️",\n'
ur_msg = '    otherAcceptedMsg: "اللہ نے اس بار یہ نیک کام کسی اور کے ذمے لگا دیا، شاید اگلی بار اللہ یہ ذمہ داری آپ کو دے۔ ❤️",\n'

# Insert translations
if "otherAcceptedMsg" not in h:
    h = h.replace('    contactTitle: "Contact Us",', en_msg + '    contactTitle: "Contact Us",')
    h = h.replace('    contactTitle: "Rabta Karein",', rm_msg + '    contactTitle: "Rabta Karein",')
    h = h.replace('    contactTitle: "رابطہ کریں",', ur_msg + '    contactTitle: "رابطہ کریں",')

# 4. Add JS Logic to listen for accepted requests
js_logic = """
  // ==========================================
  // TOAST NOTIFICATIONS (OTHER DONORS)
  // ==========================================
  let shownToasts = [];
  
  function showToast(message) {
    const container = document.getElementById('toastContainer');
    const toast = document.createElement('div');
    toast.className = 'toast-msg';
    toast.innerHTML = `<span class="icon">🤲</span> <span>${message}</span>`;
    container.appendChild(toast);
    
    setTimeout(() => {
      toast.style.animation = 'fadeOut 0.4s forwards';
      setTimeout(() => toast.remove(), 400);
    }, 6000);
  }

  // Listen for any request being accepted
  db.collection('requests').onSnapshot(snapshot => {
    snapshot.docChanges().forEach(change => {
      if (change.type === 'modified') {
        const r = change.doc.data();
        if (r.status === 'accepted' && 
            firebase.auth().currentUser && 
            r.acceptedBy !== firebase.auth().currentUser.uid && 
            r.city === currentUserCity) {
          
          if (!shownToasts.includes(change.doc.id)) {
            shownToasts.push(change.doc.id);
            const t = translations[currentLang];
            showToast(t.otherAcceptedMsg || "Allah ne is baar ye naik kaam kisi aur ke zimme laga diya...");
          }
        }
      }
    });
  });
"""

if "showToast(message)" not in h:
    h = h.replace('window.openReqModal = function(blood, city) {', js_logic + '\n  window.openReqModal = function(blood, city) {')

with open('index.html', 'w', encoding='utf-8') as f:
    f.write(h)

print("Done")
