import re

with open('index.html', 'r', encoding='utf-8') as f:
    h = f.read()

# 1. Replace the HTML block to use data-i18n
new_html = """  <div class="dl-instructions">
    <b data-i18n="dlTitle">Installation Guide:</b><br>
    <span data-i18n="dlStep1">1. Click the download button above.</span><br>
    <span data-i18n="dlStep2">2. If Google Drive warning appears, click "Download anyway".</span><br>
    <span data-i18n="dlStep3">3. Open the downloaded file and click "Install".</span><br>
    <span data-i18n="dlStep4">4. If a security warning appears, enable "Allow from this source".</span><br>
    <span data-i18n="dlStep5">5. Open the app and enjoy!</span>
  </div>"""

# Try exact match first
old_html = """  <div class="dl-instructions">
    <b>Installation Guide:</b><br>
    1. Click the download button above.<br>
    2. <b>Agar Google Drive ka warning page aaye, to "Download anyway" par click karein.</b><br>
    3. Open the downloaded file and click "Install".<br>
    4. If a security warning appears, go to Settings and enable <b>"Allow from this source"</b>.<br>
    5. Open the app and enjoy!
  </div>"""

if old_html in h:
    h = h.replace(old_html, new_html)
else:
    # Fallback regex in case spacing is different
    h = re.sub(r'<div class="dl-instructions">.*?</div>', new_html, h, flags=re.DOTALL)

# 2. Add Translation Keys
en_keys = """    dlTitle: "Installation Guide:",
    dlStep1: "1. Click the download button above.",
    dlStep2: "2. If Google Drive warning appears, click 'Download anyway'.",
    dlStep3: "3. Open the downloaded file and click 'Install'.",
    dlStep4: "4. If a security warning appears, enable 'Allow from this source'.",
    dlStep5: "5. Open the app and enjoy!",
"""

rm_keys = """    dlTitle: "Installation Guide:",
    dlStep1: "1. Upar diye gaye download button par click karein.",
    dlStep2: "2. Agar Google Drive ka warning page aaye, to 'Download anyway' par click karein.",
    dlStep3: "3. Download shuda file ko open karein aur 'Install' par click karein.",
    dlStep4: "4. Agar security warning aaye, to Settings mein ja kar 'Allow from this source' enable karein.",
    dlStep5: "5. App open karein aur enjoy karein!",
"""

ur_keys = """    dlTitle: "انسٹالیشن گائیڈ:",
    dlStep1: "1. اوپر دیے گئے ڈاؤن لوڈ بٹن پر کلک کریں۔",
    dlStep2: "2. اگر گوگل ڈرائیو کا وارننگ پیج آئے تو 'Download anyway' پر کلک کریں۔",
    dlStep3: "3. ڈاؤن لوڈ شدہ فائل کو کھولیں اور 'Install' پر کلک کریں۔",
    dlStep4: "4. اگر سیکیورٹی وارننگ آئے تو سیٹنگز میں جا کر 'Allow from this source' کو فعال کریں۔",
    dlStep5: "5. ایپ کھولیں اور استعمال کریں!",
"""

if 'dlTitle: "Installation Guide:"' not in h:
    h = h.replace('    contactTitle: "Contact Us",', en_keys + '    contactTitle: "Contact Us",')

if 'dlTitle: "Installation Guide:",\n    dlStep1: "1. Upar' not in h:
    h = h.replace('    contactTitle: "Rabta Karein",', rm_keys + '    contactTitle: "Rabta Karein",')

if 'dlTitle: "انسٹالیشن گائیڈ:"' not in h:
    h = h.replace('    contactTitle: "رابطہ کریں",', ur_keys + '    contactTitle: "رابطہ کریں",')

with open('index.html', 'w', encoding='utf-8') as f:
    f.write(h)

print("Done: Download instructions now support all 3 languages!")
