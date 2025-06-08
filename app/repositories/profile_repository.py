from app.models import Profile
from app.extensions import db
class ProfileRepository:

    @staticmethod
    def update_profile(profile: Profile, bio: str, avatar_url: str) -> Profile:
        profile.bio = bio
        profile.avatar_url = avatar_url
        db.session.commit()
        return profile