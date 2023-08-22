from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField, SubmitField
from wtforms.validators import Length, EqualTo, DataRequired, Email, ValidationError
from blog.models import User


class RegisterForm(FlaskForm):

    def validate_username(self, username_check):
        user = User.query.filter_by(username=username_check.data).first()
        if user:
            raise ValidationError('Sorry, this username is already taken')

    def validate_email_address(self, email_address_check):
        user = User.query.filter_by(email=email_address_check.data).first()
        if user:
            raise ValidationError('Sorry, this email address is already taken')

    username = StringField(label='Username:', validators=[Length(min=2, max=15), DataRequired()])
    email_address = StringField(label='Email Address:', validators=[Email(), DataRequired()])
    password = PasswordField(label='Password:', validators=[Length(min=6), DataRequired()])
    password_conf = PasswordField(label='Confirm Password:', validators=[EqualTo('password'), DataRequired()])
    submit = SubmitField(label='Sign up')


class LoginForm(FlaskForm):
    username = StringField(label='Username:', validators=[DataRequired()])
    password = PasswordField(label='Password:', validators=[DataRequired()])
    submit = SubmitField(label='Log in')
