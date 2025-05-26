const api = "http://127.0.0.1:5000";

document.getElementById("productForm").onsubmit = async function (e) {
  e.preventDefault();
  const name = document.getElementById("name").value;
  const price = parseFloat(document.getElementById("price").value);
  const category = document.getElementById("category").value;

  await fetch(`${api}/product`, {
    method: "POST",
    headers: { "Content-Type": "application/json" },
    body: JSON.stringify({ name, price, category })
  });

  this.reset();
  loadProducts();
};

async function loadProducts() {
  const res = await fetch(`${api}/products`);
  const products = await res.json();
  const container = document.getElementById("products");
  container.innerHTML = "";

  products.forEach(p => {
    const div = document.createElement("div");
    div.className = "product";
    div.innerHTML = `
      <strong>${p.name}</strong><br>
      ₹${p.price}<br>
      ${p.category}<br>
      <button onclick="editProduct('${p._id}', '${p.name}', '${p.price}', '${p.category}')">Edit</button>
      <button onclick="deleteProduct('${p._id}')">Delete</button>
    `;
    container.appendChild(div);
  });
}

async function deleteProduct(id) {
  await fetch(`${api}/product/${id}`, { method: "DELETE" });
  loadProducts();
}

function editProduct(id, name, price, category) {
  const newName = prompt("Name", name);
  const newPrice = parseFloat(prompt("Price", price));
  const newCategory = prompt("Category", category);

  fetch(`${api}/product/${id}`, {
    method: "PUT",
    headers: { "Content-Type": "application/json" },
    body: JSON.stringify({ name: newName, price: newPrice, category: newCategory })
  }).then(() => loadProducts());
}

loadProducts();
