from flask import Blueprint, jsonify, make_response, request

from website.car import Car
from .database import Database

db = Database()

bp = Blueprint("car-api", __name__, url_prefix="/api/cars/")

@bp.route("/<int:car_id>", methods=["GET", "DELETE", "PUT"])
def id_car_send(car_id):
    if request.method == "GET":
        car = db.get_car_id(car_id)
        if car:
            return car.to_json()
        else:
            return jsonify({"error": "Car not found with that ID"}), 404
    elif request.method == "DELETE":
        car = db.get_car_id(car_id)
        if car:
            db.delete_car(int(car_id))
            resp = make_response({"message": "Car successfully removed"}, 204)
            return resp
        else:
            return jsonify({"error": "Car not found with that ID"}), 404
    elif request.method == "PUT":
        json_car = request.json
        if json_car:
            car = Car.from_json(json_car)
            db.update_car(car_id, car)
            resp = make_response({"message": "Car successfully updated"}, 200)
            return resp
        else:
            return jsonify({"error": "Car not found with that ID"}), 404

@bp.route("", methods = ["GET", "POST"])
def get_post_cars():
    if request.method == "GET":
        cars = db.get_cars()
        if cars:        
            cars_json = [car.to_json() for car in cars]
            return jsonify(cars_json)
        else:
            return jsonify({"error" : "Cars not found"})
    if request.method == "POST":
        json_car = request.json
        if json_car:
            car = Car.from_json(json_car)
            db.add_car(car)
            resp = make_response(jsonify({"message": "Car successfully added"}), 201)
            return resp
        else:
            return jsonify({"error": "Car not found with that ID"}), 404


        
    
        




























