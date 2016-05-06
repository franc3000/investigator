from flask_wtf import Form
from wtforms import StringField, TextAreaField, SubmitField, validators

class ContactForm(Form):
    name = StringField('Your name:', [validators.DataRequired()])
    property_address = TextAreaField('Property Address:', [validators.DataRequired()])
    zip_code = TextAreaField('Your message:', [validators.DataRequired()])
    questions = TextAreaField('Questions:', [validators.DataRequired()])
    submit = SubmitField('Send Message')
