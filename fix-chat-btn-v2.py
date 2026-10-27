import re

with open('admin.html', 'r', encoding='utf-8') as f:
    h = f.read()

# 1. Force add the UI button using regex targeting the end of the select tag
if 'toggleChatAccess' not in h or 'Add to Chat' not in h:
    # Look for the select dropdown inside the member card and append the button
    old_str = "</select>"
    # We need to be specific to the one in the members list, not the search filters
    # The members list one ends with `</select>\n                ` : '<div style="...`
    
    pattern = r'(</select>\s*` : \'<div style="font-size:12px;font-weight:bold;color:#d35400;">Protected</div>\')'
    
    replacement = r'''</select>
                  <button onclick="toggleChatAccess('${m.id}', ${m.isChatMember || false})" style="padding:8px; border-radius:6px; border:1px solid #ccc; font-size:12px; font-weight:bold; cursor:pointer; background:${m.isChatMember ? '#f8d7da' : '#d4edda'}; color:${m.isChatMember ? '#721c24' : '#155724'}; width: 100%; margin-top:8px;">
                    ${m.isChatMember ? 'Remove from Chat' : 'Add to Chat'}
                  </button>
                ` : '<div style="font-size:12px;font-weight:bold;color:#d35400;">Protected</div>')'''

    h = re.sub(pattern, replacement, h, flags=re.DOTALL)
    print("✅ UI Button injected.")

# 2. Force add the JS function if it somehow got removed
if 'window.toggleChatAccess' not in h:
    js_func = """
    window.toggleChatAccess = async function(uid, currentStatus) {
      if (!confirm(`Kya aap waqai is user ko ${currentStatus ? 'Chat se remove' : 'Chat mein add'} karna chahte hain?`)) return;
      try {
        const newStatus = !currentStatus;
        await db.collection('users').doc(uid).update({ isChatMember: newStatus });
        await db.collection('donors').doc(uid).update({ isChatMember: newStatus }).catch(()=>{});
        alert(newStatus ? "✅ User added to Chat!" : "❌ User removed from Chat!");
        loadMembers(); 
      } catch(e) {
        alert("Error: " + e.message);
      }
    };
"""
    h = h.replace('window.switchTab = function(tab, event) {', js_func + '\n    window.switchTab = function(tab, event) {')
    print("✅ JS Function injected.")

with open('admin.html', 'w', encoding='utf-8') as f:
    f.write(h)

print("Done: Script finished executing!")
