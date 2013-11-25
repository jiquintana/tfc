#!/usr/bin/python
# -*- coding: utf-8 -*-
# vim: ts=4:sw=4:sts=4:ai:et:fileencoding=utf-8:number
import pprint
from sqlalchemy import Column, ForeignKey, Integer, String, Table, or_
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import relationship,  scoped_session, sessionmaker
from sqlalchemy import create_engine, MetaData


TraceSQL=True

DRIVER = 'sqlite:///proxy.db'
engine = create_engine(DRIVER, echo=TraceSQL)
Base = declarative_base()
#Base.metadata.bind = engine

#metadata = MetaData()

class Singleton(object):
    __instance = None
    def __new__(cls):
        if Singleton.__instance is None:
            Singleton.__instance = object.__new__(cls)
        return Singleton.__instance    

class Database(Singleton):
    __initialized__ = False
    __engine__ = None
    __DBSession__ = None
    __BASE__ = None
    session = None
    def __init__(self):
        if not self.__initialized__:
            print("not initialized")
            self.__initialized__ = True
            self.__engine__ = engine
            self.__metadata__ = MetaData()
            self.__BASE__=Base
            self.__BASE__.metadata.bind=self.__engine__
            self.__BASE__.metadata.create_all(self.__engine__)
            
            #self.__BASE__.metadata.bind =self.__engine__
            
            self.__DBSession__ = scoped_session(sessionmaker())
            self.__DBSession__.configure(bind=self.__engine__)       
            self.session = self.__DBSession__()
            #self.__BASE__.__metadata__.create_all(self.__engine__)            
            
        else:
            print("already initialized")
 
    def findUser(self, str2find):
        users_found = self.session.query(User).filter(
            or_( User.username==str2find, User.description==str2find )
            ).all()
        if users_found == []:
            users_found = self.session.query(User).filter(
                or_( User.username.ilike("%"+str2find+"%"), User.description.ilike("%"+str2find+"%") )
                ).all()
        return users_found

    def findUserByUsername(self, username):
        users_found = self.session.query(User).filter(User.username==username).first()
        return users_found

    def findUserByUID(self, uid):
        users_found = self.session.query(User).filter(User.uid==uid)
        return users_found

    def addUser(self, User):
        self.findUser
        return users_found


    def getAllUser(self):
        users_found = self.session.query(User).all()
        return users_found

    def findGroup(self, str2find):
        groups_found = self.session.query(Group).filter(
            or_( Group.groupname==str2find, Group.description==str2find )
            ).all()
        if groups_found == []:
            groups_found = self.session.query(Group).filter(
                or_( Group.groupname.ilike("%"+str2find+"%"), Group.description.ilike("%"+str2find+"%") )
                ).all()     
        return groups_found
    
    def findGroupByGroupname(self, groupname):
        groups_found = self.session.query(Group).filter(Group.groupname==str2find).first()
        return groups_found    

    def findGroupByGID(self, gid):
        groups_found = self.session.query(Group).filter(Group.gid==gid)
        return users_found

    def getAllGroups(self):
        groups_found = self.session.query(Group).all()
        return groups_found

class Groups(Base):
    __tablename__ = '_GROUPS'
    uid=Column(Integer, ForeignKey('USER.uid'), nullable=False, primary_key=True, index=True)
    gid=Column(Integer, ForeignKey('GROUP.gid'), nullable=False, primary_key=True, index=True)
    usuario = relationship("User", backref="_GROUPS")
    grupo = relationship("Group", backref="_GROUPS")
    
    def __init__(self,user, group):
        self.uid=user.uid
        self.gid=group.gid
        
    def __repr__(self):
        return "Groups(%r,%r)" % (self.uid,self.gid)
    
    def pertenece(self, User):
        if User.uid == self.uid:
            return True
        else:
            return False
    
    def contiene(self, Group):
        if User.gid == self.gid:
            return True
        else:
            return False
    
class User(Base):
    __tablename__ = 'USER'
    uid = Column(Integer, primary_key=True, autoincrement=True, unique=True, index=True)
    username = Column(String(20), nullable=False, unique=True, index=True)
    password= Column(String(16), nullable=False)
    description = Column(String(80), nullable=False)
    usuarios = relationship("Groups", backref="USER")
    def __repr__(self):
        return "User(%r,%r,%r,%r)" % (self.uid,self.username,self.password,self.description)


class Group(Base):
    __tablename__ = 'GROUP'
    #__table_args__ = ({'autoload':True},)
    gid = Column(Integer, primary_key=True, autoincrement=True, unique=True, index=True)
    groupname = Column(String(20), nullable=False, unique=True, index=True)
    description = Column(String(80), nullable=False)    
    grupos = relationship("Groups", backref="GROUP")
    
    def __repr__(self):
        return "Group(%r,%r,%r,%r)" % (self.gid, self.groupname, self.groupname, self.description)

    
if __name__ == "__main__":
    
    db=Database()
    
    for instance in db.findUser(u"ñ"):
        print("....%r" % instance)
    
    for instance in db.findGroup("b"):
        print("....%r" % instance)
        
    print("-----")
    print(db.findUserByUID(1))
    print(db.findUserByUsername('ed'))    
    '''
    for instance in db.findUser("ep"):
        print("....%r" % instance)
    
    for instance in db.findGroup("%e"):
        print("....%r" % instance)
    print("----")
    for instance in db.getAllUser():
        print("....%r" % instance)
    print("----")        
    for instance in db.getAllGroups():
        print("....%r" % instance)
    print("----")        
    '''
    
'''    
    db2=Database()
    print (User.__table__)

    print(db)
    print(db2)

    print(db.session.query(User).count())
    for instance in db.session.query(User):
        print(instance)
        
        
        
    ed_user = User(username='ed', password='Ed Jones', description='edspassword')
    ed_group = Group(groupname='ed', description='ed group')
    
    try:
        db.session.add(ed_user)
        db.session.commit()
    except:
        db.session.rollback()
    
    try:
        db.session.add(ed_group)
        db.session.commit()
    except:
        db.session.rollback()
    print('.---------------------')
    find_user = db.session.query(User).filter(User.username==ed_user.username).first()
    print (find_user)
    find_group = db.session.query(Group).filter(Group.groupname==ed_group.groupname).first()    
    #filter(Address.person == person).all()
    print('.---------------------')
    print(find_user)
    print(find_group)
    membership=Groups(find_user,find_group)
    print('X---------------------')
    print(membership)
    print('X---------------------')
    
    try:
        db.session.add(membership)
        db.session.commit()
    except:
        db.session.rollback()
    
    #for instance in db.session.query(User).order_by(User.uid):
    #    print("%r %r" % (instance.name, instance.fullname))
        
    

    print(db.session.query(User).order_by(User.uid))
    
    for instance in db2.session.query(User).join(Groups, User.uid==Groups.uid):
    #for instance in db2.session.query(User).all():
        print(instance)
    
    for instance in db.session.query(Groups).join(User).outerjoin(Group).add_entity(User).add_entity(Group):
        print(instance)
    #(Groups(1,1), User(1,'ed','Ed Jones','edspassword'), Group(1,'ed','ed','ed group'))
    #(Groups(1,3), User(1,'ed','Ed Jones','edspassword'), Group(3,'b','b','b'))
    
'''