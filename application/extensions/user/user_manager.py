from flask_login import LoginManager
from flask import Blueprint
from .models import User
from .user_manager__settings import UserManager__Settings
from .user_manager__views import UserManager__Views
from .user_manager__cli import UserManager__Cli
from .user_manager__utils import UserManager__Utils

class UserManager(UserManager__Settings,
        UserManager__Views,
        UserManager__Cli,
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
                static_folder='static',
                url_prefix='/user',)

        app.register_blueprint(blueprint)

        self._add_url_routes(app)
        self._add_cli_commands(app)

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

    def add_user(self, new_user, password):
        from sqlalchemy.exc import IntegrityError
        new_user.set_password(password)
        try:
            new_user = db.session.add(new_user)
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


    def _add_url_routes(self, user_bp):

        def test_stub():
            return self.test_view()

        def login_stub():
            return self.login_view()

        def logout_stub():
            return self.logout_view()

        def register_stub():
            if not self.USER_ENABLE_REGISTER: abort(404)
            return self.register_view()


        user_bp.add_url_rule(self.USER_TEST_URL, 'user_bp.test', test_stub, methods=['GET', 'POST'])
        user_bp.add_url_rule(self.USER_REGISTER_URL, 'user_bp.register', register_stub, methods=['GET', 'POST'])
        user_bp.add_url_rule(self.USER_LOGOUT_URL, 'user_bp.logout', logout_stub, methods=['GET', 'POST'])
        user_bp.add_url_rule(self.USER_LOGIN_URL, 'user_bp.login', login_stub, methods=['GET', 'POST'])

