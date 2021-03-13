class UserManager__Settings(object):

    USER_ENABLE_REGISTER = True
    USER_DEFAULT_GROUP_NAME = 'default'
    USER_DEFAULT_ROLE_NAME = 'user'
    USER_DEFAULT_ROLE_DESCRIPTION = 'Normal User'
    USER_TEST_URL = '/test'
    USER_LOGIN_URL = '/login'
    USER_LOGOUT_URL = '/logout'
    USER_REGISTER_URL = '/register'
    USER_LOGIN_TEMPLATE = 'user/login.html' #:
    USER_REGISTER_TEMPLATE = 'user/register.html' #:
    USER_FORGOT_PASSWORD_TEMPLATE = 'user/forgot_password.html' #:
    USER_CONFIRM_EMAIL_TEMPLATE = 'user/emails/confirm_email' #:
    USER_AFTER_LOGOUT_URL = '/'
