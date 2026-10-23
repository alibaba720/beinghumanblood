import os

# 1. Update api/send-notification.js
if os.path.exists('api/send-notification.js'):
    with open('api/send-notification.js', 'r', encoding='utf-8') as f:
        api_code = f.read()

    old_message = """    const message = {
      notification: { title, body },
      token: token,
    };"""

    new_message = """    const message = {
      notification: { title, body },
      token: token,
      webpush: {
        fcmOptions: {
          link: 'https://beinghumanblood.vercel.app/?openRequests=true'
        }
      }
    };"""

    if old_message in api_code:
        api_code = api_code.replace(old_message, new_message)
        with open('api/send-notification.js', 'w', encoding='utf-8') as f:
            f.write(api_code)
        print("API code updated.")
    else:
        print("API code pattern not found (maybe already updated).")

# 2. Update index.html
with open('index.html', 'r', encoding='utf-8') as f:
    index_code = f.read()

# Add logic to open modal if ?openRequests=true
js_logic = """
      // Check URL parameter for opening requests automatically (From Notification Click)
      const urlParams = new URLSearchParams(window.location.search);
      if (urlParams.get('openRequests') === 'true') {
        setTimeout(() => {
          if (document.getElementById('userName').textContent !== 'Login') {
            openDonorReqModal();
          }
        }, 2000); // Wait for Firebase to load user data
      }
    """

if "urlParams.get('openRequests')" not in index_code:
    # Inject inside waitForFirebase block, after loadStats()
    if "loadStats();" in index_code:
        index_code = index_code.replace("loadStats();", "loadStats();\n" + js_logic)
        with open('index.html', 'w', encoding='utf-8') as f:
            f.write(index_code)
        print("Index.html updated with notification click logic.")
    else:
        print("Index.html pattern not found.")
else:
    print("Index.html already updated.")

print("Done")
