from .user_manager import UserManager
from .models import User
from flask.cli import AppGroup
import click


user_cli = AppGroup('user')


@user_cli.command('get', help='email')
@click.argument('email')
def get_user_cli(email=None):
    pass

@user_cli.command(
        'add',
        help='Create user by setting the following variables:\
                    1. email\
                    2. firstname\
                    3. secondname\
                    Example: email:connectmaeuse@gmail.com,\
                    firstname: Justus,\
                    secondname: Voigt')
@click.option('--firstname', prompt='Firstname',)
@click.option('--secondname', prompt='Secondname',)
@click.option('--email', prompt='Email',)
@click.password_option()
def add_user_cli(firstname, secondname, email, password):
    user = User(
            firstname=firstname,
            secondname=secondname,
            email=email)
    user.set_password(password)
    user = UserManager.add_user(user)
    if isinstance(user, User):
        if user.uuid:
            click.echo('User successfully created')
        else:
            click.echo('User could not be created')
    else:
        click.echo('User already exists')
    return None

@user_cli.command('update', help='fname, sname, email, pass and role')
@click.command(context_settings=dict(ignore_unknown_options=True,))
@click.argument('user_details', nargs=-1, type=click.UNPROCESSED)
def update_user_cli(user_details):
    pass

@user_cli.command('delete', help='email')
@click.argument('email')
def delete_user_cli(email):
    pass

