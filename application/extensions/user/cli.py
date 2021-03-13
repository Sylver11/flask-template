from .user_manager import UserManager
from .models import User
from flask.cli import AppGroup
import click


user_cli = AppGroup('security')


@user_cli.command('get', help='email')
@click.argument('email')
def get_user_cli(email=None):
    pass

@user_cli.command('add-group')
@click.option('--groupname', prompt='Group Name',)
@click.option('--adminuser', prompt='Admin User Email',)
def add_group_cli(group_name, admin_user_email):
    user = User.query.filter_by(email=admin_user_email)
    if not user:
        click.echo('Group not created. Admin user does not exist.')
    if user.group_admin:
        click.echo('Group not created. User already admin of another group')
    if user.group_uuid:
        click.echo('Group not created. User already part of another group')
    group = db.session.add(Group(name=group_name))
    user.group_uuid = group.uuid
    user.group_admin = True
    db.session.commit()
    click.echo('Group successfully created')
    return None

@user_cli.command(
        'add-user',
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
@click.option('--group',
        prompt='Group name',
        default = 'default',
        help='Leave empty for default')
@click.password_option()
def add_user_cli(firstname, secondname, email, group, password):
    user = User(
            firstname=firstname,
            secondname=secondname,
            email=email)
    user.set_password(password)
    user_manager = UserManager()
    if group != 'default':
        group = user_manager.get_group_by_name(group)
        if not group:
            click.echo('User not created. The specified group does not exist')
        user.group = group
    user = user_manager.add_user(user)
    if isinstance(user, User):
        if user.uuid:
            click.echo('User successfully created and added to '\
                    + user.group.name + ' group')
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

