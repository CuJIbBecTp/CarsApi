"""
This file (test_routes.py) contains the functional tests for the all routes.

These tests use GETs,POSTs and DELETE to check for the proper response
"""
from flask import json


def test_get_cars_404(test_client):
    response = test_client.get('/cars/')
    data = json.loads(response.get_data(as_text=True))
    assert data == {'message': 'The database is empty'}


def test_post_cars_200(test_client):
    response = test_client.post('/cars/',
                                data=json.dumps({"make": "volkswagen", "model": "passat"}),
                                content_type='application/json')
    assert response.status_code == 200


def test_post_cars_404(test_client):
    response = test_client.post('/cars/',
                                data=json.dumps({"make": "volk", "model": "passat"}),
                                content_type='application/json')
    data = json.loads(response.get_data(as_text=True))
    assert response.status_code == 404
    assert data == {'message': "Make doesn't exist"}


def test_delete_cars_200(test_client):
    response = test_client.delete('/cars/1')
    assert response.status_code == 200


def test_delete_cars_404(test_client):
    response = test_client.delete('/cars/1')
    data = json.loads(response.get_data(as_text=True))
    assert response.status_code == 404
    assert data == {'message': "Could not find the car..."}


def test_get_cars_200(test_client_with_db):
    response = test_client_with_db.get('/cars/')
    assert response.status_code == 200
    assert response.headers["Content-Type"] == "application/json"
    data = json.loads(response.get_data(as_text=True))
    assert data[1] == {'avg_rating': 3.5, 'id': '2', 'make': 'BMW', 'model': 'X6'}


def test_post_rate_200(test_client_with_db):
    response = test_client_with_db.post('/rate/',
                                        data=json.dumps({"car_id": 1, "rating": 3.5}),
                                        content_type='application/json')
    data = json.loads(response.get_data(as_text=True))
    assert response.status_code == 200
    assert data == 201


def test_post_rate_404(test_client_with_db):
    response = test_client_with_db.post('/rate/',
                                        data=json.dumps({"car_id": 1, "rating": 0}),
                                        content_type='application/json')
    data = json.loads(response.get_data(as_text=True))
    assert response.status_code == 404
    assert data == {'message': 'Value does not satisfy the range [1,5]'}


def test_get_popular_200(test_client_with_db):
    response = test_client_with_db.get('/popular/')
    assert response.status_code == 200
    assert response.headers["Content-Type"] == "application/json"
    data = json.loads(response.get_data(as_text=True))
    assert data[0] == {'make': 'Audi', 'model': 'A6', 'rates_number': 4}


def test_get_popular_404(test_client_with_db):
    response = test_client_with_db.get('/popular/')
    assert response.status_code == 200
    assert response.headers["Content-Type"] == "application/json"
    data = json.loads(response.get_data(as_text=True))
    assert data[0] == {'make': 'Audi', 'model': 'A6', 'rates_number': 4}
