from flask import Blueprint, jsonify, make_response, request

from website.user import User
from .database import Database

db = Database()

bp = Blueprint("user-api", __name__, url_prefix="/api/users/")

@bp.route("/<int:user_id>", methods=["GET", "DELETE", "PUT"])
def id_user_send(user_id):
    if request.method == "GET":
        user = db.get_user_id(user_id)
        if user:
            return user.to_json()
        else:
            return jsonify({"error": "User not found with that ID"}), 404
    elif request.method == "DELETE":
        user = db.get_car_id(user_id)
        if user:
            db.delete_car(int(user_id))
            resp = make_response({"message": "User successfully removed"}, 204)
            return resp
        else:
            return jsonify({"error": "User not found with that ID"}), 404
    elif request.method == "PUT":
        json_user = request.json
        if json_user:
            user = User.from_json(json_user)
            db.update_user(user_id, user)
            resp = make_response({"message": "User successfully updated"}, 200)
            return resp
        else:
            return jsonify({"error": "User not found with that ID"}), 404

@bp.route("", methods = ["GET", "POST"])
def get_post_cars():
    if request.method == "GET":
        users = db.get_users()
        if users:        
            users_json = [user.to_json() for user in users]
            return jsonify(users_json)
        else:
            return jsonify({"error" : "Users not found"})
    if request.method == "POST":
        json_user = request.json
        if json_user:
            user = User.from_json(json_user)
            db.create_user(user)
            resp = make_response(jsonify({"message": "User successfully added"}), 201)
            return resp
        else:
            return jsonify({"error": "User not found with that ID"}), 404