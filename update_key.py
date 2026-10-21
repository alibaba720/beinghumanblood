import re

print("--- ImgBB API Key Setup ---")
api_key = input("Apni ImgBB API Key yahan paste karein aur Enter dabayein: ").strip()

if not api_key:
    print("Error: API Key khali hai. Script band ho rahi hai.")
    exit()

with open('profile.html', 'r', encoding='utf-8') as f:
    h = f.read()

# Replace any known placeholders
h = re.sub(r'YAHAN_APNI_API_KEY_LIKHO', api_key, h)
h = re.sub(r'YOUR_API_KEY_HERE', api_key, h)
h = re.sub(r'YOUR_IMGBB_KEY_HERE', api_key, h)

# Ensure the key is actually in the file
if api_key in h:
    with open('profile.html', 'w', encoding='utf-8') as f:
        f.write(h)
    print("\n✅ API Key successfully file mein daal di gayi hai!")
else:
    print("\n❌ Key update nahi ho payi. File mein placeholder nahi mila. (Check karo ke uploadDP wala code file mein hai ya nahi).")
