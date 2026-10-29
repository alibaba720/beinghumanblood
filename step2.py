with open('login.html', 'r', encoding='utf-8') as f:
    h = f.read()

old = '<button onclick="login()" id="li_btn">Login Karo</button>'
new = '''<button onclick="login()" id="li_btn">Login Karo</button>
<div style="text-align: center; margin-top: 15px;">
<a href="#" onclick="openForgotModal(); return false;" style="color: #8B0000; font-weight: bold; text-decoration: none; font-size: 14px;">Forgot Password?</a>
</div>'''

if old in h and 'openForgotModal' not in h:
    h = h.replace(old, new)
    with open('login.html', 'w', encoding='utf-8') as f:
        f.write(h)
    print("Done 2: Forgot Password link added.")
else:
    print("Error: Target not found or already added.")
