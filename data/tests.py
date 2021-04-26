import datetime
import sqlalchemy
from sqlalchemy import orm

from .db_session import SqlAlchemyBase


class Test(SqlAlchemyBase):
    __tablename__ = 'tests'

    id = sqlalchemy.Column(sqlalchemy.Integer,
                           primary_key=True, autoincrement=True)
    title = sqlalchemy.Column(sqlalchemy.String, nullable=True)
    task = sqlalchemy.Column(sqlalchemy.Text, nullable=True)  # само задание в формате json

    created_date = sqlalchemy.Column(sqlalchemy.DateTime,
                                     default=datetime.datetime.now)
    is_private = sqlalchemy.Column(sqlalchemy.Boolean, default=True)

    user_id = sqlalchemy.Column(sqlalchemy.Integer,
                                sqlalchemy.ForeignKey("users.id"))

    answers = sqlalchemy.Column(sqlalchemy.Text)  # ответы на тест в формате json
    scores = sqlalchemy.Column(sqlalchemy.Text)  # значения баллов за каждое задание, json
    is_completable = sqlalchemy.Column(sqlalchemy.Boolean, default=False)

    # sozdatetel
    user = orm.relation('User')

    # classes = orm.relation("RelationsTest", back_populates='test')
    # kto prohodil test
    users = orm.relation("User",
                         secondary="user_to_test",
                         backref="tests")

    def __repr__(self):
        return f"<Test> {self.title}, {self.created_date}, {self.user}"


user_to_test = sqlalchemy.Table(
    'user_to_test',
    SqlAlchemyBase.metadata,
    sqlalchemy.Column('testid', sqlalchemy.Integer,
                      sqlalchemy.ForeignKey('tests.id')),
    sqlalchemy.Column('userid', sqlalchemy.Integer,
                      sqlalchemy.ForeignKey('users.id')),
)
