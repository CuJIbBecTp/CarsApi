import pytest
from app import app, db, CarModel

app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///tests/database.db'


@pytest.fixture(scope='module')
def new_car():
    row = CarModel(make="Volkswagen", model="Passat", rate=3)
    return row


@pytest.fixture(scope='module')
def test_client():
    # Create a test client using the Flask application
    with app.test_client() as client:
        db.create_all()
        yield client
        db.drop_all()


@pytest.fixture(scope='module')
def test_client_with_db():
    # Create a test client using the Flask application
    with app.test_client() as client:
        db.create_all()

        data = [{"make": "Volkswagen", "model": "Passat", "rate": 3},
                {"make": "BMW", "model": "X6", "rate": 3},
                {"make": "BMW", "model": "X6", "rate": 4},
                {"make": "Mercedes-benz", "model": "ML-Class", "rate": 1},
                {"make": "Mercedes-benz", "model": "ML-Class", "rate": 2},
                {"make": "Mercedes-benz", "model": "ML-Class", "rate": 3},
                {"make": "Audi", "model": "A6", "rate": 1},
                {"make": "Audi", "model": "A6", "rate": 2},
                {"make": "Audi", "model": "A6", "rate": 3},
                {"make": "Audi", "model": "A6", "rate": 4}]

        # Insert user data
        for i in data:
            car = CarModel(make=i["make"], model=i["model"], rate=i["rate"])
            db.session.add(car)

        # Commit the changes for the users
        db.session.commit()
        yield client
        db.drop_all()
