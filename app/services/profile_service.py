from app.repositories.profile_repository import ProfileRepository
from app.models import Profile
from typing import Optional
from app.models.user import User
from app.repositories.user_repository import UserRepository


class ProfileService:

    @staticmethod
    def update_profile(profile: Profile, bio: str, avatar_url: str) -> Profile:
        return ProfileRepository.update_profile(profile, bio, avatar_url)
    
    @staticmethod
    def get_user_by_id(user_id: int) -> Optional[User]:
        return UserRepository.get_by_id(user_id)