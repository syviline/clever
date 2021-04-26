from flask_wtf import FlaskForm
from wtforms import StringField, SubmitField
from wtforms.validators import DataRequired


class ClassCreate(FlaskForm):
    name = StringField('Название', validators=[DataRequired(message='Введите название')])
    submit = SubmitField('Создать')