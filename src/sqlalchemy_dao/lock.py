# -*- coding: utf-8 -*-
from sqlalchemy.exc import ProgrammingError
from sqlalchemy_dao.errors import DbError

class Lock(object):
    def __init__(self, dao, name):
        self._dao = dao
        self._name = name
        self._session = None

    def __enter__(self):
        self._session = self._dao.create_session()
        try:
            try:
                rows = self._session.execute("select * from `lock` where name='%s' for update" % self._name).fetchall()
            except ProgrammingError:
                raise DbError('Lock "%s" not found.' % self._name)
            if len(rows) != 1:
                raise DbError('Lock "%s" not found.' % self._name)
            return self
        except:
            self._session.rollback()
            raise

    def __exit__(self, *args):
        self._session.rollback()
        