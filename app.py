from flask import Flask, request, jsonify
from flask_sqlalchemy import SQLAlchemy
from flask_cors import CORS

app = Flask(__name__)
CORS(app)  # Allow frontend requests

# SQLite Database Configuration
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///products.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
db = SQLAlchemy(app)

# Product Model
class Product(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100), nullable=False)
    brand = db.Column(db.String(50), nullable=False)
    price = db.Column(db.Float, nullable=False)
    rating = db.Column(db.Float, default=0.0)
    reviews = db.Column(db.Integer, default=0)

# Create Database
with app.app_context():
    db.create_all()

# Route: Get All Products
@app.route('/products', methods=['GET'])
def get_products():
    sort_by = request.args.get('sort', 'price')  # Sorting option (default: price)
    order = request.args.get('order', 'asc')  # asc or desc
    products = Product.query.order_by(getattr(Product, sort_by).asc() if order == 'asc' else getattr(Product, sort_by).desc()).all()
    
    return jsonify([{
        'id': p.id, 'name': p.name, 'brand': p.brand, 
        'price': p.price, 'rating': p.rating, 'reviews': p.reviews
    } for p in products])

# Route: Add Product
@app.route('/add_product', methods=['POST'])
def add_product():
    data = request.json
    new_product = Product(
        name=data['name'], brand=data['brand'],
        price=data['price'], rating=data.get('rating', 0.0),
        reviews=data.get('reviews', 0)
    )
    db.session.add(new_product)
    db.session.commit()
    return jsonify({'message': 'Product added successfully!'}), 201

# Route: Search Product
@app.route('/search', methods=['GET'])
def search_product():
    query = request.args.get('q', '')
    products = Product.query.filter(Product.name.contains(query)).all()
    return jsonify([{
        'id': p.id, 'name': p.name, 'brand': p.brand,
        'price': p.price, 'rating': p.rating, 'reviews': p.reviews
    } for p in products])

if __name__ == '__main__':
    app.run(debug=True)

