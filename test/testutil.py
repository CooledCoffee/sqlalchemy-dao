# -*- coding: utf-8 -*-
from fixtures2.case import TestCase
from sqlalchemy.schema import Column
from sqlalchemy.types import Integer, String
from sqlalchemy_dao.model import Model
from sqlalchemy_dao.testing import MysqlFixture
import os

class User(Model):
    id = Column(Integer, primary_key=True)
    name = Column(String)
    
class UserSetting(Model):
    id = Column(Integer, primary_key=True)
    key = Column(String, primary_key=True)
    value = Column(String)
    
class DbTest(TestCase):
    def setUp(self):
        super(DbTest, self).setUp()
        path = os.path.join(os.path.dirname(__file__), 'test.sql')
        fixture = MysqlFixture(db='sqlalchemy', scripts=path)
        self.mysql = self.useFixture(fixture)
        