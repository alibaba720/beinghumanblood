import re

# 1. Update login.html
with open('login.html', 'r', encoding='utf-8') as f:
    login = f.read()

if 'function getCountryFromPhone' not in login:
    login = login.replace("function normalizePhone(p) {", """function getCountryFromPhone(rawPhone) {
        rawPhone = rawPhone.trim();
        if (rawPhone.startsWith('+')) {
            if (rawPhone.startsWith('+92')) return 'Pakistan';
            if (rawPhone.startsWith('+1')) return 'USA/Canada';
            if (rawPhone.startsWith('+44')) return 'UK';
            if (rawPhone.startsWith('+971')) return 'UAE';
            if (rawPhone.startsWith('+966')) return 'Saudi Arabia';
            if (rawPhone.startsWith('+61')) return 'Australia';
            if (rawPhone.startsWith('+91')) return 'India';
            return 'Other';
        }
        return 'Pakistan';
    }

    function normalizePhone(p) {""")

login = login.replace("const phone = normalizePhone(phoneRaw);", "const country = getCountryFromPhone(phoneRaw);\n    const phone = normalizePhone(phoneRaw);")
login = login.replace("name, phone, email: emailOpt || '', city, blood, role, uid,", "name, phone, email: emailOpt || '', city, blood, role, uid, country: country,")
login = login.replace("name, phone, city, blood, role, uid,", "name, phone, city, blood, role, uid, country: country,")
# Allow + sign in phone input
login = login.replace('placeholder="03001234567" maxlength="11"', 'placeholder="+923001234567" maxlength="15"')

with open('login.html', 'w', encoding='utf-8') as f:
    f.write(login)

# 2. Update index.html
with open('index.html', 'r', encoding='utf-8') as f:
    index = f.read()

if 'function getCountryFromPhone' not in index:
    index = index.replace("function waitForFirebase(cb, tries) {", """function getCountryFromPhone(rawPhone) {
        rawPhone = rawPhone.trim();
        if (rawPhone.startsWith('+')) {
            if (rawPhone.startsWith('+92')) return 'Pakistan';
            if (rawPhone.startsWith('+1')) return 'USA/Canada';
            if (rawPhone.startsWith('+44')) return 'UK';
            if (rawPhone.startsWith('+971')) return 'UAE';
            if (rawPhone.startsWith('+966')) return 'Saudi Arabia';
            return 'Other';
        }
        return 'Pakistan';
    }

    function waitForFirebase(cb, tries) {""")

old_stats = """  <div class="impact-grid">
    <div class="impact-item">
      <span class="impact-num" id="statDonors">0</span>
      <span class="impact-lbl" data-i18n="donorsLabel">Donors</span>
    </div>
    <div class="impact-item">
      <span class="impact-num" id="statCities">0</span>
      <span class="impact-lbl" data-i18n="citiesLabel">Cities</span>
    </div>
    <div class="impact-item">
      <span class="impact-num" id="statLives">0</span>
      <span class="impact-lbl" data-i18n="livesLabel">Lives Saved</span>
    </div>
    <div class="impact-item">
      <span class="impact-num" id="statPosts">0</span>
      <span class="impact-lbl" data-i18n="postsLabel">Stories</span>
    </div>
  </div>"""

new_stats = """  <div class="impact-grid">
    <div class="impact-item">
      <span class="impact-num" id="statDonors">0</span>
      <span class="impact-lbl" data-i18n="donorsLabel">Donors</span>
    </div>
    <div class="impact-item">
      <span class="impact-num" id="statCountries">0</span>
      <span class="impact-lbl">Countries</span>
    </div>
    <div class="impact-item">
      <span class="impact-num" id="statCities">0</span>
      <span class="impact-lbl" data-i18n="citiesLabel">Cities</span>
    </div>
    <div class="impact-item">
      <span class="impact-num" id="statLives">0</span>
      <span class="impact-lbl" data-i18n="livesLabel">Lives Saved</span>
    </div>
    <div class="impact-item" style="grid-column: span 2; border-right: none;">
      <span class="impact-num" id="statPosts">0</span>
      <span class="impact-lbl" data-i18n="postsLabel">Stories</span>
    </div>
  </div>"""
index = index.replace(old_stats, new_stats)

old_load_stats = """  async function loadStats() {
    try {
      const snap = await db.collection('donors').get();
      const cities = new Set();
      snap.forEach(doc => {
        const c = doc.data().city;
        if (c) cities.add(c.toLowerCase().trim());
      });
      document.getElementById('statDonors').textContent = snap.size;
      document.getElementById('statCities').textContent = cities.size;
      document.getElementById('statLives').textContent = Math.floor(snap.size / 4);
    } catch (e) { console.error(e); }
  }"""

new_load_stats = """  async function loadStats() {
    try {
      const snap = await db.collection('donors').get();
      const cities = new Set();
      const countries = new Set();
      snap.forEach(doc => {
        const data = doc.data();
        const c = data.city;
        if (c) cities.add(c.toLowerCase().trim());
        
        if (data.country) {
          countries.add(data.country);
        } else if (data.phone) {
          const raw = data.phone.startsWith('0') ? '+92' + data.phone.substring(1) : data.phone;
          countries.add(getCountryFromPhone(raw));
        }
      });
      document.getElementById('statDonors').textContent = snap.size;
      document.getElementById('statCities').textContent = cities.size;
      document.getElementById('statCountries').textContent = countries.size > 0 ? countries.size : 1;
      document.getElementById('statLives').textContent = Math.floor(snap.size / 4);
    } catch (e) { console.error(e); }
  }"""
index = index.replace(old_load_stats, new_load_stats)

old_css = """  @media (max-width: 700px) {
    .impact-grid { grid-template-columns: repeat(2, 1fr); padding: 20px 15px; }
    .impact-item { border-right: none; padding: 10px 5px; }
    .impact-item:nth-child(odd) { border-right: 1px solid #f0e8e0; }
    .impact-item:nth-child(1), .impact-item:nth-child(2) { border-bottom: 1px solid #f0e8e0; margin-bottom: 5px; }"""
new_css = """  @media (max-width: 700px) {
    .impact-grid { grid-template-columns: repeat(2, 1fr); padding: 20px 15px; }
    .impact-item { border-right: none; padding: 15px 5px; border-bottom: 1px solid #f0e8e0; }
    .impact-item:nth-child(odd) { border-right: 1px solid #f0e8e0; }
    .impact-item:nth-last-child(1) { border-bottom: none; }"""
index = index.replace(old_css, new_css)

with open('index.html', 'w', encoding='utf-8') as f:
    f.write(index)

print("Done: Country feature added successfully!")
