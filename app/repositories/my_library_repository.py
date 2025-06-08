
from app.models.my_library import MyLibrary
from app.models.book import Book
from typing import Optional, List
from sqlalchemy import select
from app.extensions import db
from app.models.book import Book
from sqlalchemy.orm import joinedload


class MyLibraryRepository:

    @staticmethod
    def add_book_to_library(user_id: int, book_id: int) -> MyLibrary:
        """Add a book to the user's library"""
        new_book = MyLibrary(user_id=user_id, book_id=book_id)
        db.session.add(new_book)
        db.session.commit()
        return new_book

    @staticmethod
    def get_library_by_user_id(user_id: int) -> List[MyLibrary]:
        """Get library by user ID"""
        stmt = select(MyLibrary).options(joinedload(MyLibrary.book).joinedload(
            Book.author)).where(MyLibrary.user_id == user_id)
        result = db.session.execute(stmt)
        return result.scalars().all()

    @staticmethod
    def get_filtered_books(user_id: int, title: str = None, author: str = None, isbn: str = None, genre: str = None) -> List[Book]:
        """Get filtered books in the user's library"""
        stmt = select(Book).join(MyLibrary).where(MyLibrary.user_id == user_id)
        result = db.session.execute(stmt)
        books = result.scalars().all()
        if not books:
            return []
        if title:
            books = [book for book in books if book.title.lower() ==
                     title.lower()]
        if author:
            books = [book for book in books if book.author.name.lower()
                     == author.lower()]
        if isbn:
            books = [book for book in books if book.isbn == isbn]
        if genre:
            books = [b for b in books if genre.lower() in (
                b.genre or "").lower()]
        return books
