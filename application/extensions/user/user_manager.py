from flask_login import LoginManager
from flask import Blueprint
from application.database import db
from .models import User, Group, Role
from .user_manager__settings import UserManager__Settings
from .user_manager__views import UserManager__Views
from .user_manager__utils import UserManager__Utils

class UserManager(UserManager__Settings,
        UserManager__Views,
        UserManager__Utils):

    def __init__(self, app=None):
        self.app = app
        if app:
            self.init_user(app)

    def init_user(self, app):
        app.user_manager = self

        self.login_manager = LoginManager(app)
        self.login_manager.login_view = 'user_bp.login'
        @self.login_manager.user_loader
        def load_user(uuid):
            return User.query.filter_by(uuid).first()

        blueprint = Blueprint(
                'user_bp',
                __name__,
                template_folder='templates',
                static_folder='static',)

        app.register_blueprint(blueprint)

        self._add_url_routes(app)

        from .cli import user_cli
        app.cli.add_command(user_cli)

        @app.before_request
        def check_user_db_defaults(self):
            db.session.clear()
            if self.USER_DEFAULT_GROUP_NAME:
                name = self.USER_DEFAULT_GROUP_NAME
                group = Group.query.filter_by(name).first()
                if not group:
                    group = Group(name=name)
                    db.session.add(group)
            if self.USER_DEFAULT_ROLE_NAME:
                name = self.USER_DEFAULT_ROLE_NAME
                role = Role.query.filter_by(name).first()
                if not role:
                    description = self.USER_DEFAULT_ROLE_DESCRIPTION
                    role = Role(name=name, description=description)
                    db.session.add(role)
            db.session.commit()


    def deactivate_user(self, user):
        pass

    def activate_user(self, user):
        pass

    def create_role(self, **kwargs):
        pass

    def find_or_create_role(self, name, **kwargs):
        pass

    def get_user_by_email(self, email=None):
        if email:
            user = User.query.filter_by(email).first()
            return user
        users = User.query.all()
        return users

    def add_user(user_model):
        from sqlalchemy.exc import IntegrityError
        try:
            new_user = db.session.add(user_model)
            db.session.commit()
        except IntegrityError as err:
            db.session.rollback()
            return 'User already exists'
        return new_user

    def update_user(self, user):
        user = db.session.merge(user)
        db.session.commit()
        return user

    def delete_user(self, user):
        db.session.delete(user)
        db.session.commit()
        return None


    def _add_url_routes(self, app):

        def test_stub():
            return self.test_view()

        def login_stub():
            return self.login_view()

        def logout_stub():
            return self.logout_view()

        def register_stub():
            if not self.USER_ENABLE_REGISTER: abort(404)
            return self.register_view()


        app.add_url_rule(self.USER_TEST_URL, 'user_bp.test', test_stub, methods=['GET', 'POST'])
        app.add_url_rule(self.USER_REGISTER_URL, 'user_bp.register', register_stub, methods=['GET', 'POST'])
        app.add_url_rule(self.USER_LOGOUT_URL, 'user_bp.logout', logout_stub, methods=['GET', 'POST'])
        app.add_url_rule(self.USER_LOGIN_URL, 'user_bp.login', login_stub, methods=['GET', 'POST'])

