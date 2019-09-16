from todo_list import app, db
from todo_list.models import User
# command create package
import click

# custom shell command(usage: flask command)
@app.cli.command()
@click.option('--drop', is_flag=True, help='Create after drop')
def initdb(drop):
    if drop:
        click.echo('Delete current db model')
        db.drop_all()
    db.create_all()
    click.echo('Initialized database')


# command admin
@app.cli.command()
@click.option('--username', prompt=True, help='username.')
@click.option('--password', prompt=True, hide_input=True, confirmation_prompt=True, help='password.')
def admin(username, password):
    db.create_all()

    click.echo('Creating user.')
    user = User(username=username)
    user.set_password(password)
    db.session.add(user)
    db.session.commit()
    click.echo('Done.')
