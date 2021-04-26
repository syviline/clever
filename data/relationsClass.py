"""import datetime
import sqlalchemy
from sqlalchemy import orm

from .db_session import SqlAlchemyBase


class RelationsClass(SqlAlchemyBase):
    __tablename__ = 'relationsClass'

    id = sqlalchemy.Column(sqlalchemy.Integer,
                           primary_key=True, autoincrement=True)

    # user_id = sqlalchemy.Column(sqlalchemy.Integer,
    #                             sqlalchemy.ForeignKey("users.id"))
    # user = orm.relation('User')

    # class_id = sqlalchemy.Column(sqlalchemy.Integer,
    #                             sqlalchemy.ForeignKey("classes.id"))
    # _class = orm.relation('Class')

    def __repr__(self):
        return f"<RelationsClass> {self.id}, {self._class}, {self.user}"
"""