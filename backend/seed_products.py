import os
import sys
from pymongo import MongoClient
from dotenv import load_dotenv

load_dotenv()

MONGO_URI = os.getenv('MONGO_URI')
if not MONGO_URI:
    print('Error: MONGO_URI environment variable not set. Set it in your environment or in a .env file.')
    sys.exit(1)

client = MongoClient(MONGO_URI)
db = client['ecommerce']
products = db['products']

# Seed data - match the frontend product shapes
PRODUCTS = [
    { 'name': 'Yamaha YZF-R1', 'price': 17499, 'image':'https://images.unsplash.com/photo-1558981806-ec527fa84c39?ixlib=rb-1.2.1&auto=format&fit=crop&w=600&q=80', 'category':'sport', 'specs':{'engine':'998cc liquid-cooled inline 4-cylinder','power':'197 HP @ 13,500 RPM'}, 'description':'The Yamaha YZF-R1 is a legendary supersport bike with cutting-edge technology.' },
    { 'name': 'Harley-Davidson Fat Boy', 'price': 19999, 'image':'https://images.unsplash.com/photo-1580310614697-2c9d4e7290e3?ixlib=rb-1.2.1&auto=format&fit=crop&w=600&q=80', 'category':'cruiser', 'specs':{'engine':'1,868cc Milwaukee-Eight 114 V-Twin','power':'93 HP @ 5,020 RPM'}, 'description':'The iconic Fat Boy features a muscular stance and classic styling.' },
    { 'name': 'BMW R 1250 GS Adventure', 'price': 21995, 'image':'https://images.unsplash.com/photo-1568772585407-9361f9bf3a87?ixlib=rb-1.2.1&auto=format&fit=crop&w=600&q=80', 'category':'adventure', 'specs':{'engine':'1,254cc air/liquid-cooled boxer twin','power':'136 HP @ 7,750 RPM'}, 'description':'Ultimate adventure bike with BMW\'s ShiftCam technology.' },
    { 'name': 'Ducati Panigale V4', 'price': 23995, 'image':'https://images.unsplash.com/photo-1591637333184-19aa84b3e01f?ixlib=rb-1.2.1&auto=format&fit=crop&w=600&q=80', 'category':'sport', 'specs':{'engine':'1,103cc Desmosedici Stradale V4','power':'214 HP @ 13,000 RPM'}, 'description':'Ducati\'s flagship superbike with a MotoGP-derived V4 engine.' },
    { 'name': 'Indian Scout Bobber', 'price': 11999, 'image':'https://images.unsplash.com/photo-1606220838315-056192d5e716?ixlib=rb-1.2.1&auto=format&fit=crop&w=600&q=80', 'category':'cruiser', 'specs':{'engine':'1,133cc liquid-cooled V-Twin','power':'100 HP @ 7,300 RPM'}, 'description':'A stripped-down aggressive bobber with blacked-out styling.' },
    { 'name': 'KTM 1290 Super Adventure R', 'price': 18999, 'image':'https://images.unsplash.com/photo-1558980394-4c7c9299fe96?ixlib=rb-1.2.1&auto=format&fit=crop&w=600&q=80', 'category':'adventure', 'specs':{'engine':'1,301cc liquid-cooled V-Twin','power':'160 HP @ 9,000 RPM'}, 'description':'Powerful production adventure bike with off-road focused suspension.' },
    { 'name': 'Premium Helmet', 'price': 299.99, 'image':'https://images.unsplash.com/photo-1600679472829-3044539ce8ed?ixlib=rb-1.2.1&auto=format&fit=crop&w=600&q=80', 'category':'accessories', 'specs':{'type':'Full-face','material':'Carbon fiber'}, 'description':'Ultra-lightweight carbon fiber helmet.' },
    { 'name': 'Riding Jacket', 'price': 249.99, 'image':'https://images.unsplash.com/photo-1622185132923-484496db0c1e?ixlib=rb-1.2.1&auto=format&fit=crop&w=600&q=80', 'category':'accessories', 'specs':{'type':'Textile','protection':'CE Level 2 armor'}, 'description':'All-season riding jacket with premium protection.' }
]

def seed():
    inserted = 0
    for p in PRODUCTS:
        # upsert by name to avoid duplicates
        res = products.update_one({'name': p['name']}, {'$set': p}, upsert=True)
        if res.upserted_id or res.modified_count:
            inserted += 1
    print(f'Seed complete: {inserted} products upserted/modified.')

if __name__ == '__main__':
    seed()
