const bikes = [
  { id:1, name:"Ducati Panigale V4", category:"sport", description:"Superbike with cutting-edge performance.", price:25000, image:"https://images.pexels.com/photos/11537018/pexels-photo-11537018.jpeg" },
  { id:2, name:"Royal Enfield Classic 350", category:"vintage", description:"Iconic vintage motorcycle with modern reliability.", price:5500, image:"https://images.pexels.com/photos/13600185/pexels-photo-13600185.jpeg" },
  { id:3, name:"Harley Davidson Fat Boy", category:"cruiser", description:"Premium cruiser for ultimate comfort and power.", price:18000, image:"https://images.pexels.com/photos/7509255/pexels-photo-7509255.jpeg" },
  { id:4, name:"Zero SR/F", category:"electric", description:"Electric powerhouse with futuristic design.", price:20000, image:"https://images.pexels.com/photos/30396826/pexels-photo-30396826.jpeg" },
  { id:5, name:"Kawasaki Ninja ZX-10R", category:"sport", description:"Track-focused superbike for thrill seekers.", price:16000, image:"https://images.pexels.com/photos/1905744/pexels-photo-1905744.jpeg" },
  { id:6, name:"Triumph Bonneville T100", category:"vintage", description:"Retro style blended with modern performance.", price:11000, image:"https://images.pexels.com/photos/14442771/pexels-photo-14442771.jpeg" },
  { id:7, name:"BMW R 1250 GS", category:"cruiser", description:"Versatile touring bike for long adventures.", price:21000, image:"https://images.pexels.com/photos/13029163/pexels-photo-13029163.jpeg" },
  { id:8, name:"Energica Ego", category:"electric", description:"High-speed electric superbike with sleek looks.", price:23000, image:"https://images.pexels.com/photos/2868248/pexels-photo-2868248.jpeg" },
];

let filteredBikes = [...bikes];
let cart = [];

const bikeListEl = document.getElementById("bikeList");
const searchInput = document.getElementById("searchInput");
const categoryFilter = document.getElementById("categoryFilter");
const cartBtn = document.getElementById("cartBtn");
const cartCount = document.getElementById("cartCount");

const bikeModal = document.getElementById("bikeModal");
const modalImg = document.getElementById("modalImg");
const modalName = document.getElementById("modalName");
const modalDesc = document.getElementById("modalDesc");
const modalPrice = document.getElementById("modalPrice");
const addToCartBtn = document.getElementById("addToCartBtn");
const closeModal = document.getElementById("closeModal");

const cartModal = document.getElementById("cartModal");
const cartItemsEl = document.getElementById("cartItems");
const cartTotal = document.getElementById("cartTotal");
const closeCart = document.getElementById("closeCart");
const checkoutBtn = document.getElementById("checkoutBtn");

let currentBikeId = null;

function renderBikes() {
  bikeListEl.innerHTML = "";
  if (!filteredBikes.length) {
    bikeListEl.innerHTML = "<p>No bikes found.</p>";
    return;
  }
  filteredBikes.forEach(bike => {
    const card = document.createElement("div");
    card.className = "product-card";
    card.innerHTML = `
      <img src="${bike.image}" alt="${bike.name}">
      <h3>${bike.name}</h3>
      <p>$${bike.price}</p>
    `;
    card.addEventListener("click", () => openBikeModal(bike.id));
    bikeListEl.appendChild(card);
  });
}

function openBikeModal(id) {
  const bike = bikes.find(b => b.id === id);
  if (!bike) return;
  currentBikeId = id;
  modalImg.src = bike.image;
  modalName.textContent = bike.name;
  modalDesc.textContent = bike.description;
  modalPrice.textContent = `$${bike.price}`;
  bikeModal.classList.remove("hidden");
}

closeModal.addEventListener("click", () => bikeModal.classList.add("hidden"));

addToCartBtn.addEventListener("click", () => {
  const bike = bikes.find(b => b.id === currentBikeId);
  if (!bike) return;
  const existing = cart.find(item => item.id === bike.id);
  if (existing) existing.quantity++;
  else cart.push({ ...bike, quantity: 1 });
  updateCartCount();
  alert(`${bike.name} added to cart!`);
  bikeModal.classList.add("hidden");
});

function updateCartCount() {
  cartCount.textContent = cart.reduce((sum, i) => sum + i.quantity, 0);
}

function filterBikes() {
  const term = searchInput.value.toLowerCase();
  const cat = categoryFilter.value;
  filteredBikes = bikes.filter(b => {
    return b.name.toLowerCase().includes(term) && (cat ? b.category === cat : true);
  });
  renderBikes();
}

cartBtn.addEventListener("click", () => {
  renderCart();
  cartModal.classList.remove("hidden");
});
closeCart.addEventListener("click", () => cartModal.classList.add("hidden"));

function renderCart() {
  cartItemsEl.innerHTML = "";
  if (!cart.length) {
    cartItemsEl.innerHTML = "<p>Your cart is empty.</p>";
    cartTotal.textContent = "0";
    return;
  }
  let total = 0;
  cart.forEach((item, i) => {
    total += item.price * item.quantity;
    const div = document.createElement("div");
    div.innerHTML = `${item.name} (x${item.quantity}) - $${(item.price * item.quantity).toFixed(2)}
    <button data-index="${i}">Remove</button>`;
    div.querySelector("button").addEventListener("click", e => {
      cart.splice(e.target.dataset.index, 1);
      updateCartCount();
      renderCart();
    });
    cartItemsEl.appendChild(div);
  });
  cartTotal.textContent = total.toFixed(2);
}

checkoutBtn.addEventListener("click", () => {
  if (!cart.length) return alert("Cart is empty!");
  alert("Checkout feature coming soon!");
});

searchInput.addEventListener("input", filterBikes);
categoryFilter.addEventListener("change", filterBikes);

renderBikes();
updateCartCount();
