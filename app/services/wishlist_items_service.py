from typing import Optional

from app.models.wishlist_item import WishlistItem
from app.repositories.book_repository import BookRepository
from app.repositories.user_repository import UserRepository
from app.repositories.wishlist_item_repository import WishlistItemRepository


class WishlistItemsService:
    @staticmethod
    def add_to_wishlist(user_id: int, book_id: int) -> WishlistItem:
        """Add a book to the user's wishlist."""
        user = UserRepository.get_by_id(user_id)
        if not user:
            raise ValueError("User not found.")

        book = BookRepository.get_by_id(book_id)
        if not book:
            raise ValueError("Book not found.")

        return WishlistItemRepository.add_to_wishlist(user_id, book_id)

    @staticmethod
    def get_wishlist_items(user_id: int) -> list[WishlistItem]:
        """Get all wishlist items for a user."""
        return WishlistItemRepository.get_wishlist_items(user_id)

    @staticmethod
    def remove_from_wishlist(user_id: int, book_id: int) -> None:
        """Remove a book from the user's wishlist."""
        WishlistItemRepository.remove_from_wishlist(user_id, book_id)

    @staticmethod
    def clear_wishlist(user_id: int) -> None:
        """Clear all items from the user's wishlist."""
        user = UserRepository.get_by_id(user_id)
        if not user:
            raise ValueError("User not found.")

        WishlistItemRepository.clear_wishlist(user_id)

    @staticmethod
    def get_wishlist_item_by_id(wishlist_item_id: int) -> Optional[WishlistItem]:
        """Get a wishlist item by its ID."""
        return WishlistItemRepository.get_by_id(wishlist_item_id)
