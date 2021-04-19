import datetime
import sqlalchemy
from sqlalchemy import orm

from .db_session import SqlAlchemyBase


class Class(SqlAlchemyBase):
    __tablename__ = 'classes'

    id = sqlalchemy.Column(sqlalchemy.Integer,
                           primary_key=True, autoincrement=True)
    title = sqlalchemy.Column(sqlalchemy.String, nullable=True)

    created_date = sqlalchemy.Column(sqlalchemy.DateTime,
                                     default=datetime.datetime.now)
    is_private = sqlalchemy.Column(sqlalchemy.Boolean, default=True)

    user_id = sqlalchemy.Column(sqlalchemy.Integer,
                                sqlalchemy.ForeignKey("users.id"))
    # teacher
    user = orm.relation('User')
    #
    # classes = orm.relation("RelationsTest", back_populates='test')
    # childrens
    users = orm.relation("User",
                              secondary="user_to_class",
                              backref="classes")

    def __repr__(self):
        return f"<Class> {self.title}, {self.created_date}, {self.user}"


user_to_class = sqlalchemy.Table(
    'user_to_class',
    SqlAlchemyBase.metadata,
    sqlalchemy.Column('user', sqlalchemy.Integer,
                      sqlalchemy.ForeignKey('users.id')),
    sqlalchemy.Column('class', sqlalchemy.Integer,
                      sqlalchemy.ForeignKey('classes.id'))
)
