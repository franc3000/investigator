#!/usr/bin/env python
# -*- coding: utf-8 -*-
import os

from flask.ext.mail import Message, Mail
from flask_script import Manager, Shell, Server
from flask_script.commands import Clean, ShowUrls
from flask_migrate import MigrateCommand

from investigator.app import create_app
from investigator.models.user import User
from investigator.settings import DevConfig, ProdConfig
from investigator.database import db

if os.environ.get('INVESTIGATOR_ENV') == 'prod':
    app = create_app(ProdConfig)
else:
    app = create_app(DevConfig)

HERE = os.path.abspath(os.path.dirname(__file__))
TEST_PATH = os.path.join(HERE, 'tests')

manager = Manager(app)


def _make_context():
    """Return context dict for a shell session so you can access
    app, db, and the User model by default.
    """
    return {'app': app, 'db': db, 'User': User}


@manager.command
def test():
    """Run the tests."""
    import pytest
    exit_code = pytest.main([TEST_PATH, '--verbose'])
    return exit_code


class ImproperlyConfigured(Exception):
    pass


@manager.command
def send_test_email():
    """Sends test email to admins."""

    # Validate settings.
    errors = []
    if not app.config.get('MAIL_DEFAULT_SENDER'):
        errors.append('`MAIL_DEFAULT_SENDER` setting is required.')

    if not app.config.get('MAIL_PASSWORD'):
        errors.append('`MAIL_PASSWORD` setting is required.')

    if not app.config.get('MAIL_PORT'):
        errors.append('`MAIL_PORT` setting is required.')

    if not app.config.get('MAIL_SERVER'):
        errors.append('`MAIL_SERVER` setting is required.')

    if not app.config.get('MAIL_USERNAME'):
        errors.append('`MAIL_USERNAME` setting is required.')

    if not app.config.get('ADMINS'):
        errors.append('`ADMINS` setting is required and should contain a list of emails.')

    if not isinstance(app.config.get('ADMINS'), list):
        errors.append('`ADMINS` setting has to be list of emails.')

    if errors:
        raise ImproperlyConfigured(
            'Email is not configured properly. Errors:\n    {}'.format('\n    '.join(errors)))

    # Send email.
    msg = Message(
        'Test',
        sender=app.config['MAIL_DEFAULT_SENDER'],
        recipients=app.config['ADMINS'])
    Mail(app).send(msg)


manager.add_command('server', Server(host='0.0.0.0'))
manager.add_command('shell', Shell(make_context=_make_context))
manager.add_command('db', MigrateCommand)
manager.add_command('urls', ShowUrls())
manager.add_command('clean', Clean())

if __name__ == '__main__':
    manager.run()
