with open('admin.html', 'r', encoding='utf-8') as f: admin = f.read()
with open('profile.html', 'r', encoding='utf-8') as f: profile = f.read()

# ==========================================
# 1. FIX ADMIN DASHBOARD UI (Long Names)
# ==========================================
old_css = """  .member-card { display: flex; justify-content: space-between; align-items: center; background: white; padding: 12px; border-radius: 12px; margin-bottom: 10px; box-shadow: 0 2px 8px rgba(0,0,0,0.06); gap: 10px; }
  .member-info { flex: 1; min-width: 0; }
  .member-info h4 { font-size: 15px; margin-bottom: 3px; color: #333; white-space: nowrap; overflow: hidden; text-overflow: ellipsis; }
  .member-info p { font-size: 12px; color: #666; white-space: nowrap; overflow: hidden; text-overflow: ellipsis; }"""

new_css = """  .member-card { display: flex; justify-content: space-between; align-items: center; background: white; padding: 12px; border-radius: 12px; margin-bottom: 10px; box-shadow: 0 2px 8px rgba(0,0,0,0.06); gap: 10px; }
  .member-info { flex: 1; min-width: 0; word-break: break-word; }
  .member-info h4 { font-size: 15px; margin-bottom: 3px; color: #333; line-height: 1.3; display: flex; flex-wrap: wrap; align-items: center; gap: 5px; }
  .member-info p { font-size: 12px; color: #666; line-height: 1.4; margin-top: 2px; }"""

if old_css in admin:
    admin = admin.replace(old_css, new_css)

# ==========================================
# 2. FIX PROFILE PAGE (Add Force Notification Button & Logic)
# ==========================================
# Add Button
old_btns = """        <button onclick="saveProfile()" id="saveBtn">Save Karo</button>
        <button class="btn-secondary" onclick="goBack()">Wapas Jao</button>"""
new_btns = """        <button onclick="saveProfile()" id="saveBtn">Save Karo</button>
        <button class="btn-secondary" onclick="goBack()">Wapas Jao</button>
        <button class="btn-secondary" onclick="forceEnableNotifications()" style="margin-top:10px; border-color: #f39c12 !important; color: #f39c12 !important;">🔔 Enable Push Notifications</button>"""

if "forceEnableNotifications" not in profile:
    profile = profile.replace(old_btns, new_btns)

# Add JS Logic
fcm_js = """
  const VAPID_KEY = "BKajJKv3dIDBFvOdrVIPGug4O5ITYBs_kDaKW9Y_IPrKe1L2XcmDITqY--LaKBydvkppKc52JGTjQGSxrSyagcA";

  window.forceEnableNotifications = async function() {
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
  };
"""

if "forceEnableNotifications = async" not in profile:
    profile = profile.replace('window.saveProfile = async function() {', fcm_js + '\n  window.saveProfile = async function() {')

with open('admin.html', 'w', encoding='utf-8') as f: f.write(admin)
with open('profile.html', 'w', encoding='utf-8') as f: f.write(profile)

print("Done: Admin UI fixed and Profile FCM button added.")
