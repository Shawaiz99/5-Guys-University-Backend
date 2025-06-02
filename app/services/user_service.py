# user_services.py
from typing import Optional
from app.models.user import User
from app.repositories.user_repository import UserRepository


class UserService:
    @staticmethod
    def get_user_by_id(user_id: int) -> Optional[User]:
        return UserRepository.get_by_id(user_id)

    @staticmethod
    def update_user(user: User, **kwargs) -> User:
        for key, value in kwargs.items():
            if hasattr(user, key):
                setattr(user, key, value)
        return UserRepository.update(user)

    @staticmethod
    def get_user_by_email(user_email: str) -> Optional[User]:
        print(f"Fetching user by email: {user_email}")
        return UserRepository.get_by_email(user_email)

    @staticmethod
    def get_all_users(limit: int = 100, offset: int = 0) -> list[User]:
        """Get all users with pagination."""
        return UserRepository.get_all(limit, offset)
