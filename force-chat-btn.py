import re

with open('index.html', 'r', encoding='utf-8') as f:
    h = f.read()

# 1. Force inject the chat button inside header-actions if missing
if 'id="chatBtn"' not in h:
    target = '<div class="header-actions">'
    new_btn = '''<div class="header-actions">
      <button class="icon-btn" id="chatBtn" onclick="openChatModal()" title="Chat" style="display:none; background:#27ae60; color:white; position:relative;">💬<span id="chatDot" style="display:none;position:absolute;top:6px;right:6px;width:10px;height:10px;background:#e74c3c;border-radius:50%;border:1px solid white;"></span></button>'''
    h = h.replace(target, new_btn)
    print("Button injected in HTML.")

# 2. Update logic to ALWAYS show chat button for Owner/Admin, and only for normal users if isChatMember is true
old_logic = """        if (d.isChatMember) {
          const chatBtn = document.getElementById('chatBtn');
          if (chatBtn) chatBtn.style.display = 'flex';
        }"""
        
new_logic = """        if (d.isChatMember || d.role === 'owner' || d.role === 'admin') {
          const chatBtn = document.getElementById('chatBtn');
          if (chatBtn) chatBtn.style.display = 'flex';
        }"""

if old_logic in h:
    h = h.replace(old_logic, new_logic)
    print("Updated existing logic.")
elif 'const chatBtn = document.getElementById(\'chatBtn\');' not in h:
    # Fallback if the logic wasn't injected at all previously
    target_check = """        const d = doc.data();
        if (d.role === 'banned') {"""
    new_check = """        const d = doc.data();
        
        if (d.isChatMember || d.role === 'owner' || d.role === 'admin') {
          const chatBtn = document.getElementById('chatBtn');
          if (chatBtn) chatBtn.style.display = 'flex';
        }

        if (d.role === 'banned') {"""
    h = h.replace(target_check, new_check)
    print("Injected new logic.")

with open('index.html', 'w', encoding='utf-8') as f:
    f.write(h)

print("Done: Owner bypass added successfully!")
