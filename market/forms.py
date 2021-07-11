from flask.app import Flask
from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField, SubmitField
from wtforms.validators import Length, EqualTo, Email, DataRequired, ValidationError
from market.models import User


class RegisterForm(FlaskForm):

    def validate_username(self, username_to_check):
        user = User.query.filter_by(username=username_to_check.data).first()
        if user:
            raise ValidationError(
                'Username already exists! Please enter another!'
            )

    def validate_email_address(self, email_address_to_check):
        user = User.query.filter_by(
            email_address=email_address_to_check.data).first()
        if user:
            raise ValidationError(
                'Email address already exists! Please use another email!'
            )

    username = StringField(label='Username: ',
                           validators=[Length(min=5, max=20), DataRequired()])
    email_address = StringField(label='Email: ',
                                validators=[Email(), DataRequired()])
    password1 = PasswordField(label='Enter Password: ',
                              validators=[Length(min=8), DataRequired()])
    password2 = PasswordField(label='Confirm Password: ',
                              validators=[EqualTo('password1'), DataRequired()])
    submit = SubmitField(label='Create Account')


class LoginForm(FlaskForm):
    username = StringField(label='Username: ', validators=[DataRequired()])
    password = PasswordField(label='Password: ', validators=[DataRequired()])
    submit = SubmitField(label='Login')


class PurchaseItemForm(FlaskForm):
    submit = SubmitField(label='Purchase!')


class SellItemForm(FlaskForm):
    submit = SubmitField(label='Sell!')
