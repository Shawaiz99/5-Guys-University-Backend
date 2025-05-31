from app.extensions import db
from app.models.author import Author
from sqlalchemy import select
from typing import Optional, List


class AuthorRepository:
    @staticmethod
    def create_author(
        name: str,
        biography: str,
        photo_url: str
    ) -> Author:
        """Create new author"""
        author = Author(
            name=name,
            biography=biography,
            photo_url=photo_url
        )

        db.session.add(author)
        db.session.commit()
        return author

    @staticmethod
    def get_author_by_id(author_id: int) -> Optional[Author]:
        """Get author by ID"""
        stmt = select(Author).where(Author.id == author_id)
        result = db.session.execute(stmt)
        return result.scalars().first()

    @staticmethod
    def get_books_by_author_id(author_id: int) -> List[Author]:
        """Get books by author ID"""
        stmt = select(Author).where(Author.id == author_id)
        result = db.session.execute(stmt)
        return result.scalars().all()

    @staticmethod
    def update_author(author: Author) -> Author:
        """Update the author"""
        db.session.commit()
        return author

    @staticmethod
    def delete_author(author: Author) -> None:
        """Delete the author"""
        db.session.delete(author)
        db.session.commit()

    @staticmethod
    def get_all(limit: int = 100, offset: int = 0) -> List[Author]:
        """Get all authors with pagination"""
        stmt = select(Author).limit(limit).offset(offset)
        result = db.session.execute(stmt)
        return result.scalars().all()
