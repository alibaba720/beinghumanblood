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

# 2. FORCE show spinner at the start of submitReq
target_start = "window.submitReq = async function() {"
if target_start in h and "document.getElementById('globalLoadingOverlay').style.display = 'flex';" not in h:
    h = h.replace(target_start, target_start + "\n      document.getElementById('globalLoadingOverlay').style.display = 'flex';")

# 3. FORCE hide spinner and scroll when waiting box is shown
target_success = "document.getElementById('waitingBox').style.display = 'block';"
if target_success in h and "scrollIntoView" not in h:
    h = h.replace(target_success, """
      document.getElementById('waitingBox').style.display = 'block';
      document.getElementById('globalLoadingOverlay').style.display = 'none';
      setTimeout(function() {
        document.getElementById('waitingBox').scrollIntoView({ behavior: 'smooth', block: 'center' });
      }, 400);
    """)

# 4. FORCE hide spinner on error
target_error = "} catch (e) {\n      msgEl.textContent = 'Error: ' + e.message;"
if target_error in h:
    h = h.replace(target_error, "} catch (e) {\n      document.getElementById('globalLoadingOverlay').style.display = 'none';\n      msgEl.textContent = 'Error: ' + e.message;")

with open('index.html', 'w', encoding='utf-8') as f:
    f.write(h)

print("Done: Spinner fixed forcefully!")
