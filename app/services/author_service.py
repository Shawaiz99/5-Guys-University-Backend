from typing import Optional
from app.models.author import Author
from app.repositories.author_repository import AuthorRepository


class AuthorService:
    @staticmethod
    def create_author(name: str, biography: str, photo_url: str) -> Author:
        """Create a new author."""
        return AuthorRepository.create_author(name, biography, photo_url)

    @staticmethod
    def update_author(author: Author) -> Author:
        """Update an existing author."""
        return AuthorRepository.update_author(author)

    @staticmethod
    def delete_author(author: Author) -> None:
        """Delete an author."""
        AuthorRepository.delete_author(author)

    @staticmethod
    def get_books_by_author_id(author_id: int) -> list[Author]:
        """Get books by author ID."""
        return AuthorRepository.get_books_by_author_id(author_id)

    @staticmethod
    def get_author_by_id(author_id: int) -> Optional[Author]:
        """Get an author by ID."""
        return AuthorRepository.get_author_by_id(author_id)

    @staticmethod
    def get_all_authors(limit: int = 100, offset: int = 0) -> list[Author]:
        """Get all authors with pagination."""
        return AuthorRepository.get_all(limit, offset)
