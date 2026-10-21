import re

# 1. Extract ImgBB API Key from profile.html
try:
    with open('profile.html', 'r', encoding='utf-8') as f:
        prof = f.read()
    api_key = re.search(r'upload\?key=([a-zA-Z0-9]+)', prof).group(1)
except:
    print("Error: API Key profile.html se nahi mili. Pehle DP wala kaam complete karo.")
    exit()

# 2. Create create-post.html
html_post = f"""<!DOCTYPE html>
<html lang="en">
<head>
<meta charset="UTF-8">
<meta name="viewport" content="width=device-width, initial-scale=1.0">
<title>Create Memory - BeingHuman Blood</title>
<link href="https://fonts.googleapis.com/css2?family=Inter:wght@400;600;700;800&display=swap" rel="stylesheet">
<style>
  * {{ margin: 0; padding: 0; box-sizing: border-box; font-family: 'Inter', sans-serif; }}
  body {{ background: #f4f6f8; padding-bottom: 50px; }}
  .header {{ background: linear-gradient(135deg, #8B0000, #c0392b); padding: 15px; color: white; display: flex; align-items: center; justify-content: space-between; position: sticky; top: 0; z-index: 100; }}
  .header h1 {{ font-size: 18px; font-weight: 800; }}
  .back-btn {{ background: rgba(255,255,255,0.2); color: white; border: none; padding: 8px 12px; border-radius: 8px; font-weight: bold; text-decoration: none; }}
  .container {{ max-width: 500px; margin: 20px auto; padding: 0 15px; }}
  .card {{ background: white; padding: 20px; border-radius: 12px; box-shadow: 0 4px 15px rgba(0,0,0,0.05); }}
  label {{ display: block; margin-bottom: 5px; font-weight: 600; font-size: 13px; color: #333; }}
  input, textarea {{ width: 100%; padding: 12px; margin-bottom: 15px; border: 2px solid #eee; border-radius: 8px; font-size: 14px; font-family: inherit; }}
  input:focus, textarea:focus {{ outline: none; border-color: #8B0000; }}
  .img-preview {{ width: 100%; height: 200px; border-radius: 8px; border: 2px dashed #ccc; display: flex; align-items: center; justify-content: center; margin-bottom: 15px; background: #fafafa; color: #888; cursor: pointer; overflow: hidden; }}
  .img-preview img {{ width: 100%; height: 100%; object-fit: cover; }}
  button {{ width: 100%; padding: 15px; background: #8B0000; color: white; border: none; border-radius: 8px; font-weight: bold; font-size: 15px; cursor: pointer; }}
  button:disabled {{ opacity: 0.6; }}
</style>
</head>
<body>
<header class="header">
  <h1>📸 Create Memory</h1>
  <a href="index.html" class="back-btn">← Back</a>
</header>

<div class="container">
  <div class="card">
    <label>Donor ki Photo (Upload)</label>
    <label for="postImg" class="img-preview" id="imgPreview">
      <div id="previewText" style="text-align:center;">➕ Tap to upload photo</div>
      <img id="previewImg" src="" style="display:none;">
    </label>
    <input type="file" id="postImg" accept="image/*" style="display:none" onchange="previewImage(this)">

    <label>Donor ka Naam *</label>
    <input type="text" id="postName" placeholder="Ali Hassan">

    <label>City *</label>
    <input type="text" id="postCity" placeholder="Daska">

    <label>Caption / Story *</label>
    <textarea id="postCaption" rows="4" placeholder="Ye hamare bhai [Naam] hain, jinhone Daska mein kisi ki jaan bachai. Allah inke is amal ko qabool kry. ❤️"></textarea>

    <button onclick="submitPost()" id="submitBtn">Post Karo</button>
  </div>
</div>

<script src="firebase/firebase-app-compat.js"></script>
<script src="firebase/firebase-auth-compat.js"></script>
<script src="firebase/firebase-firestore-compat.js"></script>
<script>
  const firebaseConfig = {{
    apiKey: "AIzaSyAp8lKgJuBKpHdXF4pXHr7U3aXwtZUKv_4",
    authDomain: "beinghuman-blood-pk.firebaseapp.com",
    projectId: "beinghuman-blood-pk",
    storageBucket: "beinghuman-blood-pk.firebasestorage.app",
    messagingSenderId: "46427863084",
    appId: "1:46427863084:web:fff219fd6e17fd83e23989"
  }};
  firebase.initializeApp(firebaseConfig);
  const auth = firebase.auth();
  const db = firebase.firestore();

  let postImgUrl = "";

  auth.onAuthStateChanged(async (user) => {{
    if (!user) {{ window.location.href = 'login.html'; return; }}
    const doc = await db.collection('users').doc(user.uid).get();
    if (doc.exists) {{
      const r = doc.data().role;
      if (r !== 'owner' && r !== 'admin' && r !== 'moderator') {{
        alert('Access Denied! Only Owners, Admins, and Moderators can post.');
        window.location.href = 'index.html';
      }}
    }}
  }});

  window.previewImage = function(input) {{
    if (input.files && input.files[0]) {{
      const reader = new FileReader();
      reader.onload = function(e) {{
        document.getElementById('previewText').style.display = 'none';
        document.getElementById('previewImg').src = e.target.result;
        document.getElementById('previewImg').style.display = 'block';
      }};
      reader.readAsDataURL(input.files[0]);
    }}
  }};

  window.submitPost = async function() {{
    const name = document.getElementById('postName').value.trim();
    const city = document.getElementById('postCity').value.trim();
    const caption = document.getElementById('postCaption').value.trim();
    const file = document.getElementById('postImg').files[0];
    const btn = document.getElementById('submitBtn');

    if (!name || !city || !caption) return alert('Sab fields bharein!');
    if (!file) return alert('Photo upload karein!');

    btn.disabled = true; btn.textContent = 'Uploading Photo...';

    try {{
      const formData = new FormData();
      formData.append('image', file);
      const res = await fetch('https://api.imgbb.com/1/upload?key={api_key}', {{ method: 'POST', body: formData }});
      const data = await res.json();

      if (!data.success) throw new Error('Image upload failed');
      postImgUrl = data.data.url;

      btn.textContent = 'Saving Post...';
      const user = firebase.auth().currentUser;
      let authorName = 'Admin';
      if(user) {{
          const uDoc = await db.collection('users').doc(user.uid).get();
          if(uDoc.exists) authorName = uDoc.data().name;
      }}

      await db.collection('posts').add({{
        name: name, city: city, caption: caption, imgUrl: postImgUrl,
        author: authorName,
        createdAt: firebase.firestore.FieldValue.serverTimestamp()
      }});

      alert('✅ Post successfully uploaded!');
      window.location.href = 'index.html';

    }} catch (e) {{
      alert('Error: ' + e.message);
      btn.disabled = false; btn.textContent = 'Post Karo';
    }}
  }};
</script>
</body>
</html>
"""

with open('create-post.html', 'w', encoding='utf-8') as f:
    f.write(html_post)

# 3. Update index.html
with open('index.html', 'r', encoding='utf-8') as f:
    h = f.read()

# 3a. Add Header Button
if 'id="createPostBtn"' not in h:
    old_btn = """<button class="icon-btn" onclick="toggleLangMenu()" title="Language">🌐</button>"""
    new_btn = """<button class="icon-btn" id="createPostBtn" onclick="window.location.href='create-post.html'" title="Create Post" style="display:none; background:#3498db; color:white; font-size:18px;">📸</button>
      <button class="icon-btn" onclick="toggleLangMenu()" title="Language">🌐</button>"""
    h = h.replace(old_btn, new_btn)

# 3b. Show button to Owner/Admin/Moderator
if 'createPostBtn.style.display' not in h:
    old_role = """        if (d.role === 'owner' || d.role === 'admin') {
          const adminBtn = document.getElementById('adminPanelBtn');
          if (adminBtn) adminBtn.style.display = 'flex';"""
    new_role = """        if (d.role === 'owner' || d.role === 'admin' || d.role === 'moderator') {
          const adminBtn = document.getElementById('adminPanelBtn');
          if (adminBtn) adminBtn.style.display = 'flex';
          const postBtn = document.getElementById('createPostBtn');
          if (postBtn) postBtn.style.display = 'flex';"""
    
    # Check if adminPanelBtn update exists
    if old_role in h:
        h = h.replace(old_role, new_role)
    else:
        old_role_fallback = """if (d.role === 'owner' || d.role === 'admin') {
          document.getElementById('founderName').textContent = d.name || 'Ali Hassan';"""
        new_role_fallback = """if (d.role === 'owner' || d.role === 'admin' || d.role === 'moderator') {
          const postBtn = document.getElementById('createPostBtn');
          if (postBtn) postBtn.style.display = 'flex';
          document.getElementById('founderName').textContent = d.name || 'Ali Hassan';"""
        h = h.replace(old_role_fallback, new_role_fallback)

# 3c. Replace Posts Grid UI
old_grid = """  <div class="posts-grid" id="postsGrid">
    <div class="empty-posts" data-i18n="noPostsYet">🌟 Abhi koi post nahi hai. Jald hi aayegi!</div>
  </div>"""
new_grid = """  <div id="latestPostContainer">
    <div class="empty-posts">Loading latest memory...</div>
  </div>
  
  <button id="loadOldMemoriesBtn" onclick="toggleOldMemories()" style="display:none; width:100%; margin-top:15px; padding:12px; background:#fff; color:#8B0000; border:2px solid #8B0000; border-radius:10px; font-weight:700; cursor:pointer;">
    ⬇️ Purani Yaadein (Old Memories)
  </button>

  <div id="oldMemoriesContainer" style="display:none; margin-top:15px;">
    <div class="posts-grid" id="oldPostsGrid"></div>
  </div>"""
h = h.replace(old_grid, new_grid)

# 3d. Replace JS loadPosts logic
old_js_load = """  async function loadPosts() {
    try {
      const snap = await db.collection('posts').orderBy('createdAt', 'desc').limit(6).get();
      const posts = [];
      snap.forEach(doc => posts.push({ id: doc.id, ...doc.data() }));
      window.allPosts = posts;
      renderPosts(posts);
      document.getElementById('statPosts').textContent = posts.length;
    } catch (e) {
      console.error(e);
      renderPosts([]);
    }
  }
  loadPosts();

  window.renderPosts = function(posts) {
    const grid = document.getElementById('postsGrid');
    if (!posts || posts.length === 0) {
      grid.innerHTML = '<div class="empty-posts">' + (translations[currentLang].noPostsYet || '') + '</div>';
      return;
    }
    grid.innerHTML = posts.map(p => `
      <div class="post-card" onclick="openPostModal('${p.id}')">
        <div class="post-img ${p.image ? 'has-img' : ''}" ${p.image ? 'style="background-image:url(' + p.image + ')"' : ''}>${p.image ? '' : '🩸'}</div>
        <div class="post-body">
          <div class="post-tag">${p.tag || 'STORY'}</div>
          <div class="post-title">${p.title || ''}</div>
          <div class="post-text">${(p.caption || '').substring(0, 90)}${(p.caption || '').length > 90 ? '...' : ''}</div>
        </div>
      </div>
    `).join('');
  };"""

new_js_load = """  let globalPosts = [];
  
  async function loadPosts() {
    try {
      const snap = await db.collection('posts').get();
      globalPosts = [];
      snap.forEach(doc => globalPosts.push({ id: doc.id, ...doc.data() }));
      
      // Manual sort newest first
      globalPosts.sort((a, b) => {
        const tA = a.createdAt ? a.createdAt.seconds : 0;
        const tB = b.createdAt ? b.createdAt.seconds : 0;
        return tB - tA;
      });

      renderPosts(globalPosts);
      document.getElementById('statPosts').textContent = globalPosts.length;
    } catch (e) {
      console.error(e);
      document.getElementById('latestPostContainer').innerHTML = '<div class="empty-posts">Error loading posts.</div>';
    }
  }
  loadPosts();

  window.renderPosts = function(posts) {
    const latestBox = document.getElementById('latestPostContainer');
    const oldGrid = document.getElementById('oldPostsGrid');
    const oldBtn = document.getElementById('loadOldMemoriesBtn');

    if (!posts || posts.length === 0) {
      latestBox.innerHTML = '<div class="empty-posts" style="text-align:center;padding:30px;background:white;border-radius:12px;color:#888;">🌟 Abhi koi memory post nahi hui. Jald hi aayegi!</div>';
      oldBtn.style.display = 'none';
      return;
    }

    // Render Latest Post
    const latest = posts[0];
    const dateStr = latest.createdAt ? new Date(latest.createdAt.seconds * 1000).toLocaleDateString() : '';
    latestBox.innerHTML = `
      <div class="post-card" style="background:white;border-radius:16px;overflow:hidden;box-shadow:0 4px 15px rgba(0,0,0,0.08);">
        <div style="width:100%; height:250px; background:url(${latest.imgUrl}) center/cover;"></div>
        <div style="padding:20px;">
          <div style="display:flex; justify-content:space-between; align-items:center; margin-bottom:10px;">
            <h3 style="color:#8B0000; font-size:18px; margin:0;">${latest.name} <span style="font-size:12px; color:#888; font-weight:normal;">📍 ${latest.city}</span></h3>
            <span style="font-size:11px; color:#999;">${dateStr}</span>
          </div>
          <p style="font-size:14px; line-height:1.7; color:#444; margin:0;">${latest.caption}</p>
          <div style="margin-top:15px; font-size:12px; color:#888; font-style:italic;">Posted by: ${latest.author}</div>
        </div>
      </div>
    `;

    // Render Old Posts (Hidden by default)
    if (posts.length > 1) {
      oldBtn.style.display = 'block';
      const oldPosts = posts.slice(1);
      oldGrid.innerHTML = oldPosts.map(p => `
        <div class="post-card" style="background:white;border-radius:12px;overflow:hidden;box-shadow:0 2px 10px rgba(0,0,0,0.06); margin-bottom:15px;">
          <div style="width:100%; height:180px; background:url(${p.imgUrl}) center/cover;"></div>
          <div style="padding:15px;">
            <h4 style="color:#8B0000; font-size:15px; margin-bottom:5px;">${p.name} <span style="font-size:11px; color:#888; font-weight:normal;">📍 ${p.city}</span></h4>
            <p style="font-size:13px; line-height:1.6; color:#555; margin:0;">${p.caption}</p>
          </div>
        </div>
      `).join('');
    } else {
      oldBtn.style.display = 'none';
    }
  };

  window.toggleOldMemories = function() {
    const box = document.getElementById('oldMemoriesContainer');
    const btn = document.getElementById('loadOldMemoriesBtn');
    if (box.style.display === 'none') {
      box.style.display = 'block';
      btn.innerHTML = '⬆️ Purani Yaadein Chupayein (Hide)';
    } else {
      box.style.display = 'none';
      btn.innerHTML = '⬇️ Purani Yaadein (Old Memories)';
    }
  };"""

if old_js_load in h:
    h = h.replace(old_js_load, new_js_load)

with open('index.html', 'w', encoding='utf-8') as f:
    f.write(h)

print("Done: Create post page, header button, and homepage memory layout created.")
