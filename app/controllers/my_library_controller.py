from flask import Blueprint, request, jsonify
from app.services.my_library_service import MyLibraryService
from flask_jwt_extended import jwt_required, get_jwt_identity


my_library_bp = Blueprint("my_library", __name__, url_prefix="/my-library")


@my_library_bp.route("/my-library/add-book", methods=["POST"])
@jwt_required()
def add_book_to_library():
    """Add a book to the user's library"""
    user_id = get_jwt_identity()
    data = request.get_json()

    if not data or "book_id" not in data:
        return jsonify({"error": "Book ID is required"}), 400

    book_id = data["book_id"]

    try:
        book = MyLibraryService.add_book_to_library(user_id, book_id)
        return jsonify({"message": "Book added to your library", "book": book.serialize()}), 201
    except ValueError as e:
        return jsonify({"error": str(e)}), 400


@my_library_bp.route("/my-library/books", methods=["GET"])
@jwt_required()
def get_my_library_books():
    """Get all books in the user's library"""
    user_id = get_jwt_identity()
    books = MyLibraryService.get_books_by_user_id(user_id)

    if not books:
        return jsonify({"message": "No books found in your library"}), 404

    return jsonify([book.serialize() for book in books]), 200


@my_library_bp.route("/my-library/search", methods=["GET"])
@jwt_required()
def search_books_by_filter():
    """Search books in the user's library by title, author, genre, or ISBN"""
    try:
        user_id = get_jwt_identity()
        title = request.args.get("title")
        author = request.args.get("author")
        genre = request.args.get("genre")
        isbn = request.args.get("isbn")

        if not (title or author or genre or isbn):
            return jsonify({"message": "No filters provided"}), 400

        books = MyLibraryService.get_filtered_books(
            user_id, title, author, genre, isbn)

        if not books:
            return jsonify({"message": "No books found matching your criteria"}), 404

        return jsonify([book.serialize() for book in books]), 200

    except Exception as e:
        return jsonify({"error": "An unexpected error occurred", "details": str(e)}), 500
