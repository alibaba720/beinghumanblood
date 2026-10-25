import re

# --- FIX LOGIN.HTML ---
with open('login.html', 'r', encoding='utf-8') as f:
    login_code = f.read()

# Replace the entire onAuthStateChanged block to force redirect
new_auth_code = """
auth.onAuthStateChanged(async function(user) {
    if (user) {
        window.location.href = 'index.html';
        return;
    } else {
        document.getElementById('mainTabs').style.display = 'flex';
        document.getElementById('welcome').style.display = 'none';
        document.getElementById('welcome').classList.remove('show');
        document.getElementById('signup').classList.add('active');
        document.getElementById('login').classList.remove('active');
        document.getElementById('tabSignup').classList.add('active');
        document.getElementById('tabLogin').classList.remove('active');
        document.getElementById('loaderBox').style.display = 'none';
        document.getElementById('appBox').style.display = 'block';
    }
});
"""
login_code = re.sub(r"auth\.onAuthStateChanged\(async function\(user\) \{.*?\n  \}\);", new_auth_code, login_code, flags=re.DOTALL)

with open('login.html', 'w', encoding='utf-8') as f:
    f.write(login_code)


# --- FIX PROFILE.HTML ---
with open('profile.html', 'r', encoding='utf-8') as f:
    profile_code = f.read()

# Remove all existing logout buttons
profile_code = re.sub(r'<button[^>]*onclick="firebase\.auth\(\)\.signOut\(\)[^>]*>Logout</button>', '', profile_code)

# Add exactly ONE logout button below "Wapas Jao"
target = '<button class="btn-secondary" onclick="goBack()">Wapas Jao</button>'
logout_btn = """
        <button class="btn-secondary" onclick="firebase.auth().signOut().then(function(){window.location.href='login.html';})" style="background:#f8d7da; color:#721c24; border-color:#f8d7da; margin-top:10px;">Logout</button>
    """
if target in profile_code:
    profile_code = profile_code.replace(target, target + "\n" + logout_btn)

with open('profile.html', 'w', encoding='utf-8') as f:
    f.write(profile_code)

print("Done!")
