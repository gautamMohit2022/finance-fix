const auth = {

  // ================= SAVE / GET =================
  save(token, user) {
    localStorage.setItem('token', token);
    localStorage.setItem('user', JSON.stringify(user));
  },

  getToken() {
    return localStorage.getItem('token');
  },

  getUser() {
    try {
      return JSON.parse(localStorage.getItem('user')) || {};
    } catch {
      return {};
    }
  },

  isLoggedIn() {
    return !!this.getToken();
  },

  // ================= LOGOUT =================
  logout() {
    localStorage.removeItem('token');
    localStorage.removeItem('user');
    window.location.href = '../pages/login.html';
  },

  // ================= AUTH CHECK =================
  requireAuth() {
    if (!this.isLoggedIn()) {
      window.location.href = '../pages/login.html';
      return false;
    }
    return true;
  },

  // ================= ROLE-BASED UI =================
  handleRoleUI() {
    const user = this.getUser();
    const role = user.role || 'viewer';

    // 🔒 Always wait for DOM
    document.addEventListener("DOMContentLoaded", () => {

      // ===== Hide everything first =====
      document.querySelectorAll('.nav-users').forEach(el => el.style.display = 'none');
      document.querySelectorAll('.nav-analytics').forEach(el => el.style.display = 'none');

      // ===== ROLE LOGIC =====

      // ADMIN → full access
      if (role === 'admin') {
        document.querySelectorAll('.nav-users').forEach(el => el.style.display = '');
        document.querySelectorAll('.nav-analytics').forEach(el => el.style.display = '');
      }

      // ANALYST → users + analytics (view only)
      else if (role === 'analyst') {
        document.querySelectorAll('.nav-users').forEach(el => el.style.display = '');
        document.querySelectorAll('.nav-analytics').forEach(el => el.style.display = '');
      }

      // VIEWER → no extra access

    });
  },

  // ================= INIT UI =================
  initUserUI() {
    const user = this.getUser();

    document.addEventListener("DOMContentLoaded", () => {

      const nameEl = document.getElementById('userName');
      const roleEl = document.getElementById('userRole');
      const avatarEl = document.getElementById('userAvatar');

      if (nameEl) nameEl.textContent = user.full_name || user.email || 'User';
      if (roleEl) roleEl.textContent = user.role || 'Member';
      if (avatarEl) {
        avatarEl.textContent =
          (user.full_name || user.email || 'U')[0].toUpperCase();
      }

      // Apply role-based UI
      this.handleRoleUI();
    });
  }
};

// ✅ GLOBAL ACCESS
window.auth = auth;