import datetime
import sqlalchemy
from sqlalchemy import orm

from .db_session import SqlAlchemyBase


class UserAnswer(SqlAlchemyBase):
    __tablename__ = 'userAnswers'

    id = sqlalchemy.Column(sqlalchemy.Integer,
                           primary_key=True, autoincrement=True)
    answer = sqlalchemy.Column(sqlalchemy.Text, nullable=True)
    completed = sqlalchemy.Column(sqlalchemy.Boolean, nullable=True)
    score = sqlalchemy.Column(sqlalchemy.Float, nullable=True)
    maxscore = sqlalchemy.Column(sqlalchemy.Text, nullable=True)
    class_id = sqlalchemy.Column(sqlalchemy.Integer,
                                sqlalchemy.ForeignKey("classes.id"))

    user_id = sqlalchemy.Column(sqlalchemy.Integer,
                                sqlalchemy.ForeignKey("users.id"))
    user = orm.relation('User')

    test_id = sqlalchemy.Column(sqlalchemy.Integer,
                                sqlalchemy.ForeignKey("tests.id"))
    test = orm.relation('Test')

    classes = orm.relation('Class')

    def __repr__(self):
        return f"<UserAnswer> {self.title}, {self.test}, {self.user}"
