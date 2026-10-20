with open('admin.html', 'r', encoding='utf-8') as f:
    h = f.read()

old_code = """        const snap = await db.collection('requests').orderBy('createdAt', 'desc').limit(50).get();
        
        if (snap.empty) {
          list.innerHTML = '<div class="empty-msg">Koi request nahi mili.</div>';
          return;
        }

        let html = '';
        snap.forEach(doc => {
          const r = doc.data();
          const isAccepted = r.status === 'accepted';
          const date = r.createdAt ? new Date(r.createdAt.seconds * 1000).toLocaleString() : 'N/A';"""

new_code = """        const snap = await db.collection('requests').get();
        
        if (snap.empty) {
          list.innerHTML = '<div class="empty-msg">Koi request nahi mili.</div>';
          return;
        }

        let requestsArray = [];
        snap.forEach(doc => requestsArray.push({ id: doc.id, ...doc.data() }));
        
        // Manual sort (Newest first) to avoid Firebase Index error
        requestsArray.sort((a, b) => {
          const tA = a.createdAt ? (a.createdAt.seconds || 0) : 0;
          const tB = b.createdAt ? (b.createdAt.seconds || 0) : 0;
          return tB - tA;
        });
        
        requestsArray = requestsArray.slice(0, 50);

        let html = '';
        requestsArray.forEach(r => {
          const isAccepted = r.status === 'accepted';
          const date = r.createdAt ? new Date(r.createdAt.seconds * 1000).toLocaleString() : 'N/A';"""

if old_code in h:
    h = h.replace(old_code, new_code)
    with open('admin.html', 'w', encoding='utf-8') as f:
        f.write(h)
    print("Done: Admin dashboard fixed.")
else:
    print("Error: Code block not found in admin.html")
