from app.models.order import Order, OrderItem
from app.extensions import db
from sqlalchemy import select
from typing import List


class OrderRepository:
    @staticmethod
    def create_order(user_id, address_line, city, state, zipcode, card_last4, total_price, status, items_data):
        order = Order(
            user_id=user_id,
            address_line=address_line,
            city=city,
            state=state,
            zipcode=zipcode,
            card_last4=card_last4,
            total_price=total_price,
            status=status
        )
        db.session.add(order)
        db.session.flush()

        for item in items_data:
            order_item = OrderItem(
                order_id=order.id,
                book_id=item["book_id"],
                quantity=item["quantity"],
                price=item["price"]
            )
            db.session.add(order_item)
        db.session.commit()

        return order

    @staticmethod
    def get_orders_by_user(user_id: int) -> List[Order]:
        stmt = select(Order).where(Order.user_id == user_id)
        result = db.session.execute(stmt)
        return result.scalars().all()

    @staticmethod
    def get_order_by_id(order_id: int) -> Order | None:
        stmt = select(Order).where(Order.id == order_id)
        result = db.session.execute(stmt)
        return result.scalars().first()

    @staticmethod
    def delete_order(order_id: int) -> None:
        order = db.session.get(Order, order_id)
        if order:
            db.session.delete(order)
            db.session.commit()

    @staticmethod
    def get_all_orders() -> List[Order]:
        stmt = select(Order)
        result = db.session.execute(stmt)
        return result.scalars().all()
