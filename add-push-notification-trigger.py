import os

file_path = 'index.html'
if os.path.exists(file_path):
    with open(file_path, 'r', encoding='utf-8') as f:
        h = f.read()

    if "fetch('/api/send-notification'" not in h:
        injection = """
              // ==========================================
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
              }

              // 2. Prepare WhatsApp link for Owner"""

        target = "// 2. Prepare WhatsApp link for Owner"
        if target in h:
            h = h.replace(target, injection)
            with open(file_path, 'w', encoding='utf-8') as f:
                f.write(h)
            print("Done: Push notification trigger added to submitReq.")
        else:
            print("Error: Target string not found.")
    else:
        print("Already exists.")
else:
    print("index.html not found.")
