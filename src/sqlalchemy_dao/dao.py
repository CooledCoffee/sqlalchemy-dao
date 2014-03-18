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
    def __init__(self, url, pool_size=sqlalchemy_dao.POOL_DEFAULT):
        pool_class = NullPool if pool_size == sqlalchemy_dao.POOL_DISABLED else None
        self._engine = engine.create_engine(url, poolclass=pool_class, pool_size=pool_size,
                max_overflow=sys.maxsize, pool_recycle=3600)
        self._Session = session.sessionmaker(bind=self._engine, class_=Session)
        
    def create_session(self):
        return self._Session()
    
    def Lock(self, name):
        return Lock(self, name)
        
    def SessionContext(self, **kw):
        return SessionContext(self, **kw)
    