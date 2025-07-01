from app.repositories.order_repository import OrderRepository
from app.repositories.shopping_cart_repository import ShoppingCartRepository
from app.models.my_library import MyLibrary
from app.extensions import db


class OrderService:
    @staticmethod
    def create_order_from_cart(user_id, address_line, city, state, zipcode, card_last4):
        cart_items = ShoppingCartRepository.get_cart_items(user_id)
        if not cart_items:
            return None, "Cart is empty"

        items_data = []
        total_price = 0
        for item in cart_items:
            price = float(item.book.price or 0)
            items_data.append({
                "book_id": item.book_id,
                "quantity": 1,
                "price": price
            })
            total_price += price

        order = OrderRepository.create_order(
            user_id=user_id,
            address_line=address_line,
            city=city,
            state=state,
            zipcode=zipcode,
            card_last4=card_last4,
            total_price=total_price,
            status="Pending",
            items_data=items_data
        )

        for item in order.items:
            exists = db.session.query(MyLibrary).filter_by(
                user_id=user_id, book_id=item.book_id).first()
            if not exists:
                db.session.add(
                    MyLibrary(user_id=user_id, book_id=item.book_id))
        db.session.commit()

        ShoppingCartRepository.clear_cart(user_id)
        return order, None

    @staticmethod
    def get_user_orders(user_id):
        return OrderRepository.get_orders_by_user(user_id)

    @staticmethod
    def get_order(order_id):
        return OrderRepository.get_order_by_id(order_id)
