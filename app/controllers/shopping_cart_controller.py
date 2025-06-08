from flask import Blueprint, request, jsonify
from flask_jwt_extended import jwt_required, get_jwt_identity
from app.services.shopping_cart_service import ShoppingCartService

shopping_cart_bp = Blueprint("shopping_cart", __name__)


@shopping_cart_bp.route("/cart", methods=["GET"])
@jwt_required()
def get_cart_items():
    user_id = get_jwt_identity()
    items = ShoppingCartService.get_cart_items(user_id)
    if not items:
        return jsonify({"message": "Cart is empty"}), 200
    return jsonify({"items": [{"User_ID": item.user_id, "book_id": item.book_id} for item in items]})


@shopping_cart_bp.route("/cart/books/<int:book_id>", methods=["POST"])
@jwt_required()
def add_to_cart(book_id: int):
    """Add a book to the logged-in user's shopping cart."""
    user_id = get_jwt_identity()
    try:
        item = ShoppingCartService.add_book_to_cart(user_id, book_id)
        # Return 201 Created status
        return jsonify({"message": "Item added", "id": item.id, "book_id": item.book_id}), 201
    except ValueError as e:
        # Handle case where book is already in cart
        return jsonify({"error": str(e)}), 400


@shopping_cart_bp.route("/cart/<int:book_id>", methods=["DELETE"])
@jwt_required()
def remove_from_cart(book_id: int):
    user_id = get_jwt_identity()
    try:
        ShoppingCartService.remove_from_cart(user_id, book_id)
        return jsonify({"message": "Item removed"})
    except ValueError as e:
        return jsonify({"error": str(e)}), 400


@shopping_cart_bp.route("/cart/clear", methods=["POST"])
@jwt_required()
def clear_cart():
    user_id = get_jwt_identity()
    ShoppingCartService.clear_cart(user_id)
    return jsonify({"message": "Cart cleared"})
