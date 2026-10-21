import sys

with open('profile.html', 'r', encoding='utf-8') as f:
    h = f.read()

# Check if JS logic exists
if "window.uploadDP = async function" not in h:
    print("\n--- ImgBB API Key Setup ---")
    api_key = input("Apni ImgBB API Key yahan paste karein aur Enter dabayein: ").strip()

    if not api_key:
        print("API Key khali hai. Process rok diya gaya hai.")
        sys.exit()

    js_code = f"""
  // DP UPLOAD LOGIC
  window.uploadDP = async function(input) {{
    if (!input.files || !input.files[0]) return;
    const file = input.files[0];
    const formData = new FormData();
    formData.append('image', file);
    
    const preview = document.getElementById('dpPreview');
    if(preview) preview.style.opacity = '0.5';
    
    try {{
      const res = await fetch('https://api.imgbb.com/1/upload?key={api_key}', {{
        method: 'POST',
        body: formData
      }});
      const data = await res.json();
      if (data.success) {{
        const url = data.data.url;
        const user = firebase.auth().currentUser;
        if (user) {{
            await db.collection('users').doc(user.uid).update({{ dpUrl: url }});
            await db.collection('donors').doc(user.uid).update({{ dpUrl: url }}).catch(()=>{{}});
        }}
        if(preview) preview.src = url;
        alert("✅ Photo upload ho gayi!");
      }} else {{
        alert("Upload error: " + (data.error ? data.error.message : 'Unknown error'));
      }}
    }} catch(e) {{
      alert("Network error: " + e.message);
    }}
    if(preview) preview.style.opacity = '1';
  }};
"""

    # Inject JS
    if "window.saveProfile = async function" in h:
        h = h.replace("window.saveProfile = async function", js_code + "\n\n    window.saveProfile = async function")
    else:
        h = h.replace("</script>", js_code + "\n</script>")
        
    # Load existing DP
    old_load = "document.getElementById('p_name').value = d.name || '';"
    new_load = "document.getElementById('p_name').value = d.name || '';\n        if(d.dpUrl) { const img = document.getElementById('dpPreview'); if(img) img.src = d.dpUrl; }"
    if old_load in h and "if(d.dpUrl)" not in h:
        h = h.replace(old_load, new_load)

    with open('profile.html', 'w', encoding='utf-8') as f:
        f.write(h)
    
    print("\n✅ Photo upload logic aur API Key successfully file mein daal di gayi hai!")
else:
    print("\n✅ Code pehle se maujood hai. (Agar upload kaam nahi kar raha, to API key galat ho sakti hai).")
