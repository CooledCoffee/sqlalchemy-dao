# -*- coding: utf-8 -*-
from fixtures._fixtures.tempdir import TempDir
from fixtures2.patches import PatchesFixture
from sqlalchemy_dao.dao import Dao
import doctest
import os
import sqlalchemy_dao
import subprocess

class MysqlFixture(PatchesFixture):
    def __init__(self, host='localhost', port=3306, username='test', password='test',
            db='test', scripts=(), daos=(), dao_class=Dao):
        super(MysqlFixture, self).__init__()
        self._host = os.getenv('TEST_MYSQL_HOST', host)
        self._port = os.getenv('TEST_MYSQL_PORT')
        self._port = port if self._port is None else int(self._port)
        self._username = os.getenv('TEST_MYSQL_USERNAME', username)
        self._password = os.getenv('TEST_MYSQL_PASSWORD', password)
        self._db = db
        self._scripts = [scripts] if isinstance(scripts, basestring) else scripts
        self._daos = daos
        self._dao_class = dao_class
        
    def setUp(self):
        super(MysqlFixture, self).setUp()
        self.tempdir = self.useFixture(TempDir())
        self._init_dbs()
        self.dao = self._create_dao()
        self._patch_daos()
        
    def _create_dao(self):
        url = 'mysql://%s:%s@%s:%d/%s?charset=utf8' \
                % (self._username, self._password, self._host, self._port, self._db)
        return self._dao_class(url, pool_size=sqlalchemy_dao.POOL_DISABLED)
        
    def _init_dbs(self):
        self._mysql_execute_sql('drop database if exists %s' % self._db)
        self._mysql_execute_sql('create database %s' % self._db)
        for script in self._scripts:
            self._mysql_execute_file(script)
            
    def _mysql_execute_file(self, path):
        patched_path = self.tempdir.join('patched.sql')
        with open(path) as f:
            sql = f.read()
        sql = sql.replace(' not null', '')
        with open(patched_path, 'w') as f:
            f.write(sql)
        cmd = 'MYSQL_PWD=%s mysql -h %s -u %s %s <%s' \
                % (self._password, self._host, self._username, self._db, patched_path)
        _shell(cmd)
        
    def _mysql_execute_sql(self, sql):
        cmd = 'MYSQL_PWD=%s mysql -h %s -u %s -e "%s"' \
                % (self._password, self._host, self._username, sql)
        _shell(cmd)
        
    def _patch_daos(self):
        for path in self._daos:
            self.patch(path, self.dao)
        
def _shell(cmd):
    retcode = subprocess.call(cmd, shell=True)
    if retcode != 0:
        raise Exception('Failed to execute "%s".' % cmd)

if __name__ == '__main__':
    doctest.testmod()
    