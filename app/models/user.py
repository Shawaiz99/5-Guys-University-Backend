from datetime import datetime
from sqlalchemy.orm import Mapped, mapped_column, relationship
from sqlalchemy import String, DateTime, Integer, Boolean, Enum
from app.extensions import db
from werkzeug.security import generate_password_hash, check_password_hash


class User(db.Model):
    __tablename__ = "users"

    id: Mapped[int] = mapped_column(primary_key=True)
    username: Mapped[str] = mapped_column(db.String(255), unique=True)
    email: Mapped[str] = mapped_column(
        db.String, unique=True, nullable=False, index=True)
    password: Mapped[str] = mapped_column(db.String, nullable=False)
    is_active: Mapped[bool] = mapped_column(db.Boolean, default=True)
    created_at: Mapped[datetime] = mapped_column(
        DateTime, default=datetime.utcnow, nullable=False)
    updated_at: Mapped[datetime] = mapped_column(
        DateTime, default=datetime.utcnow, onupdate=datetime.utcnow, nullable=False)

    user_role: Mapped[str] = mapped_column(
        Enum("Student", "Professor", "Librarian", name="role"),
        default="Student"
    )
    is_admin: Mapped[bool] = mapped_column(db.Boolean, default=False)

    profile = relationship("Profile", back_populates="user",
                           uselist=False, cascade="all, delete-orphan")
    wishlist_items = relationship(
        "WishlistItem", back_populates="user", cascade="all, delete-orphan")
    library = relationship(
        "MyLibrary", back_populates="user", cascade="all, delete-orphan")
    shopping_cart = relationship(
        "ShoppingCart", back_populates="user", cascade="all, delete-orphan")

    def set_password(self, password):
        self.password = generate_password_hash(password)

    def check_password(self, password):
        return check_password_hash(self.password, password)

    def serialize(self):
        return {
            "id": self.id,
            "username": self.username,
            "email": self.email,
            "role": self.user_role,
            "is_active": self.is_active,
            "created_at": self.created_at.isoformat(),
            "updated_at": self.updated_at.isoformat(),
            "is_admin": self.is_admin,
            "profile": self.profile.serialize() if self.profile else None,
            "wishlist_items": [item.serialize() for item in self.wishlist_items],
            "library": self.library.serialize() if self.library else None,
            "shopping_cart": [cart.serialize() for cart in self.shopping_cart] if self.shopping_cart else []
        }
