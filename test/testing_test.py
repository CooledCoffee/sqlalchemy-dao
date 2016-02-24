# -*- coding: utf-8 -*-
from testutil import DbTest, UserSetting

class MysqlFixtureTest(DbTest):
    def test_not_null_field(self):
        with self.mysql.dao.create_session() as session:
            session.add(UserSetting(id=1, key='a', value='aaa'))
            session.add(UserSetting(id=1, key='b'))
            