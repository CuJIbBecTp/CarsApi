FROM python:3.8.0

RUN pip install --upgrade pip
ADD . /CarsApi
WORKDIR /CarsApi
RUN pip install -r requirements.txt
EXPOSE 5000
ENV FLASK_APP=app.py