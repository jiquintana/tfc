#!/bin/python
from sqlalchemy import *
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import relation, sessionmaker, relationship
 
Base = declarative_base()
 
class Users(Base):
    __tablename__ = 'USERS'
    uid = Column(Integer, primary_key=True, autoincrement=True, unique=True)
    name = Column(String(20), nullable=False)
    password_hash = Column(String(16), nullable=False)
    description = Column(String(80), nullable=False)
    
    def __init__(self, name=None):
        self.name = name
 
    def __repr__(self):
        return "User(%r)" % (self.name)

class Groups(Base):
    __tablename__ = 'GROUPS'
    gid = Column(Integer, primary_key=True, autoincrement=True, unique=True)
    name = Column(String(80), nullable=False)
    
    def __init__(self, name=None):
        self.name = name
 
    def __repr__(self):
        return "Groups(%r)" % (self.name)


class rules_time(Base):
    __tablename__ = 'RULES_TIME'
    rtid = Column(Integer, primary_key=True, autoincrement=True, unique=True)
    
    
    def __init__(self, name=None):
        self.name = name
        
    def __repr__(self):
        return "RuleTime(%r)" % (self.rtid)
    
    
class rules_uris(Base):
    __tablename__ = 'RULES_URIS'
    
    ruid = Column(Integer, primary_key=True, autoincrement=True, unique=True, name='ruid')
    name = Column(String(256))
    
    
    def __init__(self, name=None):
        self.name = name
 
    def __repr__(self):
        return "RuleURI(%r)" % (self.ruid)    

class rules_words(Base):
    __tablename__ = 'RULES_WORDS'
    rwid = Column(Integer, primary_key=True, autoincrement=True, unique=True)
    words = Column(String(256), nullable=False)
    
    def __init__(self, name=None):
        self.name = name
 
    def __repr__(self):
        return "RuleURI(%r)" % (self.ruid)    

class _map_group2time(Base):
    __tablename__ = '_M_G2T'
#    __table_args__ = (
#        ForeignKeyConstraint(['gid', 'rtid'],['GROUPS.gid','RULES_TIME.rtid'])
#        )
   
   http://docs.sqlalchemy.org/en/rel_0_8/core/constraints.html
    #gid = ForeignKeyConstraint(columns, refcolumns)
    fk=ForeignKeyConstraint(['gid', 'rtid'],['GROUPS.gid','RULES_TIME.rtid'])
    #id = Column(Integer,primary_key=True, autoincrement=True, unique=True)
    #id=Column(Integer, primary_key=True, ForeignKeyConstraint(['gid', 'rtid'],['GROUPS.gid','RULES_TIME.rtid']))
    gid = Column(Integer, ForeignKey('GROUPS.gid', name='allowed_time'), nullable=False, primary_key=True)
    rtid = Column(Integer, ForeignKey('RULES_TIME.rtid', name='time_allowed'), nullable=False, primary_key=True)
    gid = Column(Integer, relationship("Groups"))
    
    #@words = Column(String(256), nullable=False)
    
    def __init__(self, name=None):
        self.name = name
 
    def __repr__(self):
        return "RuleURI(%r)" % (self.ruid)    

 
engine = create_engine('sqlite:///pepe.db', echo=True)
Base.metadata.create_all(engine)
