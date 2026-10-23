import os

VAPID_KEY = "BKajJKv3dIDBFvOdrVIPGug4O5ITYBs_kDaKW9Y_IPrKe1L2XcmDITqY--LaKBydvkppKc52JGTjQGSxrSyagcA"

# 1. Create firebase-messaging-sw.js
sw_content = f"""importScripts('https://www.gstatic.com/firebasejs/10.12.0/firebase-app-compat.js');
importScripts('https://www.gstatic.com/firebasejs/10.12.0/firebase-messaging-compat.js');

const firebaseConfig = {{
  apiKey: "AIzaSyAp8lKgJuBKpHdXF4pXHr7U3aXwtZUKv_4",
  authDomain: "beinghuman-blood-pk.firebaseapp.com",
  projectId: "beinghuman-blood-pk",
  storageBucket: "beinghuman-blood-pk.firebasestorage.app",
  messagingSenderId: "46427863084",
  appId: "1:46427863084:web:fff219fd6e17fd83e23989"
}};

firebase.initializeApp(firebaseConfig);
const messaging = firebase.messaging();

messaging.onBackgroundMessage((payload) => {{
  console.log('[firebase-messaging-sw.js] Received background message ', payload);
  const notificationTitle = payload.notification.title || 'BeingHuman Blood';
  const notificationOptions = {{
    body: payload.notification.body || 'Naya message aaya hai!',
    icon: '/firebase-logo.png' // You can replace this with your logo
  }};
  self.registration.showNotification(notificationTitle, notificationOptions);
}});
"""
with open('firebase-messaging-sw.js', 'w', encoding='utf-8') as f:
    f.write(sw_content)

# 2. Function to inject FCM logic into HTML files
fcm_js_logic = f"""
  // ==========================================
  // FCM PUSH NOTIFICATIONS
  // ==========================================
  const VAPID_KEY = "{VAPID_KEY}";
  
  async function requestNotificationPermission() {{
    try {{
      const permission = await Notification.requestPermission();
      if (permission === 'granted') {{
        console.log('Notification permission granted.');
        if ('serviceWorker' in navigator) {{
          const registration = await navigator.serviceWorker.register('/firebase-messaging-sw.js');
          const messaging = firebase.messaging();
          const token = await messaging.getToken({{
            vapidKey: VAPID_KEY,
            serviceWorkerRegistration: registration
          }});
          
          if (token) {{
            console.log('FCM Token:', token);
            const user = firebase.auth().currentUser;
            if (user) {{
              await db.collection('users').doc(user.uid).update({{ fcmToken: token }}).catch(()=>{{}});
              await db.collection('donors').doc(user.uid).update({{ fcmToken: token }}).catch(()=>{{}});
            }}
          }}
        }}
      }} else {{
        console.log('Notification permission denied.');
      }}
    }} catch (e) {{
      console.error('Error getting notification permission:', e);
    }}
  }}

  function setupFCM() {{
    if ('Notification' in window && 'serviceWorker' in navigator && 'PushManager' in window) {{
      if (Notification.permission === 'granted') {{
        requestNotificationPermission();
      }} else if (Notification.permission !== 'denied') {{
        // Ask after 3 seconds so page loads first
        setTimeout(() => {{
          requestNotificationPermission();
        }}, 3000);
      }}
    }}
  }}
"""

# 3. Update index.html
with open('index.html', 'r', encoding='utf-8') as f:
    index = f.read()

if "requestNotificationPermission" not in index:
    # Add script tag
    index = index.replace('<script src="firebase/firebase-firestore-compat.js"></script>', 
                          '<script src="firebase/firebase-firestore-compat.js"></script>\n<script src="firebase/firebase-messaging-compat.js"></script>')
    # Inject JS
    index = index.replace('// TOAST NOTIFICATIONS (OTHER DONORS)', fcm_js_logic + '\n// TOAST NOTIFICATIONS (OTHER DONORS)')
    # Call setupFCM on auth state change
    index = index.replace("checkForRequests();", "checkForRequests();\n        setupFCM();")
    with open('index.html', 'w', encoding='utf-8') as f:
        f.write(index)

# 4. Update login.html
with open('login.html', 'r', encoding='utf-8') as f:
    login = f.read()

if "requestNotificationPermission" not in login:
    login = login.replace('<script src="firebase/firebase-firestore-compat.js"></script>', 
                          '<script src="firebase/firebase-firestore-compat.js"></script>\n<script src="firebase/firebase-messaging-compat.js"></script>')
    login = login.replace('// INIT LANGUAGE', fcm_js_logic + '\n// INIT LANGUAGE')
    # Call setupFCM after successful login
    login = login.replace("goToHome = function()", "setupFCM();\n  window.goToHome = function()")
    # If already logged in, call on auth state
    login = login.replace("window.goToHome();", "setupFCM();\n      window.goToHome();")
    with open('login.html', 'w', encoding='utf-8') as f:
        f.write(login)

print("Done: FCM setup complete. Service worker created.")
