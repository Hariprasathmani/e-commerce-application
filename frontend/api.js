// api.js

// Fetch products
async function getProducts() {
  const response = await fetch('http://127.0.0.1:5000/products');
  return response.json();
}

// Add product
async function addProduct(product) {
  const response = await fetch('http://127.0.0.1:5000/product', {
    method: 'POST',
    headers: { 'Content-Type': 'application/json' },
    body: JSON.stringify(product)
  });
  return response.json();
}

// Update product
async function updateProduct(id, updateData) {
  const response = await fetch(`http://127.0.0.1:5000/product/${id}`, {
    method: 'PUT',
    headers: { 'Content-Type': 'application/json' },
    body: JSON.stringify(updateData)
  });
  return response.json();
}

// Delete product
async function deleteProduct(id) {
  const response = await fetch(`http://127.0.0.1:5000/product/${id}`, {
    method: 'DELETE'
  });
  return response.json();
}
