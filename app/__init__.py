from flask import Flask
from app.config import get_config
from app.extensions import db, migrate, cors, jwt
from app.admin import init_admin
from app.controllers.auth_controller import auth_bp
from app.controllers.author_controller import author_bp
from app.controllers.book_controller import book_bp
from app.controllers.user_controller import user_bp
from app.controllers.my_library_controller import my_library_bp
from app.controllers.wishlist_item_controller import wishlist_items_bp
from app.controllers.shopping_cart_controller import shopping_cart_bp
from app.error_handlers import register_error_handlers


def create_app(env: str | None = None) -> Flask:
    app = Flask(__name__)
    app.config.from_object(get_config(env))

    db.init_app(app)
    migrate.init_app(app, db)
    cors.init_app(app)
    init_admin(app)
    jwt.init_app(app)

    # Register error handlers
    register_error_handlers(app)

    # register blueprints
    app.register_blueprint(auth_bp, url_prefix="/api/v1/auth")
    app.register_blueprint(author_bp, url_prefix="/api/v1")
    app.register_blueprint(book_bp, url_prefix="/api/v1")
    app.register_blueprint(user_bp, url_prefix="/api/v1")
    app.register_blueprint(my_library_bp, url_prefix="/api/v1")
    app.register_blueprint(wishlist_items_bp, url_prefix="/api/v1")
    app.register_blueprint(shopping_cart_bp, url_prefix="/api/v1")r

    # health check

    @app.get("/ping")
    def ping():
        return {"status": "ok"}

    return app
