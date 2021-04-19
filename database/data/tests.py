import datetime
import sqlalchemy
from sqlalchemy import orm

from .db_session import SqlAlchemyBase


class Test(SqlAlchemyBase):
    __tablename__ = 'tests'

    id = sqlalchemy.Column(sqlalchemy.Integer,
                           primary_key=True, autoincrement=True)
    title = sqlalchemy.Column(sqlalchemy.String, nullable=True)
    task = sqlalchemy.Column(sqlalchemy.Text, nullable=True)

    created_date = sqlalchemy.Column(sqlalchemy.DateTime,
                                     default=datetime.datetime.now)
    is_private = sqlalchemy.Column(sqlalchemy.Boolean, default=True)

    user_id = sqlalchemy.Column(sqlalchemy.Integer,
                                sqlalchemy.ForeignKey("users.id"))
    # sozdatetel
    user = orm.relation('User')

    # classes = orm.relation("RelationsTest", back_populates='test')
    # klassi u kotorih etot test
    classes = orm.relation("Class",
                           secondary="class_to_test",
                           backref="tests")
    # kto prohodil test
    users = orm.relation("User",
                         secondary="class_to_test",
                         backref="tests")

    def __repr__(self):
        return f"<Test> {self.title}, {self.created_date}, {self.user}"


class_to_test = sqlalchemy.Table(
    'class_to_test',
    SqlAlchemyBase.metadata,
    sqlalchemy.Column('test', sqlalchemy.Integer,
                      sqlalchemy.ForeignKey('tests.id')),
    sqlalchemy.Column('class', sqlalchemy.Integer,
                      sqlalchemy.ForeignKey('classes.id'))
)

user_to_test = sqlalchemy.Table(
    'user_to_test',
    SqlAlchemyBase.metadata,
    sqlalchemy.Column('test', sqlalchemy.Integer,
                      sqlalchemy.ForeignKey('tests.id')),
    sqlalchemy.Column('user', sqlalchemy.Integer,
                      sqlalchemy.ForeignKey('user.id'))
)
