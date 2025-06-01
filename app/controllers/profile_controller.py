from flask import Blueprint, jsonify, request
from app.repositories.user_repository import UserRepository
from app.extensions import db
from app.utils.validators import is_valid_name, is_valid_bio, is_valid_url

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
        "avatar_url": profile.avatar_url,
        "created_at": profile.created_at.isoformat(),
        "updated_at": profile.updated_at.isoformat(),
    }), 200

@profile_bp.route("/api/users/<int:user_id>/profile", methods=["PUT"])
def update_profile(user_id):
    user = UserRepository.get_by_id(user_id)
    if not user or not user.profile:
        return jsonify({"error": "Profile not found"}), 404

    data = request.get_json()
    profile = user.profile

    first_name = data.get("first_name", profile.first_name)
    last_name = data.get("last_name", profile.last_name)
    bio = data.get("bio", profile.bio)
    avatar_url = data.get("avatar_url", profile.avatar_url)

    if not is_valid_name(first_name):
        return jsonify({"error": "Invalid first name"}), 400
    if not is_valid_name(last_name):
        return jsonify({"error": "Invalid last name"}), 400
    if not is_valid_bio(bio):
        return jsonify({"error": "Invalid bio"}), 400
    if not is_valid_url(avatar_url):
        return jsonify({"error": "Invalid avatar URL"}), 400

    profile.first_name = first_name
    profile.last_name = last_name
    profile.bio = bio
    profile.avatar_url = avatar_url

    db.session.commit()

    return jsonify({
        "message": "Profile updated",
        "profile": {
            "first_name": profile.first_name,
            "last_name": profile.last_name,
            "bio": profile.bio,
            "avatar_url": profile.avatar_url,
            "created_at": profile.created_at.isoformat(),
            "updated_at": profile.updated_at.isoformat(),
        }
    }), 200