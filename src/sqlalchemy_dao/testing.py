# -*- coding: utf-8 -*-
from fixtures._fixtures.monkeypatch import MonkeyPatch
from fixtures.fixture import Fixture
from sqlalchemy_dao.dao import Dao
import subprocess

class MysqlFixture(Fixture):
    def __init__(self, sql_pathes, dao_pathes=None):
        super(MysqlFixture, self).__init__()
        self._sql_pathes = sql_pathes
        self._dao_pathes = dao_pathes or []
        
    def setUp(self):
        super(MysqlFixture, self).setUp()
        self._init_db('test')
        self._stub_daos()
        
    def _init_db(self, database):
        _call_mysql('mysql --user=test --password=test -e "drop database if exists %s"' % database)
        _call_mysql('mysql --user=test --password=test -e "create database %s default character set utf8 default collate utf8_general_ci"' % database)
        for path in self._sql_pathes:
            _call_mysql('mysql --user=test --password=test %s <%s' % (database, path))
            
    def _stub_daos(self):
        self.dao = Dao('mysql://test:test@localhost/test?charset=utf8')
        for path in self._dao_pathes:
            self.useFixture(MonkeyPatch(path, self.dao))
            
def _call_mysql(cmd):
    retcode = subprocess.call(cmd, shell=True)
    if retcode != 0:
        raise Exception('Failed to execute mysql command "%s".' % cmd)
    