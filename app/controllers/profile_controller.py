from flask import Blueprint, jsonify, request
from app.repositories.user_repository import UserRepository
from app.extensions import db

profile_bp = Blueprint("profile", __name__)

@profile_bp.route("/api/users/<int:user_id>/profile", methods=["GET"])
def get_profile(user_id):
    user = UserRepository.get_by_id(user_id)
    if not user or not user.profile:
        return jsonify({"error": "Profile not found"}), 404

    profile = user.profile
    return jsonify({
        "first_name": profile.first_name,
        "last_name": profile.last_name,
        "bio": profile.bio,
        "avatar_url": profile.avatar_url
    }), 200


@profile_bp.route("/api/users/<int:user_id>/profile", methods=["PUT"])
def update_profile(user_id):
    user = UserRepository.get_by_id(user_id)
    if not user or not user.profile:
        return jsonify({"error": "Profile not found"}), 404

    data = request.json
    profile = user.profile
    profile.first_name = data.get("first_name", profile.first_name)
    profile.last_name = data.get("last_name", profile.last_name)
    profile.bio = data.get("bio", profile.bio)
    profile.avatar_url = data.get("avatar_url", profile.avatar_url)

    db.session.commit()

    return jsonify({
        "message": "Profile updated",
        "profile": {
            "first_name": profile.first_name,
            "last_name": profile.last_name,
            "bio": profile.bio,
            "avatar_url": profile.avatar_url
        }
    }), 200