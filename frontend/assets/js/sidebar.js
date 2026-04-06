const Sidebar = {
  init() {
    const user = auth.getUser();
    const role = user.role || 'viewer';

    // ===== STEP 1: HIDE EVERYTHING FIRST =====
    document.querySelectorAll('.nav-users').forEach(el => el.style.display = 'none');
    document.querySelectorAll('.nav-analytics').forEach(el => el.style.display = 'none');
    document.querySelectorAll('.sidebar-users-section').forEach(el => el.style.display = 'none');

    // ===== STEP 2: ROLE-BASED VISIBILITY =====

    // ✅ ADMIN → full access
    if (role === 'admin') {
      document.querySelectorAll('.nav-users').forEach(el => el.style.display = '');
      document.querySelectorAll('.nav-analytics').forEach(el => el.style.display = '');
      document.querySelectorAll('.sidebar-users-section').forEach(el => el.style.display = '');

      this.loadUsers(); // only admin loads sidebar users
    }

    // ✅ ANALYST → view users + analytics (no sidebar list)
    else if (role === 'analyst') {
      document.querySelectorAll('.nav-users').forEach(el => el.style.display = '');
      document.querySelectorAll('.nav-analytics').forEach(el => el.style.display = '');
    }

    // ❌ VIEWER → nothing extra (default hidden)

    // ===== STEP 3: SEARCH =====
    const ss = document.getElementById('sidebarSearch');
    if (ss) {
      ss.addEventListener('input', utils.debounce(e => {
        const q = e.target.value.trim();
        if (q.length > 1) {
          window.location.href = `transaction.html?search=${encodeURIComponent(q)}`;
        }
      }, 400));
    }

    // ===== STEP 4: INIT SIDEBAR UI =====
    utils.initSidebar();
  },

  async loadUsers() {
    try {
      const users = await api.getAllUsers();

      // Update count
      const countEl = document.getElementById('userCount');
      if (countEl) countEl.textContent = users.length;

      // Sidebar list
      const listEl = document.getElementById('sidebarUserList');
      if (!listEl) return;

      listEl.innerHTML = users.slice(0, 8).map(u => `
        <div class="su-item">
          <div class="su-av ${u.role}">
            ${(u.full_name || u.email || 'U')[0].toUpperCase()}
          </div>

          <div style="flex:1;min-width:0">
            <div class="su-name">
              ${u.full_name || u.username || '—'}
            </div>
            <div class="su-role">${u.email}</div>
          </div>

          <span class="su-badge ${u.role}">
            ${u.role}
          </span>
        </div>
      `).join('');

    } catch (e) {
      console.log("Sidebar users load failed:", e.message);
    }
  }
};