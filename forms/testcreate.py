from flask_wtf import FlaskForm
from wtforms import StringField, SubmitField, BooleanField
from wtforms.validators import DataRequired


class TestCreate(FlaskForm):
    name = StringField('Название', validators=[DataRequired(message='Введите название')])
    canseeresults = BooleanField('Может ли ученик просматривать результаты')
    submit = SubmitField('Создать')