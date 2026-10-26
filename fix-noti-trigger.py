with open('index.html', 'r', encoding='utf-8') as f:
    h = f.read()

# Find the old notification block and replace it with a safer query
old_block = """              // ==========================================
              // TRIGGER PUSH NOTIFICATIONS
              // ==========================================
              try {
                const donorsSnap = await db.collection('donors')
                  .where('blood', '==', currentReqBlood)
                  .where('city', '==', currentReqCity.toLowerCase().trim())
                  .get();

                donorsSnap.forEach(doc => {
                  const donor = doc.data();
                  if (donor.fcmToken) {
                    fetch('/api/send-notification', {
                      method: 'POST',
                      headers: { 'Content-Type': 'application/json' },
                      body: JSON.stringify({
                        token: donor.fcmToken,
                        title: '🚨 Blood Needed in ' + currentReqCity,
                        body: `${currentReqBlood} ki zarurat hai. Hospital: ${hospital}. Kya aap madad kar sakte hain?`
                      })
                    }).catch(e => console.log('Push error:', e));
                  }
                });
              } catch (error) {
                console.error("Error sending push notifications:", error);
              }"""

new_block = """              // ==========================================
              // TRIGGER PUSH NOTIFICATIONS (SAFE MODE)
              // ==========================================
              try {
                // Fetch all donors and filter in JS to avoid missing index errors
                const donorsSnap = await db.collection('donors').get();
                
                donorsSnap.forEach(doc => {
                  const donor = doc.data();
                  const matchBlood = donor.blood === currentReqBlood;
                  const matchCity = donor.city && donor.city.toLowerCase().trim() === currentReqCity.toLowerCase().trim();
                  
                  if (matchBlood && matchCity && donor.fcmToken) {
                    fetch('/api/send-notification', {
                      method: 'POST',
                      headers: { 'Content-Type': 'application/json' },
                      body: JSON.stringify({
                        token: donor.fcmToken,
                        title: '🚨 Blood Needed in ' + currentReqCity,
                        body: `${currentReqBlood} ki zarurat hai. Hospital: ${hospital}. Kya aap madad kar sakte hain?`
                      })
                    }).catch(e => console.log('Push error:', e));
                  }
                });
              } catch (error) {
                console.error("Error sending push notifications:", error);
              }"""

if old_block in h:
    h = h.replace(old_block, new_block)
    with open('index.html', 'w', encoding='utf-8') as f:
        f.write(h)
    print("Done: Notification trigger fixed safely!")
else:
    print("Error: Could not find the exact block. Let me know.")
