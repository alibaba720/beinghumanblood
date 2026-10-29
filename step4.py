with open('login.html', 'r', encoding='utf-8') as f:
    h = f.read()

# 1. Add validation in signup function
old_validation = """    if (!name || !phoneRaw || !pass || !city || !blood) {
      return showMsg('su_msg', t.fillAll, 'error');
    }"""
    
new_validation = """    const secretQ = document.getElementById('su_secret_q').value;
    const secretA = document.getElementById('su_secret_a').value.trim();

    if (!name || !phoneRaw || !pass || !city || !blood || !secretQ || !secretA) {
      return showMsg('su_msg', 'Sab fields bharna zaroori hai (Secret Q/A ke sath)!', 'error');
    }"""

if old_validation in h:
    h = h.replace(old_validation, new_validation)

# 2. Save to users collection
old_users = """        await db.collection('users').doc(uid).set({
          name, phone, email: emailOpt || '', city, blood, role, uid, country: country,"""
          
new_users = """        await db.collection('users').doc(uid).set({
          name, phone, email: emailOpt || '', city, blood, role, uid, country: country,
          secretQuestion: secretQ, secretAnswer: secretA,"""

if old_users in h:
    h = h.replace(old_users, new_users)

# 3. Save to donors collection
old_donors = """        await db.collection('donors').doc(uid).set({
          name, phone, city, blood, role, uid, country: country,"""
          
new_donors = """        await db.collection('donors').doc(uid).set({
          name, phone, city, blood, role, uid, country: country,
          secretQuestion: secretQ, secretAnswer: secretA,"""

if old_donors in h:
    h = h.replace(old_donors, new_donors)

with open('login.html', 'w', encoding='utf-8') as f:
    f.write(h)
    print("Done 4: Signup logic updated to save Secret Q/A.")
