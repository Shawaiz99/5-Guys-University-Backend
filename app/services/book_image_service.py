from app.repositories.book_repository import BookRepository
from app.repositories.book_image_repository import BookImageRepository
from app.utils.cloudinary_utils import upload_image_to_cloudinary
from app.models.book_image import BookImage
from app.extensions import db
from werkzeug.exceptions import NotFound


class BookImageService:
    def __init__(self):
        self.book_repo = BookRepository()
        self.image_repo = BookImageRepository()

    def upload_book_image(self, book_id, file, is_primary=False, caption=None):
        book = self.book_repo.get_by_id(book_id)
        if not book:
            raise NotFound("Book not found")

        upload_result = upload_image_to_cloudinary(file)

        if is_primary:
            self.image_repo.unset_primary_image(book_id)

        image = BookImage(
            book_id=book_id,
            image_url=upload_result['secure_url'],
            cloudinary_public_id=upload_result['public_id'],
            is_primary=is_primary,
            caption=caption
        )
        db.session.add(image)
        db.session.commit()
        return image
