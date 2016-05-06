# Investigator

An app to investigate individual properties.


## Quickstart

First, set your app's secret key as an environment variable. For example, example add the following to ``.bashrc`` or ``.bash_profile``.

```
export INVESTIGATOR_SECRET='something-really-secret'
```

Then run the following commands to bootstrap your environment.


```
git clone https://github.com/franc3000/investigator
cd investigator
pip install -r requirements/dev.txt
python manage.py server
```

You will see a pretty welcome screen.

Once you have installed your DBMS, run the following to create your app's database tables and perform the initial migration:

```
python manage.py db init
python manage.py db migrate
python manage.py db upgrade
python manage.py server
```


## Deployment

In your production environment, make sure the ``INVESTIGATOR_ENV`` environment variable is set to ``"prod"``.


## Shell

To open the interactive shell, run ::

```
python manage.py shell
```

By default, you will have access to ``app``, ``db``, and the ``User`` model.


## Running Tests

To run all tests, run ::

```
python manage.py test
```


## Migrations

Whenever a database migration needs to be made. Run the following commands:

```
python manage.py db migrate
```

This will generate a new migration script. Then run:

```
python manage.py db upgrade
```

To apply the migration.

For a full migration command reference, run `python manage.py db --help`.

## Environment variables with email settings.
```
INVESTIGATOR_MAIL_SERVER          # Email server
INVESTIGATOR_MAIL_PORT            # Mail port, default 25
INVESTIGATOR_MAIL_USE_SSL         # Use SSL, default False
INVESTIGATOR_MAIL_USERNAME        # Username
INVESTIGATOR_MAIL_PASSWORD        # Password
INVESTIGATOR_MAIL_DEFAULT_SENDER  # Sender
INVESTIGATOR_ADMINS               # Comma separated list of emails who will receive the questions.
```

How to setup email on heroku (debugmail.io example).

```bash
heroku config:add INVESTIGATOR_MAIL_SERVER='debugmail.io'
heroku config:add INVESTIGATOR_MAIL_PORT=25
heroku config:add INVESTIGATOR_MAIL_USE_SSL=0
heroku config:add INVESTIGATOR_MAIL_USERNAME='<username>'
heroku config:add INVESTIGATOR_MAIL_PASSWORD='<password>'
heroku config:add INVESTIGATOR_MAIL_DEFAULT_SENDER='<sender>'
heroku config:add INVESTIGATOR_ADMINS='user1@example.com,user2@example.com'
```

After setup you can send test email to verify email sending.
```bash
heroku run python manage.py send_test_email
```
This command checks your config and sends email to the admins.
