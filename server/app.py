#!/usr/bin/env python3

from flask import Flask, make_response, jsonify
from flask_migrate import Migrate

from models import db, Bakery, BakedGood

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///app.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
app.json.compact = False

migrate = Migrate(app, db)

db.init_app(app)

@app.route('/')
def index():
    return '<h1>Bakery GET API</h1>'

@app.route('/bakeries')
def bakeries():
    bakeries = Bakery.query.all()

    # Serialize the list of bakeries using SQLAlchemy-serializer's serialize function
    bakery_list = []
    for bakery in bakeries:
        bakery_dict = bakery.to_dict()
        bakery_list.append(bakery_dict)

    return jsonify(bakery_list)

    

@app.route('/bakeries/<int:id>')
def bakery_by_id(id):
    bakery = Bakery.query.filter_by(id=id).first()

    bakery_dict = bakery.to_dict()
    bakery_dict['baked_goods'] = [good.to_dict() for good in bakery.baked_goods]

    response = make_response(
        jsonify(bakery_dict),
        200
    )
    return response

@app.route('/baked_goods/by_price')
def baked_goods_by_price():
    # Query baked goods, sort by price in descending order, and serialize
    baked_goods = (
        BakedGood.query
        .order_by(BakedGood.price.desc())
        .all()
    )

    baked_goods_list = [good.to_dict() for good in baked_goods]
    return jsonify(baked_goods_list)

@app.route('/baked_goods/most_expensive')
def most_expensive_baked_good():
    # Query the most expensive baked good, sort by price in descending order, and limit to one result
    most_expensive_good = (
        BakedGood.query
        .order_by(BakedGood.price.desc())
        .first()  # Limit to one result (the most expensive)
    )
    # Serialize the most expensive baked good
    most_expensive_dict = most_expensive_good.to_dict()
    return jsonify(most_expensive_dict)

if __name__ == '__main__':
    app.run(port=5554, debug=True)
