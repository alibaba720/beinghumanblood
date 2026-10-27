with open('index.html', 'r', encoding='utf-8') as f:
    h = f.read()

# Text ko replace karein
h = h.replace('📥 Install BH Chats', '📲 Send to Desktop')
h = h.replace('📥 Install App', '📲 Send to Desktop')

with open('index.html', 'w', encoding='utf-8') as f:
    f.write(h)

print("Done: Text changed to 'Send to Desktop'")
