"""
Execute with:  python seed_db.py
"""
from faker import Faker
from app import create_app
from app.extensions import db
from app.models.user import User

fake = Faker()


def run():
    app = create_app()
    with app.app_context():
        for _ in range(10):
            email = fake.unique.email()
            username = fake.unique.user_name()
            password = fake.password()
            if not db.session.scalar(db.select(User).filter_by(email=email)):
                db.session.add(User(
                    email=email,
                    username=username,
                    password=password
                ))  # type: ignore
        db.session.commit()
        print("🌱  Seeded 10 fake users")


if __name__ == "__main__":
    run()
