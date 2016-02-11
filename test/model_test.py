# -*- coding: utf-8 -*-
from testutil import User, UserSetting
from unittest.case import TestCase

class TableNameTest(TestCase):
    def test(self):
        self.assertEqual('user', User.__tablename__)  # @UndefinedVariable
        self.assertEqual('user_setting', UserSetting.__tablename__)  # @UndefinedVariable
    
class FieldsTest(TestCase):
    def test_normal(self):
        user = User(id=1, name='user1')
        d = user.fields()
        self.assertEquals(2, len(d))
        self.assertEquals(1, d['id'])
        self.assertEquals('user1', d['name'])
        
    def test_extra_fields(self):
        user = User(id=1, name='user1')
        user.extra = 'extra data'
        self.assertEqual('extra data', user.extra)
        d = user.fields()
        self.assertEquals(2, len(d))
        self.assertEquals(1, d['id'])
        self.assertEquals('user1', d['name'])
        self.assertNotIn('extra', d)
        
class KeysTest(TestCase):
    def test_single(self):
        user = User(id=1, name='user1')
        keys = user.keys()
        self.assertEquals((1, ), keys)
        
    def test_multi(self):
        user = UserSetting(id=1, key='email', value='user1@test.com')
        keys = user.keys()
        self.assertEquals((1, 'email'), keys)
        
class ReprTest(TestCase):
    def test_class(self):
        result = User.repr(1)  # @UndefinedVariable
        self.assertEquals('<User 1>', result)
        
    def test_instance(self):
        user = User(id=1, name='user1')
        result = repr(user)
        self.assertEquals('<User 1>', result)
        
    def test_multi_keys(self):
        setting = UserSetting(id=1, key='email')
        result = repr(setting)
        self.assertEqual('<UserSetting 1, email>', result)
    
class JsonTest(TestCase):
    def test(self):
        user = User(id=1, name='user1')
        result = user.__json__()
        self.assertEqual(2, len(result))
        self.assertEquals(1, result['id'])
        self.assertEquals('user1', result['name'])
        
class UpdateTest(TestCase):
    def test_normal(self):
        user = User(id=1, name='user1')
        user.update({'id': 1, 'name': 'user2'})
        self.assertEquals(1, user.id)
        self.assertEquals('user2', user.name)
        
    def test_extra_fields(self):
        user = User(id=1, name='user1')
        user.update({'name': 'user2', 'extra': 'extra field'})
        self.assertFalse(hasattr(user, 'extra'))
        
class CmpTest(TestCase):
    def test_basic(self):
        self.assertEqual(1, cmp(User(id=2), User(id=1)))
        self.assertEqual(0, cmp(User(id=1), User(id=1)))
        self.assertEqual(-1, cmp(User(id=1), User(id=2)))
        
    def test_not_model(self):
        self.assertEqual(1, cmp(User(id=1), 'a'))
        self.assertEqual(1, cmp(User(id=1), None))
        