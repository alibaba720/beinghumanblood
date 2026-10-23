import os

sw_file = 'firebase-messaging-sw.js'

if os.path.exists(sw_file):
    with open(sw_file, 'r', encoding='utf-8') as f:
        sw_code = f.read()

    # Check if notificationclick is already there
    if "self.addEventListener('notificationclick'" not in sw_code:
        click_logic = """

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
"""
        sw_code += click_logic
        with open(sw_file, 'w', encoding='utf-8') as f:
            f.write(sw_code)
        print("Done: Notification click handler added to Service Worker.")
    else:
        print("Already exists in Service Worker.")
else:
    print("Error: firebase-messaging-sw.js not found.")
