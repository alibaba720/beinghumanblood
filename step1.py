with open('login.html', 'r', encoding='utf-8') as f:
    h = f.read()

old = '<label>Email <span class="optional">(optional)</span></label>'
new = '''<label>Secret Question *</label>
<select id="su_secret_q">
<option value="">-- Select --</option>
<option value="Aapki Ammi ka naam?">Aapki Ammi ka naam?</option>
<option value="Aapki pehli school ka naam?">Aapki pehli school ka naam?</option>
</select>
<label>Secret Answer *</label>
<input type="text" id="su_secret_a" placeholder="Apna jawab likhein">
<label>Email <span class="optional">(optional)</span></label>'''

if old in h and 'su_secret_q' not in h:
    h = h.replace(old, new)
    with open('login.html', 'w', encoding='utf-8') as f:
        f.write(h)
    print("Done 1: Secret Question fields added.")
else:
    print("Error: Target not found or already added.")
