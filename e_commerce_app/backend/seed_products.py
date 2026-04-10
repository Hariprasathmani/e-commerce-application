"""
Seed products into MongoDB.
Run: python seed_products.py
"""
import os
from dotenv import load_dotenv
from pymongo import MongoClient

# Load environment variables from .env file
load_dotenv()

MONGO_URI = os.getenv("MONGO_URI")

PRODUCTS = [
    {
        'name': 'Yamaha YZF-R1',
        'price': 17499,
        'image': 'https://images.unsplash.com/photo-1558981806-ec527fa84c39?auto=format&fit=crop&w=600&q=80',
        'category': 'sport',
        'description': 'The Yamaha YZF-R1 is a legendary supersport bike with cutting-edge MotoGP-derived technology.',
        'specs': {'engine': '998cc liquid-cooled inline 4-cylinder', 'power': '197 HP @ 13,500 RPM', 'weight': '199 kg'}
    },
    {
        'name': 'Ducati Panigale V4',
        'price': 23995,
        'image': 'https://images.unsplash.com/photo-1591637333184-19aa84b3e01f?auto=format&fit=crop&w=600&q=80',
        'category': 'sport',
        'description': "Ducati's flagship superbike with a MotoGP-derived V4 engine that produces breathtaking performance.",
        'specs': {'engine': '1,103cc Desmosedici Stradale V4', 'power': '214 HP @ 13,000 RPM', 'weight': '195 kg'}
    },
    {
        'name': 'Harley-Davidson Fat Boy',
        'price': 19999,
        'image': 'https://images.unsplash.com/photo-1580310614697-2c9d4e7290e3?auto=format&fit=crop&w=600&q=80',
        'category': 'cruiser',
        'description': 'The iconic Fat Boy features a muscular softail frame, classic Milwaukee-Eight power, and timeless style.',
        'specs': {'engine': '1,868cc Milwaukee-Eight 114 V-Twin', 'power': '93 HP @ 5,020 RPM', 'weight': '317 kg'}
    },
    {
        'name': 'Indian Scout Bobber',
        'price': 11999,
        'image': 'https://images.unsplash.com/photo-1606220838315-056192d5e716?auto=format&fit=crop&w=600&q=80',
        'category': 'cruiser',
        'description': 'A stripped-down aggressive bobber with blacked-out styling and an all-aluminum liquid-cooled powertrain.',
        'specs': {'engine': '1,133cc liquid-cooled V-Twin', 'power': '100 HP @ 7,300 RPM', 'weight': '253 kg'}
    },
    {
        'name': 'BMW R 1250 GS Adventure',
        'price': 21995,
        'image': 'https://images.unsplash.com/photo-1568772585407-9361f9bf3a87?auto=format&fit=crop&w=600&q=80',
        'category': 'adventure',
        'description': "The ultimate adventure bike with BMW's ShiftCam technology and massive range for any terrain.",
        'specs': {'engine': '1,254cc air/liquid-cooled boxer twin', 'power': '136 HP @ 7,750 RPM', 'weight': '268 kg'}
    },
    {
        'name': 'KTM 1290 Super Adventure R',
        'price': 18999,
        'image': 'https://images.unsplash.com/photo-1558980394-4c7c9299fe96?auto=format&fit=crop&w=600&q=80',
        'category': 'adventure',
        'description': 'The most powerful production adventure bike, with off-road-focused suspension and aggressive styling.',
        'specs': {'engine': '1,301cc liquid-cooled V-Twin', 'power': '160 HP @ 9,000 RPM', 'weight': '223 kg'}
    },
    {
        'name': 'Kawasaki Z H2',
        'price': 17000,
        'image': 'https://images.unsplash.com/photo-1558981359-219d6364c9c8?auto=format&fit=crop&w=600&q=80',
        'category': 'sport',
        'description': 'Supercharged hypernaked with 200 horsepower and a dramatic angular design for street domination.',
        'specs': {'engine': '998cc supercharged inline-4', 'power': '200 HP @ 11,000 RPM', 'weight': '239 kg'}
    },
    {
        'name': 'Royal Enfield Himalayan 450',
        'price': 5499,
        'image': 'https://images.unsplash.com/photo-1558981420-87aa9dad1c89?auto=format&fit=crop&w=600&q=80',
        'category': 'adventure',
        'description': 'Purpose-built adventure tourer designed for high-altitude Himalayan passes and everyday urban commuting.',
        'specs': {'engine': '452cc water-cooled single', 'power': '40 HP @ 8,000 RPM', 'weight': '196 kg'}
    },
    {
        'name': 'Premium Carbon Helmet',
        'price': 299.99,
        'image': 'https://images.unsplash.com/photo-1600679472829-3044539ce8ed?auto=format&fit=crop&w=600&q=80',
        'category': 'accessories',
        'description': 'Ultra-lightweight carbon fiber full-face helmet with aerodynamic design and pinlock-ready visor.',
        'specs': {'type': 'Full-face', 'material': 'Carbon fiber', 'safety': 'ECE 22.06 / DOT certified'}
    },
    {
        'name': 'All-Season Riding Jacket',
        'price': 249.99,
        'image': 'https://images.unsplash.com/photo-1622185132923-484496db0c1e?auto=format&fit=crop&w=600&q=80',
        'category': 'accessories',
        'description': 'Versatile textile riding jacket with CE Level 2 shoulder and elbow armour, waterproof and ventilated.',
        'specs': {'type': 'Textile touring', 'protection': 'CE Level 2 armor', 'waterproof': 'Yes'}
    },
]

def seed():
    print("Connecting to MongoDB Atlas...")
    try:
        client = MongoClient(MONGO_URI, serverSelectionTimeoutMS=5000)
        client.admin.command('ping')
    except Exception as e:
        print(f"Failed to connect to MongoDB: {e}")
        return

    db = client['ecommerce']
    products_col = db['products']
    
    print("Checking existing products...")
    # Get existing names to avoid duplicates
    existing_names = [p['name'] for p in products_col.find({}, {"name": 1})]
    
    added = 0
    for p in PRODUCTS:
        if p['name'] not in existing_names:
            products_col.insert_one(p)
            added += 1

    print(f'✅ Seed complete: {added} new products added to MongoDB.')

if __name__ == '__main__':
    seed()
