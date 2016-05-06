from flask_wtf import Form
from wtforms import StringField, TextAreaField, validators


class ContactForm(Form):
    name = StringField('Your name:', [validators.DataRequired()])
    property_address = StringField('Property Address:', [validators.DataRequired()])
    zip_code = StringField('Zip Code:', [validators.DataRequired()])
    questions = TextAreaField('Questions:', [validators.DataRequired()])
