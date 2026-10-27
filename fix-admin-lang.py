with open('admin.html', 'r', encoding='utf-8') as f:
    admin = f.read()

# 1. Fix toggleChatAccess (Add/Remove from Chat)
old_toggle = """      if (!confirm(`Kya aap waqai is user ko ${currentStatus ? 'Chat se remove' : 'Chat mein add'} karna chahte hain?`)) return;"""
new_toggle = """      const lang = localStorage.getItem('bh_lang') || 'en';
      let confirmMsg = "";
      if (currentStatus) {
          confirmMsg = lang === 'urdu' ? "کیا آپ واقعی اس صارف کو چیٹ سے نکالنا چاہتے ہیں؟" : lang === 'roman' ? "Kya aap waqai is user ko Chat se remove karna chahte hain?" : "Are you sure you want to remove this user from Chat?";
      } else {
          confirmMsg = lang === 'urdu' ? "کیا آپ واقعی اس صارف کو چیٹ میں شامل کرنا چاہتے ہیں؟" : lang === 'roman' ? "Kya aap waqai is user ko Chat mein add karna chahte hain?" : "Are you sure you want to add this user to Chat?";
      }
      if (!confirm(confirmMsg)) return;"""
if old_toggle in admin:
    admin = admin.replace(old_toggle, new_toggle)

# 2. Fix updateRole
old_role = """      if (newRole === 'banned') {
        if (!confirm(`WARNING: Kya aap waqai is user ko BAN karna chahte hain?`)) return loadMembers();
      } else {
        if (!confirm(`Kya aap waqai is user ka role change karke '${newRole}' karna chahte hain?`)) return loadMembers();
      }"""
new_role = """      const lang = localStorage.getItem('bh_lang') || 'en';
      let confirmMsg = "";
      if (newRole === 'banned') {
        confirmMsg = lang === 'urdu' ? "انتباہ: کیا آپ واقعی اس صارف کو بین کرنا چاہتے ہیں؟" : lang === 'roman' ? "WARNING: Kya aap waqai is user ko BAN karna chahte hain?" : "WARNING: Are you sure you want to BAN this user?";
      } else {
        confirmMsg = lang === 'urdu' ? `کیا آپ واقعی اس صارف کا رول '${newRole}' کرنا چاہتے ہیں؟` : lang === 'roman' ? `Kya aap waqai is user ka role change karke '${newRole}' karna chahte hain?` : `Are you sure you want to change this user's role to '${newRole}'?`;
      }
      if (!confirm(confirmMsg)) return loadMembers();"""
if old_role in admin:
    admin = admin.replace(old_role, new_role)

# 3. Fix Mute prompts
old_mute = """      if (isMuted) {
        if(!confirm(`Unmute ${name}?`)) return;"""
new_mute = """      const lang = localStorage.getItem('bh_lang') || 'en';
      if (isMuted) {
        let unmuteMsg = lang === 'urdu' ? `کیا آپ ${name} کو ان میوٹ کرنا چاہتے ہیں؟` : lang === 'roman' ? `Unmute ${name}?` : `Unmute ${name}?`;
        if(!confirm(unmuteMsg)) return;"""
if old_mute in admin:
    admin = admin.replace(old_mute, new_mute)

old_mute_prompt = """        const hours = prompt(`Mute ${name} for how many hours? (Enter number e.g., 24)`, "24");"""
new_mute_prompt = """        let mutePrompt = lang === 'urdu' ? `${name} کو کتنے گھنٹے کے لیے میوٹ کرنا ہے؟` : lang === 'roman' ? `Mute ${name} for how many hours? (Enter number e.g., 24)` : `Mute ${name} for how many hours? (Enter number e.g., 24)`;
        const hours = prompt(mutePrompt, "24");"""
if old_mute_prompt in admin:
    admin = admin.replace(old_mute_prompt, new_mute_prompt)

# 4. Fix Alerts for Chat Add/Remove (to match language)
old_alert = """        // Language based simple alert
        const lang = localStorage.getItem('bh_lang') || 'en';
        let msg = "";
        if (newStatus) {
            msg = lang === 'urdu' ? "✅ ممبر چیٹ میں شامل ہو گیا۔" : lang === 'roman' ? "✅ Member chat mein add ho gaya." : "✅ Member added to chat.";
        } else {
            msg = lang === 'urdu' ? "❌ ممبر چیٹ سے نکال دیا گیا۔" : lang === 'roman' ? "❌ Member chat se remove ho gaya." : "❌ Member removed from chat.";
        }
        alert(msg);"""
new_alert = """        const lang = localStorage.getItem('bh_lang') || 'en';
        let msg = "";
        if (newStatus) {
            msg = lang === 'urdu' ? "✅ ممبر چیٹ میں شامل ہو گیا۔" : lang === 'roman' ? "✅ Member chat mein add ho gaya." : "✅ Member added to chat.";
        } else {
            msg = lang === 'urdu' ? "❌ ممبر چیٹ سے نکال دیا گیا۔" : lang === 'roman' ? "❌ Member chat se remove ho gaya." : "❌ Member removed from chat.";
        }
        alert(msg);"""
if old_alert in admin:
    admin = admin.replace(old_alert, new_alert)

with open('admin.html', 'w', encoding='utf-8') as f:
    f.write(admin)

print("Done: Admin popups now respect the selected language!")
