# -*- coding: utf-8 -*-
from decorated.base.dict import Dict
from sqlalchemy.ext import declarative
from sqlalchemy.ext.declarative import DeclarativeMeta
import doctest
import inflection

class ModelBase(object):
    @classmethod
    def repr(cls, *keys):
        keys = [str(k) for k in keys]
        return '<%s %s>' % (cls.__name__, ', '.join(keys))

    def __repr__(self):
        return type(self).repr(*self.keys())
    
    def __json__(self):
        return self.fields()
    
    def fields(self):
        fields = Dict()
        for column in self.__table__.columns:
            fields[column.name] = getattr(self, column.name)
        return fields
    
    def keys(self):
        columns = self.__table__.primary_key.columns
        return tuple([getattr(self, c.name) for c in columns])
    
    def update(self, fields):
        for column in self.__table__.columns:
            if column.name in fields:
                setattr(self, column.name, fields[column.name])
                
class AutoTableNameType(DeclarativeMeta):
    def __init__(cls, classname, bases, dict_): #@NoSelf
        cls.__tablename__ = inflection.underscore(classname)
        DeclarativeMeta.__init__(cls, classname, bases, dict_)
        
def create_model_base(**options):
    options.setdefault('cls', ModelBase)
    options.setdefault('metaclass', AutoTableNameType)
    return declarative.declarative_base(**options)

Model = create_model_base()

if __name__ == '__main__':
    doctest.testmod()
    