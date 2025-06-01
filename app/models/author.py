from sqlalchemy import String, Integer
from sqlalchemy.orm import mapped_column, relationship
from app.extensions import db


class Author(db.Model):
    __tablename__ = "authors"
    id = mapped_column(Integer, primary_key=True)
    name = mapped_column(String(255), nullable=False)
    biography = mapped_column(String(1000), nullable=True)
    photo_url = mapped_column(String(255), nullable=True)

    # One author has many books
    books = relationship("Book", back_populates="author",
                         cascade="all, delete-orphan")

    def serialize(self):
        return {
            "id": self.id,
            "name": self.name,
            "biography": self.biography,
            "photo_url": self.photo_url
        }
