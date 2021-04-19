import datetime
import sqlalchemy
from sqlalchemy import orm

from .db_session import SqlAlchemyBase


class UserAnswer(SqlAlchemyBase):
    __tablename__ = 'userAnswers'

    id = sqlalchemy.Column(sqlalchemy.Integer,
                           primary_key=True, autoincrement=True)
    title = sqlalchemy.Column(sqlalchemy.String, nullable=True)
    answer = sqlalchemy.Column(sqlalchemy.Text, nullable=True)
    completed = sqlalchemy.Column(sqlalchemy.Boolean, nullable=True)
    score = sqlalchemy.Column(sqlalchemy.Float, nullable=True)
    scores = sqlalchemy.Column(sqlalchemy.Text, nullable=True)

    user_id = sqlalchemy.Column(sqlalchemy.Integer,
                                sqlalchemy.ForeignKey("users.id"))
    user = orm.relation('User')

    test_id = sqlalchemy.Column(sqlalchemy.Integer,
                                sqlalchemy.ForeignKey("tests.id"))
    test = orm.relation('Test')

    def __repr__(self):
        return f"<UserAnswer> {self.title}, {self.test}, {self.user}"