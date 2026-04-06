const API_BASE = 'http://127.0.0.1:8000';

const api = {
  _token: () => localStorage.getItem('token'),

  _headers(isForm = false) {
    const h = {};
    const t = this._token();
    if (t) h['Authorization'] = `Bearer ${t}`;
    if (!isForm) h['Content-Type'] = 'application/json';
    return h;
  },

  async _req(method, path, body = null, isForm = false) {
    const opts = { method, headers: this._headers(isForm) };
    if (body) opts.body = isForm ? body : JSON.stringify(body);

    try {
      const res = await fetch(API_BASE + path, opts);
      const data = await res.json().catch(() => ({}));

      if (!res.ok) {
        throw new Error(data.detail || `HTTP ${res.status}`);
      }

      return data;
    } catch (e) {
      throw e;
    }
  },

  // ================= AUTH =================
  async login(username, password) {
    const form = new URLSearchParams();
    form.append('username', username);
    form.append('password', password);
    return this._req('POST', '/auth/login', form, true);
  },

  // ================= USERS =================
  async register(data)        { return this._req('POST', '/users/register', data); },
  async getMe()               { return this._req('GET',  '/users/me'); },
  async updateMe(data)        { return this._req('PUT',  '/users/me', data); },

  // ✅ FIXED FUNCTION
  async getAllUsers()         { return this._req('GET',  '/users/'); },

  async updateUser(id, data)  { return this._req('PUT',  `/users/${id}` , data); },
  async deleteUser(id)        { return this._req('DELETE', `/users/${id}`); },

  // ================= TRANSACTIONS =================
  async getTransactions(params = {}) {
    const q = new URLSearchParams(params).toString();
    const res = await this._req('GET', `/transactions${q ? '?' + q : ''}`);
    return res.transactions || res || [];
  },

  async createTransaction(data)     { return this._req('POST', '/transactions', data); },
  async updateTransaction(id, data) { return this._req('PUT', `/transactions/${id}`, data); },
  async deleteTransaction(id)       { return this._req('DELETE', `/transactions/${id}`); },

  // ================= BUDGET =================
  async getBudgets()           { return this._req('GET', '/budget'); },
  async createBudget(data)     { return this._req('POST', '/budget', data); },
  async updateBudget(id, data) { return this._req('PUT', `/budget/${id}`, data); },
  async deleteBudget(id)       { return this._req('DELETE', `/budget/${id}`); },

  // ================= SUMMARY =================
  async getSummary() {
    return this._req('GET', '/summary');
  },
};

// ✅ VERY IMPORTANT (fixes your error)
window.api = api;