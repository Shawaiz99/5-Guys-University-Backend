from flask import Blueprint, request, jsonify
from app.services.book_service import BookService
from app.repositories.book_repository import BookRepository
from sqlalchemy.exc import IntegrityError
from flask_jwt_extended import jwt_required, get_jwt_identity

book_bp = Blueprint("books", __name__)


@book_bp.route("/books", methods=["POST"])
# @jwt_required()
def create_book():
    """Create a new book
    Request body:
    {
        "title": "Book Title",
        "author": "Author Name",
        "isbn": "123-4567890123"
        "availabilaty_status": "Available"
    }
    Returns 
        201: Book successfully created
        400: Validation error
    """
    data = request.get_json()

    # Manual validation
    if not data or "title" not in data or not data.get("title"):
        return jsonify({"error": "title property cannot be empty or missing"}), 400

    # Check if title already exists
    if BookRepository.get_by_title(data["title"]):
        return jsonify({"error": "A book with this title already exists."}), 400

    if BookRepository.get_by_isbn(data.get("isbn")):
        return jsonify({"error": "A book with this ISBN already exists."}), 400

    if not data.get("author_id"):
        return jsonify({"error": "author_id property cannot be empty or missing"}), 400

    if not data.get("availabilaty_status"):
        return jsonify({"error": "availabilaty_status property cannot be empty or missing"}), 400

    if not data.get("isbn"):
        return jsonify({"error": "isbn property cannot be empty or missing"}), 400
    if len(data.get("isbn", "")) > 14:
        return jsonify({"error": "isbn cannot be longer than 14 characters"}), 400

    try:
        book = BookService.create_book(
            title=data["title"],
            author_id=data["author_id"],
            genre=data.get("genre"),
            description=data.get("description"),
            pages=data.get("pages"),
            rating=data.get("rating"),
            price=data.get("price"),
            availabilaty_status=data.get("availabilaty_status", "Available"),
            quantity=data.get("quantity", 0),
            cover_image_url=data.get("cover_image_url"),
            isbn=data["isbn"],
            publication_year=data.get("publication_year"),
            publisher=data.get("publisher")
        )
        return jsonify(
            {
                "message": "Book successfully created!",
                "book": book.serialize(),
            }
        ), 201
    except ValueError as e:
        return jsonify({"error": "Book creation failed", "message": str(e)}), 400
    except Exception as e:
        # Log the exception if needed
        return jsonify({"error": "Internal server error", "message": str(e)}), 500


@book_bp.route("/books", methods=["GET"])
# @jwt_required()
def get_books():
    """Get all books
    Returns 
        200: List of books
    """
    try:
        books = BookService.get_all_books()
        return jsonify(
            {
                "books": [book.serialize() for book in books]
            }
        ), 200
    except Exception as e:
        # Log the exception if needed
        return jsonify({"error": "Internal server error", "message": str(e)}), 500


@book_bp.route("/books/<int:book_id>", methods=["GET"])
# @jwt_required()
def get_book(book_id):
    """Get book by ID
    Returns 
        200: Book details
        404: Book not found
    """
    try:
        book = BookService.get_book_by_id(book_id)
        if not book:
            return jsonify({"error": "Book not found"}), 404
        return jsonify(
            {
                "book": book.serialize()
            }
        ), 200
    except Exception as e:
        # Log the exception if needed
        return jsonify({"error": "Internal server error", "message": str(e)}), 500


@book_bp.route("/books/<int:book_id>", methods=["PUT"])
# @jwt_required()
def update_book(book_id):
    """Update book details
    Request body:
    {
        "title": "Updated Book Title",
        "author": "Updated Author Name",
        "isbn": "123-4567890123"
    }
    Returns 
        200: Book successfully updated
        400: Validation error
        404: Book not found
    """
    data = request.get_json()

    if not data or "title" not in data or not data.get("title"):
        return jsonify({"error": "title property cannot be empty or missing"}), 400

    if not data.get("author_id"):
        return jsonify({"error": "author_id property cannot be empty or missing"}), 400

    if not data.get("isbn"):
        return jsonify({"error": "isbn property cannot be empty or missing"}), 400
    if len(data.get("isbn", "")) > 13:
        return jsonify({"error": "isbn cannot be longer than 13 characters"}), 400

    try:
        book = BookService.update_book(
            book_id=book_id,
            title=data["title"],
            author_id=data["author_id"],
            genre=data.get("genre"),
            description=data.get("description"),
            pages=data.get("pages"),
            rating=data.get("rating"),
            price=data.get("price"),
            availabilaty_status=data.get("availabilaty_status", "Available"),
            quantity=data.get("quantity", 0),
            cover_image_url=data.get("cover_image_url")
        )
        if not book:
            return jsonify({"error": "Book not found"}), 404
        return jsonify(
            {
                "message": "Book successfully updated!",
                "book": book.serialize(),
            }
        ), 200
    except ValueError as e:
        return jsonify({"error": "Book update failed", "message": str(e)}), 400
    except Exception as e:
        # Log the exception if needed
        return jsonify({"error": "Internal server error", "message": str(e)}), 500


@book_bp.route("/books/<int:book_id>", methods=["DELETE"])
# @jwt_required()
def delete_book(book_id):
    """Delete a book
    Returns 
        204: Book successfully deleted
        404: Book not found
    """
    try:
        book = BookService.get_book_by_id(book_id)
        if not book:
            return jsonify({"error": "Book not found"}), 404

        # Optional: Check if book is referenced in order_items before attempting delete
        from app.models.order import OrderItem
        from app.extensions import db
        referenced = db.session.query(
            OrderItem).filter_by(book_id=book_id).first()
        if referenced:
            return jsonify({"error": "Cannot delete book because it is referenced in an order."}), 400

        BookService.delete_book(book_id)
        return jsonify({"message": f"Book with '{book.title}' name successfully deleted"}), 200
    except IntegrityError as e:
        return jsonify({"error": "Cannot delete book because it is referenced in an order."}), 400
    except ValueError:
        return jsonify({"error": "Book not found"}), 404
    except Exception as e:
        return jsonify({"error": "Internal server error", "message": str(e)}), 500


@book_bp.route("/books/bulk", methods=["POST"])
def bulk_create_books():
    """Bulk create books
    Request body:
    [
        {
            "title": "Book Title 1",
            "author_id": 1,
            "isbn": "123-4567890123",
            "availabilaty_status": "Available"
        },
        {
            "title": "Book Title 2",
            "author_id": 2,
            "isbn": "123-4567890124",
            "availabilaty_status": "Available"
        }
    ]
    Returns 
        201: Books successfully created
        400: Validation error
    """
    data = request.get_json()

    if not isinstance(data, list) or not data:
        return jsonify({"error": "Request body must be a non-empty list"}), 400

    created_books = []
    for book_data in data:
        if not book_data.get("title") or not book_data.get("author_id") or not book_data.get("isbn"):
            return jsonify({"error": "Each book must have title, author_id, and isbn"}), 400

        if BookRepository.get_by_title(book_data["title"]):
            return jsonify({"error": f"A book with title '{book_data['title']}' already exists."}), 400

        if BookRepository.get_by_isbn(book_data["isbn"]):
            return jsonify({"error": f"A book with ISBN '{book_data['isbn']}' already exists."}), 400

        try:
            book = BookService.create_book(
                title=book_data["title"],
                author_id=book_data["author_id"],
                genre=book_data.get("genre"),
                description=book_data.get("description"),
                pages=book_data.get("pages"),
                rating=book_data.get("rating"),
                price=book_data.get("price"),
                availabilaty_status=book_data.get(
                    "availabilaty_status", "Available"),
                quantity=book_data.get("quantity", 0),
                cover_image_url=book_data.get("cover_image_url"),
                isbn=book_data["isbn"],
                publication_year=book_data.get("publication_year"),
                publisher=book_data.get("publisher")
            )
            created_books.append(book.serialize())
        except ValueError as e:
            return jsonify({"error": str(e)}), 400

    return jsonify(
        {
            "message": f"{len(created_books)} books successfully created!",
            "books": created_books,
        }
    ), 201
