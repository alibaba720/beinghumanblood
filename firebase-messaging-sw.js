importScripts('https://www.gstatic.com/firebasejs/10.12.0/firebase-app-compat.js');
importScripts('https://www.gstatic.com/firebasejs/10.12.0/firebase-messaging-compat.js');

const firebaseConfig = {
  apiKey: "AIzaSyAp8lKgJuBKpHdXF4pXHr7U3aXwtZUKv_4",
  authDomain: "beinghuman-blood-pk.firebaseapp.com",
  projectId: "beinghuman-blood-pk",
  storageBucket: "beinghuman-blood-pk.firebasestorage.app",
  messagingSenderId: "46427863084",
  appId: "1:46427863084:web:fff219fd6e17fd83e23989"
};

firebase.initializeApp(firebaseConfig);
const messaging = firebase.messaging();

messaging.onBackgroundMessage((payload) => {
  console.log('[firebase-messaging-sw.js] Received background message ', payload);
  const notificationTitle = payload.notification.title || 'BeingHuman Blood';
  const notificationOptions = {
    body: payload.notification.body || 'Naya message aaya hai!',
    icon: '/firebase-logo.png' // You can replace this with your logo
  };
  self.registration.showNotification(notificationTitle, notificationOptions);
});


// Handle notification clicks
self.addEventListener('notificationclick', function(event) {
  event.notification.close(); // Close the notification
  
  // URL to open when clicked
  const urlToOpen = new URL('https://beinghumanblood.vercel.app/?openRequests=true', self.location.origin).href;

  event.waitUntil(
    clients.matchAll({ type: 'window', includeUncontrolled: true }).then((windowClients) => {
      // Check if there is already a window/tab open with the target URL
      for (let i = 0; i < windowClients.length; i++) {
        const client = windowClients[i];
        if (client.url === urlToOpen && 'focus' in client) {
          return client.focus();
        }
      }
      // If not, open a new window
      if (clients.openWindow) {
        return clients.openWindow(urlToOpen);
      }
    })
  );
});
