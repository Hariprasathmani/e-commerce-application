from flask import Flask, request, jsonify
from flask_cors import CORS
from pymongo import MongoClient
from bson import ObjectId
import os
from dotenv import load_dotenv

load_dotenv()

app = Flask(__name__)
CORS(app)

client = MongoClient(os.getenv("MONGO_URI"))
db = client['ecommerce']
products = db['products']

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

if __name__ == "__main__":
    app.run(debug=True)
