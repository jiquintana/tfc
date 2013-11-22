#!/bin/python
# -*- coding: utf-8 -*-
# vim: ts=4:sw=4:sts=4:ai:et:fileencoding=utf-8:number

from sqlalchemy import *
from sqlalchemy.ext.declarative import declarative_base, declared_attr, DeferredReflection
from sqlalchemy.orm import relation, sessionmaker, relationship,scoped_session, sessionmaker

Base = declarative_base()
groups = Table(
    'groups', Base.metadata,
    Column('uid', Integer, ForeignKey('USER.uid'), nullable=False, primary_key=True, index=True),
    Column('gid', Integer, ForeignKey('GROUP.gid'), nullable=False, primary_key=True, index=True),
    relationship("USER", backref="groups"),
    relationship("GROUPS", backref="groups")
)

class User(Base):
    __tablename__ = 'USER'
    uid = Column(Integer, Sequence('user_id_seq'), primary_key=True, autoincrement=True, unique=True, index=True)
    name = Column(String(20), nullable=False, unique=True, index=True)
    password_hash = Column(String(16), nullable=False)
    description = Column(String(80), nullable=False)

    def __repr__(self):
        return "User(%r,%r,%r,%r)" % (self.uid,self.name,self.password_hash,self.description)

class Group(Base):
    __tablename__ = 'GROUP'
    gid = Column(Integer, Sequence('group_id_seq'), primary_key=True, autoincrement=True, unique=True, index=True)
    name = Column(String(80), nullable=False)

    def __repr__(self):
        return "Group(%r,%r)" % (self.gid,self.name)

engine = create_engine('sqlite:///pepe.db', echo=True)
Base.metadata.create_all(engine) 

thisUser=User(name='b', password_hash='xxx', description='usuario de prueba')
print(thisUser.__repr__())

Session = sessionmaker()
Session.configure(bind=engine)

session = Session()
session.add(thisUser)
session.commit()

written_user= session.query(User).filter_by(name='pepe').first()

print(written_user.__repr__())
