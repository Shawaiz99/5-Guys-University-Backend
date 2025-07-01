from typing import Any, Dict, Optional

from app.models.profile import Profile
from app.models.user import User
from app.repositories.profile_repository import ProfileRepository
from app.repositories.user_repository import UserRepository


class ProfileService:

    @staticmethod
    def get_profile_by_user_id(user_id: int) -> Optional[Profile]:
        """
        Retrieve a profile by user ID.
        """
        return ProfileRepository.get_by_user_id(user_id)

    @staticmethod
    def update_user_profile(
            user_id: int, data: Dict[str, Any]) -> Optional[Profile]:
        profile = ProfileRepository.get_by_user_id(user_id)
        if not profile:
            raise ValueError(f"Profile with user_id {user_id} not found.")
        for key, value in data.items():
            if hasattr(profile, key):
                setattr(profile, key, value)
        return ProfileRepository.update(profile)

    @staticmethod
    def delete_profile_by_user_id(user_id: int) -> bool:
        """
        Delete a profile by user ID.
        """
        profile = ProfileRepository.get_by_user_id(user_id)
        if not profile:
            raise ValueError(f"Profile with user_id {user_id} not found.")
        return ProfileRepository.delete(profile)

    @staticmethod
    def create_profile_for_user(user: User, data: Dict[str, Any]) -> Profile:
        """
        Create a new profile for a user.
        """
        if not user:
            raise ValueError("User must be provided to create a profile.")
        data = dict(data)
        data.pop("user_id", None)
        profile = Profile(user_id=user.id, **data)
        return ProfileRepository.create(profile)
