# CarsApi

A simple REST API  - a basic car makes and models database interacting with an external API

The deployed server of CarsApi is accessible at the heroku virtual machine :
- https://testcarsapi.herokuapp.com

## How to use:

There are two ways to run the CarsApi project:
1. execute wsgi.py using python
2. build a docker container

### The First way:

1. Clone the directory on your device
    - git clone https://github.com/CuJIbBecTp/CarsApi.git
2. Install Python 3 if you don't have it (https://www.python.org/downloads/
3. Create the virtual environment inside the project folder
    - python -m venv \path\to\MyCars
4. activate the created environment
    - cd \venv\Scripts
    - activate
5. Install all the required libraries from requirements.txt
    - pip install -r requirements.txt
6. You can run the application now using
    - python wsgi.py

### The second way:

1. Clone the directory on your device
    - https://github.com/CuJIbBecTp/CarsApi.git
3. install docker and docker-compose
    - https://docs.docker.com/compose/install/
3. enter the project folder
    - cd \path\to\MyCars
4. execute the following commands:
    - docker-compose build
    - docker-compose up

At this step, the application should be working.
To check that API is working, simply open a browser and click:
http://127.0.0.1:5000/cars/
If everything was installed correctly, you will get the following text on the response:
{"message": "The database is empty"}

## API commands description

1. POST /cars/

   Request body contains car make and model name.
   Based on this data, its existence is checked here https://vpic.nhtsa.dot.gov/api/

   If the car doesn't exist - it returns an error:
    - {"message": "Make doesn't exist"}

   If the car exists - it should be saved in the database
    - Content-Type: application/json;charset=UTF-8
    - {"make" : "Volkswagen","model" : "Golf"}

2. DELETE /cars/{ id }

   Deletes the car with the given id from database.

   If the car doesn't exist in database - returns an error:
    - {'message': "Could not find the car..."}

3. POST /rate/

   Adds a rate for a car from 1 to 5:
    - Content-Type: application/json;charset=UTF-8
    - {"car_id" : 1,"rating" : 5}

   Returns an error if rate is out of the range:
    - {"message": "Value does not satisfy the range [1,5]"}

4. GET /cars

   Fetches a list of all cars already present in application database with their current average rate
    - Content-Type: application/json;charset=UTF-8

   Response:
    - [{"id" : 1,"make" : "Volkswagen","model" : "Golf","avg_rating" : 5.0},
    - {"id" : 2,"make" : "Volkswagen","model" : "Passat","avg_rating" : 4.7}]

   Returns an error if the database is empty:
    - {"message": "The database is empty"}

5. GET /popular/

   Returns top cars already present in the database ranking based on a number of rates (not average rate values!)
    - Content-Type: application/json;charset=UTF-8

   Response:
    - [{"id" : 1,"make" : "Volkswagen","model" : "Golf","rates_number" : 100},
    - {"id" : 2,"make" : "Volkswagen","model" : "Passat","rates_number" : 31}]

   Returns an error if the database is empty:
    - {"message": "The database is empty"}