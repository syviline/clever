"""import datetime
import sqlalchemy
from sqlalchemy import orm

from .db_session import SqlAlchemyBase


class RelationsTest(SqlAlchemyBase):
    __tablename__ = 'relationsTest'

    id = sqlalchemy.Column(sqlalchemy.Integer,
                           primary_key=True, autoincrement=True)

    # test_id = sqlalchemy.Column(sqlalchemy.Integer,
    #                             sqlalchemy.ForeignKey("tests.id"))
    # test = orm.relation('Test')

    # class_id = sqlalchemy.Column(sqlalchemy.Integer,
    #                             sqlalchemy.ForeignKey("classes.id"))
    # _class = orm.relation('Class')

    def __repr__(self):
        return f"<RelationsTest> {self.id}, {self._class}, {self.test}"
"""