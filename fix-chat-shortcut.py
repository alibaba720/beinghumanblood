import os

# 1. Create manifest-chat.json
manifest_chat = """{
  "name": "BH Chats",
  "short_name": "BH Chats",
  "start_url": "index.html?openChat=true",
  "display": "standalone",
  "background_color": "#8B0000",
  "theme_color": "#8B0000",
  "icons": [
    {
      "src": "https://cdn-icons-png.flaticon.com/512/149/149071.png",
      "sizes": "512x512",
      "type": "image/png"
    }
  ]
}"""
with open('manifest-chat.json', 'w', encoding='utf-8') as f:
    f.write(manifest_chat)

# 2. Create install-chat.html
install_html = """<!DOCTYPE html>
<html lang="en">
<head>
  <meta charset="UTF-8">
  <meta name="viewport" content="width=device-width, initial-scale=1.0">
  <title>Install BH Chats</title>
  <link rel="manifest" href="manifest-chat.json">
  <style>
    body { font-family: 'Segoe UI', Arial, sans-serif; text-align: center; padding: 50px 20px; background: #f4f6f8; }
    .container { background: white; padding: 30px; border-radius: 15px; max-width: 400px; margin: 0 auto; box-shadow: 0 4px 15px rgba(0,0,0,0.1); }
    h1 { color: #8B0000; margin-bottom: 10px; }
    p { color: #666; margin-bottom: 25px; font-size: 15px; }
    button { padding: 15px 30px; font-size: 16px; background: #27ae60; color: white; border: none; border-radius: 10px; cursor: pointer; width: 100%; font-weight: bold; }
    button:disabled { background: #ccc; }
    .icon { font-size: 60px; margin-bottom: 15px; }
  </style>
</head>
<body>
  <div class="container">
    <div class="icon">💬</div>
    <h1>BH Chats</h1>
    <p>Install this shortcut to open the chat directly.</p>
    <button id="installBtn" style="display:none;">Install BH Chats</button>
    <p id="manualText" style="display:none; margin-top:15px; color:#e74c3c;">Agar button na dikhe, to apne browser ke menu (⋮) se <b>"Add to Home Screen"</b> par click karein.</p>
  </div>

  <script>
    let deferredPrompt;
    window.addEventListener('beforeinstallprompt', (e) => {
      e.preventDefault();
      deferredPrompt = e;
      document.getElementById('installBtn').style.display = 'block';
    });

    document.getElementById('installBtn').addEventListener('click', async () => {
      if (deferredPrompt) {
        deferredPrompt.prompt();
        const { outcome } = await deferredPrompt.userChoice;
        if (outcome === 'accepted') {
          alert("✅ BH Chats installed! Ab aap home screen par icon dekh sakte hain.");
          window.close();
        }
        deferredPrompt = null;
      }
    });

    setTimeout(() => {
      if (!deferredPrompt) {
        document.getElementById('manualText').style.display = 'block';
      }
    }, 2000);
  </script>
</body>
</html>"""
with open('install-chat.html', 'w', encoding='utf-8') as f:
    f.write(install_html)

# 3. Update index.html
with open('index.html', 'r', encoding='utf-8') as f:
    h = f.read()

# A. Change Install button to open the new page with correct text
old_btn = """<button onclick="installPWA()" style="width: 100%; text-align: left; padding: 12px 15px; background: none; border: none; border-bottom: 1px solid #eee; font-size: 14px; cursor: pointer; font-weight: bold; color: #333;">📲 Send to Desktop</button>"""
new_btn = """<button onclick="window.open('install-chat.html', '_blank')" style="width: 100%; text-align: left; padding: 12px 15px; background: none; border: none; border-bottom: 1px solid #eee; font-size: 14px; cursor: pointer; font-weight: bold; color: #333;">📲 Send to Desktop</button>"""

if old_btn in h:
    h = h.replace(old_btn, new_btn)

# B. Auto-open chat if ?openChat=true and hide main layout
old_load = """  auth.onAuthStateChanged(async function(user) {"""
new_load = """  // Check if URL has openChat=true to auto-open chat
  setTimeout(() => {
    if (new URLSearchParams(window.location.search).get('openChat') === 'true') {
      const chatBtn = document.getElementById('chatBtn');
      if (chatBtn) {
        openChatModal();
      }
    }
  }, 2000); // Wait for auth and UI to load

  auth.onAuthStateChanged(async function(user) {"""

if 'openChat=true' not in h:
    h = h.replace(old_load, new_load)

with open('index.html', 'w', encoding='utf-8') as f:
    f.write(h)

print("Done: Dedicated Chat shortcut fixed!")
