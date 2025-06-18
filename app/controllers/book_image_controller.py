from flask import Blueprint, request, jsonify
from flask_jwt_extended import jwt_required
from app.services.book_image_service import upload_image

book_image_bp = Blueprint("book_image_bp", __name__)

@book_image_bp.route("/<int:book_id>/images", methods=["POST"])
@jwt_required()
def upload_book_image(book_id):
    return upload_image(book_id, request)