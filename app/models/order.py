from sqlalchemy import Integer, String, DateTime, Float, ForeignKey
from sqlalchemy.orm import mapped_column, relationship
from app.extensions import db
from datetime import datetime, timezone


class Order(db.Model):
    __tablename__ = "orders"
    id = mapped_column(Integer, primary_key=True)
    user_id = mapped_column(Integer, ForeignKey("users.id"), nullable=False)
    address_line = mapped_column(String(255), nullable=False)
    city = mapped_column(String(100), nullable=False)
    state = mapped_column(String(100), nullable=False)
    zipcode = mapped_column(String(20), nullable=False)
    card_last4 = mapped_column(String(4), nullable=False)
    total_price = mapped_column(Float, nullable=False)
    status = mapped_column(String(50), default="Pending", nullable=False)
    created_at = mapped_column(
        DateTime, default=lambda: datetime.now(timezone.utc), nullable=False)

    user = relationship("User")
    items = relationship("OrderItem", back_populates="order",
                         cascade="all, delete-orphan")

    def serialize(self):
        return {
            "id": self.id,
            "user_id": self.user_id,
            "address_line": self.address_line,
            "city": self.city,
            "state": self.state,
            "zipcode": self.zipcode,
            "card_last4": self.card_last4,
            "total_price": self.total_price,
            "status": self.status,
            "created_at": self.created_at.isoformat(),
            "items": [item.serialize() for item in self.items]
        }

    def is_new(self):
        now = datetime.now(timezone.utc)
        date_added = self.created_at
        if date_added.tzinfo is None:
            date_added = date_added.replace(tzinfo=timezone.utc)
        return (now - date_added).days < 60


class OrderItem(db.Model):
    __tablename__ = "order_items"
    id = mapped_column(Integer, primary_key=True)
    order_id = mapped_column(Integer, ForeignKey("orders.id"), nullable=False)
    book_id = mapped_column(Integer, ForeignKey("books.id"), nullable=False)
    quantity = mapped_column(Integer, default=1, nullable=False)
    price = mapped_column(Float, nullable=False)

    order = relationship("Order", back_populates="items")
    book = relationship("Book")

    def serialize(self):
        return {
            "id": self.id,
            "order_id": self.order_id,
            "book_id": self.book_id,
            "quantity": self.quantity,
            "price": self.price,
            "book": self.book.serialize() if self.book else None
        }
