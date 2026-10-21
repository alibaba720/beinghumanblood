import re

# 1. Extract API key from profile.html
with open('profile.html', 'r', encoding='utf-8') as f:
    prof = f.read()

match = re.search(r'upload\?key=([a-zA-Z0-9]+)', prof)
if match:
    api_key = match.group(1)
else:
    api_key = input("API Key profile.html se nahi mili. Apni ImgBB key yahan paste karein: ").strip()

# 2. Update login.html
with open('login.html', 'r', encoding='utf-8') as f:
    login = f.read()

# Add DP UI inside signup section
dp_html = """
        <!-- SIGNUP DP -->
        <div style="text-align:center; margin-bottom: 15px;">
          <div style="position:relative; display:inline-block;">
            <img id="signupDPPreview" src="https://cdn-icons-png.flaticon.com/512/149/149071.png" style="width:80px; height:80px; border-radius:50%; object-fit:cover; border:3px solid #8B0000;">
            <label for="signupDPInput" style="position:absolute; bottom:0; right:0; background:#8B0000; color:white; width:28px; height:28px; border-radius:50%; display:flex; align-items:center; justify-content:center; cursor:pointer; border:2px solid white; font-size:12px;">📷</label>
            <input type="file" id="signupDPInput" accept="image/*" style="display:none" onchange="uploadSignupDP(this)">
          </div>
          <p style="font-size:11px; color:#888; margin-top:5px;">Profile Photo (Optional)</p>
        </div>
"""
if 'id="signupDPPreview"' not in login:
    login = login.replace('<label>Poora Naam *</label>', dp_html + '\n        <label>Poora Naam *</label>')

# Add JS upload function
js_code = f"""
  window.signupDP_Url = "";
  window.uploadSignupDP = async function(input) {{
    if (!input.files || !input.files[0]) return;
    const file = input.files[0];
    const formData = new FormData();
    formData.append('image', file);
    
    const preview = document.getElementById('signupDPPreview');
    if(preview) preview.style.opacity = '0.5';
    
    try {{
      const res = await fetch('https://api.imgbb.com/1/upload?key={api_key}', {{
        method: 'POST',
        body: formData
      }});
      const data = await res.json();
      if (data.success) {{
        window.signupDP_Url = data.data.url;
        if(preview) preview.src = window.signupDP_Url;
        alert("✅ Photo upload ho gayi!");
      }} else {{
        alert("Upload error: " + (data.error ? data.error.message : 'Unknown error'));
      }}
    }} catch(e) {{
      alert("Network error: " + e.message);
    }}
    if(preview) preview.style.opacity = '1';
  }};
"""
if 'uploadSignupDP' not in login:
    login = login.replace('window.signup = async function() {', js_code + '\n  window.signup = async function() {')

# Update Firestore Save logic to include DP
old_users_save = """        await db.collection('users').doc(uid).set({
          name, email, city, blood, phone, role, uid,"""
new_users_save = """        await db.collection('users').doc(uid).set({
          name, email, city, blood, phone, role, uid,
          dpUrl: window.signupDP_Url || "","""
login = login.replace(old_users_save, new_users_save)

old_donors_save = """        await db.collection('donors').doc(uid).set({
          name, city, blood, phone, uid, role,"""
new_donors_save = """        await db.collection('donors').doc(uid).set({
          name, city, blood, phone, uid, role,
          dpUrl: window.signupDP_Url || "","""
login = login.replace(old_donors_save, new_donors_save)

# Clear DP after signup
old_clear = "['su_name','su_phone','su_pass','su_city','su_blood','su_email'].forEach(id => document.getElementById(id).value = '');"
new_clear = """['su_name','su_phone','su_pass','su_city','su_blood','su_email'].forEach(id => document.getElementById(id).value = '');
        window.signupDP_Url = "";
        document.getElementById('signupDPPreview').src = 'https://cdn-icons-png.flaticon.com/512/149/149071.png';"""
login = login.replace(old_clear, new_clear)

with open('login.html', 'w', encoding='utf-8') as f:
    f.write(login)

print("Done: Signup DP added")
