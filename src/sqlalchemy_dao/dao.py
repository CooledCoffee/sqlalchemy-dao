# -*- coding: utf-8 -*-
from sqlalchemy import engine
from sqlalchemy.orm import session
from sqlalchemy_dao.context import SessionContext
from sqlalchemy_dao.lock import Lock
from sqlalchemy_dao.session import Session

class Dao(object):
    def __init__(self, url):
        self._engine = engine.create_engine(url, echo=False)
        self._Session = session.sessionmaker(bind=self._engine, class_=Session)
        
    def create_session(self):
        return self._Session()
    
    def Lock(self, name):
        return Lock(self, name)
        
    def SessionContext(self, **kw):
        return SessionContext(self, **kw)
    