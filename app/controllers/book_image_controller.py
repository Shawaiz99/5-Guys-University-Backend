from flask import Blueprint, request, jsonify
from flask_jwt_extended import jwt_required
from app.services.book_image_service import BookImageService

book_image_bp = Blueprint("book_image_bp", __name__)
book_image_service = BookImageService()


@book_image_bp.route("/<int:book_id>/images", methods=["POST"])
def upload_book_image(book_id):
    file = request.files["file"]
    is_primary = request.form.get("is_primary", "false").lower() == "true"
    caption = request.form.get("caption")

    return jsonify(book_image_service.upload_book_image(book_id, file, is_primary, caption).to_dict()), 201
