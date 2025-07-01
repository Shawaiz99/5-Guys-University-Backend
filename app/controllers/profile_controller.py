from flask import Blueprint, jsonify, request
from app.repositories.user_repository import UserRepository
from app.extensions import db
from app.utils.validators import is_valid_name, is_valid_bio, is_valid_url
from app.services.profile_service import ProfileService
from flask_jwt_extended import get_jwt_identity, jwt_required

profile_bp = Blueprint("profile_bp", __name__)


@profile_bp.route("/users/<int:user_id>/profile", methods=["GET"])
@jwt_required()
def get_user_profile(user_id: int):
    user_id_jwt = int(get_jwt_identity())

    if not user_id_jwt == user_id:
        return jsonify({"error": "You are not authorized to access this account."})

    # find the profile
    profile = ProfileService.get_profile_by_user_id(user_id)

    if profile:
        return jsonify(profile.serialize()), 200
    else:
        return (
            jsonify({"error": "404 Not Found",
                    "message": f"User with id: {user_id} not found."}),
            404,
        )


@profile_bp.route("/users/<int:user_id>/profile", methods=["PUT"])
@jwt_required()
def update_user_profile(user_id: int):
    user_id_jwt = int(get_jwt_identity())

    if not user_id_jwt == user_id:
        return jsonify({"error": "You are not authorized to access this account."})

    profile = ProfileService.get_profile_by_user_id(user_id)

    if not profile:
        return (
            jsonify({"error": "404 Not Found",
                    "message": f"User with id: {user_id} not found."}),
            404,
        )

    data = request.get_json()

    if not data:
        return jsonify({"error": "400 Bad Request", "message": "Data as JSON not provided"}), 400

    # update data
    try:
        profile = ProfileService.update_user_profile(user_id, data)
        return jsonify(
            {"message": "User profile successfully updated.",
                "profile": profile.serialize()}
        )
    except ValueError as e:
        return jsonify({"error": "Something went wrong", "message": str(e)})


@profile_bp.route("/users/<int:user_id>/profile/image", methods=["PATCH"])
@jwt_required()
def update_user_profile_image(user_id: int):
    user_id_jwt = int(get_jwt_identity())

    if not user_id_jwt == user_id:
        return jsonify({"error": "You are not authorized to access this account."})

    profile = ProfileService.get_profile_by_user_id(user_id)
    if not profile:
        return jsonify({"error": "User Not Found"}), 404

    if not request.content_type.startswith("multipart/form-data"):
        return jsonify({"error": "Content type should be multipart/form-data"})

    image_file = request.files.get("image")

    if not image_file:
        return jsonify({"error": "Image not provided"}), 400

    if profile.cloudinary_public_id:
        print(f"cloudinary public id {profile.cloudinary_public_id}")
        cloudinary.uploader.destroy(profile.cloudinary_public_id)

    uploaded_result = cloudinary.uploader.upload(
        image_file, folder="profile_images")
    print(uploaded_result)
    profile.avatar_url = uploaded_result["secure_url"]
    profile.cloudinary_public_id = uploaded_result["public_id"]

    ProfileService.update_user_profile(
        user_id,
        {"avatar_url": profile.avatar_url,
            "cloudinary_public_id": profile.cloudinary_public_id},
    )

    return jsonify({"message": "successfully uploaded image", "profile": profile.serialize()})


@profile_bp.route("/users/<int:user_id>/profile", methods=["DELETE"])
@jwt_required()
def delete_user_profile(user_id: int):
    user_id_jwt = int(get_jwt_identity())

    if not user_id_jwt == user_id:
        return jsonify({"error": "You are not authorized to access this account."}), 403

    try:
        ProfileService.delete_profile_by_user_id(user_id)
        return jsonify({"message": "User profile successfully deleted."}), 200
    except ValueError as e:
        return jsonify({"error": "Something went wrong", "message": str(e)}), 400


@profile_bp.route("/users/<int:user_id>/create/profile", methods=["POST"])
@jwt_required()
def create_user_profile(user_id: int):
    user_id_jwt = int(get_jwt_identity())

    if not user_id_jwt == user_id:
        return jsonify({"error": "You are not authorized to access this account."}), 403

    data = request.get_json()

    if not data:
        return jsonify({"error": "400 Bad Request", "message": "Data as JSON not provided"}), 400

    # validate data
    if "name" in data and not is_valid_name(data["name"]):
        return jsonify({"error": "Invalid name format"}), 400

    if "bio" in data and not is_valid_bio(data["bio"]):
        return jsonify({"error": "Invalid bio format"}), 400

    if "website" in data and not is_valid_url(data["website"]):
        return jsonify({"error": "Invalid website URL"}), 400

    try:
        user = UserRepository.get_by_id(user_id)
        profile = ProfileService.create_profile_for_user(user, data)
        return jsonify(
            {"message": "User profile successfully created.",
                "profile": profile.serialize()}
        ), 201
    except ValueError as e:
        return jsonify({"error": "Something went wrong", "message": str(e)}), 400
