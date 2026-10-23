with open('profile.html', 'r', encoding='utf-8') as f:
    h = f.read()

# 1. Add Messaging Script to profile.html if missing
if 'firebase-messaging-compat.js' not in h:
    h = h.replace('<script src="firebase/firebase-firestore-compat.js"></script>', 
                  '<script src="firebase/firebase-firestore-compat.js"></script>\n<script src="firebase/firebase-messaging-compat.js"></script>')

# 2. Replace the FCM function with a Debug Version
old_js = """  window.forceEnableNotifications = async function() {
    try {
      if (!('serviceWorker' in navigator) || !('PushManager' in window)) {
        return alert("Ye browser push notifications support nahi karta.");
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
            alert("✅ Token successfully saved!\\n\\nToken start: " + token.substring(0, 15) + "...");
          } else {
            alert("Error: User not logged in.");
          }
        } else {
          alert("❌ Permission granted, but token was empty.");
        }
      } else {
        alert("❌ Permission denied. Please allow notifications in browser settings.");
      }
    } catch (e) {
      alert("FCM Error: " + e.message);
      console.error(e);
    }
  };"""

new_js = """  window.forceEnableNotifications = async function() {
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

if old_js in h:
    h = h.replace(old_js, new_js)
    print("Replaced old JS with Debug JS")
else:
    print("Old JS not found. Adding debug JS from scratch.")
    # Fallback if exact match fails
    if 'forceEnableNotifications = async' not in h:
        h = h.replace('window.saveProfile = async function() {', new_js + '\n  window.saveProfile = async function() {')

with open('profile.html', 'w', encoding='utf-8') as f:
    f.write(h)

print("Done")
