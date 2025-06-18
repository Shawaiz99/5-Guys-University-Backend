from app.extensions import db
from app.models.book_image import BookImage


class BookImageRepository:
    def get_images_by_book_id(self, book_id):
        return BookImage.query.filter_by(book_id=book_id).all()

    def unset_primary_image(self, book_id):
        db.session.query(BookImage)\
            .filter_by(book_id=book_id, is_primary=True)\
            .update({"is_primary": False})
        db.session.flush()