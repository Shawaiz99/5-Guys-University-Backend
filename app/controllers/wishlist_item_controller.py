from flask import Blueprint, jsonify
from flask_jwt_extended import get_jwt_identity, jwt_required
from app.models.wishlist_item import WishlistItem
from app.extensions import db

wishlist_items_bp = Blueprint("wishlist_items", __name__)


@wishlist_items_bp.route("/wishlist/books/<int:book_id>", methods=["POST"])
@jwt_required()
def add_to_wishlist(book_id):
    user_id = get_jwt_identity()
    existing = WishlistItem.query.filter_by(
        user_id=user_id, book_id=book_id).first()
    if existing:
        return jsonify({"message": "Book already in wishlist"}), 200
    wishlist_item = WishlistItem(user_id=user_id, book_id=book_id)
    db.session.add(wishlist_item)
    try:
        db.session.commit()
        return jsonify({"message": "Book added to wishlist"}), 201
    except Exception as e:
        db.session.rollback()
        return jsonify({"error": str(e)}), 500


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
def remove_from_wishlist(book_id):
    """Remove a book from the logged-in user's wishlist."""
    user_id = get_jwt_identity()
    item = WishlistItem.query.filter_by(
        user_id=user_id, book_id=book_id).first()
    if not item:
        return jsonify({"error": "Not found"}), 404
    db.session.delete(item)
    db.session.commit()
    return jsonify({"message": "Removed"}), 200


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
