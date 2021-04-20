from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField, BooleanField, SubmitField, SelectMultipleField
from wtforms.validators import DataRequired, Email, EqualTo


class RegisterForm(FlaskForm):
    firstname = StringField('Ваше имя', validators=[DataRequired()])
    lastname = StringField('Ваша фамилия', validators=[DataRequired()])
    email = StringField('Почта', validators=[DataRequired(), Email(message='Введите действительный почтовый адрес')])
    password = PasswordField('Пароль', validators=[DataRequired()])
    passwordRepeat = PasswordField('Повторите пароль', validators=[DataRequired(), EqualTo('password', message='Пароли должны совпадать')])
    submit = SubmitField('Зарегистрироваться')