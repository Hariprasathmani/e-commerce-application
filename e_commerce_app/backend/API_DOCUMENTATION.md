# MotoShowroom Backend API

Complete REST API for the MotoShowroom e-commerce platform.

## Quick Start

### 1. Setup Environment

```bash
# Create virtual environment
python -m venv venv

# Activate (Windows)
venv\Scripts\activate

# Activate (macOS/Linux)
source venv/bin/activate

# Install dependencies
pip install -r requirements.txt
```

### 2. Database Configuration

Edit `.env` file with your MongoDB URI:
```
MONGO_URI=mongodb+srv://username:password@cluster.mongodb.net/?retryWrites=true&w=majority&appName=MyCluster
```

### 3. Seed Products

```bash
python seed_products.py
```

This creates 8 sample products in the database.

### 4. Run Server

```bash
python app.py
```

Server runs at: `http://127.0.0.1:5000`

## API Endpoints Documentation

### Base URL
```
http://127.0.0.1:5000
```

### Authentication

Most endpoints require JWT token in the Authorization header:

```
Authorization: Bearer <your_jwt_token>
```

---

## Products API

### Get All Products
```
GET /products
```

**Response:**
```json
[
  {
    "_id": "ObjectId",
    "name": "Product Name",
    "price": 19999,
    "image": "https://...",
    "category": "sport",
    "description": "Product description",
    "specs": {
      "engine": "1000cc",
      "power": "150 HP"
    }
  }
]
```

### Add Product
```
POST /product
Authorization: Bearer <token>
Content-Type: application/json
```

**Request Body:**
```json
{
  "name": "Yamaha R1",
  "price": 17499,
  "image": "https://...",
  "category": "sport",
  "description": "Sports bike",
  "specs": {
    "engine": "998cc",
    "power": "197 HP"
  }
}
```

**Response:**
```json
{
  "inserted_id": "ObjectId..."
}
```

### Update Product
```
PUT /product/<id>
Authorization: Bearer <token>
Content-Type: application/json
```

**Request Body:** (any fields to update)
```json
{
  "price": 18000,
  "description": "Updated description"
}
```

**Response:**
```json
{
  "updated": 1
}
```

### Delete Product
```
DELETE /product/<id>
Authorization: Bearer <token>
```

**Response:**
```json
{
  "deleted": 1
}
```

---

## Authentication API

### Register User
```
POST /register
Content-Type: application/json
```

**Request Body:**
```json
{
  "username": "john_doe",
  "email": "john@example.com",
  "password": "password123"
}
```

**Response:**
```json
{
  "user": {
    "_id": "ObjectId",
    "username": "john_doe",
    "email": "john@example.com"
  },
  "token": "eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9..."
}
```

### Login User
```
POST /login
Content-Type: application/json
```

**Request Body:**
```json
{
  "email": "john@example.com",
  "password": "password123"
}
```

**Response:**
```json
{
  "user": {
    "_id": "ObjectId",
    "username": "john_doe",
    "email": "john@example.com"
  },
  "token": "eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9..."
}
```

### Get Current User
```
GET /user
Authorization: Bearer <token>
```

**Response:**
```json
{
  "_id": "ObjectId",
  "username": "john_doe",
  "email": "john@example.com"
}
```

---

## Orders API

### Place Order
```
POST /order
Authorization: Bearer <token>
Content-Type: application/json
```

**Request Body:**
```json
{
  "items": [
    {
      "productId": "ObjectId",
      "name": "Yamaha R1",
      "price": 17499,
      "quantity": 1
    }
  ],
  "shippingInfo": {
    "fullName": "John Doe",
    "email": "john@example.com",
    "address": "123 Main St",
    "city": "New York",
    "zip": "10001",
    "country": "USA"
  },
  "total": 17499,
  "status": "pending"
}
```

**Response:**
```json
{
  "order_id": "ObjectId..."
}
```

### Get User's Orders
```
GET /user-orders
Authorization: Bearer <token>
```

**Response:**
```json
[
  {
    "_id": "ObjectId",
    "user_id": "ObjectId",
    "items": [...],
    "shippingInfo": {...},
    "total": 17499,
    "status": "pending",
    "createdAt": "2024-01-15T10:30:00.000Z"
  }
]
```

### Get All Orders (Admin)
```
GET /orders
Authorization: Bearer <token>
```

**Response:**
```json
[
  {
    "_id": "ObjectId",
    "user_id": "ObjectId",
    "items": [...],
    "shippingInfo": {...},
    "total": 17499,
    "status": "pending",
    "createdAt": "2024-01-15T10:30:00.000Z"
  }
]
```

### Get Single Order
```
GET /order/<id>
Authorization: Bearer <token>
```

**Response:**
```json
{
  "_id": "ObjectId",
  "user_id": "ObjectId",
  "items": [...],
  "shippingInfo": {...},
  "total": 17499,
  "status": "pending",
  "createdAt": "2024-01-15T10:30:00.000Z"
}
```

---

## Error Responses

All errors return appropriate HTTP status codes:

```json
{
  "error": "Error message describing what went wrong"
}
```

**Common Status Codes:**
- `200` - Success
- `400` - Bad Request (invalid data)
- `401` - Unauthorized (missing/invalid token)
- `404` - Not Found
- `409` - Conflict (e.g., email already exists)
- `500` - Server Error

---

## Testing with cURL

### Get Products
```bash
curl http://127.0.0.1:5000/products
```

### Register User
```bash
curl -X POST http://127.0.0.1:5000/register \
  -H "Content-Type: application/json" \
  -d '{"username":"testuser","email":"test@example.com","password":"pass123"}'
```

### Login
```bash
curl -X POST http://127.0.0.1:5000/login \
  -H "Content-Type: application/json" \
  -d '{"email":"test@example.com","password":"pass123"}'
```

### Place Order (replace TOKEN with actual token)
```bash
curl -X POST http://127.0.0.1:5000/order \
  -H "Content-Type: application/json" \
  -H "Authorization: Bearer TOKEN" \
  -d '{
    "items": [{"productId":"...","name":"Bike","price":5000,"quantity":1}],
    "shippingInfo": {...},
    "total": 5000
  }'
```

---

## Testing with Postman

1. Import the API endpoints above into Postman
2. Set Base URL to `http://127.0.0.1:5000`
3. For protected endpoints, add Authorization header:
   - Type: Bearer Token
   - Token: (JWT token from login response)

---

## Security Notes

1. **Password Security**: All passwords are hashed with bcrypt (10 rounds)
2. **JWT Tokens**: Tokens expire after 7 days
3. **CORS**: Enabled for development (frontend: localhost:5500/3000)
4. **MongoDB**: Use connection string with authentication
5. **Environment Variables**: Store sensitive data in `.env`

---

## Database Models

### User Schema
```python
{
  "_id": ObjectId,
  "username": str,
  "email": str (unique),
  "password": str (hashed),
}
```

### Product Schema
```python
{
  "_id": ObjectId,
  "name": str,
  "price": float,
  "image": str,
  "category": str,
  "description": str,
  "specs": dict,
}
```

### Order Schema
```python
{
  "_id": ObjectId,
  "user_id": ObjectId,
  "items": list,
  "shippingInfo": dict,
  "total": float,
  "status": str,
  "createdAt": str (ISO format),
}
```

---

## Troubleshooting

### MongoDB Connection Error
- Check MONGO_URI in .env
- Verify IP whitelist in MongoDB Atlas
- Test connection: `python -c "from pymongo import MongoClient; ..."`

### CORS Issues
- Ensure Flask-CORS is installed
- Check frontend URL matches CORS settings
- Clear browser cache and cookies

### JWT Token Issues
- Ensure token is included in Authorization header
- Check token expiry: `exp` claim in token payload
- Verify JWT_SECRET matches in app.py

### Port Already in Use
```bash
# Kill process on port 5000
lsof -i :5000  # macOS/Linux
Get-Process -Id (Get-NetTCPConnection -LocalPort 5000).OwningProcess  # Windows
```

---

## Performance Tips

1. Index frequently queried fields in MongoDB
2. Implement pagination for large datasets
3. Use caching for product listings
4. Optimize database queries
5. Monitor API response times

---

## Version History

- **v1.0** (2024) - Initial release with core functionality

---

**Happy coding! 🏍️**
