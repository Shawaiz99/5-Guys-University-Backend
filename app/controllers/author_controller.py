from flask import Blueprint, request, jsonify
from app.services.author_service import AuthorService


author_bp = Blueprint("authors", __name__)


@author_bp.route("/authors", methods=["GET"])
def get_all_authors():
    authors = AuthorService.get_all_authors()
    print(f"Retrieved {authors} authors")
    return jsonify([author.serialize() for author in authors]), 200


@author_bp.route("/authors/books/<int:author_id>", methods=["GET"])
def get_books_by_author(author_id):
    books = AuthorService.get_books_by_author_id(author_id)
    if not books:
        return jsonify({"error": "No books found for this author"}), 404
    return jsonify([book.serialize() for book in books]), 200


@author_bp.route("/authors/<int:author_id>", methods=["GET"])
def get_author_by_id(author_id):
    author = AuthorService.get_author_by_id(author_id)
    if not author:
        return jsonify({"error": "Author not found"}), 404
    return jsonify(author.serialize()), 200


@author_bp.route("/authors", methods=["POST"])
def create_author():
    data = request.get_json()
    if not data or not all(key in data for key in ("name", "biography", "photo_url")):
        return jsonify({"error": "Missing required fields"}), 400

    author = AuthorService.create_author(
        name=data["name"],
        biography=data["biography"],
        photo_url=data["photo_url"]
    )
    return jsonify({"message": "Author created successfully", "author": author.serialize()}), 201


@author_bp.route("/authors/<int:author_id>", methods=["PUT"])
def update_author(author_id):
    data = request.get_json()
    author = AuthorService.get_author_by_id(author_id)

    if not author:
        return jsonify({"error": "Author not found"}), 404

    if not data or not all(key in data for key in ("name", "biography", "photo_url")):
        return jsonify({"error": "Missing required fields"}), 400

    # Update the author object fields
    author.name = data["name"]
    author.biography = data["biography"]
    author.photo_url = data["photo_url"]

    updated_author = AuthorService.update_author(author)
    return jsonify(updated_author.serialize()), 200


@author_bp.route("/authors/<int:author_id>", methods=["DELETE"])
def delete_author(author_id):
    author = AuthorService.get_author_by_id(author_id)

    if not author:
        return jsonify({"error": "Author not found"}), 404

    AuthorService.delete_author(author)
    return jsonify({"message": f"Author with id: {author_id} successfully deleted"}), 200


@author_bp.route("/authors/bulk", methods=["POST"])
def create_authors_bulk():
    data = request.get_json()
    if not data or not isinstance(data, list):
        return jsonify({"error": "A list of authors is required."}), 400

    created = []
    for author_data in data:
        if not all(key in author_data for key in ("name", "biography", "photo_url")):
            continue
        author = AuthorService.create_author(
            name=author_data["name"],
            biography=author_data["biography"],
            photo_url=author_data["photo_url"]
        )
        created.append(author.serialize())
    return jsonify({"message": f"{len(created)} authors created.", "authors": created}), 201
