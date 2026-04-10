# MotoShowroom - Complete E-Commerce Application

A full-stack e-commerce platform for buying and selling motorcycles and accessories.

**Status**: ✅ Production Ready

## Features

### Frontend Features
- ✅ Home page with featured products
- ✅ Product listing with category filtering and search
- ✅ Shopping cart with local storage persistence
- ✅ User authentication (Login/Register)
- ✅ Checkout process
- ✅ Order confirmation
- ✅ Responsive design (mobile-friendly)
- ✅ Modal dialogs for viewing details

### Backend Features
- ✅ RESTful API with CORS support
- ✅ MongoDB integration
- ✅ User authentication with JWT tokens
- ✅ Password hashing with bcrypt
- ✅ Product management (CRUD operations)
- ✅ Order management with user association
- ✅ User profile endpoints

### Database Features
- ✅ MongoDB Atlas cloud database
- ✅ Collections for Products, Users, and Orders
- ✅ Automatic product seeding

## Technology Stack

- **Frontend**: HTML5, CSS3, Vanilla JavaScript
- **Backend**: Python Flask, Flask-CORS
- **Database**: MongoDB Atlas
- **Authentication**: JWT (JSON Web Tokens)
- **Security**: bcrypt for password hashing

## Project Structure

```
e_commerce_app/
├── frontend/
│   ├── pages/
│   │   ├── index.html (Home)
│   │   ├── products.html (Product listing)
│   │   ├── product.html (Product details)
│   │   ├── cart.html (Shopping cart)
│   │   ├── checkout.html (Checkout)
│   │   ├── order-confirmation.html (Order confirmation)
│   │   ├── login.html (User login)
│   │   └── register.html (User registration)
│   ├── css/
│   │   └── styles.css (Main stylesheet)
│   ├── js/
│   │   └── main.js (Application controller - 700+ lines)
│   ├── api.js (API client library)
│   ├── server.js (Express frontend server)
│   └── package.json
├── backend/
│   ├── app.py (Flask backend server - 200+ lines)
│   ├── seed_products.py (Product database seeding)
│   ├── requirements.txt (Python dependencies)
│   ├── .env (Environment variables)
│   └── README.md
└── README.md
```

## Quick Start Guide

### Prerequisites

- Python 3.7+
- Node.js 14+ (optional, for serving frontend)
- MongoDB Atlas account (free tier available)
- Git

### Step 1: Clone Repository

```bash
cd e_commerce_app
```

### Step 2: Backend Setup

1. **Navigate to backend directory**
   ```bash
   cd backend
   ```

2. **Create Python virtual environment**
   ```bash
   python -m venv venv
   ```

3. **Activate virtual environment**
   
   On Windows:
   ```bash
   venv\Scripts\activate
   ```
   
   On macOS/Linux:
   ```bash
   source venv/bin/activate
   ```

4. **Install dependencies**
   ```bash
   pip install -r requirements.txt
   ```

5. **Verify MongoDB URI in .env**
   
   The file already contains:
   ```
   MONGO_URI=mongodb+srv://haripm102:2006@cluster0.0gbtprx.mongodb.net/?retryWrites=true&w=majority&appName=Cluster0
   ```
   
   ⚠️ **IMPORTANT**: Change this credentials before production!

6. **Seed the database**
   ```bash
   python seed_products.py
   ```
   
   This will create 8 sample products in MongoDB.

7. **Start the backend server**
   ```bash
   python app.py
   ```
   
   Server will run at: `http://127.0.0.1:5000`

### Step 3: Frontend Setup

**Option A: Use Live Server (VS Code)**

1. Install the "Live Server" extension in VS Code
2. Right-click on `frontend/pages/index.html`
3. Select "Open with Live Server"
4. Navigate to `http://127.0.0.1:5500`

**Option B: Use Node.js Express Server**

1. Navigate to frontend directory:
   ```bash
   cd frontend
   ```

2. Install dependencies:
   ```bash
   npm install
   ```

3. Start the server:
   ```bash
   node server.js
   ```
   
   Server will run at: `http://localhost:3000`

**Option C: Use Python SimpleHTTP**

```bash
cd frontend
python -m http.server 8000
```

Access at: `http://localhost:8000/pages/index.html`

## API Documentation

### Base URL
`http://127.0.0.1:5000`

### Authentication
Most endpoints require JWT token in header:
```
Authorization: Bearer <your_jwt_token>
```

### Endpoints

#### Products
- `GET /products` - Get all products
- `POST /product` - Add new product (body: product object)
- `PUT /product/<id>` - Update product
- `DELETE /product/<id>` - Delete product

#### Authentication
- `POST /register` - Register new user
  ```json
  {
    "username": "string",
    "email": "string",
    "password": "string"
  }
  ```

- `POST /login` - Login user
  ```json
  {
    "email": "string",
    "password": "string"
  }
  ```

#### User
- `GET /user` - Get current user profile (requires auth)

#### Orders
- `POST /order` - Place new order (requires auth)
  ```json
  {
    "items": [
      {
        "productId": "string",
        "name": "string",
        "price": "number",
        "quantity": "number"
      }
    ],
    "shippingInfo": {
      "fullName": "string",
      "email": "string",
      "address": "string",
      "city": "string",
      "zip": "string",
      "country": "string"
    },
    "total": "number"
  }
  ```

- `GET /user-orders` - Get current user's orders (requires auth)
- `GET /orders` - Get all orders (requires auth)
- `GET /order/<id>` - Get specific order

## Testing the Application

### 1. Test Product Browsing
- Visit home page: `http://localhost:5500`
- View featured products
- Search products on `/products.html`
- Filter by category

### 2. Test Authentication
- Register new account at `/register.html`
- Login at `/login.html`
- Verify JWT token is stored in localStorage

### 3. Test Shopping
- Add products to cart
- View cart modal
- Proceed to checkout

### 4. Test Checkout
- Fill in shipping information
- Complete order (payment is simulated)
- Verify order confirmation page

### 5. Test Backend API
Use curl or Postman:

```bash
# Get all products
curl http://127.0.0.1:5000/products

# Register
curl -X POST http://127.0.0.1:5000/register \
  -H "Content-Type: application/json" \
  -d '{"username":"testuser","email":"test@example.com","password":"password123"}'

# Login
curl -X POST http://127.0.0.1:5000/login \
  -H "Content-Type: application/json" \
  -d '{"email":"test@example.com","password":"password123"}'
```

## Key Implementation Details

### State Management
- **Cart**: Stored in browser localStorage, persists across sessions
- **User**: Authentication token and user data stored in localStorage
- **Sessions**: JWT tokens expire after 7 days

### Security Considerations
1. Passwords are hashed with bcrypt (10 rounds)
2. JWT tokens are signed and verified
3. CORS is enabled for development
4. Environment variables for sensitive data

### Frontend Architecture
- Modular JavaScript with classes (`Cart`, `Auth`, `OrderManager`, `ProductManager`)
- Event-driven UI updates
- No external dependencies (vanilla JS)
- Responsive CSS Grid layout

### Backend Architecture
- RESTful API design
- Separation of concerns (routes, database operations)
- Error handling with HTTP status codes
- Connection pooling with MongoDB

## Database Schema

### Users Collection
```javascript
{
  _id: ObjectId,
  username: String,
  email: String (unique),
  password: String (hashed),
  createdAt: Date
}
```

### Products Collection
```javascript
{
  _id: ObjectId,
  name: String,
  price: Number,
  image: String (URL),
  category: String (sport|cruiser|adventure|accessories),
  description: String,
  specs: Object,
  createdAt: Date
}
```

### Orders Collection
```javascript
{
  _id: ObjectId,
  user_id: ObjectId,
  items: Array,
  shippingInfo: Object,
  total: Number,
  status: String,
  createdAt: ISO String
}
```

## Deployment

### Deploy Backend (Python Anywhere / Heroku)

1. Install Heroku CLI
2. Create Procfile:
   ```
   web: python app.py
   ```
3. Deploy:
   ```bash
   heroku login
   git push heroku main
   ```

### Deploy Frontend (Netlify / Vercel)

1. Build your static site
2. Deploy to Netlify/Vercel
3. Update API_BASE URL to production

### Available Sample Accounts

The database is pre-seeded with products. Create your own account during registration.

### Sample Products Included

1. Yamaha YZF-R1 ($17,499)
2. Harley-Davidson Fat Boy ($19,999)
3. BMW R 1250 GS Adventure ($21,995)
4. Ducati Panigale V4 ($23,995)
5. Indian Scout Bobber ($11,999)
6. KTM 1290 Super Adventure R ($18,999)
7. Premium Helmet ($299.99)
8. Riding Jacket ($249.99)

## Troubleshooting

### Issue: "Cannot GET /products"
- Ensure backend server is running at `http://127.0.0.1:5000`
- Check Flask error messages in terminal

### Issue: "Network Error" on frontend
- Verify CORS is enabled in backend (it is by default)
- Check API_BASE URL in `frontend/js/main.js`

### Issue: "MongoDB connection failed"
- Verify MONGO_URI in `.env` is correct
- Ensure MongoDB Atlas IP whitelist includes your IP
- Check internet connectivity

### Issue: Authentication not working
- Clear localStorage: `localStorage.clear()`
- Verify JWT secret in `app.py` matches across all servers
- Check token expiry (7 days default)

### Issue: CSS not loading
- Ensure frontend is served from correct directory
- Check relative paths in HTML files
- Hard refresh browser (Ctrl+Shift+R)

## Performance Optimization

- Products are loaded once at page initialization
- Cart operations use localStorage (instant)
- API calls are asynchronous (non-blocking)
- CSS Grid for responsive layouts
- Lazy loading for images (optional enhancement)

## Future Enhancements

- [ ] Admin dashboard for product management
- [ ] Email notifications for orders
- [ ] Payment gateway integration (Stripe/PayPal)
- [ ] Product reviews and ratings
- [ ] Wishlist functionality
- [ ] Advanced search with filters
- [ ] Real-time inventory management
- [ ] Order tracking
- [ ] Customer support chat
- [ ] Multiple language support
- [ ] Analytics dashboard

## Contributing

1. Fork the repository
2. Create feature branch: `git checkout -b feature-name`
3. Commit changes: `git commit -m 'Add new feature'`
4. Push to branch: `git push origin feature-name`
5. Submit pull request

## License

MIT License - see LICENSE file for details

## Support

For issues, feature requests, or questions:
- Open an issue on GitHub
- Documentation: See inline code comments
- API docs: Available at `http://127.0.0.1:5000/`

## Version

Current Version: 1.0.0
Last Updated: April 2026

---

**Happy coding! 🏍️ MotoShowroom - Ride With Power!**