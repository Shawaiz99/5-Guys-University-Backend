from flask import Blueprint, jsonify
from app.services.user_service import UserService
from flask_jwt_extended import jwt_required

user_bp = Blueprint("users", __name__)


@user_bp.route("/users", methods=["GET"])
@jwt_required()
def get_users():
    users = UserService.get_all_users()
    return jsonify({"users": [user.serialize() for user in users]}), 200


@user_bp.route("/users/<int:user_id>", methods=["GET"])
@jwt_required()
def get_user(user_id):
    user = UserService.get_user_by_id(user_id)
    if not user:
        return jsonify({"error": "User not found"}), 404
    return jsonify({"user": user.serialize()}), 200
