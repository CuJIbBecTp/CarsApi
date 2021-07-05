"""
This file (test_models.py) contains the unittests for the database model.
"""


def test_new_car(new_car):
    """
    GIVEN a CarModel
    WHEN a new Car is created
    THEN check the make, model and rate are defined correctly
    """
    assert new_car.make == "Volkswagen"
    assert new_car.model == "Passat"
    assert new_car.rate == 3
