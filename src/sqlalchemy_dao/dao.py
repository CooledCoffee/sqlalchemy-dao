# -*- coding: utf-8 -*-
from sqlalchemy import engine
from sqlalchemy.orm import session
from sqlalchemy.pool import NullPool
from sqlalchemy_dao.context import SessionContext
from sqlalchemy_dao.lock import Lock
from sqlalchemy_dao.session import Session
import sqlalchemy_dao
import sys

class Dao(object):
    session_class = Session
    session_context_class = SessionContext
    
    def __init__(self, url, pool_size=sqlalchemy_dao.POOL_DEFAULT):
        if pool_size == sqlalchemy_dao.POOL_DISABLED:
            self._engine = engine.create_engine(url, poolclass=NullPool)
        else:
            self._engine = engine.create_engine(url, pool_size=pool_size, pool_recycle=3600,
                    max_overflow=sys.maxsize)
        self._Session = session.sessionmaker(bind=self._engine, class_=self.session_class) # pylint: disable=invalid-name
        
    def create_session(self):
        return self._Session()
    
    def Lock(self, name): # pylint: disable=invalid-name
        return Lock(self, name)
        
    def SessionContext(self, **kw): # pylint: disable=invalid-name
        return self.session_context_class(self, **kw)
    