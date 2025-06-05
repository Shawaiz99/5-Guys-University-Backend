from flask import Blueprint, jsonify
from flask_jwt_extended import get_jwt_identity, jwt_required

from app.services.wishlist_items_service import WishlistItemsService

wishlist_items_bp = Blueprint("wishlist_items", __name__)


@wishlist_items_bp.route("/wishlist/books/<int:book_id>", methods=["POST"])
@jwt_required()
def add_to_wishlist(book_id: int):
    """Add a book to the logged-in user's wishlist."""
    user_id = get_jwt_identity()
    try:
        wishlist_item = WishlistItemsService.add_to_wishlist(user_id, book_id)
        return jsonify({"message": "Book added to wishlist", "wishlist_item": wishlist_item.serialize()}), 201
    except ValueError as e:
        return jsonify({"error": str(e)}), 400


@wishlist_items_bp.route("/wishlist/books", methods=["GET"])
@jwt_required()
def get_wishlist_items():
    """Get all wishlist items for the logged-in user."""
    user_id = get_jwt_identity()
    try:
        wishlist_items = WishlistItemsService.get_wishlist_items(user_id)
        return jsonify({"wishlist_items": [item.serialize() for item in wishlist_items]}), 200
    except ValueError as e:
        return jsonify({"error": str(e)}), 400


@wishlist_items_bp.route("/wishlist/books/<int:book_id>", methods=["DELETE"])
@jwt_required()
def remove_from_wishlist(book_id: int):
    """Remove a book from the logged-in user's wishlist."""
    user_id = get_jwt_identity()
    try:
        book_title = WishlistItemsService.get_book_title(book_id)
        WishlistItemsService.remove_from_wishlist(user_id, book_id)
        return jsonify({"message": f"Book '{book_title}' removed from wishlist"}), 200
    except ValueError as e:
        return jsonify({"error": str(e)}), 400


@wishlist_items_bp.route("/wishlist/clear", methods=["POST"])
@jwt_required()
def clear_wishlist():
    """Clear all items from the logged-in user's wishlist."""
    user_id = get_jwt_identity()
    try:
        WishlistItemsService.clear_wishlist(user_id)
        return jsonify({"message": "Wishlist cleared"}), 200
    except ValueError as e:
        return jsonify({"error": str(e)}), 400
