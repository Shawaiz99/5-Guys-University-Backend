from app.models.book import Book
from app.models.shopping_cart import ShoppingCart
from typing import List

from sqlalchemy import select
from sqlalchemy.exc import IntegrityError

from app.extensions import db


class ShoppingCartRepository:
    @staticmethod
    def add_to_cart(user_id: int, book_id: int) -> ShoppingCart:

        book = db.session.get(Book, book_id)
        if not book:
            raise ValueError("This book is not registered.")

        stmt = select(ShoppingCart).where(
            ShoppingCart.user_id == user_id,
            ShoppingCart.book_id == book_id
        )
        result = db.session.execute(stmt)
        existing = result.scalars().first()
        if existing:
            raise ValueError("This book is already in your cart.")

        cart_item = ShoppingCart(user_id=user_id, book_id=book_id)
        db.session.add(cart_item)
        try:
            db.session.commit()
        except IntegrityError:
            db.session.rollback()
            raise ValueError("Database error while adding to cart.")
        return cart_item

    @staticmethod
    def get_cart_items(user_id: int) -> List[ShoppingCart]:
        """Get all cart items for a user."""
        stmt = select(ShoppingCart).where(ShoppingCart.user_id == user_id)
        result = db.session.execute(stmt)
        return result.scalars().all()

    @staticmethod
    def remove_from_cart(user_id: int, book_id: int) -> None:
        """Remove a book from the user's shopping cart."""
        stmt = select(ShoppingCart).where(
            ShoppingCart.user_id == user_id,
            ShoppingCart.book_id == book_id
        )
        result = db.session.execute(stmt)
        cart_item = result.scalars().first()
        if cart_item:
            db.session.delete(cart_item)
            db.session.commit()
        else:
            raise ValueError("This book is not in your cart.")

    @staticmethod
    def clear_cart(user_id: int) -> None:
        """Clear the user's shopping cart."""
        stmt = select(ShoppingCart).where(ShoppingCart.user_id == user_id)
        result = db.session.execute(stmt)
        cart_items = result.scalars().all()
        for item in cart_items:
            db.session.delete(item)
        db.session.commit()
        if not cart_items:
            raise ValueError("Your cart is already empty.")
        return cart_items

    @staticmethod
    def get_cart_item(user_id: int, book_id: int) -> ShoppingCart | None:
        """Get a specific cart item by user_id and book_id."""
        stmt = select(ShoppingCart).where(
            ShoppingCart.user_id == user_id,
            ShoppingCart.book_id == book_id
        )
        result = db.session.execute(stmt)
        return result.scalars().first()
