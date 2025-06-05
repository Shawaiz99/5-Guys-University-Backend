from typing import List, Optional

from sqlalchemy import select
from sqlalchemy.exc import IntegrityError

from app.extensions import db
from app.models.book import Book
from app.models.wishlist_item import WishlistItem


class WishlistItemRepository:
    @staticmethod
    def add_to_wishlist(user_id: int, book_id: int) -> WishlistItem:
        """Add a book to the user's wishlist."""
        wishlist_item = WishlistItem(user_id=user_id, book_id=book_id)
        db.session.add(wishlist_item)
        try:
            db.session.commit()
        except IntegrityError:
            db.session.rollback()
            raise ValueError("This book is already in your wishlist.")
        return wishlist_item

    @staticmethod
    def get_wishlist_items(user_id: int) -> List[WishlistItem]:
        """Get all wishlist items for a user."""
        stmt = select(WishlistItem).where(WishlistItem.user_id == user_id)
        result = db.session.execute(stmt)
        return result.scalars().all()

    @staticmethod
    def remove_from_wishlist(user_id: int, book_id: int) -> None:
        """Remove a book from the user's wishlist."""
        stmt = select(WishlistItem).where(
            WishlistItem.user_id == user_id,
            WishlistItem.book_id == book_id
        )
        result = db.session.execute(stmt)
        wishlist_item = result.scalars().first()
        if wishlist_item:
            db.session.delete(wishlist_item)
            db.session.commit()
