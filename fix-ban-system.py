import re

# 1. UPDATE ADMIN.HTML
with open('admin.html', 'r', encoding='utf-8') as f:
    admin = f.read()

# Add Ban option to dropdown
old_select = """<option value="admin">Make Admin</option>"""
new_select = """<option value="admin">Make Admin</option>
                    <option value="banned" style="color:#e74c3c; font-weight:bold;">Ban User (Cancel Reg)</option>"""
if old_select in admin and 'Ban User (Cancel Reg)' not in admin:
    admin = admin.replace(old_select, new_select)

# Update updateRole logic to handle Ban specifically
old_update_role = """      if (!confirm(`Kya aap waqai is user ka role change karke '${newRole}' karna chahte hain?`)) {"""
new_update_role = """      if (newRole === 'banned') {
        if (!confirm(`WARNING: Kya aap waqai is user ko BAN karna chahte hain? Wo dobara login nahi kar sakega.`)) return loadMembers();
      } else {
        if (!confirm(`Kya aap waqai is user ka role change karke '${newRole}' karna chahte hain?`)) return loadMembers();
      }"""
if old_update_role in admin:
    admin = admin.replace(old_update_role, new_update_role)

# Add CSS for banned role badge
if '.role-banned' not in admin:
    admin = admin.replace('.role-donor {', '.role-banned { background: #333; color: white; }\n  .role-donor {')

with open('admin.html', 'w', encoding='utf-8') as f:
    f.write(admin)


# 2. UPDATE LOGIN.HTML
with open('login.html', 'r', encoding='utf-8') as f:
    login = f.read()

# Update login function to check for ban
old_login_try = """      const fakeEmail = phone + '@beinghumanblood.app';
      await auth.signInWithEmailAndPassword(fakeEmail, pass);"""
new_login_try = """      const fakeEmail = phone + '@beinghumanblood.app';
      const userCred = await auth.signInWithEmailAndPassword(fakeEmail, pass);
      
      // Check if banned
      const doc = await db.collection('users').doc(userCred.user.uid).get();
      if (doc.exists && doc.data().role === 'banned') {
        await auth.signOut();
        showMsg('li_msg', 'Aapka account ban kar diya gaya hai. Baraye meharbani admin se rabta karein.', 'error');
        btn.disabled = false;
        btn.textContent = 'Login Karo';
        return;
      }"""
if old_login_try in login:
    login = login.replace(old_login_try, new_login_try)

# Update onAuthStateChanged to prevent auto-login if banned
old_auth_state = """auth.onAuthStateChanged(async function(user) {
    if (user) {
        window.location.href = 'index.html';
        return;"""
new_auth_state = """auth.onAuthStateChanged(async function(user) {
    if (user) {
        const doc = await db.collection('users').doc(user.uid).get();
        if (doc.exists && doc.data().role === 'banned') {
            await auth.signOut();
            window.location.reload();
            return;
        }
        window.location.href = 'index.html';
        return;"""
if old_auth_state in login:
    login = login.replace(old_auth_state, new_auth_state)

with open('login.html', 'w', encoding='utf-8') as f:
    f.write(login)


# 3. UPDATE INDEX.HTML
with open('index.html', 'r', encoding='utf-8') as f:
    index = f.read()

# Update auth state to kick out banned users
old_index_auth = """      const doc = await db.collection('users').doc(user.uid).get();
      if (doc.exists) {
        const d = doc.data();"""
new_index_auth = """      const doc = await db.collection('users').doc(user.uid).get();
      if (doc.exists) {
        const d = doc.data();
        if (d.role === 'banned') {
          await auth.signOut();
          window.location.href = 'login.html';
          return;
        }"""
if old_index_auth in index and "if (d.role === 'banned')" not in index:
    index = index.replace(old_index_auth, new_index_auth)

with open('index.html', 'w', encoding='utf-8') as f:
    f.write(index)

print("Done: Ban System Added Successfully!")
