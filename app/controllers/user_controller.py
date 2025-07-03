from flask import Blueprint, jsonify, request
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

@user_bp.route("/users/<int:user_id>", methods=["DELETE"])
@jwt_required()
def delete_user(user_id):
    user = UserService.get_user_by_id(user_id)
    if not user:
        return jsonify({"error": "User not found"}), 404

    UserService.delete_user(user)
    return jsonify({"message": "User deleted successfully"}), 200

@user_bp.route("/users/<int:user_id>", methods=["PUT"])
@jwt_required()
def update_user_route(user_id):
    user = UserService.get_user_by_id(user_id)
    if not user:
        return jsonify({"error": "User not found"}), 404

    data = request.get_json()

    try:
        updated_user = UserService.update_user(user, data)
        return jsonify({"user": updated_user.serialize()}), 200
    except Exception as e:
        return jsonify({"error": str(e)}), 400

@user_bp.route("/users/<int:user_id>/change-password", methods=["POST"])
@jwt_required()
def change_password(user_id):
    user = UserService.get_user_by_id(user_id)
    if not user:
        return jsonify({"error": "User not found"}), 404

    data = request.get_json()
    print("Received data for change password:", data)
    try:
        updated_user = UserService.change_password(user, data)
        return jsonify({"user": updated_user.serialize()}), 200
    except Exception as e:
        return jsonify({"error": str(e)}), 400

   
