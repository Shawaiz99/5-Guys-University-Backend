from datetime import datetime, timezone
from sqlalchemy import String, DateTime, Integer, Boolean, Enum
from sqlalchemy.orm import mapped_column, relationship
from app.extensions import db
from werkzeug.security import generate_password_hash, check_password_hash
from datetime import datetime


class User(db.Model):
    __tablename__ = "users"

    id = mapped_column(Integer, primary_key=True)
    username = mapped_column(String(255), unique=True,
                             nullable=False, index=True)
    email = mapped_column(String(255), unique=True, nullable=False, index=True)
    password = mapped_column(String(255), nullable=False)
    is_active = mapped_column(Boolean, default=True)
    is_admin = mapped_column(Boolean, default=False)
    created_at = mapped_column(
        DateTime, default=lambda: datetime.now(timezone.utc), nullable=False)
    updated_at = mapped_column(DateTime, default=lambda: datetime.now(
        timezone.utc), onupdate=lambda: datetime.now(timezone.utc), nullable=False)
    user_role = mapped_column(
        Enum("Student", "Professor", "Librarian", name="role"),
        default="Student",
        nullable=False
    )

# relationships:
    # profile = relationship(
    #     "Profile",
    #     back_populates="user",
    #     uselist=False,
    #     cascade="all, delete-orphan")
    library = relationship(
        "MyLibrary", back_populates="user", cascade="all, delete-orphan")

    def set_password(self, password):
        self.password = generate_password_hash(password)

    def check_password(self, password):
        return check_password_hash(self.password, password)

    def serialize(self):
        return {
            "id": self.id,
            "username": self.username,
            "email": self.email,
            "user_role": self.user_role,
            "is_active": self.is_active,
            "is_admin": self.is_admin,
            "created_at": self.created_at.isoformat(),
            "updated_at": self.updated_at.isoformat()
        }


iso_str = "2025-05-23T23:55:30.264983"
dt = datetime.fromisoformat(iso_str)
print(dt)  # Output: 2025-05-23 23:55:30.264983
