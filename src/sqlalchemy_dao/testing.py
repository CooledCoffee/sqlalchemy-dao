# -*- coding: utf-8 -*-
from fixtures._fixtures.monkeypatch import MonkeyPatch
from fixtures.fixture import Fixture
from sqlalchemy_dao.dao import Dao
import sqlalchemy_dao
import subprocess

class MysqlFixture(Fixture):
    def __init__(self, scripts, daos=None):
        super(MysqlFixture, self).__init__()
        self._scripts = scripts
        self._daos = daos or []
        
    def setUp(self):
        super(MysqlFixture, self).setUp()
        self._init_db('test')
        self.dao = self._create_dao()
        self._patch_daos()
        
    def _create_dao(self):
        return Dao('mysql://test:test@localhost/test?charset=utf8',
                pool_size=sqlalchemy_dao.POOL_DISABLED)
        
    def _init_db(self, database):
        _call_mysql('mysql --user=test --password=test -e "drop database if exists %s"' % database)
        _call_mysql('mysql --user=test --password=test -e "create database %s default character set utf8 default collate utf8_general_ci"' % database)
        for script in self._scripts:
            _call_mysql('mysql --user=test --password=test %s <%s' % (database, script))
            
    def _patch_daos(self):
        for path in self._daos:
            self.useFixture(MonkeyPatch(path, self.dao))
            
def _call_mysql(cmd):
    retcode = subprocess.call(cmd, shell=True)
    if retcode != 0:
        raise Exception('Failed to execute mysql command "%s".' % cmd)
    