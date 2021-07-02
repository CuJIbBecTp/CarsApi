from flask import Flask, request
from flask_restful import Api, Resource, reqparse, abort

app = Flask(__name__)
api = Api(app)

car_put_args = reqparse.RequestParser()
car_put_args.add_argument("make", type=str, help="Manufacturer of the car", required=True)
car_put_args.add_argument("model", type=str, help="Model of the car", required=True)
car_put_args.add_argument("rate", type=float, help="Rating of the car", default=0.0)

car_post_args = reqparse.RequestParser()
car_post_args.add_argument("make", type=str, help="Make of the car", required=True)
car_post_args.add_argument("model", type=str, help="Model of the car", required=True)

cars = {}


def abort_if_make_or_model_doesnt_exist(make, model):
    if make or model not in []:
        abort(404, message="The specified {make} or {model} doesn't exist")


def abort_if_car_id_doesnt_exist(car_id):
    if car_id not in cars:
        abort(404, message="Could not find the car...")


def abort_if_car_exists(car_id):
    if car_id in cars:
        abort(409, message="The car with id={car_id} already exists")


@api.resource("/cars/<int:car_id>")
class Car(Resource):
    def get(self, car_id):
        abort_if_car_id_doesnt_exist(car_id)
        return cars[car_id]

    def put(self, car_id):
        abort_if_car_exists(car_id)
        args = car_put_args.parse_args()
        cars[car_id] = args
        return cars[car_id], 201

    def delete(self, car_id):
        abort_if_car_id_doesnt_exist(car_id)
        del cars[car_id]
        return '', 204


if __name__ == "__main__":
    app.run(debug=True)
