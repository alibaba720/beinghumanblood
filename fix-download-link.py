with open('index.html', 'r', encoding='utf-8') as f:
    h = f.read()

# Old link (which shows virus scan warning)
old_link = "https://drive.google.com/uc?export=download&id=1aO86NQHZ8xtqdk2jSUWMyllFltM3PkeB"

# New link (bypasses the warning and downloads directly)
new_link = "https://drive.google.com/uc?export=download&confirm=t&id=1aO86NQHZ8xtqdk2jSUWMyllFltM3PkeB"

# Replace in the download button and floating button
h = h.replace(old_link, new_link)

# Update the instruction text inside the download section
old_instruction = """  <div class="dl-instructions">
    <b>Installation Guide:</b><br>
    1. Download the APK file.<br>
    2. Open the file and click "Install".<br>
    3. If a warning appears, go to Settings and enable <b>"Allow from this source"</b>.<br>
    4. Open the app and enjoy!
  </div>"""

new_instruction = """  <div class="dl-instructions">
    <b>Installation Guide:</b><br>
    1. Click the download button above.<br>
    2. <b>Agar Google Drive ka warning page aaye, to "Download anyway" par click karein.</b><br>
    3. Open the downloaded file and click "Install".<br>
    4. If a security warning appears, go to Settings and enable <b>"Allow from this source"</b>.<br>
    5. Open the app and enjoy!
  </div>"""

if old_instruction in h:
    h = h.replace(old_instruction, new_instruction)

with open('index.html', 'w', encoding='utf-8') as f:
    f.write(h)

print("Done: Download link updated to bypass warning & instructions added.")
