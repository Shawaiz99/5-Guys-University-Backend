from sqlalchemy import Boolean, ForeignKey, Integer, String, Text
from sqlalchemy.orm import mapped_column, relationship
from app.extensions import db
from datetime import datetime
from app.models.user import User
from sqlalchemy import DateTime


class Profile(db.Model):
    __tablename__ = "profiles"
    id = mapped_column(Integer, primary_key=True)
    user_id = mapped_column(Integer, ForeignKey(
        "users.id"), unique=True, nullable=False)
    first_name = mapped_column(String(255), nullable=True)
    last_name = mapped_column(String(255), nullable=True)
    bio = mapped_column(Text, nullable=True)
    avatar_url = mapped_column(String(255), nullable=True)
    cloudinary_public_id = mapped_column(String(255), nullable=True)
    is_deleted = mapped_column(Boolean, default=False, nullable=False)

    # relationships:
    user = relationship("User", back_populates="profile")

    def serialize(self):
        return {
            "id": self.id,
            "user_id": self.user_id,
            "first_name": self.first_name,
            "last_name": self.last_name,
            "bio": self.bio,
            "avatar_url": self.avatar_url,
            "is_deleted": self.is_deleted,
        }
