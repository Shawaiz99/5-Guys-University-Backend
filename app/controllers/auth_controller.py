from flask import Blueprint, request, jsonify
from app.utils.validators import is_valid_email, is_valid_password, is_valid_username, equals_case_insensitive
from app.services.auth_service import AuthService
from app.services.user_service import UserService
from flask_jwt_extended import create_access_token


auth_bp = Blueprint("auth", __name__)


@auth_bp.route("/register", methods=["POST"])
def register():
    """Register new user
    Request body:
    {
        "email": "",
        "username": "new_username",
        "password": "qwerty" 
    }
    Returns 
        201: User successfully created
        400: Validation error
    """
    data = request.get_json()

    # Manual validation
    if not data or "email" not in data or not data.get("email"):
        return jsonify({"error": "email property cannot be empty or missing"}), 400

    if not is_valid_email(data.get("email")):
        return jsonify({"error": f"Invalid email format {data.get('email')}"}), 400

    if "username" not in data or not data.get("username"):
        return jsonify({"error": "username property cannot be empty or missing"}), 400

    if not is_valid_username(data.get("username")):
        return jsonify({"error": f"Invalid username format cannot contain spaces '{data.get('username')}'"}), 400

    if "password" not in data or not data.get("password"):
        return jsonify({"error": "password property cannot be empty or missing"}), 400

    if not is_valid_password(data.get("password")):
        return jsonify({"error": f"Invalid password format {data.get('password')}"}), 400
    if equals_case_insensitive(data.get("username"), data.get("email")):
        return jsonify({"error": "Username and email cannot be the same"}), 400

    try:
        user = AuthService.register(
            email=data["email"],
            username=data["username"],
            password=data["password"]
        )
        return jsonify(
            {
                "message": "User successfully created!",
                "user": user.serialize(),
            }
        ), 201
    except ValueError as e:
        return jsonify({"error": "Registration failed", "message": str(e)}), 400
    except Exception as e:
        # Log the exception if needed
        return jsonify({"error": "Internal server error", "message": str(e)}), 500


@auth_bp.route('/login', methods=['POST'])
def login():
    """
        {
            "email": "",
            "password": ""
        }
    """

    data = request.get_json()

    if not data or "email" not in data or "password" not in data:
        return jsonify({"error": "Missing email or password fields"})

    user = UserService.get_user_by_email(data.get("email"))

    if not user:
        return jsonify({"error": f"No user with email {data.get('email')} found"})

    if not data.get("password"):
        return jsonify({"error": "Password is required"})

    if not user.check_password(data.get("password")):
        return jsonify({"error": "The password provided does not match the original one."})

    access_token = create_access_token(
        identity=str(user.id), additional_claims={"email": data.get("email")}
    )

    return jsonify({"user": user.serialize(), "token": access_token})
