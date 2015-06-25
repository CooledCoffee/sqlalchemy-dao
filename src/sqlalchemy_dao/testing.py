# -*- coding: utf-8 -*-
from fixtures2.patches import PatchesFixture
from sqlalchemy_dao.dao import Dao
import doctest
import sqlalchemy_dao
import subprocess

class MysqlFixture(PatchesFixture):
    def __init__(self, host='localhost', username='test', password='test',
            db='test', scripts=(), daos=(), dao_class=Dao):
        super(MysqlFixture, self).__init__()
        self._host = host
        self._username = username
        self._password = password
        self._db = db
        self._scripts = [scripts] if isinstance(scripts, basestring) else scripts
        self._daos = daos
        self._dao_class = dao_class
        
    def setUp(self):
        super(MysqlFixture, self).setUp()
        self._init_dbs()
        self.dao = self._create_dao()
        self._patch_daos()
        
    def _create_dao(self):
        url = 'mysql://%s:%s@%s/%s?charset=utf8' \
                % (self._username, self._password, self._host, self._db)
        return self._dao_class(url, pool_size=sqlalchemy_dao.POOL_DISABLED)
        
    def _init_dbs(self):
        self._mysql_execute_sql('drop database if exists %s' % self._db)
        self._mysql_execute_sql('create database %s' % self._db)
        for script in self._scripts:
            self._mysql_execute_file(script)
            
    def _mysql_execute_file(self, path):
        cmd = 'MYSQL_PWD=%s mysql -h %s -u %s %s <%s' \
                % (self._password, self._host, self._username, self._db, path)
        _shell(cmd)
        
    def _mysql_execute_sql(self, sql):
        cmd = 'mysql -h %s --user=%s --password=%s -e "%s"' \
                % (self._host, self._username, self._password, sql)
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
    