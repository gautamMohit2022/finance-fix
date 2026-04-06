const utils = {
  // Format currency
  currency(amount, symbol = '₹') {
    const n = parseFloat(amount) || 0;
    return symbol + n.toLocaleString('en-IN', { minimumFractionDigits: 2, maximumFractionDigits: 2 });
  },

  // Format date
  date(d) {
    if (!d) return '—';
    return new Date(d).toLocaleDateString('en-IN', { day: '2-digit', month: 'short', year: 'numeric' });
  },

  // Relative time
  relTime(d) {
    if (!d) return '';
    const diff = Date.now() - new Date(d).getTime();
    const mins = Math.floor(diff / 60000);
    if (mins < 1)  return 'Just now';
    if (mins < 60) return `${mins}m ago`;
    const hrs = Math.floor(mins / 60);
    if (hrs < 24) return `${hrs}h ago`;
    const days = Math.floor(hrs / 24);
    if (days < 7)  return `${days}d ago`;
    return this.date(d);
  },

  // Category colors
  catColor(cat) {
    const map = {
      food:'#FF8C42', rent:'#4F8EF7', salary:'#00E5B0', travel:'#9B6DFF',
      shopping:'#FF5C7C', health:'#FFB830', education:'#00D4FF', entertainment:'#FF6B6B',
      utilities:'#6BCB77', investment:'#FFD166', other:'#8B95B0'
    };
    return map[(cat||'').toLowerCase()] || '#8B95B0';
  },

  // Category icons
  catIcon(cat) {
    const map = {
      food:'🍕', rent:'🏠', salary:'💼', travel:'✈️', shopping:'🛍️',
      health:'🏥', education:'📚', entertainment:'🎬', utilities:'⚡',
      investment:'📈', other:'📌'
    };
    return map[(cat||'').toLowerCase()] || '📌';
  },

  // Toast notifications
  toast(msg, type = 'success') {
    let container = document.querySelector('.toast-container');
    if (!container) {
      container = document.createElement('div');
      container.className = 'toast-container';
      document.body.appendChild(container);
    }
    const icons = { success:'✅', error:'❌', warning:'⚠️', info:'ℹ️' };
    const toast = document.createElement('div');
    toast.className = `toast ${type}`;
    toast.innerHTML = `<span class="toast-icon">${icons[type]||'ℹ️'}</span><span class="toast-msg">${msg}</span>`;
    container.appendChild(toast);
    requestAnimationFrame(() => toast.classList.add('show'));
    setTimeout(() => {
      toast.classList.replace('show','hide');
      setTimeout(() => toast.remove(), 400);
    }, 3500);
  },

  // Confirm dialog (uses browser confirm for simplicity)
  async confirm(msg) { return window.confirm(msg); },

  // Truncate text
  truncate(str, len = 30) {
    if (!str) return '';
    return str.length > len ? str.slice(0, len) + '...' : str;
  },

  // Debounce
  debounce(fn, ms = 300) {
    let t;
    return (...args) => { clearTimeout(t); t = setTimeout(() => fn(...args), ms); };
  },

  // Format percent
  percent(val, total) {
    if (!total) return 0;
    return Math.min(100, Math.round((val / total) * 100));
  },

  // Progress color
  progressColor(pct) {
    if (pct >= 90) return 'var(--expense)';
    if (pct >= 70) return 'var(--warning)';
    return 'var(--income)';
  },

  // Month name
  monthName(n) {
    return ['Jan','Feb','Mar','Apr','May','Jun','Jul','Aug','Sep','Oct','Nov','Dec'][n] || '';
  },

  // Set loading state on button
  setLoading(btn, loading) {
    if (loading) {
      btn.dataset.orig = btn.innerHTML;
      btn.innerHTML = '<span class="spinner"></span>';
      btn.disabled = true;
    } else {
      btn.innerHTML = btn.dataset.orig || btn.innerHTML;
      btn.disabled = false;
    }
  },

  // Sidebar toggle
  initSidebar() {
    const toggle = document.getElementById('menuToggle');
    const sidebar = document.querySelector('.sidebar');
    const overlay = document.getElementById('sidebarOverlay');
    if (toggle && sidebar) {
      toggle.addEventListener('click', () => {
        sidebar.classList.toggle('open');
        if (overlay) overlay.classList.toggle('show');
      });
    }
    if (overlay) {
      overlay.addEventListener('click', () => {
        sidebar.classList.remove('open');
        overlay.classList.remove('show');
      });
    }
  }
};
