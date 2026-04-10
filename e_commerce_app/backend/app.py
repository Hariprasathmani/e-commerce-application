from flask import Flask, request, jsonify
from flask_cors import CORS
from pymongo import MongoClient
import pymongo
from bson import ObjectId
import os
from dotenv import load_dotenv
import bcrypt
import jwt
from datetime import datetime, timedelta

load_dotenv()

app = Flask(__name__)
# Enable CORS for frontend requests
CORS(app, origins="*")

# ─── MONGODB SETUP ────────────────────────────────────────────────
MONGO_URI = os.getenv("MONGO_URI")
try:
    print(f"Attempting to connect to MongoDB...")
    # Add a server selection timeout so it doesn't hang indefinitely on bad networks
    client = MongoClient(MONGO_URI, serverSelectionTimeoutMS=5000)
    # Trigger a ping to verify connection
    client.admin.command('ping')
    print("✅ Successfully connected to MongoDB Atlas!")
except Exception as e:
    print(f"❌ Failed to connect to MongoDB. Ensure your IP is whitelisted in Atlas and your DNS allows SRV records.")
    print(f"Error details: {e}")

db = client['ecommerce']
products_col = db['products']
orders_col = db['orders']
users_col = db['users']

JWT_SECRET = os.getenv('JWT_SECRET', 'motoshowroom_secret_2025')
JWT_ALGO = 'HS256'

def serialize(doc):
    """Convert MongoDB document to JSON-serializable dict."""
    if '_id' in doc:
        doc['_id'] = str(doc['_id'])
    return doc

def decode_token(req):
    """Extract and verify JWT from Authorization header."""
    auth = req.headers.get('Authorization', '')
    if not auth.startswith('Bearer '):
        return None, ('Authorization required', 401)
    token = auth.split(' ', 1)[1]
    try:
        payload = jwt.decode(token, JWT_SECRET, algorithms=[JWT_ALGO])
        return payload, None
    except jwt.ExpiredSignatureError:
        return None, ('Token expired, please login again', 401)
    except Exception as e:
        return None, (f'Invalid token: {str(e)}', 401)


# ─── PRODUCTS ────────────────────────────────────────────────────
@app.route("/products", methods=["GET"])
def get_products():
    try:
        result = [serialize(p) for p in products_col.find()]
        return jsonify(result)
    except Exception as e:
        return jsonify({'error': str(e)}), 500

@app.route("/product", methods=["POST"])
def add_product():
    data = request.json
    if not data:
        return jsonify({'error': 'No data'}), 400
    try:
        result = products_col.insert_one(data)
        return jsonify({"inserted_id": str(result.inserted_id)}), 201
    except Exception as e:
        return jsonify({'error': str(e)}), 500

@app.route("/product/<id>", methods=["GET"])
def get_product(id):
    try:
        p = products_col.find_one({'_id': ObjectId(id)})
        if not p:
            return jsonify({'error': 'Not found'}), 404
        return jsonify(serialize(p))
    except Exception:
        return jsonify({'error': 'Invalid ID'}), 400

@app.route("/product/<id>", methods=["PUT"])
def update_product(id):
    data = request.json
    try:
        result = products_col.update_one({'_id': ObjectId(id)}, {'$set': data})
        return jsonify({"updated": result.modified_count})
    except Exception:
        return jsonify({'error': 'Invalid ID'}), 400

@app.route("/product/<id>", methods=["DELETE"])
def delete_product(id):
    try:
        result = products_col.delete_one({'_id': ObjectId(id)})
        return jsonify({"deleted": result.deleted_count})
    except Exception:
        return jsonify({'error': 'Invalid ID'}), 400


# ─── AUTH ────────────────────────────────────────────────────────
@app.route('/register', methods=['POST'])
def api_register():
    data = request.json or {}
    email = data.get('email')
    password = data.get('password')
    
    if not email or not password:
        return jsonify({'error': 'Email and password are required'}), 400

    try:
        if users_col.find_one({'email': email}):
            return jsonify({'error': 'An account with this email already exists'}), 409

        pw_hash = bcrypt.hashpw(password.encode('utf-8'), bcrypt.gensalt())
        username = data.get('username', email.split('@')[0])

        res = users_col.insert_one({
            'username': username,
            'email': email,
            'password': pw_hash,
            'createdAt': datetime.utcnow().isoformat(),
            'isAdmin': False
        })

        user = {'_id': str(res.inserted_id), 'username': username, 'email': email, 'isAdmin': False}
        payload = {'user_id': user['_id'], 'email': user['email'], 'exp': datetime.utcnow() + timedelta(days=7)}
        token = jwt.encode(payload, JWT_SECRET, algorithm=JWT_ALGO)
        return jsonify({'user': user, 'token': token}), 201
    except Exception as e:
        return jsonify({'error': str(e)}), 500

@app.route('/login', methods=['POST'])
def api_login():
    data = request.json or {}
    email = data.get('email')
    
    if not email or not data.get('password'):
        return jsonify({'error': 'Email and password are required'}), 400

    try:
        u = users_col.find_one({'email': email})
        if not u:
            return jsonify({'error': 'Invalid email or password'}), 401

        stored_pw = u.get('password')
        try:
            ok = bcrypt.checkpw(data['password'].encode('utf-8'), stored_pw)
        except Exception:
            try:
                ok = bcrypt.checkpw(data['password'].encode('utf-8'), stored_pw.encode('utf-8'))
            except Exception:
                ok = False

        if not ok:
            return jsonify({'error': 'Invalid email or password'}), 401

        user = {
            '_id': str(u['_id']),
            'username': u.get('username', ''),
            'email': u.get('email', ''),
            'isAdmin': u.get('isAdmin', False)
        }
        payload = {'user_id': user['_id'], 'email': user['email'], 'exp': datetime.utcnow() + timedelta(days=7)}
        token = jwt.encode(payload, JWT_SECRET, algorithm=JWT_ALGO)
        return jsonify({'user': user, 'token': token})
    except Exception as e:
         return jsonify({'error': str(e)}), 500


# ─── ORDERS ──────────────────────────────────────────────────────
@app.route("/order", methods=["POST"])
def place_order():
    payload, err = decode_token(request)
    if err:
        return jsonify({'error': err[0]}), err[1]

    data = request.json or {}
    data['user_id'] = payload.get('user_id')  # stored as string to match schema
    data['createdAt'] = datetime.utcnow().isoformat()
    data['status'] = data.get('status', 'confirmed')

    try:
        result = orders_col.insert_one(data)
        return jsonify({"order_id": str(result.inserted_id)}), 201
    except Exception as e:
        return jsonify({'error': str(e)}), 500

@app.route("/user-orders", methods=["GET"])
def get_user_orders():
    payload, err = decode_token(request)
    if err:
        return jsonify({'error': err[0]}), err[1]

    user_id = payload.get('user_id')
    try:
        order_list = [serialize(o) for o in orders_col.find({'user_id': user_id})]
        return jsonify(order_list)
    except Exception as e:
        return jsonify({'error': str(e)}), 500

@app.route("/orders", methods=["GET"])
def get_all_orders():
    try:
        order_list = [serialize(o) for o in orders_col.find().sort('createdAt', pymongo.DESCENDING)]
        return jsonify(order_list)
    except Exception as e:
        return jsonify({'error': str(e)}), 500

@app.route("/order/<id>", methods=["GET"])
def get_order(id):
    try:
        o = orders_col.find_one({'_id': ObjectId(id)})
        if not o:
            return jsonify({'error': 'Order not found'}), 404
        return jsonify(serialize(o))
    except Exception:
        return jsonify({'error': 'Invalid order ID'}), 400


# ─── USER ────────────────────────────────────────────────────────
@app.route("/user", methods=["GET"])
def get_user():
    payload, err = decode_token(request)
    if err:
        return jsonify({'error': err[0]}), err[1]

    user_id = payload.get('user_id')
    try:
        u = users_col.find_one({'_id': ObjectId(user_id)})
        if not u:
            return jsonify({'error': 'User not found'}), 404

        return jsonify({
            '_id': str(u['_id']),
            'username': u.get('username', ''),
            'email': u.get('email', ''),
            'isAdmin': u.get('isAdmin', False)
        })
    except Exception:
        return jsonify({'error': 'Invalid user ID'}), 400


# ─── ADMIN STATS ─────────────────────────────────────────────────
@app.route("/admin/stats", methods=["GET"])
def admin_stats():
    try:
        total_products = products_col.count_documents({})
        total_orders = orders_col.count_documents({})
        total_users = users_col.count_documents({})
        
        # Calculate revenue by summing the order totals
        # This requires the order document to contain a numeric 'total' field
        pipeline = [
            {"$group": {"_id": None, "total_revenue": {"$sum": "$total"}}}
        ]
        rev_cursor = list(orders_col.aggregate(pipeline))
        revenue = rev_cursor[0]['total_revenue'] if rev_cursor else 0

        return jsonify({
            'total_products': total_products,
            'total_orders': total_orders,
            'total_users': total_users,
            'revenue': revenue
        })
    except Exception as e:
        return jsonify({'error': str(e)}), 500


# ─── ROOT ────────────────────────────────────────────────────────
@app.route("/")
def home():
    return jsonify({
        "message": "MotoShowroom Backend API",
        "database": "MongoDB",
        "endpoints": {
            "GET /products": "List all products",
            "POST /product": "Add product",
            "GET /product/<id>": "Get single product",
            "PUT /product/<id>": "Update product",
            "DELETE /product/<id>": "Delete product",
            "POST /register": "Register user",
            "POST /login": "Login user",
            "GET /user": "Get current user (auth)",
            "POST /order": "Place order (auth)",
            "GET /user-orders": "Get user orders (auth)",
            "GET /orders": "Get all orders (admin)",
            "GET /order/<id>": "Get single order",
            "GET /admin/stats": "Admin stats"
        }
    })

if __name__ == "__main__":
    print("\n🏍️  MotoShowroom Backend API")
    print("   Running on: http://127.0.0.1:5000")
    print("   Database backing: MongoDB Atlas\n")
    app.run(debug=True, host='127.0.0.1', port=5000, use_reloader=False)
