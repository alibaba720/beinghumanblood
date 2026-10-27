with open('index.html', 'r', encoding='utf-8') as f:
    h = f.read()

# Find the sendChatMessage function and inject the digit restriction
old_code = """  window.sendChatMessage = async function() {
    const input = document.getElementById('chatInput');
    const text = input.value.trim();
    const user = firebase.auth().currentUser;
    
    if (!text || !user) return;"""

new_code = """  window.sendChatMessage = async function() {
    const input = document.getElementById('chatInput');
    const text = input.value.trim();
    const user = firebase.auth().currentUser;
    
    if (!text || !user) return;

    // RESTRICTION: Block 5 or more consecutive digits (ignoring spaces/dashes)
    const cleanText = text.replace(/[\\s\\-\\(\\)\\.]/g, '');
    if (/\\d{5,}/.test(cleanText)) {
      alert("⚠️ Baraye meharbani chat mein apna ya kisi ka number share na karein.");
      input.value = text; // Restore text so they don't lose it but can edit
      return;
    }"""

if old_code in h:
    h = h.replace(old_code, new_code)
    with open('index.html', 'w', encoding='utf-8') as f:
        f.write(h)
    print("Done: Number restriction added successfully!")
else:
    print("Error: Could not find the function to inject restriction.")
