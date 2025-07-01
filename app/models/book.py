from datetime import datetime, timezone, timedelta
from sqlalchemy import String, DateTime, Integer, Enum, Float, DECIMAL, ForeignKey
from sqlalchemy.orm import mapped_column, relationship
from app.extensions import db
from datetime import datetime


class Book(db.Model):
    __tablename__ = "books"

    id = mapped_column(Integer, primary_key=True)
    title = mapped_column(String(255), nullable=False)
    description = mapped_column(String(1000), nullable=True)
    isbn = mapped_column(String(13), unique=True, nullable=False, index=True)
    genre = mapped_column(String(100), nullable=True)
    publication_year = mapped_column(Integer, nullable=True)
    publisher = mapped_column(String(255), nullable=True)
    pages = mapped_column(Integer, nullable=True)
    rating = mapped_column(Float, nullable=True)
    price = mapped_column(DECIMAL(10, 2), nullable=True)
    availabilaty_status = mapped_column(
        Enum("Available", "Unavailable", "Out of Stock",
             name="availability_status"),
        default="Available",
        nullable=False
    )
    quantity = mapped_column(Integer, default=0, nullable=False)
    author_id = mapped_column(
        Integer, ForeignKey("authors.id"), nullable=False)
    cover_image_url = mapped_column(String(255), nullable=True)
    date_added = mapped_column(
        DateTime, default=lambda: datetime.now(timezone.utc), nullable=False)
    created_at = mapped_column(
        DateTime, default=lambda: datetime.now(timezone.utc), nullable=False)
    updated_at = mapped_column(
        DateTime, default=lambda: datetime.now(timezone.utc),
        onupdate=lambda: datetime.now(timezone.utc), nullable=False
    )

   # relationships:
    author = relationship("Author", back_populates="books")

    # wishlist_items = relationship(
    wishlist_items = relationship(
        "WishlistItem", back_populates="book", cascade="all, delete-orphan")

    images = relationship("BookImage", back_populates="book",
                          cascade="all, delete-orphan")

    purchased_by = relationship(
        "MyLibrary", back_populates="book", cascade="all, delete-orphan")

    def is_new(self):
        """This method checks if the book is new based on the date added."""
        now = datetime.now(timezone.utc)
        date_added = self.date_added
        if date_added.tzinfo is None:
            date_added = date_added.replace(tzinfo=timezone.utc)
        return (now - date_added).days < 60

    def serialize(self):
        return {
            "id": self.id,
            "title": self.title,
            "description": self.description,
            "isbn": self.isbn,
            "genre": self.genre,
            "publication_year": self.publication_year,
            "publisher": self.publisher,
            "pages": self.pages,
            "rating": self.rating,
            "price": float(self.price) if self.price is not None else None,
            "availabilaty_status": self.availabilaty_status,
            "quantity": self.quantity,
            "author_id": self.author_id,
            "author": self.author.serialize() if hasattr(self.author, 'serialize') else None,
            "cover_image_url": self.cover_image_url,
            "date_added": self.date_added.isoformat(),
            "created_at": self.created_at.isoformat(),
            "updated_at": self.updated_at.isoformat(),
            "is_new": self.is_new(),
            "images": [img.serialize() for img in self.images],
            "wishlist_items": [item.serialize() for item in self.wishlist_items],
            "purchased_by": [lib.serialize() for lib in self.purchased_by]
        }
