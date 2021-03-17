from .security_manager import SecurityManager
from .models import User
from flask.cli import AppGroup
import click


security_cli = AppGroup('security')


@user_cli.command('get', help='email')
@click.argument('email')
def get_user_cli(email=None):
    pass

@user_cli.command('add-group')
@click.option('--groupname', prompt='Group Name',required=True)
@click.option('--adminuser', prompt='Admin User Email',required=True)
def add_group_cli(group_name, admin_user_email):
    user = User.query.filter_by(email=admin_user_email)
    if not user:
        click.echo('Group not created. Admin user does not exist.')
        return None
    if user.group_name:
        click.echo('Group not created. User already part of another group')
        return None
    if user.group_admin:
        click.echo('Group not created. User already admin of another group')
        return None
    group = db.session.add(Group(name=group_name))
    user.group_uuid = group.uuid
    user.group_admin = True
    db.session.commit()
    click.echo('Group successfully created')
    return None

@user_cli.command('add-user',)
@click.option('--firstname', prompt='Firstname',required=True)
@click.option('--secondname', prompt='Secondname',required=True)
@click.option('--email', prompt='Email',required=True)
@click.password_option(required=True)
@click.option('--group',
        prompt='Group name (optional)',
        default='None'
        help='Leave empty for default')
def add_user_cli(firstname, secondname, email, password, group):
    user = User(
            firstname=firstname,
            secondname=secondname,
            email=email)
    user.set_password(password)
    security_manager = SecurityManager()
    if group != 'None':
        group = security_manager.get_group_by_name(group)
        if not group:
            click.echo('User not created. The specified group does not exist')
            return None
        user.group = group
    user = security_manager.add_user(user)
    if isinstance(user, User):
        if user.uuid:
            feedback = 'User successfully created'
            if user.group:
                feedback += ' and added to ' + user.group.name + ' group.'
            click.echo(feedback)
            return None
        else:
            click.echo('User could not be created')
            return None
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

