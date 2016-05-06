# -*- coding: utf-8 -*-
"""Public section, including homepage and signup."""
from flask import (Blueprint, request, render_template, flash, url_for, send_from_directory, make_response,
                   redirect, current_app)
import datetime

from flask_login import login_required, logout_user
from flask.ext.mail import Message, Mail

from investigator.forms.property_request import ContactForm

from investigator.extensions import login_manager
from investigator.models.user import User
from investigator.forms.public import LoginForm
from investigator.forms.user import RegisterForm
from investigator.utils import flash_errors, render_extensions


blueprint = Blueprint('public', __name__, static_folder='../static')


@login_manager.user_loader
def load_user(id):
    return User.get_by_id(int(id))


@blueprint.route('/', methods=['GET', 'POST'])
def home():

    form = ContactForm(request.form)

    if request.method == 'POST':
        if form.validate_on_submit():
            flash('Questions sent.', 'success')

            # Send email.
            body = '''
                Question from investigator.

                Name:             {}
                Property address: {}
                Zip Code:         {}
                Questions:

                {}
            '''.format(form.name.data, form.property_address.data, form.zip_code.data, form.questions.data)
            msg = Message(
                'Question from investigator',
                body=body,
                sender=current_app.config['MAIL_DEFAULT_SENDER'],
                recipients=current_app.config['ADMINS'])
            Mail(current_app).send(msg)
            return redirect('/')
        else:
            flash_errors(form)
    return render_extensions('public/home.html', form=form)


@blueprint.route('/logout/')
@login_required
def logout():
    logout_user()
    flash('You are logged out.', 'info')
    return redirect(url_for('public.home'))


@blueprint.route("/register/", methods=['GET', 'POST'])
def register():
    form = RegisterForm(request.form, csrf_enabled=False)
    if form.validate_on_submit():
        User.create(username=form.username.data,
                    first_name=form.first_name.data,
                    last_name=form.last_name.data,
                    email=form.email.data,
                    password=form.password.data,
                    active=True)
        flash('Thank you for registering. You can now log in.', 'success')
        return redirect(url_for('public.home'))
    else:
        flash_errors(form)
    return render_extensions('public/register.html', form=form)


@blueprint.route('/about/')
def about():
    form = LoginForm(request.form)
    return render_extensions('public/about.html', form=form)


@blueprint.route('/robots.txt')
@blueprint.route('/favicon.ico')
def static_from_root():
    return send_from_directory(current_app.static_folder, request.path[1:])


@blueprint.route('/sitemap.xml', methods=['GET'])
def sitemap():
    """
    Generate sitemap.xml. Makes a list of urls and date modified.
    """
    pages = []
    ten_days_ago = datetime.datetime.now() - datetime.timedelta(days=10)
    ten_days_ago = ten_days_ago.date().isoformat()
    # static pages
    for rule in current_app.url_map.iter_rules():
        if 'GET' in rule.methods and len(rule.arguments) == 0:
            pages.append([rule.rule, ten_days_ago])

    sitemap_xml = render_template('public/sitemap_template.xml', pages=pages)
    response = make_response(sitemap_xml)
    response.headers['Content-Type'] = 'application/xml'

    return response
