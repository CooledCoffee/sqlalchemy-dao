# -*- coding: utf-8 -*-
from fixtures.testcase import TestWithFixtures
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
    
class DbTest(TestWithFixtures):
    def setUp(self):
        path = os.path.join(os.path.dirname(__file__), 'test.sql')
        fixture = MysqlFixture([path])
        self.useFixture(fixture)
        self.dao = fixture.dao
        