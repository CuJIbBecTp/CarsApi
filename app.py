from flask import Flask, request
from flask_restful import Api, Resource, reqparse, abort, fields, marshal_with
from flask_sqlalchemy import SQLAlchemy

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
car_put_args.add_argument("make", type=str, help="Manufacturer of the car", required=True)
car_put_args.add_argument("model", type=str, help="Model of the car", required=True)
car_put_args.add_argument("rate", type=float, help="Rating of the car", default=0.0)

car_post_args = reqparse.RequestParser()
car_post_args.add_argument("make", type=str, help="Make of the car", required=True)
car_post_args.add_argument("model", type=str, help="Model of the car", required=True)

car_update_args = reqparse.RequestParser()
car_update_args.add_argument("rate", type=float, help="Rating of the car", required=False)

resource_fields = {
    'id': fields.String,
    'make': fields.String,
    'model': fields.String,
    'rate': fields.Float
}


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
        if args['rate']:
            result.rate = args['rate']
        db.session.commit()
        return result


if __name__ == "__main__":
    app.run(debug=True)
