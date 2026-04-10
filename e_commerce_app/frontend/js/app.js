/**
 * MotoShowroom — Complete Frontend App Controller
 * Handles: Auth, Cart, Products, Orders, UI
 */

const API = 'http://127.0.0.1:5000';

// ─────────────────────────────────────────────
// TOAST NOTIFICATIONS
// ─────────────────────────────────────────────
function showToast(message, type = 'success') {
  const container = document.getElementById('toast-container');
  if (!container) return;
  const icons = { success: '✅', error: '❌', warning: '⚠️', info: 'ℹ️' };
  const toast = document.createElement('div');
  toast.className = `toast ${type !== 'success' ? type : ''}`;
  toast.innerHTML = `
    <span class="toast-icon">${icons[type] || icons.success}</span>
    <span class="toast-msg">${message}</span>
  `;
  container.appendChild(toast);
  setTimeout(() => {
    toast.classList.add('removing');
    setTimeout(() => toast.remove(), 300);
  }, 3500);
}

// ─────────────────────────────────────────────
// CART
// ─────────────────────────────────────────────
const Cart = {
  items: [],
  init() {
    try { this.items = JSON.parse(localStorage.getItem('moto_cart')) || []; } catch { this.items = []; }
    this.updateBadge();
  },
  save() {
    localStorage.setItem('moto_cart', JSON.stringify(this.items));
    this.updateBadge();
  },
  addItem(product) {
    const exist = this.items.find(i => i._id === product._id);
    if (exist) { exist.quantity += 1; }
    else { this.items.push({ ...product, quantity: 1 }); }
    this.save();
    showToast(`🛒 ${product.name} added to cart!`);
  },
  removeItem(id) {
    this.items = this.items.filter(i => i._id !== id);
    this.save();
  },
  updateQty(id, qty) {
    const item = this.items.find(i => i._id === id);
    if (item) { item.quantity = Math.max(1, parseInt(qty) || 1); this.save(); }
  },
  clear() { this.items = []; this.save(); },
  getTotal() { return this.items.reduce((s, i) => s + i.price * i.quantity, 0); },
  getCount() { return this.items.reduce((s, i) => s + i.quantity, 0); },
  updateBadge() {
    document.querySelectorAll('.cart-count').forEach(el => el.textContent = this.getCount());
  }
};

// ─────────────────────────────────────────────
// AUTH
// ─────────────────────────────────────────────
const Auth = {
  user: null,
  token: null,
  init() {
    try {
      this.user = JSON.parse(localStorage.getItem('moto_user'));
      this.token = localStorage.getItem('moto_token');
    } catch { this.user = null; this.token = null; }
    this.updateNav();
  },
  isLoggedIn() { return !!this.token && !!this.user; },
  setUser(user, token) {
    this.user = user;
    this.token = token;
    localStorage.setItem('moto_user', JSON.stringify(user));
    localStorage.setItem('moto_token', token);
    this.updateNav();
  },
  logout() {
    this.user = null;
    this.token = null;
    localStorage.removeItem('moto_user');
    localStorage.removeItem('moto_token');
    Cart.clear();
    this.updateNav();
    showToast('You have been logged out.', 'info');
    setTimeout(() => { window.location.href = 'landing.html'; }, 1000);
  },
  async login(email, password) {
    const res = await fetch(`${API}/login`, {
      method: 'POST',
      headers: { 'Content-Type': 'application/json' },
      body: JSON.stringify({ email, password })
    });
    const data = await res.json();
    if (!res.ok) throw new Error(data.error || 'Login failed');
    this.setUser(data.user, data.token);
    return data.user;
  },
  async register(username, email, password) {
    const res = await fetch(`${API}/register`, {
      method: 'POST',
      headers: { 'Content-Type': 'application/json' },
      body: JSON.stringify({ username, email, password })
    });
    const data = await res.json();
    if (!res.ok) throw new Error(data.error || 'Registration failed');
    this.setUser(data.user, data.token);
    return data.user;
  },
  updateNav() {
    const area = document.getElementById('auth-nav-area');
    if (!area) return;
    if (this.isLoggedIn()) {
      const name = this.user.username || this.user.email.split('@')[0];
      area.innerHTML = `
        <div class="user-menu">
          <button class="user-btn" id="user-btn" onclick="toggleUserMenu()">
            👤 ${name} ▾
          </button>
          <div class="user-dropdown" id="user-dropdown">
            <a href="orders.html">📦 My Orders</a>
            ${this.user.isAdmin ? '<a href="admin.html">⚙️ Admin Panel</a>' : ''}
            <button onclick="Auth.logout()">🚪 Sign Out</button>
          </div>
        </div>`;
    } else {
      area.innerHTML = `
        <a href="login.html" class="btn btn-outline btn-sm" style="border-color:rgba(255,255,255,0.4);color:white;font-size:0.85rem;">Sign In</a>
        <a href="register.html" class="btn btn-primary btn-sm" style="margin-left:0.5rem;font-size:0.85rem;">Sign Up</a>`;
    }
  }
};

function toggleUserMenu() {
  document.getElementById('user-dropdown')?.classList.toggle('open');
}
document.addEventListener('click', e => {
  if (!e.target.closest('.user-menu')) {
    document.getElementById('user-dropdown')?.classList.remove('open');
  }
});

// ─────────────────────────────────────────────
// API HELPERS
// ─────────────────────────────────────────────
async function fetchProducts() {
  try {
    const res = await fetch(`${API}/products`);
    if (!res.ok) throw new Error('Failed to fetch products');
    return await res.json();
  } catch (err) {
    console.error('fetchProducts:', err);
    return [];
  }
}

async function placeOrder(items, shippingInfo) {
  if (!Auth.isLoggedIn()) {
    showToast('Please sign in to place an order', 'warning');
    setTimeout(() => window.location.href = 'login.html', 1000);
    return null;
  }
  const res = await fetch(`${API}/order`, {
    method: 'POST',
    headers: {
      'Content-Type': 'application/json',
      'Authorization': `Bearer ${Auth.token}`
    },
    body: JSON.stringify({
      items: items.map(i => ({ productId: i._id, name: i.name, price: i.price, quantity: i.quantity, image: i.image })),
      shippingInfo,
      total: Cart.getTotal(),
      status: 'confirmed'
    })
  });
  const data = await res.json();
  if (!res.ok) throw new Error(data.error || 'Order failed');
  return data.order_id;
}

async function getUserOrders() {
  if (!Auth.isLoggedIn()) return [];
  try {
    const res = await fetch(`${API}/user-orders`, {
      headers: { 'Authorization': `Bearer ${Auth.token}` }
    });
    // If endpoint returns 404 or similar, fallback to /orders
    if (!res.ok) return [];
    return await res.json();
  } catch { return []; }
}

// ─────────────────────────────────────────────
// PRODUCT CARD RENDERER
// ─────────────────────────────────────────────
function renderProductCard(p) {
  const price = typeof p.price === 'number' ? p.price.toLocaleString('en-US', { minimumFractionDigits: 2 }) : p.price;
  const category = (p.category || '').charAt(0).toUpperCase() + (p.category || '').slice(1);
  return `
    <div class="product-card" onclick="openProductModal('${p._id}')">
      <div class="product-img-wrap">
        <img class="product-img" src="${p.image || 'https://images.unsplash.com/photo-1558981806-ec527fa84c39?auto=format&fit=crop&w=600&q=80'}"
             alt="${p.name}" loading="lazy">
        <div class="product-badge">${category}</div>
        <div class="product-overlay">
          <button class="btn btn-primary btn-sm" onclick="event.stopPropagation(); addToCart('${p._id}')">Quick Add 🛒</button>
        </div>
      </div>
      <div class="product-info">
        <div class="product-category">${category}</div>
        <div class="product-name">${p.name}</div>
        <div class="product-desc">${p.description || ''}</div>
        <div class="product-footer">
          <div class="product-price">$${price}</div>
          <button class="add-to-cart-btn" onclick="event.stopPropagation(); addToCart('${p._id}')">Add to Cart</button>
        </div>
      </div>
    </div>`;
}

// ─────────────────────────────────────────────
// PRODUCT MODAL
// ─────────────────────────────────────────────
let allProducts = [];

async function openProductModal(productId) {
  let product = allProducts.find(p => p._id === productId);
  if (!product) {
    const prods = await fetchProducts();
    product = prods.find(p => p._id === productId);
  }
  if (!product) return;

  const modal = document.getElementById('product-modal');
  if (!modal) return;

  const price = typeof product.price === 'number' ? product.price.toLocaleString('en-US', { minimumFractionDigits: 2 }) : product.price;
  const specs = product.specs ? Object.entries(product.specs).map(([k,v]) => `
    <div class="pm-spec-row">
      <span class="pm-spec-key">${k.charAt(0).toUpperCase() + k.slice(1)}</span>
      <span class="pm-spec-val">${v}</span>
    </div>`).join('') : '';

  modal.querySelector('.pm-img').src = product.image || '';
  modal.querySelector('.pm-img').alt = product.name;
  modal.querySelector('.pm-category').textContent = product.category || '';
  modal.querySelector('.pm-name').textContent = product.name;
  modal.querySelector('.pm-price').textContent = `$${price}`;
  modal.querySelector('.pm-desc').textContent = product.description || 'No description available.';
  modal.querySelector('.pm-specs-list').innerHTML = specs || '<p style="color:var(--text-light);font-size:0.9rem;">No specs available.</p>';
  modal.querySelector('.pm-add-btn').onclick = () => { addToCart(product._id); closeProductModal(); };
  modal.classList.add('open');
  document.body.style.overflow = 'hidden';
}

function closeProductModal() {
  const modal = document.getElementById('product-modal');
  modal?.classList.remove('open');
  document.body.style.overflow = '';
}

// ─────────────────────────────────────────────
// ADD TO CART
// ─────────────────────────────────────────────
async function addToCart(productId) {
  let product = allProducts.find(p => p._id === productId);
  if (!product) {
    const prods = await fetchProducts();
    allProducts = prods;
    product = prods.find(p => p._id === productId);
  }
  if (product) { Cart.addItem(product); }
}

// ─────────────────────────────────────────────
// CART PANEL
// ─────────────────────────────────────────────
function openCart() {
  renderCartPanel();
  document.getElementById('cart-overlay').classList.add('open');
  document.body.style.overflow = 'hidden';
}
function closeCart() {
  document.getElementById('cart-overlay').classList.remove('open');
  document.body.style.overflow = '';
}

function renderCartPanel() {
  const body = document.getElementById('cart-body');
  if (!body) return;
  if (Cart.items.length === 0) {
    body.innerHTML = `
      <div class="cart-empty">
        <div class="cart-empty-icon">🛒</div>
        <h3>Your cart is empty</h3>
        <p>Browse our amazing motorcycle collection!</p>
        <a href="index.html" class="btn btn-primary mt-2" style="margin-top:1rem;" onclick="closeCart()">Shop Now</a>
      </div>`;
  } else {
    body.innerHTML = Cart.items.map(item => `
      <div class="cart-item">
        <img class="cart-item-img" src="${item.image}" alt="${item.name}">
        <div class="cart-item-info">
          <div class="cart-item-name">${item.name}</div>
          <div class="cart-item-price">$${(item.price * item.quantity).toLocaleString('en-US',{minimumFractionDigits:2})}</div>
          <div class="cart-qty-controls">
            <button class="qty-btn" onclick="cartQty('${item._id}', ${item.quantity - 1})">−</button>
            <span class="qty-value">${item.quantity}</span>
            <button class="qty-btn" onclick="cartQty('${item._id}', ${item.quantity + 1})">+</button>
          </div>
        </div>
        <button class="cart-item-remove" onclick="cartRemove('${item._id}')">🗑</button>
      </div>`).join('');
  }

  // Update totals
  const subtotal = Cart.getTotal();
  const tax = subtotal * 0.1;
  const totalEl = document.getElementById('cart-total-amount');
  const subtotalEl = document.getElementById('cart-subtotal');
  const taxEl = document.getElementById('cart-tax');
  if (totalEl) totalEl.textContent = `$${(subtotal + tax).toLocaleString('en-US',{minimumFractionDigits:2})}`;
  if (subtotalEl) subtotalEl.textContent = `$${subtotal.toLocaleString('en-US',{minimumFractionDigits:2})}`;
  if (taxEl) taxEl.textContent = `$${tax.toLocaleString('en-US',{minimumFractionDigits:2})}`;
}

function cartQty(id, qty) {
  if (qty < 1) { cartRemove(id); return; }
  Cart.updateQty(id, qty);
  renderCartPanel();
}
function cartRemove(id) {
  Cart.removeItem(id);
  renderCartPanel();
  showToast('Item removed from cart', 'info');
}

function goToCheckout() {
  if (Cart.items.length === 0) { showToast('Your cart is empty!', 'warning'); return; }
  if (!Auth.isLoggedIn()) {
    showToast('Please sign in to checkout', 'warning');
    setTimeout(() => window.location.href = 'login.html?redirect=checkout.html', 800);
    return;
  }
  closeCart();
  window.location.href = 'checkout.html';
}

// ─────────────────────────────────────────────
// HAMBURGER MENU
// ─────────────────────────────────────────────
function initHamburger() {
  const btn = document.getElementById('hamburger');
  const nav = document.getElementById('main-nav');
  if (!btn || !nav) return;
  btn.addEventListener('click', () => {
    nav.classList.toggle('open');
  });
  document.addEventListener('click', e => {
    if (!e.target.closest('#hamburger') && !e.target.closest('#main-nav')) {
      nav.classList.remove('open');
    }
  });
}

// ─────────────────────────────────────────────
// PAGE LOADER
// ─────────────────────────────────────────────
function hideLoader() {
  const loader = document.getElementById('page-loader');
  if (loader) {
    setTimeout(() => loader.classList.add('hidden'), 800);
  }
}

// ─────────────────────────────────────────────
// INIT
// ─────────────────────────────────────────────
document.addEventListener('DOMContentLoaded', () => {
  Cart.init();
  Auth.init();
  initHamburger();
  hideLoader();

  // Cart overlay click to close
  const cartOverlay = document.getElementById('cart-overlay');
  if (cartOverlay) {
    cartOverlay.addEventListener('click', e => {
      if (e.target === cartOverlay) closeCart();
    });
  }

  // Product modal click to close
  const productModal = document.getElementById('product-modal');
  if (productModal) {
    productModal.addEventListener('click', e => {
      if (e.target === productModal) closeProductModal();
    });
  }
});
