import re

# 1. UPDATE ADMIN.HTML
with open('admin.html', 'r', encoding='utf-8') as f:
    admin = f.read()

old_toggle_alert = """        await db.collection('donors').doc(uid).update(updateData).catch(()=>{});
        alert(newStatus ? "✅ User added to Chat! (Purani chats usko nazar nahi aayengi)" : "❌ User removed from Chat!");
        loadMembers();"""

new_toggle_alert = """        await db.collection('donors').doc(uid).update(updateData).catch(()=>{});
        
        // Language based simple alert
        const lang = localStorage.getItem('bh_lang') || 'en';
        let msg = "";
        if (newStatus) {
            msg = lang === 'urdu' ? "✅ ممبر چیٹ میں شامل ہو گیا۔" : lang === 'roman' ? "✅ Member chat mein add ho gaya." : "✅ Member added to chat.";
        } else {
            msg = lang === 'urdu' ? "❌ ممبر چیٹ سے نکال دیا گیا۔" : lang === 'roman' ? "❌ Member chat se remove ho gaya." : "❌ Member removed from chat.";
        }
        alert(msg);
        loadMembers();"""

if old_toggle_alert in admin:
    admin = admin.replace(old_toggle_alert, new_toggle_alert)

# Update Mute alerts to be simple
old_mute_alert = """          alert("User unmuted successfully.");
          loadMembers();
        } catch(e) { alert(e.message); }
      } else {
        const hours = prompt(`Mute ${name} for how many hours? (Enter number e.g., 24)`, "24");"""
        
new_mute_alert = """          alert(localStorage.getItem('bh_lang') === 'urdu' ? "✅ ممبر کو ان میوٹ کر دیا گیا ہے۔" : "✅ User unmuted successfully.");
          loadMembers();
        } catch(e) { alert(e.message); }
      } else {
        const hours = prompt(`Mute ${name} for how many hours? (Enter number e.g., 24)`, "24");"""
if old_mute_alert in admin:
    admin = admin.replace(old_mute_alert, new_mute_alert)

old_mute_alert2 = """            alert(`User muted for ${hours} hours.`);
            loadMembers();"""
new_mute_alert2 = """            alert(localStorage.getItem('bh_lang') === 'urdu' ? `ممبر کو ${hours} گھنٹے کے لیے میوٹ کر دیا گیا ہے۔` : `User muted for ${hours} hours.`);
            loadMembers();"""
if old_mute_alert2 in admin:
    admin = admin.replace(old_mute_alert2, new_mute_alert2)

with open('admin.html', 'w', encoding='utf-8') as f:
    f.write(admin)
    print("✅ Admin popups simplified and translated.")


# 2. UPDATE CHAT.HTML (Language support for errors)
with open('chat.html', 'r', encoding='utf-8') as f:
    chat = f.read()

# Mute alert in chat
chat = chat.replace('alert("⚠️ Aapko mute kar diya gaya hai.");', 
"""const lang = localStorage.getItem('bh_lang') || 'en';
            alert(lang === 'urdu' ? "⚠️ آپ کو چیٹ سے میوٹ کر دیا گیا ہے۔" : "⚠️ Aapko mute kar diya gaya hai.");""")

# Number restriction alert in chat
chat = chat.replace('alert("⚠️ Number share na karein.");', 
"""const lang = localStorage.getItem('bh_lang') || 'en';
            alert(lang === 'urdu' ? "⚠️ نمبر شیئر نہ کریں۔" : "⚠️ Number share na karein.");""")

with open('chat.html', 'w', encoding='utf-8') as f:
    f.write(chat)
    print("✅ Chat alerts translated.")


# 3. UPDATE INDEX.HTML (Language support for chat errors)
with open('index.html', 'r', encoding='utf-8') as f:
    index = f.read()

index = index.replace('alert("⚠️ Aapko chat se mute kar diya gaya hai. Waqt khatam hone tak intezar karein.");', 
"""const lang = localStorage.getItem('bh_lang') || 'en';
            alert(lang === 'urdu' ? "⚠️ آپ کو چیٹ سے میوٹ کر دیا گیا ہے۔" : "⚠️ Aapko chat se mute kar diya gaya hai.");""")

index = index.replace('alert("⚠️ Baraye meharbani chat mein phone number share na karein.");', 
"""const lang = localStorage.getItem('bh_lang') || 'en';
            alert(lang === 'urdu' ? "⚠️ چیٹ میں نمبر شیئر نہ کریں۔" : "⚠️ Baraye meharbani chat mein phone number share na karein.");""")

with open('index.html', 'w', encoding='utf-8') as f:
    f.write(index)
    print("✅ Index.html alerts translated.")

print("Done: All alerts fixed!")
