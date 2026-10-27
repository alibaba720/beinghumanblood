import re

# ==========================================
# 1. UPDATE ADMIN.HTML (Add chatJoinedAt Timestamp)
# ==========================================
with open('admin.html', 'r', encoding='utf-8') as f:
    admin = f.read()

old_toggle = """      try {
        const newStatus = !currentStatus;
        await db.collection('users').doc(uid).update({ isChatMember: newStatus });
        await db.collection('donors').doc(uid).update({ isChatMember: newStatus }).catch(()=>{});
        alert(newStatus ? "✅ User added to Chat!" : "❌ User removed from Chat!");
        loadMembers();
      } catch(e) {"""

new_toggle = """      try {
        const newStatus = !currentStatus;
        const updateData = { isChatMember: newStatus };
        
        // If adding to chat, set the join timestamp
        if (newStatus) {
            updateData.chatJoinedAt = firebase.firestore.FieldValue.serverTimestamp();
        }
        
        await db.collection('users').doc(uid).update(updateData);
        await db.collection('donors').doc(uid).update(updateData).catch(()=>{});
        alert(newStatus ? "✅ User added to Chat! (Purani chats usko nazar nahi aayengi)" : "❌ User removed from Chat!");
        loadMembers();
      } catch(e) {"""

if old_toggle in admin:
    admin = admin.replace(old_toggle, new_toggle)
    with open('admin.html', 'w', encoding='utf-8') as f:
        f.write(admin)
    print("✅ Admin Panel updated with chatJoinedAt timestamp.")


# ==========================================
# 2. UPDATE CHAT.HTML (Filter old messages)
# ==========================================
with open('chat.html', 'r', encoding='utf-8') as f:
    chat = f.read()

old_load = """    db.collection('chat_messages').orderBy('createdAt', 'desc').limit(200).onSnapshot(snapshot => {
      msgBox.innerHTML = '';
      let validMessages = [];
      snapshot.forEach(doc => {
        const msg = doc.data();
        if (msg.createdAt && msg.createdAt.toDate() >= sevenDaysAgo) validMessages.push(msg);
      });"""

new_load = """    let joinedAtTime = 0;
    // Owner and Admin see all messages. Normal users only see messages after they joined.
    if (currentUserData && currentUserData.role !== 'owner' && currentUserData.role !== 'admin') {
        if (currentUserData.chatJoinedAt) {
            joinedAtTime = currentUserData.chatJoinedAt.toMillis();
        } else {
            joinedAtTime = Date.now(); // Fallback: only see new messages
        }
    }

    db.collection('chat_messages').orderBy('createdAt', 'desc').limit(200).onSnapshot(snapshot => {
      msgBox.innerHTML = '';
      let validMessages = [];
      snapshot.forEach(doc => {
        const msg = doc.data();
        const msgTime = msg.createdAt ? msg.createdAt.toMillis() : Date.now();
        
        // Only push if message is after joined time AND within 7 days
        if (msgTime >= joinedAtTime && msg.createdAt && msg.createdAt.toDate() >= sevenDaysAgo) {
            validMessages.push(msg);
        }
      });"""

if old_load in chat:
    chat = chat.replace(old_load, new_load)
    with open('chat.html', 'w', encoding='utf-8') as f:
        f.write(chat)
    print("✅ chat.html updated to filter old messages.")


# ==========================================
# 3. UPDATE INDEX.HTML (Same logic for in-app chat)
# ==========================================
with open('index.html', 'r', encoding='utf-8') as f:
    index = f.read()

old_index_load = """      // Fetch latest 200 messages ordered by newest first
      chatUnsubscribe = db.collection('chat_messages')
        .orderBy('createdAt', 'desc')
        .limit(200)
        .onSnapshot(snapshot => {
          msgBox.innerHTML = '';
          
          let validMessages = [];
          snapshot.forEach(doc => {
            const msg = doc.data();
            // Only keep messages from last 7 days
            if (msg.createdAt && msg.createdAt.toDate() >= sevenDaysAgo) {
              validMessages.push(msg);
            }
          });"""

new_index_load = """      // Determine if we need to filter by join time
      let joinedAtTime = 0;
      if (window.currentUserData && window.currentUserData.role !== 'owner' && window.currentUserData.role !== 'admin') {
          if (window.currentUserData.chatJoinedAt) {
              joinedAtTime = window.currentUserData.chatJoinedAt.toMillis();
          } else {
              joinedAtTime = Date.now();
          }
      }

      // Fetch latest 200 messages ordered by newest first
      chatUnsubscribe = db.collection('chat_messages')
        .orderBy('createdAt', 'desc')
        .limit(200)
        .onSnapshot(snapshot => {
          msgBox.innerHTML = '';
          
          let validMessages = [];
          snapshot.forEach(doc => {
            const msg = doc.data();
            const msgTime = msg.createdAt ? msg.createdAt.toMillis() : Date.now();
            
            // Only keep messages after joined time AND within 7 days
            if (msgTime >= joinedAtTime && msg.createdAt && msg.createdAt.toDate() >= sevenDaysAgo) {
              validMessages.push(msg);
            }
          });"""

if old_index_load in index:
    index = index.replace(old_index_load, new_index_load)
    with open('index.html', 'w', encoding='utf-8') as f:
        f.write(index)
    print("✅ index.html updated to filter old messages.")

print("Done: Chat history clear feature added!")
