from datetime import datetime, timezone

from sqlalchemy import DateTime, ForeignKey, Integer, UniqueConstraint
from sqlalchemy.orm import mapped_column, relationship

from app.extensions import db


class WishlistItem(db.Model):
    __tablename__ = "wishlist_items"
    __table_args__ = (UniqueConstraint(
        "user_id", "book_id", name="uq_wishlist_item"),)

    id = mapped_column(Integer, primary_key=True)
    user_id = mapped_column(Integer, ForeignKey("users.id"), nullable=False)
    book_id = mapped_column(Integer, ForeignKey("books.id"), nullable=False)
    created_at = mapped_column(
        DateTime(timezone=True), default=datetime.now(timezone.utc))

    user = relationship("User", back_populates="wishlist_items")
    book = relationship("Book", back_populates="wishlist_items")

    def serialize(self):
        return {
            "id": self.id,
            "user_id": self.user_id,
            "book_id": self.book_id,
            "created_at": self.created_at.isoformat()
        }
