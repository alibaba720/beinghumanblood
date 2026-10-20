with open('index.html', 'r', encoding='utf-8') as f:
    h = f.read()

old_js = """  async function checkForRequests() {
    if (!currentUserCity || !currentUserBlood) return;
    try {
      const snap = await db.collection('requests')
        .where('city', '==', currentUserCity)
        .where('blood', '==', currentUserBlood)
        .where('status', '==', 'pending')
        .get();
      
      activeRequests = [];
      snap.forEach(doc => activeRequests.push({ id: doc.id, ...doc.data() }));
      
      const dot = document.getElementById('reqDot');
      if (activeRequests.length > 0 && document.getElementById('userName').textContent !== 'Login') {
        dot.style.display = 'block';
      } else {
        dot.style.display = 'none';
      }
    } catch (e) { console.error("Error fetching requests:", e); }
  }"""

new_js = """  async function checkForRequests() {
    if (!currentUserCity || !currentUserBlood) return;
    try {
      // Sirf pending requests uthao (bina extra filters ke taake Firebase Index na maange)
      const snap = await db.collection('requests').where('status', '==', 'pending').get();
      
      const allPending = [];
      snap.forEach(doc => allPending.push({ id: doc.id, ...doc.data() }));
      
      // Ab JavaScript mein filter karo
      activeRequests = allPending.filter(r => 
        r.city && r.city.toLowerCase().trim() === currentUserCity.toLowerCase().trim() && 
        r.blood === currentUserBlood
      );
      
      const dot = document.getElementById('reqDot');
      if (activeRequests.length > 0 && document.getElementById('userName').textContent !== 'Login') {
        dot.style.display = 'block';
      } else {
        dot.style.display = 'none';
      }
    } catch (e) { console.error("Error fetching requests:", e); }
  }"""

h = h.replace(old_js, new_js)

with open('index.html', 'w', encoding='utf-8') as f:
    f.write(h)

print("Done")
