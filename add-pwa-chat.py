import re
import os

# 1. Create manifest.json
manifest_data = """{
  "name": "BeingHuman Chat",
  "short_name": "BH Chat",
  "start_url": "/index.html",
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
with open('manifest.json', 'w', encoding='utf-8') as f:
    f.write(manifest_data)
print("Manifest file created.")

# 2. Update index.html
with open('index.html', 'r', encoding='utf-8') as f:
    h = f.read()

# Link the manifest in <head>
if 'rel="manifest"' not in h:
    h = h.replace('<link rel="preconnect" href="https://fonts.googleapis.com">', '<link rel="manifest" href="manifest.json">\n<link rel="preconnect" href="https://fonts.googleapis.com">')

# 3. Update Chat Header (Add 3-dots menu)
old_header = """    <div style="background: #8B0000; color: white; padding: 15px; display: flex; justify-content: space-between; align-items: center;">
      <h3 style="margin: 0; font-size: 16px;">🩸 BeingHuman Chat</h3>
      <button onclick="closeChatModal()" style="background: none; border: none; color: white; font-size: 20px; cursor: pointer;">✕</button>
    </div>"""
new_header = """    <div style="background: #8B0000; color: white; padding: 15px; display: flex; justify-content: space-between; align-items: center;">
      <h3 style="margin: 0; font-size: 16px;">🩸 BeingHuman Chat</h3>
      <div style="display: flex; gap: 15px; align-items: center;">
        <button onclick="toggleChatMenu()" style="background: none; border: none; color: white; font-size: 20px; cursor: pointer; font-weight:bold;">⋮</button>
        <button onclick="closeChatModal()" style="background: none; border: none; color: white; font-size: 20px; cursor: pointer;">✕</button>
      </div>
    </div>
    
    <!-- CHAT DROPDOWN MENU -->
    <div id="chatDropdown" style="display:none; position: absolute; right: 15px; top: 55px; background: white; border-radius: 8px; box-shadow: 0 4px 15px rgba(0,0,0,0.2); z-index: 1000; overflow: hidden; width: 180px;">
      <button onclick="installPWA()" style="width: 100%; text-align: left; padding: 12px 15px; background: none; border: none; border-bottom: 1px solid #eee; font-size: 14px; cursor: pointer; font-weight: bold; color: #333;">📥 Install App</button>
    </div>"""
if 'id="chatDropdown"' not in h:
    h = h.replace(old_header, new_header)

# 4. Add PWA Install Logic
pwa_logic = """
  // ==========================================
  // PWA INSTALL LOGIC
  // ==========================================
  let deferredPrompt;

  window.addEventListener('beforeinstallprompt', (e) => {
    e.preventDefault();
    deferredPrompt = e;
  });

  window.toggleChatMenu = function() {
    const menu = document.getElementById('chatDropdown');
    if (menu.style.display === 'none') {
      menu.style.display = 'block';
    } else {
      menu.style.display = 'none';
    }
  };

  window.installPWA = async function() {
    document.getElementById('chatDropdown').style.display = 'none';
    
    if (deferredPrompt) {
      deferredPrompt.prompt();
      const { outcome } = await deferredPrompt.userChoice;
      if (outcome === 'accepted') {
        console.log('User accepted the install prompt');
      }
      deferredPrompt = null;
    } else {
      alert("📱 Apne browser ke 3-dots (⋮) menu par click karein aur 'Add to Home Screen' select karein.");
    }
  };

  // Close menu when clicking outside
  document.addEventListener('click', function(e) {
    const menu = document.getElementById('chatDropdown');
    if (menu && menu.style.display === 'block' && !e.target.closest('#chatDropdown') && !e.target.closest('button[onclick="toggleChatMenu()"]')) {
      menu.style.display = 'none';
    }
  });
"""

if 'window.installPWA' not in h:
    h = h.replace('window.openChatModal = function() {', pwa_logic + '\n  window.openChatModal = function() {')

with open('index.html', 'w', encoding='utf-8') as f:
    f.write(h)
    print("Index.html updated with PWA Chat Menu.")

print("Done!")
