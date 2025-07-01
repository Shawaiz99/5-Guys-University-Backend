from app.extensions import db
from sqlalchemy.orm import mapped_column, relationship
from sqlalchemy import Integer, DateTime, ForeignKey, UniqueConstraint
from datetime import datetime, timezone


class MyLibrary(db.Model):
    __tablename__ = "my_library"
    __table_args__ = (UniqueConstraint(
        "user_id", "book_id", name="unique_user_book"),)
    id = mapped_column(db.Integer, primary_key=True)
    user_id = mapped_column(Integer, ForeignKey("users.id"), nullable=False)
    book_id = mapped_column(Integer, ForeignKey("books.id"), nullable=False)
    created_at = mapped_column(
        DateTime, default=lambda: datetime.now(timezone.utc), nullable=False)

    user = relationship("User", back_populates="library")
    book = relationship("Book", back_populates="purchased_by")

    def serialize(self):
        return {
            "id": self.id,
            "user_id": self.user_id,
            "book_id": self.book_id,
            "created_at": self.created_at.isoformat(),
            "book": self.book.serialize() if self.book else None

        }
