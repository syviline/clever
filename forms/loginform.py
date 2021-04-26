from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField, BooleanField, SubmitField
from wtforms.validators import DataRequired, Email


class LoginForm(FlaskForm):
    email = StringField('Почта', validators=[DataRequired(message='Введите почту'), Email(message='Введите адрес электронной почты')])
    password = PasswordField('Пароль', validators=[DataRequired(message='Введите пароль')])
    submit = SubmitField('Войти')