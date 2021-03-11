from flask.cli import AppGroup
import click


user_cli = AppGroup('user')

class UserManager__Cli(object):

    @user_cli.command('get', help='email')
    @click.argument('email')
    def _get_user_cli(self, email=None):
        pass

    @user_cli.command('add', help='fname, sname, email, pass and role')
    @click.command(context_settings=dict(ignore_unknown_options=True,))
    @click.argument('user_details', nargs=-1, type=click.UNPROCESSED)
    def _add_user_cli(self, user_details):
        user = self.user(user_details)
        user = self.add_user(user)
        if isinstance(user, self.user):
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
    def _update_user_cli(self, user_details):
        pass

    @user_cli.command('delete', help='email')
    @click.argument('email')
    def _delete_user_cli(self, email=None):
        pass

    def _add_cli_commands(self, user_bp):
        user_bp.cli.add_command(user_cli)


