with open('index.html', 'r', encoding='utf-8') as f: index = f.read()
with open('admin.html', 'r', encoding='utf-8') as f: admin = f.read()

# === 1. FIX HEADER UI (index.html) ===
old_header_css = """  .header-inner {
    max-width: 1100px;
    margin: 0 auto;
    padding: 12px 18px;
    display: flex;
    align-items: center;
    justify-content: space-between;
  }"""
new_header_css = """  .header-inner {
    max-width: 1100px;
    margin: 0 auto;
    padding: 10px 15px;
    display: flex;
    flex-wrap: wrap;
    align-items: center;
    justify-content: space-between;
    gap: 10px;
  }"""
index = index.replace(old_header_css, new_header_css)

old_actions_css = """  .header-actions { display: flex; align-items: center; gap: 8px; }"""
new_actions_css = """  .header-actions { display: flex; flex-wrap: wrap; align-items: center; justify-content: flex-end; gap: 6px; }"""
index = index.replace(old_actions_css, new_actions_css)

old_icon_btn = """  .icon-btn {
    background: rgba(255,255,255,0.15);
    border: none;
    color: white;
    width: 38px; height: 38px;
    border-radius: 50%;
    font-size: 18px;
    cursor: pointer;
    display: flex;
    align-items: center;
    justify-content: center;
    transition: background 0.2s;
  }"""
new_icon_btn = """  .icon-btn {
    background: rgba(255,255,255,0.15);
    border: none;
    color: white;
    width: 34px; height: 34px;
    border-radius: 50%;
    font-size: 16px;
    cursor: pointer;
    display: flex;
    align-items: center;
    justify-content: center;
    transition: background 0.2s;
  }"""
index = index.replace(old_icon_btn, new_icon_btn)

old_user_btn = """  .user-btn {
    background: rgba(255,255,255,0.15);
    border: none;
    color: white;
    padding: 0 14px;
    height: 38px;
    border-radius: 20px;
    font-size: 13px;
    font-weight: 600;
    cursor: pointer;
    display: flex;
    align-items: center;
    gap: 6px;
  }"""
new_user_btn = """  .user-btn {
    background: rgba(255,255,255,0.15);
    border: none;
    color: white;
    padding: 0 10px;
    height: 34px;
    border-radius: 20px;
    font-size: 12px;
    font-weight: 600;
    cursor: pointer;
    display: flex;
    align-items: center;
    gap: 5px;
  }"""
index = index.replace(old_user_btn, new_user_btn)

with open('index.html', 'w', encoding='utf-8') as f: f.write(index)


# === 2. FIX ADMIN DASHBOARD (Sorting & Overlap) ===
old_css_member_card = """  .member-card { display: flex; justify-content: space-between; align-items: center; background: white; padding: 15px; border-radius: 12px; margin-bottom: 10px; box-shadow: 0 2px 8px rgba(0,0,0,0.06); }
  .member-info h4 { font-size: 15px; margin-bottom: 3px; color: #333; }
  .member-info p { font-size: 12px; color: #666; }"""
new_css_member_card = """  .member-card { display: flex; justify-content: space-between; align-items: center; background: white; padding: 12px; border-radius: 12px; margin-bottom: 10px; box-shadow: 0 2px 8px rgba(0,0,0,0.06); gap: 10px; }
  .member-info { flex: 1; min-width: 0; }
  .member-info h4 { font-size: 15px; margin-bottom: 3px; color: #333; white-space: nowrap; overflow: hidden; text-overflow: ellipsis; }
  .member-info p { font-size: 12px; color: #666; white-space: nowrap; overflow: hidden; text-overflow: ellipsis; }"""
admin = admin.replace(old_css_member_card, new_css_member_card)

# 2b. Fix Sorting Logic (Newest first)
old_sorting = """        // Sort by Role
        const roleOrder = { owner: 1, admin: 2, moderator: 3, donor: 4 };
        allMembersList.sort((a, b) => (roleOrder[a.role] || 4) - (roleOrder[b.role] || 4));"""
new_sorting = """        // Sort: Owner first, then newest members first
        allMembersList.sort((a, b) => {
          if (a.role === 'owner') return -1;
          if (b.role === 'owner') return 1;
          const timeA = a.createdAt ? a.createdAt.seconds : 0;
          const timeB = b.createdAt ? b.createdAt.seconds : 0;
          return timeB - timeA;
        });"""
admin = admin.replace(old_sorting, new_sorting)

# 2c. Fix HTML template inside renderMembers
old_member_html = """          <div class="member-card">
            <div style="display:flex; align-items:center; gap:10px;">
              <img src="${m.dpUrl || 'https://cdn-icons-png.flaticon.com/512/149/149071.png'}" style="width:45px; height:45px; border-radius:50%; object-fit:cover; border:2px solid #eee;">
              <div class="member-info">"""
new_member_html = """          <div class="member-card">
            <div style="display:flex; align-items:center; gap:10px; flex:1; min-width:0;">
              <img src="${m.dpUrl || 'https://cdn-icons-png.flaticon.com/512/149/149071.png'}" style="width:45px; height:45px; border-radius:50%; object-fit:cover; border:2px solid #eee; flex-shrink:0;">
              <div class="member-info">"""
admin = admin.replace(old_member_html, new_member_html)

with open('admin.html', 'w', encoding='utf-8') as f: f.write(admin)

print("Done: Header UI and Admin Dashboard fixed.")
