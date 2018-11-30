
from flask import Flask, jsonify, abort, request, render_template
from config import Config

app = Flask(__name__)
app.config.from_object(Config)


from flask_sqlalchemy import SQLAlchemy
from flask_marshmallow import Marshmallow
db = SQLAlchemy(app)
ma = Marshmallow(app)

from models import Product
from schemas import products_schema
from schemas import product_schema

@app.route('/')
def home():
    products = db.session.query(Product).all()
    return render_template('home.html', products=products)

@app.route('/product_detail/<id>')
def product_detail():
    product = db.session.query(Product).get(id)
    return render_template('product_detail.html', products=product)


@app.route('/hello')
def hello():
    return "Hello World!"

@app.route('/products', methods=["GET", "POST"])
def products():
    if request.method == "GET":
        products = db.session.query(Product).all() # SQLAlchemy request => 'SELECT * FROM products'
        result = products_schema.jsonify(products)
    else:
        product_name = request.json['name']
        product_desc = request.json['description']
        new_product = Product(product_name, product_desc)
        db.session.add(new_product)
        db.session.commit()
        result = product_schema.jsonify(new_product)
    return result

@app.route('/products/<int:id>', methods=['GET', 'DELETE', 'PATCH'])
def product_by_id(id):
    if request.method == "GET":
        product = db.session.query(Product).get(id)
        result = product_schema.jsonify(product)
    elif request.method == 'PATCH':
        product = db.session.query(Product).get(id)
        product.name = request.json['name']
        product.description = request.json['description']
        db.session.commit()
        result = product_schema.jsonify(product)
    else:
        product = db.session.query(Product).get(id)
        db.session.delete(product)
        db.session.commit()
        result = product_schema.jsonify(product)

    return render_template('product_detail.html', product=product)

