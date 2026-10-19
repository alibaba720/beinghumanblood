import os

# 1. Rename files so Homepage becomes the main entry point
if os.path.exists('index.html') and not os.path.exists('login.html'):
    os.rename('index.html', 'login.html')
if os.path.exists('home.html') and not os.path.exists('index.html'):
    os.rename('home.html', 'index.html')

# 2. Fix Login Page (login.html)
with open('login.html', 'r', encoding='utf-8') as f: login_code = f.read()
# Save city in lowercase during signup
login_code = login_code.replace(
    "const city = document.getElementById('su_city').value.trim();", 
    "const city = document.getElementById('su_city').value.trim().toLowerCase();"
)
# Redirect to index.html after login
login_code = login_code.replace("window.location.href = 'home.html';", "window.location.href = 'index.html';")
with open('login.html', 'w', encoding='utf-8') as f: f.write(login_code)

# 3. Fix Homepage (index.html)
with open('index.html', 'r', encoding='utf-8') as f: home_code = f.read()
# Make search lowercase
home_code = home_code.replace(
    "const city = document.getElementById('searchCity').value.trim();", 
    "const city = document.getElementById('searchCity').value.trim().toLowerCase();"
)

# Allow public access (remove forced login redirect) & show Login button if not logged in
old_auth_block = """auth.onAuthStateChanged(async function(user) {
    if (!user) { window.location.href = 'index.html'; return; }
    try {
      const doc = await db.collection('users').doc(user.uid).get();
      if (doc.exists) {
        const d = doc.data();
        document.getElementById('userName').textContent = (d.name || 'User').split(' ')[0];
        if (d.role === 'owner' || d.role === 'admin') {
          document.getElementById('founderName').textContent = d.name || 'Ali Hassan';
          document.getElementById('founderAvatar').textContent = (d.name || 'A').charAt(0).toUpperCase();
        }
      }
    } catch (e) { console.error(e); }
  });"""

new_auth_block = """auth.onAuthStateChanged(async function(user) {
    if (!user) { 
      document.getElementById('userName').textContent = 'Login';
      return; 
    }
    try {
      const doc = await db.collection('users').doc(user.uid).get();
      if (doc.exists) {
        const d = doc.data();
        document.getElementById('userName').textContent = (d.name || 'User').split(' ')[0];
        if (d.role === 'owner' || d.role === 'admin') {
          document.getElementById('founderName').textContent = d.name || 'Ali Hassan';
          document.getElementById('founderAvatar').textContent = (d.name || 'A').charAt(0).toUpperCase();
        }
      }
    } catch (e) { console.error(e); }
  });

  window.goToProfile = function() { 
    if (firebase.auth().currentUser) {
      window.location.href = 'profile.html'; 
    } else {
      window.location.href = 'login.html';
    }
  };"""
home_code = home_code.replace(old_auth_block, new_auth_block)
# Remove old goToProfile if it exists separately
home_code = home_code.replace("window.goToProfile = function() { window.location.href = 'profile.html'; };", "")

with open('index.html', 'w', encoding='utf-8') as f: f.write(home_code)

# 4. Fix Profile Page (profile.html)
with open('profile.html', 'r', encoding='utf-8') as f: profile_code = f.read()
profile_code = profile_code.replace("window.location.href = 'auth.html';", "window.location.href = 'login.html';")
profile_code = profile_code.replace("window.location.href = 'index.html';", "window.location.href = 'login.html';")
# Save city in lowercase during profile edit
profile_code = profile_code.replace(
    "const city = document.getElementById('p_city').value.trim();", 
    "const city = document.getElementById('p_city').value.trim().toLowerCase();"
)
# Update back button link to go to homepage
profile_code = profile_code.replace('<a href="auth.html" class="back">‹</a>', '<a href="index.html" class="back">‹</a>')
with open('profile.html', 'w', encoding='utf-8') as f: f.write(profile_code)

print("Done: Website structure fixed and lowercase city bug solved.")
