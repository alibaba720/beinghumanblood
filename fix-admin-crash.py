with open('admin.html', 'r', encoding='utf-8') as f:
    h = f.read()

# Fix the broken syntax (replacing the ')' with '}' at the end of the member card block)
broken_code = """</div>')
                ` : '<div style="font-size:12px;font-weight:bold;color:#d35400;">Protected</div>')}"""
                
fixed_code = """</div>
                ` : '<div style="font-size:12px;font-weight:bold;color:#d35400;">Protected</div>'}"""

if broken_code in h:
    h = h.replace(broken_code, fixed_code)
    print("Fixed syntax error.")

# Also ensure the button is there properly
old_block = """</select>
                ` : '<div style="font-size:12px;font-weight:bold;color:#d35400;">Protected</div>'}"""

new_block = """</select>
                  <button onclick="toggleChatAccess('${m.id}', ${m.isChatMember || false})" style="padding:8px; border-radius:6px; border:1px solid #ccc; font-size:12px; font-weight:bold; cursor:pointer; background:${m.isChatMember ? '#f8d7da' : '#d4edda'}; color:${m.isChatMember ? '#721c24' : '#155724'}; width: 100%; margin-top:5px;">
                    ${m.isChatMember ? 'Remove from Chat' : 'Add to Chat'}
                  </button>
                ` : '<div style="font-size:12px;font-weight:bold;color:#d35400;">Protected</div>'}"""

if old_block in h:
    h = h.replace(old_block, new_block)
    print("Injected button correctly.")

with open('admin.html', 'w', encoding='utf-8') as f:
    f.write(h)

print("Done!")
