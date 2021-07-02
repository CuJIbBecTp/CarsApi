import requests

BASE = "http://127.0.0.1:5000/"

data = [{"make": "volkswagen", "model": "passat", "rate": 3},
        {"make": "BMW", "model": "s5", "rate": 4},
        {"make": "mercedes", "model": "E220", "rate": 1},
        {"make": "renault", "model": "scenic"}]

print('Add 4 rows to the DB')
for i in range(len(data)):
    response = requests.put(BASE + "cars/" + str(i), data[i])
    print(response.json())

print('Add 1 row using POST and models check')
response = requests.post(BASE + "cars/", {"make": "Volkswagen", "model": "Golf"})
print(response.json())

input()
response = requests.get(BASE + "cars/2")
print(response.json())

# test of rate update
input()
print('Test of the rating update')
response = requests.post(BASE + "rate/", {"car_id": 1, "rating": 5})
print(response.json())
response = requests.post(BASE + "rate", {"car_id": 1, "rating": 5})
print(response.json())

input()
print('Everything that database has:')
response = requests.get(BASE + "cars/")
print(response.json())
print('Everything that database has:')
response = requests.get(BASE + "cars")
print(response.json())

print('Deletion of all database')
for i in range(len(data)):
    response = requests.delete(BASE + "cars/" + str(i))
print(response.json())
