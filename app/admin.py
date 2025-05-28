from flask_admin import Admin
from flask_admin.contrib.sqla import ModelView
from app.extensions import db
from app.models.user import User
from app.models.author import Author

admin_panel = Admin(name='Admin Panel', template_mode='bootstrap4')


class UserView(ModelView):
    column_list = [
        c.name for c in User.__table__.columns if not c == "password"]
    form_columns = [c.name for c in User.__table__.columns]  # type: ignore


class AuthorView(ModelView):
    column_list = ['id', 'name', 'bio', 'photo_url']


def init_admin(app):
    admin_panel.init_app(app)
    admin_panel.add_view(UserView(User, db.session))
    admin_panel.add_view(AuthorView(Author, db.session))
    return admin_panel
