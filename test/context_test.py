# -*- coding: utf-8 -*-
from testutil import DbTest, User

class SessionContextTest(DbTest):
    def test_success(self):
        # test
        with self.mysql.dao.SessionContext() as ctx:
            user = ctx.session.get(User, 1)
            user.name = 'user2'

        # verify
        with self.mysql.dao.create_session() as session:
            user = session.get(User, 1)
            self.assertEqual('user2', user.name)

    def test_error(self):
        # test
        with self.assertRaises(Exception):
            with self.mysql.dao.SessionContext() as ctx:
                user = ctx.session.get(User, 1)
                user.name = 'user2'
                raise Exception()
             
        # verify
        with self.mysql.dao.create_session() as session:
            user = session.get(User, 1)
            self.assertEqual('user1', user.name)
            