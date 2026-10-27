from PIL import Image, ImageDraw
import json
import os

# 1. Create a custom Chat Icon (512x512)
img = Image.new('RGB', (512, 512), color='#8B0000') # Deep Red Background
d = ImageDraw.Draw(img)

# Draw a white chat bubble (Rounded Rectangle)
# (x0, y0, x1, y1, radius)
d.rounded_rectangle([100, 100, 412, 350], radius=50, fill='white')

# Draw the little tail of the chat bubble
d.polygon([(150, 350), (200, 350), (150, 420)], fill='white')

# Draw a small red blood drop inside the chat bubble
# Triangle top
d.polygon([(256, 160), (200, 240), (312, 240)], fill='#8B0000')
# Circle bottom
d.ellipse([200, 220, 312, 320], fill='#8B0000')

# Save the icon
img.save('chat-icon.png')
print("✅ Custom Chat Icon ban gaya hai (chat-icon.png).")

# 2. Update manifest-chat.json
manifest_path = 'manifest-chat.json'
if os.path.exists(manifest_path):
    with open(manifest_path, 'r', encoding='utf-8') as f:
        manifest = json.load(f)
    
    # Update icon paths
    manifest['icons'] = [
        {
            "src": "chat-icon.png",
            "sizes": "512x512",
            "type": "image/png",
            "purpose": "any maskable"
        }
    ]
    
    with open(manifest_path, 'w', encoding='utf-8') as f:
        json.dump(manifest, f, indent=2)
    print("✅ manifest-chat.json update ho gaya hai.")
else:
    print("⚠️ manifest-chat.json nahi mili.")
