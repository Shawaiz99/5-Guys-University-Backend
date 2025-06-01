from sqlalchemy.orm import mapped_column, Mapped
from app.extensions import db
from datetime import datetime
from app.models.user import User
from sqlalchemy import DateTime

class Profile(db.Model):
    __tablename__ = "profiles"

    id: Mapped[int] = mapped_column(primary_key=True)
    user_id: Mapped[int] = mapped_column(db.ForeignKey("users.id"), nullable=False, unique=True)
    first_name: Mapped[str] = mapped_column(db.String(255))
    last_name: Mapped[str] = mapped_column(db.String(255))
    bio: Mapped[str] = mapped_column(db.Text)
    avatar_url: Mapped[str] = mapped_column(db.String)
    created_at = mapped_column(DateTime, default=datetime.utcnow, nullable=False)
    updated_at = mapped_column(DateTime, default=datetime.utcnow, onupdate=datetime.utcnow, nullable=False)


    user = db.relationship("User", back_populates="profile")