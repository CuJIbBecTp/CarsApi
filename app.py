from flask import Flask
import requests
from flask_restful import Api, Resource, reqparse, abort, fields, marshal_with
from flask_sqlalchemy import SQLAlchemy
import pandas as pd
import io

# Download the list of Dealers
makes_url = 'https://vpic.nhtsa.dot.gov/api/vehicles/GetAllMakes?format=csv'
makes_string = requests.get(makes_url).text
makes = io.StringIO(makes_string)
makes_pd = pd.read_csv(makes, sep=",")
makes = [i.lower() for i in (makes_pd.iloc[:,1]).values.tolist()]


app = Flask(__name__)
api = Api(app)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///database.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = True
db = SQLAlchemy(app)


class CarModel(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    make = db.Column(db.String(100), nullable=False)
    model = db.Column(db.String(100), nullable=False)
    rate = db.Column(db.Float(32), nullable=False)

#db.create_all()


car_put_args = reqparse.RequestParser()
car_put_args.add_argument("make", type=str, help="Make of the car", required=True)
car_put_args.add_argument("model", type=str, help="Model of the car", required=True)
car_put_args.add_argument("rate", type=float, help="Rating of the car", default=1.0)

car_update_args = reqparse.RequestParser()
car_update_args.add_argument("car_id", type=int, help="id of the car", required=True)
car_update_args.add_argument("rating", type=float, help="Rating of the car in the range [1,5]", required=True)

resource_fields = {
    'id': fields.String,
    'make': fields.String,
    'model': fields.String,
    'rate': fields.Float
}


@api.resource("/cars","/cars/")
class Cars(Resource):
    @marshal_with(resource_fields)
    def post(self):
        args = car_put_args.parse_args()
        make = args['make'].lower()
        if make not in makes:
            abort(404, message="Make doesn't exist")
        model_url = f'https://vpic.nhtsa.dot.gov/api/vehicles/GetModelsForMake/{make}?format=csv'
        model_string = requests.get(model_url).text
        model = io.StringIO(model_string)
        model_pd = pd.read_csv(model, sep=",")
        models = [i.lower() for i in (model_pd.iloc[:,3]).values.tolist()]
        model = args['model'].lower()
        if model not in models:
            abort(404, message="Model doesn't exist")
        car = CarModel(make=make.capitalize(), model=model.capitalize(), rate=args['rate'])
        db.session.add(car)
        db.session.commit()
        return car, 201

    @marshal_with(resource_fields)
    def get(self):
        result = CarModel.query.all()
        if not result:
            abort(404, message=f'The database is empty')
        print(result)
        return result


@api.resource("/rate","/rate/")
class CarsRating(Resource):
    @marshal_with(resource_fields)
    def post(self):
        args = car_update_args.parse_args()
        result = CarModel.query.filter_by(id=args['car_id']).first()
        if not result:
            abort(404, message="Car doesn't exist, cannot update")
        if 1 <= args['rating'] <= 5:
            result.rate = args['rating']
        else:
            abort(404, message="Value does not satisfy the range [1,5]")
        db.session.commit()
        return result


@api.resource("/cars/<int:car_id>")
class Car(Resource):
    @marshal_with(resource_fields)
    def get(self, car_id):
        result = CarModel.query.filter_by(id=car_id).first()
        if not result:
            abort(404, message=f'Could not find car with id={car_id}')
        return result

    @marshal_with(resource_fields)
    def put(self, car_id):
        args = car_put_args.parse_args()
        result = CarModel.query.filter_by(id=car_id).first()
        if result:
            abort(409, message="Car id already taken...")

        car = CarModel(id=car_id, make=args['make'], model=args['model'], rate=args['rate'])
        db.session.add(car)
        db.session.commit()
        return car, 201

    @marshal_with(resource_fields)
    def delete(self, car_id):
        result = CarModel.query.filter_by(id=car_id).first()
        if not result:
            abort(404, message="Could not find the car...")
        db.session.delete(result)
        db.session.commit()
        return 204

    @marshal_with(resource_fields)
    def patch(self, car_id):
        args = car_update_args.parse_args()
        result = CarModel.query.filter_by(id=car_id).first()
        if not result:
            abort(404, message="Car doesn't exist, cannot update")
        if args['rating']:
            result.rate = args['rating']
        db.session.commit()
        return result


if __name__ == "__main__":
    app.run(debug=True)
