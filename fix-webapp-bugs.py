import os
import re

# 1. Fix login.html
if os.path.exists('login.html'):
    with open('login.html', 'r', encoding='utf-8') as f:
        h = f.read()

    # Add Spinner HTML/CSS
    if 'id="loadingOverlay"' not in h:
        spinner_html = """
        <!-- LOADING SPINNER -->
        <div id="loadingOverlay" style="display:none; position:fixed; top:0; left:0; width:100%; height:100%; background:rgba(255,255,255,0.9); z-index:9999; justify-content:center; align-items:center; flex-direction:column;">
          <div style="border: 6px solid #f3f3f3; border-top: 6px solid #8B0000; border-radius: 50%; width: 50px; height: 50px; animation: spin 1s linear infinite;"></div>
          <p style="margin-top:15px; color:#8B0000; font-weight:bold; font-size:16px;">Processing...</p>
        </div>
        <style>
          @keyframes spin { 0% { transform: rotate(0deg); } 100% { transform: rotate(360deg); } }
        </style>
        """
        h = h.replace('<body class="lang-en">', '<body class="lang-en">\n' + spinner_html)

    # Update Signup Logic
    if "loadingOverlay').style.display = 'flex'" not in h:
        h = h.replace("btn.disabled = true;\n      btn.textContent = t.signingUp;", "document.getElementById('loadingOverlay').style.display = 'flex';")
        h = h.replace("btn.disabled = false;\n    btn.textContent = t.createAccount;", "document.getElementById('loadingOverlay').style.display = 'none';\n    btn.disabled = false;")
        
        # Add redirect after signup
        if "setTimeout(() => { window.location.href = 'index.html'; }, 1500);" not in h:
            h = h.replace("['su_name','su_phone','su_pass','su_city','su_blood','su_email'].forEach(id => document.getElementById(id).value = '');", 
                          "['su_name','su_phone','su_pass','su_city','su_blood','su_email'].forEach(id => document.getElementById(id).value = '');\n      setTimeout(() => { window.location.href = 'index.html'; }, 1500);")

    # Update Login Logic
    if "btn.disabled = true;\n      btn.textContent = t.loggingIn;" in h:
        h = h.replace("btn.disabled = true;\n      btn.textContent = t.loggingIn;", "document.getElementById('loadingOverlay').style.display = 'flex';")
        h = h.replace("btn.disabled = false;\n        btn.textContent = t.loginBtn;", "document.getElementById('loadingOverlay').style.display = 'none';\n        btn.disabled = false;")

    # Remove Welcome Screen and Redirect Instantly
    old_auth_check = """    if (user) {
      try {
        const doc = await db.collection('users').doc(user.uid).get();
        if (doc.exists) {
          const d = doc.data();
          mainTabs.style.display = 'none';
          document.querySelectorAll('.section').forEach(s => s.classList.remove('active'));
          welcome.classList.add('show');
          document.getElementById('w_avatar').textContent = (d.name || 'U').charAt(0).toUpperCase();
          document.getElementById('w_name').textContent = d.name || 'User';
          document.getElementById('w_phone').textContent = d.phone || '';
          document.getElementById('w_city').textContent = d.city || '';
          document.getElementById('w_blood').textContent = d.blood || '';
          if (d.email) {
            document.getElementById('w_email').textContent = d.email;
            document.getElementById('w_email_row').style.display = 'block';
          } else {
            document.getElementById('w_email_row').style.display = 'none';
          }
          const roleEl = document.getElementById('w_role');
          roleEl.textContent = (d.role || 'donor').toUpperCase();
          roleEl.className = 'role-badge role-' + (d.role || 'donor');
        }
      } catch (e) { console.error(e); }
    } else {"""

    new_auth_check = """    if (user) {
      window.location.href = 'index.html';
      return;
    } else {"""
    
    if old_auth_check in h:
        h = h.replace(old_auth_check, new_auth_check)
    elif "if (user) {\n      window.location.href = 'index.html';" not in h:
        # Fallback regex if exact match fails
        h = re.sub(r"if \(user\) \{.*?\} else \{", new_auth_check, h, flags=re.DOTALL)

    # Fix Logout in login.html
    h = h.replace("window.logout = async function() { await auth.signOut(); location.reload(); };", "window.logout = async function() { await auth.signOut(); window.location.href='login.html'; };")

    with open('login.html', 'w', encoding='utf-8') as f:
        f.write(h)
    print("login.html updated.")

# 2. Fix index.html and profile.html logout
for file in ['index.html', 'profile.html']:
    if os.path.exists(file):
        with open(file, 'r', encoding='utf-8') as f:
            h = f.read()
        h = h.replace("await auth.signOut();\n        location.reload();", "await auth.signOut();\n        window.location.href='login.html';")
        h = h.replace("await auth.signOut(); location.reload();", "await auth.signOut(); window.location.href='login.html';")
        with open(file, 'w', encoding='utf-8') as f:
            f.write(h)
        print(file + " updated.")

print("All web bugs fixed.")
