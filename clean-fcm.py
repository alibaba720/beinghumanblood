with open('profile.html', 'r', encoding='utf-8') as f:
    h = f.read()

old_debug_code = """  window.forceEnableNotifications = async function() {
    try {
      alert("Step 1: Checking browser support...");
      if (!('serviceWorker' in navigator) || !('PushManager' in window)) {
        return alert("❌ Ye browser push notifications support nahi karta.");
      }
      
      alert("Step 2: Asking for permission...");
      const permission = await Notification.requestPermission();
      alert("Permission result: " + permission);
      
      if (permission === 'granted') {
        alert("Step 3: Registering Service Worker...");
        const registration = await navigator.serviceWorker.register('/firebase-messaging-sw.js');
        alert("Service Worker Registered!");
        
        alert("Step 4: Fetching Token from Firebase...");
        const messaging = firebase.messaging();
        
        const token = await messaging.getToken({
          vapidKey: VAPID_KEY,
          serviceWorkerRegistration: registration
        });
        
        if (token) {
          alert("Token Mila: " + token.substring(0, 10) + "...\\n\\nStep 5: Saving to Database...");
          const user = firebase.auth().currentUser;
          if (user) {
            await db.collection('users').doc(user.uid).update({ fcmToken: token });
            await db.collection('donors').doc(user.uid).update({ fcmToken: token }).catch(()=>{});
            alert("✅ Token successfully saved to DB!");
          } else {
            alert("❌ Error: User not logged in.");
          }
        } else {
          alert("❌ Permission granted, but token was empty.");
        }
      } else {
        alert("❌ Permission denied. Please allow notifications in browser settings.");
      }
    } catch (e) {
      alert("❌ FCM Error: " + e.message);
      console.error(e);
    }
  };"""

new_clean_code = """  window.forceEnableNotifications = async function() {
    try {
      if (!('serviceWorker' in navigator) || !('PushManager' in window)) {
        return alert("Aapka browser push notifications support nahi karta.");
      }
      
      const permission = await Notification.requestPermission();
      if (permission === 'granted') {
        const registration = await navigator.serviceWorker.register('/firebase-messaging-sw.js');
        const messaging = firebase.messaging();
        
        const token = await messaging.getToken({
          vapidKey: VAPID_KEY,
          serviceWorkerRegistration: registration
        });
        
        if (token) {
          const user = firebase.auth().currentUser;
          if (user) {
            await db.collection('users').doc(user.uid).update({ fcmToken: token });
            await db.collection('donors').doc(user.uid).update({ fcmToken: token }).catch(()=>{});
            alert("✅ Notifications successfully enabled! Ab aapko blood requests ki alerts milengi.");
          } else {
            alert("Error: User not logged in.");
          }
        } else {
          alert("Permission granted, lekin token generate nahi hua. Dobara try karein.");
        }
      } else {
        alert("Aapne notifications block kar di hain. Browser settings se allow karein.");
      }
    } catch (e) {
      alert("Notification enable karne mein masla aaya: " + e.message);
      console.error(e);
    }
  };"""

if old_debug_code in h:
    h = h.replace(old_debug_code, new_clean_code)
    with open('profile.html', 'w', encoding='utf-8') as f:
        f.write(h)
    print("Done: FCM Debug code removed and replaced with clean code.")
else:
    print("Error: Debug code not found. Maybe it was already updated.")
