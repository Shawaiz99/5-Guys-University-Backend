from app.models.book import Book
from app.extensions import db
from sqlalchemy import select, func, DECIMAL
from typing import Optional, List
from sqlalchemy.orm import Session


class BookRepository:
    @staticmethod
    def create_book(
        title: str,
        description: str,
        isbn: str,
        genre: str,
        publication_year: int,
        publisher: str,
        pages: int,
        rating: float,
        price: float,
        availabilaty_status: str,
        quantity: int,
        author_id: int,
        cover_image_url: str
    ) -> Book:
        """Create a new book"""
        book = Book(
            title=title,
            description=description,
            isbn=isbn,
            genre=genre,
            publication_year=publication_year,
            publisher=publisher,
            pages=pages,
            rating=rating,
            price=price,
            availabilaty_status=availabilaty_status,
            quantity=quantity,
            author_id=author_id,
            cover_image_url=cover_image_url
        )
        db.session.add(book)
        db.session.commit()
        return book

    @staticmethod
    def get_by_id(book_id: int) -> Optional[Book]:
        """Get book by ID"""
        stmt = select(Book).where(Book.id == book_id)
        result = db.session.execute(stmt)
        return result.scalars().first()

    @staticmethod
    def get_by_title(title: str) -> Optional[Book]:
        """Get book by title (case-insensitive)"""
        stmt = select(Book).where(func.lower(Book.title) == title.lower())
        result = db.session.execute(stmt)
        return result.scalars().first()

    @staticmethod
    def get_all_books() -> List[Book]:
        """Get all books"""
        stmt = select(Book)
        result = db.session.execute(stmt)
        return result.scalars().all()

    @staticmethod
    def update_book(book: Book) -> Book:
        """Update an existing book"""
        db.session.commit()
        return book

    @staticmethod
    def delete_book(book: Book) -> None:
        """Delete a book"""
        db.session.delete(book)
        db.session.commit()

    @staticmethod
    def get_books_by_author(author_id: int) -> List[Book]:
        """Get all books by a specific author"""
        stmt = select(Book).where(Book.author_id == author_id)
        result = db.session.execute(stmt)
        return result.scalars().all()

    @staticmethod
    def get_books_by_genre(genre: str) -> List[Book]:
        """Get all books by genre"""
        stmt = select(Book).where(func.lower(Book.genre) == genre.lower())
        result = db.session.execute(stmt)
        return result.scalars().all()

    @staticmethod
    def get_books_by_availability(availabilaty_status: str) -> List[Book]:
        """Get all books by availability status"""
        stmt = select(Book).where(func.lower(
            Book.availabilaty_status) == availabilaty_status.lower())
        result = db.session.execute(stmt)
        return result.scalars().all()

    @staticmethod
    def get_by_isbn(isbn: str) -> Optional[Book]:
        """Get book by ISBN (case-insensitive)"""
        stmt = select(Book).where(func.lower(Book.isbn) == isbn.lower())
        result = db.session.execute(stmt)
        return result.scalars().first()
