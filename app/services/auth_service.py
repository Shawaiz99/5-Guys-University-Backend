from app.repositories.user_repository import UserRepository
from app.models.user import User
from werkzeug.security import generate_password_hash


class AuthService:
    @staticmethod
    def register(email: str, username: str, password: str, user_role: str = "Student") -> User:
        if UserRepository.get_by_email(email):
            raise ValueError(
                f"Email '{email}' already exists. Please try another one.")

        if UserRepository.get_by_username(username):
            raise ValueError(
                f"Username '{username}' already exists. Please try another one.")

        user = UserRepository.create_user(
            email, username, password, user_role=user_role
        )
        return user
