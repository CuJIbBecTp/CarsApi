import requests

BASE = "http://127.0.0.1:5000/"

data = [{"make": "volkswagen", "model": "passat", "rate": 3},
        {"make": "BMW", "model": "s5", "rate": 4},
        {"make": "mercedes", "model": "E220", "rate": 5},
        {"make": "renault", "model": "scenic"}]

for i in range(len(data)):
    response = requests.put(BASE + "cars/" + str(i), data[i])
    print(response.json())

input()
response = requests.delete(BASE + "cars/0")
print(response)
input()
response = requests.get(BASE + "cars/2")
print(response.json())
#response = requests.post(BASE + "helloworld")
#print(response.json())
