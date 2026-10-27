import re

# Extracted Google Drive File ID
FILE_ID = "1aO86NQHZ8xtqdk2jSUWMyllFltM3PkeB"
DIRECT_LINK = f"https://drive.google.com/uc?export=download&id={FILE_ID}"

with open('index.html', 'r', encoding='utf-8') as f:
    h = f.read()

# 1. Add CSS for the download section
css_code = """
/* DOWNLOAD SECTION */
.download-section {
  background: linear-gradient(135deg, #fff8e1, #ffecb3);
  border: 2px solid #FFD700;
  border-radius: 16px;
  padding: 25px 20px;
  text-align: center;
  margin: 20px 18px;
  box-shadow: 0 4px 15px rgba(0,0,0,0.1);
}
.download-section h2 { color: #8B0000; font-size: 22px; margin-bottom: 10px; }
.download-section p { font-size: 14px; color: #555; margin-bottom: 15px; line-height: 1.6; }
.dl-btn {
  display: inline-block;
  background: linear-gradient(135deg, #8B0000, #c0392b);
  color: white !important;
  padding: 15px 30px;
  border-radius: 30px;
  font-size: 16px;
  font-weight: 800;
  text-decoration: none;
  box-shadow: 0 5px 15px rgba(139,0,0,0.3);
  margin-bottom: 15px;
  width: 100%;
  max-width: 300px;
  transition: transform 0.2s;
}
.dl-btn:active { transform: scale(0.95); }
.dl-instructions {
  background: white;
  border-radius: 10px;
  padding: 15px;
  text-align: left;
  font-size: 13px;
  color: #444;
  margin-top: 15px;
  border-left: 4px solid #f39c12;
}
"""

if '.download-section {' not in h:
    h = h.replace('</style>', css_code + '\n</style>')

# 2. Add HTML for the download section (before footer)
download_html = f"""
<!-- DOWNLOAD APK SECTION -->
<section class="download-section">
  <h2>📱 Download BeingHuman App</h2>
  <p>Get the official Android app for a faster and better experience. Bilkul free!</p>
  
  <a href="{DIRECT_LINK}" class="dl-btn" target="_blank">📥 Download APK Now</a>
  
  <div class="dl-instructions">
    <b>Installation Guide:</b><br>
    1. Download the APK file.<br>
    2. Open the file and click "Install".<br>
    3. If a warning appears, go to Settings and enable <b>"Allow from this source"</b>.<br>
    4. Open the app and enjoy!
  </div>
</section>

<!-- FOOTER -->"""

if 'id="download-apk-section"' not in h:
    # Add an ID to the section for future reference
    download_html = download_html.replace('<section class="download-section">', '<section class="download-section" id="download-apk-section">')
    h = h.replace('<!-- FOOTER -->', download_html)

# 3. Add a small download link in the header (optional but good)
# We'll add it as a floating button at the bottom for easy access
floating_btn = f"""
<a href="{DIRECT_LINK}" target="_blank" style="position:fixed; bottom:20px; right:20px; background:#27ae60; color:white; padding:12px 20px; border-radius:30px; font-weight:bold; text-decoration:none; box-shadow:0 4px 15px rgba(0,0,0,0.3); z-index:9999; display:flex; align-items:center; gap:8px; font-size:14px;">
  📥 Download App
</a>
"""
if 'position:fixed; bottom:20px; right:20px' not in h:
    h = h.replace('</body>', floating_btn + '\n</body>')

with open('index.html', 'w', encoding='utf-8') as f:
    f.write(h)

print("Done: Download section and floating button added successfully!")
