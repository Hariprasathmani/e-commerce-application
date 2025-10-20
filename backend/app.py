from flask import Flask, request, jsonify
from flask_cors import CORS
from pymongo import MongoClient
from bson import ObjectId
import os
from dotenv import load_dotenv
import bcrypt
import jwt
from datetime import datetime, timedelta

load_dotenv()

app = Flask(__name__)
CORS(app)

client = MongoClient(os.getenv("MONGO_URI"))
db = client['ecommerce']
products = db['products']
orders = db['orders']
users = db['users']

JWT_SECRET = os.getenv('JWT_SECRET', 'change_this_dev_secret')
JWT_ALGO = 'HS256'

@app.route("/products", methods=["GET"])
def get_products():
    product_list = []
    for product in products.find():
        product['_id'] = str(product['_id'])
        product_list.append(product)
    return jsonify(product_list)

@app.route("/product", methods=["POST"])
def add_product():
    data = request.json
    print(data)
    result = products.insert_one(data)
    return jsonify({"inserted_id": str(result.inserted_id)})

@app.route("/product/<id>", methods=["PUT"])
def update_product(id):
    data = request.json
    result = products.update_one({"_id": ObjectId(id)}, {"$set": data})
    return jsonify({"updated": result.modified_count})

@app.route("/product/<id>", methods=["DELETE"])
def delete_product(id):
    result = products.delete_one({"_id": ObjectId(id)})
    return jsonify({"deleted": result.deleted_count})


@app.route("/order", methods=["POST"])
def place_order():
    # require Authorization: Bearer <token>
    auth = request.headers.get('Authorization', '')
    token = None
    if auth.startswith('Bearer '):
        token = auth.split(' ',1)[1]
    if not token:
        return jsonify({'error':'authorization required'}), 401
    try:
        payload = jwt.decode(token, JWT_SECRET, algorithms=[JWT_ALGO])
    except Exception as e:
        return jsonify({'error':'invalid token', 'msg': str(e)}), 401
    data = request.json or {}
    # attach user id from token
    data['user_id'] = payload.get('user_id')
    data['createdAt'] = datetime.utcnow().isoformat()
    result = orders.insert_one(data)
    return jsonify({"order_id": str(result.inserted_id)})


@app.route('/register', methods=['POST'])
def api_register():
    data = request.json
    # expected: { username, email, password }
    if not data or 'email' not in data or 'password' not in data:
        return jsonify({'error':'missing fields'}), 400
    # check existing
    if users.find_one({'email': data['email']}):
        return jsonify({'error':'email exists'}), 409
    # hash password
    pw_hash = bcrypt.hashpw(data['password'].encode('utf-8'), bcrypt.gensalt())
    res = users.insert_one({'username': data.get('username',''), 'email': data['email'], 'password': pw_hash})
    user = {'_id': str(res.inserted_id), 'username': data.get('username',''), 'email': data['email']}
    # create token
    payload = {'user_id': user['_id'], 'email': user['email'], 'exp': datetime.utcnow() + timedelta(days=7)}
    token = jwt.encode(payload, JWT_SECRET, algorithm=JWT_ALGO)
    return jsonify({'user': user, 'token': token})


@app.route('/login', methods=['POST'])
def api_login():
    data = request.json
    if not data or 'email' not in data or 'password' not in data:
        return jsonify({'error':'missing fields'}), 400
    u = users.find_one({'email': data['email']})
    if not u:
        return jsonify({'error':'invalid credentials'}), 401
    stored_pw = u.get('password')
    # stored_pw may be bytes if inserted as hashed
    try:
        ok = bcrypt.checkpw(data['password'].encode('utf-8'), stored_pw)
    except Exception:
        # if stored as string, try encode
        ok = bcrypt.checkpw(data['password'].encode('utf-8'), stored_pw.encode('utf-8'))
    if not ok:
        return jsonify({'error':'invalid credentials'}), 401
    user = {'_id': str(u['_id']), 'username': u.get('username',''), 'email': u.get('email')}
    payload = {'user_id': user['_id'], 'email': user['email'], 'exp': datetime.utcnow() + timedelta(days=7)}
    token = jwt.encode(payload, JWT_SECRET, algorithm=JWT_ALGO)
    return jsonify({'user': user, 'token': token})


@app.route("/orders", methods=["GET"])
def get_orders():
    order_list = []
    for o in orders.find():
        o['_id'] = str(o['_id'])
        order_list.append(o)
    return jsonify(order_list)


@app.route("/")
def home():
    return "Backend is running"

if __name__ == "__main__":
    # Run without the auto-reloader on Windows to avoid socket errors during restarts
    app.run(debug=False, host='127.0.0.1', port=5000)
