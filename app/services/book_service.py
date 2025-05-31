from typing import Any, Dict, List, Optional
from app.models.book import Book
from app.repositories.book_repository import BookRepository
from sqlalchemy import DECIMAL


class BookService:
    @staticmethod
    def create_book(
        title: str,
        author_id: int,
        genre: str = None,
        description: str = None,
        pages: int = None,
        rating: float = None,
        price: float = None,
        availabilaty_status: str = "Available",
        quantity: int = 0,
        cover_image_url: str = None,
        isbn: str = None,
        publication_year: int = None,
        publisher: str = None
    ) -> 'Book':
        """Create a new book"""
        from app.repositories.book_repository import BookRepository
        return BookRepository.create_book(
            title=title,
            author_id=author_id,
            genre=genre,
            description=description,
            pages=pages,
            rating=rating,
            price=price,
            availabilaty_status=availabilaty_status,
            quantity=quantity,
            cover_image_url=cover_image_url,
            isbn=isbn,
            publication_year=publication_year,
            publisher=publisher
        )

    @staticmethod
    def get_book_by_id(book_id: int) -> 'Book':
        """Get book by ID"""
        from app.repositories.book_repository import BookRepository
        return BookRepository.get_by_id(book_id)

    @staticmethod
    def get_all_books() -> list['Book']:
        """Get all books"""
        from app.repositories.book_repository import BookRepository
        return BookRepository.get_all_books()

    @staticmethod
    def update_book(
        book_id: int,
        title: str,
        author_id: int,
        genre: str,
        description: str,
        pages: int,
        rating: float,
        price: float,
        availabilaty_status: str,
        quantity: int,
        cover_image_url: str
    ) -> 'Book':
        """Update an existing book"""
        from app.repositories.book_repository import BookRepository
        book = BookRepository.get_by_id(book_id)
        if not book:
            raise ValueError("Book not found")

        book.title = title
        book.author_id = author_id
        book.genre = genre
        book.description = description
        book.pages = pages
        book.rating = rating
        book.price = price
        book.availabilaty_status = availabilaty_status
        book.quantity = quantity
        book.cover_image_url = cover_image_url

        return BookRepository.update_book(book)

    @staticmethod
    def delete_book(book_id: int) -> None:
        """Delete a book"""
        from app.repositories.book_repository import BookRepository
        book = BookRepository.get_by_id(book_id)
        if not book:
            raise ValueError("Book not found")

        BookRepository.delete_book(book)
