from flask import Blueprint, request, jsonify
from flask_jwt_extended import jwt_required, get_jwt_identity
from app.services.order_service import OrderService

order_bp = Blueprint("order_api", __name__)


@order_bp.route("/orders", methods=["POST"])
@jwt_required()
def create_order():
    user_id = get_jwt_identity()
    data = request.get_json()
    address_line = data.get("address_line")
    city = data.get("city")
    state = data.get("state")
    zipcode = data.get("zipcode")
    card_last4 = data.get("card_last4")

    if not all([address_line, city, state, zipcode, card_last4]):
        return jsonify({"error": "All address and card fields are required."}), 400

    order, error = OrderService.create_order_from_cart(
        user_id, address_line, city, state, zipcode, card_last4
    )
    if error:
        return jsonify({"error": error}), 400

    return jsonify({"order": order.serialize()}), 201


@order_bp.route("/orders", methods=["GET"])
@jwt_required()
def get_user_orders():
    user_id = get_jwt_identity()
    orders = OrderService.get_user_orders(user_id)
    return jsonify([order.serialize() for order in orders]), 200


@order_bp.route("/orders/<int:order_id>", methods=["GET"])
@jwt_required()
def get_order(order_id):
    order = OrderService.get_order(order_id)
    if not order:
        return jsonify({"error": "Order not found"}), 404
    return jsonify(order.serialize()), 200
