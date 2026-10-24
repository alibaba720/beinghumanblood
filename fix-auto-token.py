import os

if os.path.exists('index.html'):
    with open('index.html', 'r', encoding='utf-8') as f:
        h = f.read()

    # 1. Inject the silent token updater function
    token_func = """
    async function updateTokenSilently() {
      try {
        if (typeof Notification !== 'undefined' && Notification.permission === 'granted') {
          const registration = await navigator.serviceWorker.register('/firebase-messaging-sw.js');
          const messaging = firebase.messaging();
          const currentToken = await messaging.getToken({
            vapidKey: "BKajJKv3dIDBFvOdrVIPGug4O5ITYBs_kDaKW9Y_IPrKe1L2XcmDITqY--LaKBydvkppKc52JGTjQGSxrSyagcA",
            serviceWorkerRegistration: registration
          });
          if (currentToken) {
            const user = firebase.auth().currentUser;
            if (user) {
              // Update silently in background
              await db.collection('users').doc(user.uid).update({ fcmToken: currentToken }).catch(()=>{});
              await db.collection('donors').doc(user.uid).update({ fcmToken: currentToken }).catch(()=>{});
              console.log("Token updated silently.");
            }
          }
        }
      } catch (e) {
        console.log("Silent token update error:", e);
      }
    }
    """

    if "updateTokenSilently" not in h:
        # Inject the function before auth state change
        h = h.replace("auth.onAuthStateChanged(async function(user) {", token_func + "\n\n    auth.onAuthStateChanged(async function(user) {")

        # Call the function when user is logged in
        if "setupFCM();" in h:
            h = h.replace("setupFCM();", "setupFCM();\n        updateTokenSilently();")
        
        with open('index.html', 'w', encoding='utf-8') as f:
            f.write(h)
        print("Done: Auto-token update logic added.")
    else:
        print("Already exists.")
else:
    print("Error: index.html not found.")
