from flask_admin import Admin
from flask_admin.contrib.sqla import ModelView
from app.extensions import db
from app.models.author import Author
from app.models.my_library import MyLibrary
from app.models import User, Author, Book, WishlistItem, ShoppingCart

admin_panel = Admin(name='Admin Panel', template_mode='bootstrap4')


class UserView(ModelView):
    column_list = [
        c.name for c in User.__table__.columns if c.name != "password"]
    form_columns = [c.name for c in User.__table__.columns]  # type: ignore


class AuthorView(ModelView):
    column_list = [c.name for c in Author.__table__.columns]
    form_columns = [c.name for c in Author.__table__.columns]  # type: ignore



class BookView(ModelView):
    column_list = [c.name for c in Book.__table__.columns]
    form_columns = [c.name for c in Book.__table__.columns]  # type: ignore


class LibraryView(ModelView):
    column_list = [c.name for c in MyLibrary.__table__.columns]
    # type: ignore
    form_columns = [c.name for c in MyLibrary.__table__.columns]

class WishlistItemView(ModelView):
    column_list = [c.name for c in WishlistItem.__table__.columns]
    # type: ignore
    form_columns = [c.name for c in WishlistItem.__table__.columns]


class ShoppingCartView(ModelView):
    column_list = [c.name for c in ShoppingCart.__table__.columns]
    form_columns = [c.name for c in ShoppingCart.__table__.columns]



def init_admin(app):
    admin_panel.init_app(app)
    admin_panel.add_view(UserView(User, db.session))
    admin_panel.add_view(AuthorView(Author, db.session))
    admin_panel.add_view(BookView(Book, db.session))
    admin_panel.add_view(LibraryView(MyLibrary, db.session))
    admin_panel.add_view(WishlistItemView(WishlistItem, db.session))
    admin_panel.add_view(ShoppingCartView(ShoppingCart, db.session))
    return admin_panel
