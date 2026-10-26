import re

with open('index.html', 'r', encoding='utf-8') as f:
    h = f.read()

# 1. Add Spinner HTML/CSS
if 'id="globalLoadingOverlay"' not in h:
    spinner_html = """
<div id="globalLoadingOverlay" style="display:none; position:fixed; top:0; left:0; width:100%; height:100%; background:rgba(255,255,255,0.95); z-index:999999; flex-direction:column; justify-content:center; align-items:center; backdrop-filter:blur(4px);">
    <div style="border: 6px solid #f3f3f3; border-top: 6px solid #8B0000; border-radius: 50%; width: 60px; height: 60px; animation: spin 1s linear infinite;"></div>
    <p style="margin-top:20px; color:#8B0000; font-weight:bold; font-size:18px;">Please wait processing...</p>
</div>
<style>
    @keyframes spin { 0% { transform: rotate(0deg); } 100% { transform: rotate(360deg); } }
</style>
"""
    h = h.replace('<body class="lang-en">', '<body class="lang-en">\n' + spinner_html)

# 2. Show Spinner on Submit
old_submit = """      btn.disabled = true;
      btn.textContent = 'Saving...';
      try {"""
new_submit = """      document.getElementById('globalLoadingOverlay').style.display = 'flex';
      btn.disabled = true;
      btn.textContent = 'Saving...';
      try {"""
        
if old_submit in h and "document.getElementById('globalLoadingOverlay').style.display = 'flex';" not in h:
    h = h.replace(old_submit, new_submit)

# 3. Hide Spinner and Auto-Scroll after save
old_wait_box = """      // Show Waiting Box
      document.getElementById('waitingBox').style.display = 'block';
      document.getElementById('donorFoundBox').style.display = 'none';"""
    
new_wait_box = """      // Show Waiting Box
      document.getElementById('waitingBox').style.display = 'block';
      document.getElementById('donorFoundBox').style.display = 'none';
      
      // Hide Spinner
      document.getElementById('globalLoadingOverlay').style.display = 'none';
      
      // Auto scroll to waiting box
      setTimeout(function() {
        document.getElementById('waitingBox').scrollIntoView({ behavior: 'smooth', block: 'center' });
      }, 400);"""
      
if old_wait_box in h and "scrollIntoView" not in h:
    h = h.replace(old_wait_box, new_wait_box)

# 4. Hide Spinner on error
old_catch = """    } catch (e) {
      msgEl.textContent = 'Error: ' + e.message;"""
new_catch = """    } catch (e) {
      document.getElementById('globalLoadingOverlay').style.display = 'none';
      msgEl.textContent = 'Error: ' + e.message;"""
if old_catch in h:
    h = h.replace(old_catch, new_catch)

with open('index.html', 'w', encoding='utf-8') as f:
    f.write(h)

print("Done: Spinner and auto-scroll added successfully!")
