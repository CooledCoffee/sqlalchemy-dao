# -*- coding: utf-8 -*-
from sqlalchemy.orm.session import Session
from sqlalchemy_dao.errors import DbError

class Session(Session):
    def __enter__(self):
        return self
    
    def __exit__(self, error_type, error_value, traceback):
        if error_value is None:
            self.commit()
        else:
            self.rollback()
        self.close()
        
    def execute_for_all(self, sql):
        return self.execute(sql).fetchall()
    
    def execute_for_first(self, sql):
        return self.execute(sql).first()
    
    def execute_for_one(self, sql):
        row = self.execute_for_first(sql)
        if row is None:
            raise DbError("No row returned.")
        return row
        
    def execute_for_scalar(self, sql):
        rows = self.execute_for_all(sql)
        if len(rows) == 1:
            return rows[0][0]
        else:
            raise DbError('Expecting 1 row, %d rows returned.' % len(rows))
        
    def get(self, model_class, *keys):
        if len(keys) == 1:
            keys = keys[0]
        return self.query(model_class).get(keys)
    
    def get_or_create(self, model_class, *keys):
        model = self.get(model_class, keys)
        if not model:
            model = model_class()
            for column, key in zip(model.__table__.primary_key.columns, keys):
                setattr(model, column.name, key)
            self.add(model)
        return model
    
    def load(self, model_class, *keys):
        model = self.get(model_class, *keys)
        if model:
            return model
        else:
            raise DbError('%s not found.' % model_class.repr(*keys))
        