import sqlite3

from flask_jwt import jwt_required
from flask_restful import Resource, reqparse

from models.item_model import ItemModel


class Item(Resource):
    parser = reqparse.RequestParser()
    parser.add_argument("price",
                        type=float,
                        required=True,
                        help="This field is required.")
    parser.add_argument("store_id",
                        type=int,
                        required=True,
                        help="This field is required.")

    @jwt_required()
    def get(self, name):
        item = ItemModel.find_by_name(name)
        if item:
            return item.json(), 200
        return {"message": "Item not found"}, 404

    def post(self, name):
        data = Item.parser.parse_args()
        item = ItemModel(name, data["price"], data["store_id"])
        try:
            item.save_to_db()
        except:
            return {"message": "Something went wrong while inserting"}, 500

        return {"message": "Item created", "created_item": item.json()}, 201

    def delete(self, name):
        item = ItemModel.find_by_name(name)
        if item:
            item.delete_from_db()

        return {'message': "Item deleted."}

    def put(self, name):

        data = Item.parser.parse_args()
        item = ItemModel.find_by_name(name)

        if item is None:
            item = ItemModel(name, data["price"], data["store_id"])
        else:
            item.price = data['price']
            item.store_id = data["store_id"]
        item.save_to_db()
        return item.json(), 201


class ItemList(Resource):
    def get(self):
        # return {"items": [item.json() for item in ItemModel.query.all()]}
        return {"items": list(map(lambda x: x.json(), ItemModel.query.all()))}
