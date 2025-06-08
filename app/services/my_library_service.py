from app.repositories.my_library_repository import MyLibraryRepository
from app.models.my_library import MyLibrary
from typing import List


class MyLibraryService:

    @staticmethod
    def add_book_to_library(user_id: int, book_id: int) -> MyLibrary:
        """Add book to the user's library."""
        return MyLibraryRepository.add_book_to_library(user_id, book_id)

    @staticmethod
    def get_books_by_user_id(user_id: int) -> List[MyLibrary]:
        """Get all books in the user's library."""
        return MyLibraryRepository.get_library_by_user_id(user_id)

    @staticmethod
    def get_filtered_books(
        user_id: int,
        title: str = None,
        author: str = None,
        genre: str = None,
        isbn: str = None
    ) -> List[MyLibrary]:
        """Get filtered books in the user's library."""
        return MyLibraryRepository.get_filtered_books(user_id, title, author, isbn, genre)
