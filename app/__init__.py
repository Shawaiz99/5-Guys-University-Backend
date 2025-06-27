from flask import Flask
from flask_cors import CORS
from app.config import get_config
from app.extensions import db, migrate, cors, jwt
from app.controllers.auth_controller import auth_bp
from app.controllers.book_controller import book_bp
from app.controllers.user_controller import user_bp
from app.controllers.author_controller import author_bp
from app.controllers.wishlist_item_controller import wishlist_items_bp
from app.controllers.profile_controller import profile_bp
from app.controllers.my_library_controller import my_library_bp
from app.controllers.shopping_cart_controller import shopping_cart_bp
from app.controllers.order_controller import order_bp
from app.error_handlers import register_error_handlers
from app.admin import init_admin
from app.controllers.book_image_controller import book_image_bp


def create_app(env: str | None = None) -> Flask:
    app = Flask(__name__)
    app.config.from_object(get_config(env))

    # Sadece belirli bir origin'e izin ver
    CORS(app, origins=["http://localhost:5173"])  # veya frontend adresin neyse

    init_admin(app)
    db.init_app(app)
    migrate.init_app(app, db)
    cors.init_app(app)
    jwt.init_app(app)

    register_error_handlers(app)

    # register blueprints
    app.register_blueprint(auth_bp, url_prefix="/api/v1/auth")
    app.register_blueprint(profile_bp)
    app.register_blueprint(book_bp, url_prefix="/api/v1")
    app.register_blueprint(user_bp, url_prefix="/api/v1")
    app.register_blueprint(author_bp, url_prefix="/api/v1")
    app.register_blueprint(wishlist_items_bp, url_prefix="/api/v1")
    app.register_blueprint(my_library_bp, url_prefix="/api/v1")
    app.register_blueprint(shopping_cart_bp, url_prefix="/api/v1")
    app.register_blueprint(book_image_bp, url_prefix="/api/v1")
    app.register_blueprint(order_bp, url_prefix="/api/v1")

    # health check
    @app.get("/ping")
    def ping():
        return {"status": "ok"}

    return app
