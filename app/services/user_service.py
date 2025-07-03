from typing import Optional, Dict, Any, List
from datetime import datetime

from app.extensions import db
from app.models.user import User
from app.models.profile import Profile
from app.repositories.user_repository import UserRepository
from app.repositories.profile_repository import ProfileRepository




class UserService:
    @staticmethod
    def get_user_by_id(user_id: int) -> Optional[User]:
        return UserRepository.get_by_id(user_id)

    @staticmethod
    def update_user(user: User, data: dict) -> User:
        allowed_fields = ["username", "email", "is_active", "user_role"]

        for key in allowed_fields:
            if key in data:
                print(f"Updating {key} from {getattr(user, key)} to {data[key]}")
                setattr(user, key, data[key])

        db.session.commit()
        print("User updated and committed")
        return user



    @staticmethod
    def get_user_by_email(user_email: str) -> Optional[User]:
        print(f"Fetching user by email: {user_email}")
        return UserRepository.get_by_email(user_email)

    @staticmethod
    def get_all_users(limit: int = 100, offset: int = 0) -> list[User]:
        """Get all users with pagination."""
        return UserRepository.get_all(limit, offset)

    @staticmethod
    def get_profile_by_user_id(user_id: int) -> Optional[Profile]:
        return ProfileRepository.get_by_user_id(user_id)

    @staticmethod
    def delete_user(user):
        db.session.delete(user)
        db.session.commit()

    @staticmethod
    def change_password(user, data):
        current_password = data.get("current_password")
        new_password = data.get("new_password")

        if not current_password or not new_password:
            raise Exception("Current password and new password are required")

        print(f"User: {user.id}, Current password received: {current_password}")
        if not user.check_password(current_password):
            print("Password check failed!")
            raise Exception("Wrong password")

        user.set_password(new_password)
        user.updated_at = datetime.utcnow()
        db.session.commit()

        return user
