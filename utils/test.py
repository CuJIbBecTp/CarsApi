import requests

BASE = "http://127.0.0.1:5000/"

data = [{"make": "volkswagen", "model": "passat", "rate": 3},
        {"make": "BMW", "model": "X6", "rate": 3},
        {"make": "BMW", "model": "X6", "rate": 4},
        {"make": "mercedes-benz", "model": "ML-Class", "rate": 1},
        {"make": "mercedes-benz", "model": "ML-Class", "rate": 2},
        {"make": "mercedes-benz", "model": "ML-Class", "rate": 3},
        {"make": "audi", "model": "A6", "rate": 1},
        {"make": "audi", "model": "A6", "rate": 2},
        {"make": "audi", "model": "A6", "rate": 3},
        {"make": "audi", "model": "A6", "rate": 4}]

for i in data:
    print('Add 1 row using POST and models check')
    response = requests.post(BASE + "cars/", i)
    print(response.json())


# test of rate update
print('Test of the rating update')
response = requests.post(BASE + "rate/", {"car_id": 6, "rating": 3.5})
print(response.json())
response = requests.post(BASE + "rate", {"car_id": 7, "rating": 4.5})
print(response.json())

print('All the unique models of the database:')
response = requests.get(BASE + "cars/")
print(response.json())

print('Popularity of the cars:')
response = requests.get(BASE + "popular/")
print(response.json())

#print('Deletion of one row')
#response = requests.delete(BASE + "cars/" + str(5))
#print(response)
