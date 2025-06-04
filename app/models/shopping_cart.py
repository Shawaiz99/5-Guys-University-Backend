from sqlalchemy import Integer, ForeignKey
from sqlalchemy.orm import mapped_column, relationship
from app.extensions import db


class ShoppingCart(db.Model):
    __tablename__ = "shopping_carts"
    id = mapped_column(Integer, primary_key=True)
    user_id = mapped_column(Integer, ForeignKey("users.id"), nullable=False)
    book_id = mapped_column(Integer, ForeignKey("books.id"), nullable=False)
    user = relationship("User", back_populates="shopping_cart")
    book = relationship("Book")

    def serialize(self):
        return {
            "id": self.id,
            "user_id": self.user_id,
            "book_id": self.book_id,
            "user": self.user.serialize() if self.user else None,
            "book": self.book.serialize() if self.book else None
        }
