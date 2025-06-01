"""
Execute with:  python seed_db.py
"""
from faker import Faker
from app import create_app
from app.extensions import db
from app.models.user import User
from app.models.profile import Profile

fake = Faker()


def run():
    app = create_app()
    with app.app_context():
        for _ in range(10):
            email = fake.unique.email()
            username = fake.unique.user_name()
            password = fake.password()

            if not db.session.scalar(db.select(User).filter_by(email=email)):
                user = User(
                    email=email,
                    username=username,
                    password=password
                )
                profile = Profile(
                    first_name=fake.first_name(),
                    last_name=fake.last_name(),
                    bio=fake.sentence(),
                    avatar_url=fake.image_url()
                )
                user.profile = profile
                db.session.add(user)
        db.session.commit()
        print("🌱  Seeded 10 fake users")


if __name__ == "__main__":
    run()
