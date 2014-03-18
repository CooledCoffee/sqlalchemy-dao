Introduction
============

SQLAlchemy is very powerful and flexible.
But some convenience is sacrificed to achieve that.
With sqlalchemy-dao, we are trying to achieve 80% functionality of sqlalchemy with 20% of complexity.

Installation
============

pip install sqlalchemy-dao

or

easy_install sqlalchemy-dao

Model
=====

A model is defined something like this using sqlalchemy:

	from sqlalchemy import Column, Integer, String
	from sqlalchemy.ext.declarative import declarative_base
	
	Base = declarative_base()
	
	class User(Base):
		__tablename__ = 'user'
		id = Column(Integer, primary_key=True)
		name = Column(String)
		
Most of the time, the \_\_tablename\_\_ is a direct mapping of the class name.
With sqlalchemy-dao, you can achieve the same thing like this:

	from sqlalchemy import Column, Integer, String
	from sqlalchemy_dao import Model
	
	class User(Model):
		id = Column(Integer, primary_key=True)
		name = Column(String)
		
Similarly, a UserSetting class will be mapped to a user_setting table.
The algorithm simply maps a camel-style class name to a underscore-style table name.

This saves you two lines of code. It may not seem a lot, but it is a beginning.
The base class Model comes with some other methods:

	user = User(id=1, name='user1')
	user.timestamp = 123
	
	# the non-field timestamp is ignored
	assert user.fields() == {'id': 1, 'name': 'user1'}
	
	# this returns a tuple containing all key values in the order they are defined
	assert user.keys() == (1, )
	
	# this updates fields from a dict, ignoring non-field values.
	# it can be convenient when you are receiving the dict from a browser request that is messed up by extra fields.
	user.update({'id': 1, 'name': 'user2', 'timestamp': 123})
	assert user.name == 'user2'
	assert not hasattr(user, 'timestamp')

Session
=======

The standard way of using a sqlalchemy session is:

	from sqlalchemy import create_engine
	from sqlalchemy.orm import sessionmaker
	
	engine = create_engine('mysql://test:test@localhost/test')
	Session = sessionmaker(bind=engine)
	session = Session
	try:
		user = session.query(User).get(1)
		user.name = 'user2'
		session.commit()
	except:
		session.rollback()
		raise
	finally:
		session.close()
	
This looks alien to me. A more intuitive way (using sqlalchemy-dao) is:

	from sqlalchemy_dao import Dao
	
	dao = Dao('mysql://test:test@localhost/test')
	with dao.create_session() as session:
		user = session.query(User).get(1)
		user.name = 'user2'
	
The returned session from sqlalchemy-dao implements the context manager protocol.
So you don't have to worry about committing & closing.

Here is a little more demonstration of sqlalchemy_dao.Session:

	# instead of writing session.query(User).get(1), we can write
	user = session.get(User, 1)
	
	# this will raise an error in case the row does not exist
	user = session.load(User, 2)
	
	# returns user 2 if it exists,
	# otherwise creates a new model with id=2 and add it to the session
	user_may_or_may_not_exist = session.get_or_create(User, 2)
	user_may_or_may_not_exist.name = 'user2'
	
	# execute a sql and returns the only field
	user_name = session.execute_scalar("select name from user where id=1")

Session Context
===============

Sometimes you have a very deep call stack, you create a session at the bottom of the stack,
and then you will have to pass it all the way to the top of the call stack.
This is common in web applications when you are trying to achieve the one-transaction-per-request pattern.
sqlalchemy-dao provides a solution for this:

	from decorated.base.context import ctx
	from sqlalchemy_dao import Dao
	
	dao = Dao('mysql://test:test@localhost/test')
	
	def root():
		with dao.SessionContext():
			foo()
		
	def foo():
		bar()
		
	def bar():
		user = ctx.session.get(User, 1)
		
The SessionContext method creates a session and store it in a context.
You can achieve the session using ctx.session.
SessionContext is based on the context mechanism from <a href="https://www.github.com/CooledCoffee/decorated/" target="_blank">decorated</a>.
It is implemented using thread local thus is thread safe.

Lock
====

sqlalchemy-dao provides a simple distributed lock using mysql.

	lock = dao.Lock('lock1')
	
	def foo():
		with lock:
			pass
			
	def bar():
		with lock:
			pass
			
Or even better:

	from decorated import synchronized
	
	lock = dao.Lock('lock1')
	
	@synchronized(lock)
	def foo():
		pass
		
	@synchronized(lock)
	def bar():
		pass
		
Now the code guarded by the lock is thread safe. Note that the lock mechanism is based on mysql.
It is not likely to work on other databases.

Author
======

Mengchen LEE: <a href="https://plus.google.com/117704742936410336204" target="_blank">Google Plus</a>, <a href="https://cn.linkedin.com/pub/mengchen-lee/30/8/23a" target="_blank">LinkedIn</a>
