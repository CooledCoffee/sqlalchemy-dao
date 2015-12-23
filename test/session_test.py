# -*- coding: utf-8 -*-
from sqlalchemy.orm.exc import DetachedInstanceError
from sqlalchemy_dao.errors import DbError
from testutil import User, DbTest

class WithTest(DbTest):
    def test_success(self):
        # test
        with self.mysql.dao.create_session() as session:
            user = session.query(User).get(1)
            user.name = 'user2'
            
        # verify: should be expunged
        with self.assertRaises(DetachedInstanceError):
            user.id
        
        # verify: should be committed
        with self.mysql.dao.create_session() as session:
            user = session.query(User).get(1)
            self.assertEqual('user2', user.name)
        
    def test_failed(self):
        # test
        with self.assertRaises(Exception):
            with self.mysql.dao.create_session() as session:
                user = session.query(User).get(1)
                user.name = 'user2'
                raise Exception()
        
        # verify: should be expunged
        with self.assertRaises(DetachedInstanceError):
            user.id
        
        # verify: should be rollbacked
        with self.mysql.dao.create_session() as session:
            user = session.query(User).get(1)
            self.assertEqual('user1', user.name)
        
class ExecuteForAllTest(DbTest):
    def test(self):
        with self.mysql.dao.create_session() as session:
            users = session.execute_for_all("select * from user")
            self.assertEqual(2, len(users))
            self.assertEqual(1, users[0].id)
            self.assertEqual(2, users[1].id)
            
class ExecuteForFirstTest(DbTest):
    def test_success(self):
        with self.mysql.dao.create_session() as session:
            user = session.execute_for_first("select * from user")
            self.assertEqual(1, user.id)
            
    def test_not_found(self):
        with self.mysql.dao.create_session() as session:
            user = session.execute_for_first("select * from user where id=0")
            self.assertIsNone(user)
            
class ExecuteForOneTest(DbTest):
    def test_success(self):
        with self.mysql.dao.create_session() as session:
            user = session.execute_for_one("select * from user")
            self.assertEqual(1, user.id)
            
    def test_not_found(self):
        with self.assertRaises(DbError):
            with self.mysql.dao.create_session() as session:
                session.execute_for_one("select * from user where id=0")
            
class ExecuteForScalarTest(DbTest):
    def test_success(self):
        with self.mysql.dao.create_session() as session:
            result = session.execute_for_scalar("select name from user where id=1")
            self.assertEqual('user1', result)
        
    def test_not_found(self):
        with self.assertRaises(DbError):
            with self.mysql.dao.create_session() as session:
                session.execute_for_scalar("select name from user where id=3")
                
    def test_multi_rows(self):
        with self.assertRaises(DbError):
            with self.mysql.dao.create_session() as session:
                session.execute_for_scalar("select name from user")
                
class GetTest(DbTest):
    def test_found(self):
        with self.mysql.dao.create_session() as session:
            user = session.get(User, 1)
            self.assertEqual('user1', user.name)
            
    def test_not_found(self):
        with self.mysql.dao.create_session() as session:
            user = session.get(User, 3)
            self.assertIsNone(user)
            
class GetOrCreateTest(DbTest):
    def test_found(self):
        with self.mysql.dao.create_session() as session:
            user = session.get_or_create(User, 1)
            self.assertEqual(1, user.id)
            self.assertEqual('user1', user.name)
            
    def test_not_found(self):
        # test
        with self.mysql.dao.create_session() as session:
            user = session.get_or_create(User, 3)
            self.assertEqual(3, user.id)
            self.assertIsNone(user.name)
            user.name = 'user3'
            
        # verify
        with self.mysql.dao.create_session() as session:
            user = session.get(User, 3)
            self.assertEqual('user3', user.name)
            
class LoadTest(DbTest):
    def test_found(self):
        with self.mysql.dao.create_session() as session:
            user = session.load(User, 1)
            self.assertEqual('user1', user.name)
            
    def test_not_found(self):
        with self.assertRaises(DbError):
            with self.mysql.dao.create_session() as session:
                session.load(User, 3)
            