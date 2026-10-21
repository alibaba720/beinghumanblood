with open('profile.html', 'r', encoding='utf-8') as f:
    h = f.read()

js_code = """
  // DP UPLOAD LOGIC
  const IMGBB_API_KEY = "YAHAN_APNI_API_KEY_LIKHO";
  
  window.uploadDP = async function(input) {
    if (!input.files || !input.files[0]) return;
    const file = input.files[0];
    const formData = new FormData();
    formData.append('image', file);
    
    const preview = document.getElementById('dpPreview');
    preview.style.opacity = '0.5';
    
    try {
      const res = await fetch('https://api.imgbb.com/1/upload?key=' + IMGBB_API_KEY, {
        method: 'POST',
        body: formData
      });
      const data = await res.json();
      if (data.success) {
        const url = data.data.url;
        await db.collection('users').doc(currentUser.uid).update({ dpUrl: url });
        await db.collection('donors').doc(currentUser.uid).update({ dpUrl: url }).catch(()=>{});
        preview.src = url;
        alert("✅ Photo upload ho gayi!");
      } else {
        alert("Upload error: " + data.error.message);
      }
    } catch(e) {
      alert("Network error: " + e.message);
    }
    preview.style.opacity = '1';
  };
"""

if "uploadDP" not in h:
    # Inject JS right before saveProfile
    if "window.saveProfile = async function() {" in h:
        h = h.replace("window.saveProfile = async function() {", js_code + "\n  window.saveProfile = async function() {")
    else:
        # Fallback: inject before closing script tag
        h = h.replace("</script>", js_code + "\n</script>")
        
    # Load existing DP
    old_load = "document.getElementById('p_name').value = d.name || '';"
    new_load = "document.getElementById('p_name').value = d.name || '';\n        if(d.dpUrl) document.getElementById('dpPreview').src = d.dpUrl;"
    if old_load in h and "if(d.dpUrl) document.getElementById('dpPreview')" not in h:
        h = h.replace(old_load, new_load)

    with open('profile.html', 'w', encoding='utf-8') as f:
        f.write(h)
    print("Done")
else:
    print("Already exists")
