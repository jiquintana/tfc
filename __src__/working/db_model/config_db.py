#!/usr/bin/python
# -*- coding: utf-8 -*-
# vim: ts=4:sw=4:sts=4:ai:et:fileencoding=utf-8:number
import pprint
from sqlalchemy import Column, ForeignKey, Integer, String, Boolean, Table, or_, CHAR
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import relationship,  scoped_session, sessionmaker
from sqlalchemy import create_engine, MetaData, event

TraceSQL = False
MAXUSERS = 1024
MAXGROUPS = 65536

DRIVER = 'sqlite:///proxy.db'
#DRIVER = 'sqlite://'
engine = create_engine(DRIVER, echo=TraceSQL)
Base = declarative_base()
#Base.metadata.bind = engine
#metadata = MetaData()


@event.listens_for(engine, "connect")
def _fk_pragma_on_connect(dbapi_con, con_record):
    dbapi_con.execute('PRAGMA journal_mode=MEMORY')




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
        users_found = self.session.query(User).filter(User.uid==uid).first()
        return users_found

    def getAllUser(self):
        users_found = self.session.query(User).all()
        return users_found
    
    def getLowestUnusedUIDfromUser(self):        
        theUID=None
        uids_found = [r for (r, ) in self.session.query(User.uid).all()]
        for testUID in range(1,MAXUSERS+1):
            if (theUID == None) and  not (testUID in uids_found):
                theUID = testUID        
        return theUID
     
    def addUser(self,newUser):
        theUID = None
        theGID = -1
        transaction_succesful=False            
        
        
        # Obtenemos el UID libre mas bajo; el uid no supera el máximo de MAXUSERS usrs
        theUID = self.getLowestUnusedUIDfromUser()
        
        # Comprobamos que el grupo no exista, y si esta libre, creamos el UID y GID con el mismo valor:
        # Correspondencia 1:1 entre usuario y grupo cuando el UID<MAXUSERS
        if (theUID != None) and (self.findGroupByGID(theUID) == None):
            theGID = theUID
            
        testUSR = self.findUserByUsername(newUser.username)
        testGRP = self.findGroupByGroupname('dfl_grp_'+newUser.username)
        
        # Comprobamos si ya existe un usuario o grupo con igual clave primaria
        if (testUSR != None) or (testGRP != None):
            # Existe: forzamos NO ejecucion...
            theGID = -1
        
        # Si hemos encontrado un usuario libre y el grupo libre...
        # y ademas no existen las claves primarias de usuario.username y grupo.groupname...
        #  => (todo OK hasta el momento...)
        # en la inicializacion hemos forzado valores diferentes para evitar que esta comparacion sea
        # cierta por defecto
        if theUID == theGID:
            # Todos los valores recibidos en newUser, salvo el UID, son validos. Ahora alocamos el UID
            newUser.uid = theUID    
            
            newGroup = Group()         
            newGroup.gid=theGID
            newGroup.description='Grupo de '+newUser.description
            newGroup.groupname='dfl_grp_'+newUser.username
            
            relacionUsrGrp = Groups(newUser, newGroup)
            
            # Tenemos todo preparado... intentamos ejecutar la transaccion
            try:
                self.session.add(newUser)
                self.session.add(newGroup)
                self.session.add(relacionUsrGrp)
                self.session.commit()
                transaction_succesful=True
            except e:
                print(e)
                self.session.rollback()
                
        # Si todo ha ido bien (creacion del usuario, creacion del grupo y creacion de acl), devolvemos
        # un registro con el usuario creado
        # si ha ido mal, devolvemos None
        if transaction_succesful:
            storedUser = self.findUserByUID(theUID)
        else:
            storedUser = None
            
        return storedUser
    
    def setUserAdmin(self,requestedUser):
        if requestedUser != None:
            storedUser=self.findUserByUsername(requestedUser.username)
            if storedUser != None:
                theUser = self.session.query(User).filter(User.uid==storedUser.uid).update({'admin': True})
                self.session.commit()
            return self.findUserByUsername(requestedUser.username)
        else:
            return None
        
        
    def unsetUserAdmin(self,requestedUser):
        if requestedUser != None:
            storedUser=self.findUserByUsername(requestedUser.username)
            if storedUser != None:
                theUser = self.session.query(User).filter(User.uid==storedUser.uid).update({'admin': False})
                self.session.commit()
            return self.findUserByUsername(requestedUser.username)
        else:
            return None
    
    def changeUserPassword(self,requestedUser):
        if requestedUser != None:
            storedUser=self.findUserByUsername(requestedUser.username)
            if storedUser != None:
                theUser = self.session.query(User).filter(User.uid==storedUser.uid).update({'password': requestedUser.password})
                self.session.commit()
            return self.findUserByUsername(requestedUser.username)
        else:
            return None 
        
    def changeUserDescription(self,requestedUser):
        if requestedUser != None:
            storedUser=self.findUserByUsername(requestedUser.username)
            if storedUser != None:
                theUser = self.session.query(User).filter(User.uid==storedUser.uid).update({'description': requestedUser.description})
                self.session.commit()
            return self.findUserByUsername(requestedUser.username)
        else:
            return None 
        
        
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
        groups_found = self.session.query(Group).filter(Group.groupname==groupname).first()
        return groups_found                    


    def findGroupByGID(self, gid):
        groups_found = self.session.query(Group).filter(Group.gid==gid).first()
        return groups_found

    def getAllGroups(self):
        groups_found = self.session.query(Group).all()
        return groups_found
    
    def getLowestUnusedGIDfromGroup(self):
        theGID=None
        gids_found = [r for (r, ) in self.session.query(Group.gid).all()]
        for testGID in range(MAXUSERS+1,MAXGROUPS+1):
            if (theGID == None) and  not (testGID in gids_found):
                theGID = testGID
        return theGID
    
    def addGroup(self,newGroup):
        theGID = None
        transaction_succesful=False
        
        # Obtenemos el GID libre mas bajo... 
        theGID = self.getLowestUnusedGIDfromGroup()
        # e intentamos localizar un grupo con el mismo nombre
        testGRP = self.findGroupByGroupname(newGroup.groupname)
        
        # si el GID esta libre y no hemos encontrado un grupo con la misma clave primaria..
        if theGID != None and testGRP == None:
            # Todos los valores recibidos en newUser, salvo el UID, son validos. Ahora alocamos el UID
            newGroup.gid = theGID    
            try:
                self.session.add(newGroup)
                self.session.commit()
                transaction_succesful=True
            except:
                self.session.rollback()
                
        # Si todo ha ido bien (creacion del grupo), devolvemos
        # un registro con el grupo creado, M, X, J, V, S, D 
        # si ha ido mal, devolvemos None
        if transaction_succesful:
            storedGroup = self.findGroupByGID(theGID)
        else:
            storedGroup = None
            
        return storedGroup
   
    def changeGroupDescription(self,requestedGroup):
        if requestedGroup != None:
            storedGroup=self.findGroupByGroupname(requestedGroup.groupname)
            if storedGroup != None:
                theGroup = self.session.query(Group).filter(Group.gid==storedGroup.gid).update({'description': requestedGroup.description})
                self.session.commit()
            return self.findGroupByGroupname(requestedGroup.groupname)
        else:
            return None             
    

class Groups(Base):
    __tablename__ = '_GROUPS'
    uid=Column(Integer, ForeignKey('USER.uid'), nullable=False, primary_key=True, index=True)
    gid=Column(Integer, ForeignKey('GROUP.gid'), nullable=False, primary_key=True, index=True)
    usuario = relationship("User", backref="_GROUPS")
    grupo = relationship("Group", backref="_GROUPS")
    
    def __init__(self, user, group):
        self.uid=user.uid
        self.gid=group.gid
        
    def __repr__(self):
        return "Groups(%r,%r)" % (self.uid,self.gid)

    def __eq__(self, other):
        print(". %r" % self.__repr__())
        print(". %r" % other.__repr__())
        return self.__dict__ == other.__dict__    

    def pertenece(self, user):
        if user.uid == self.uid:
            return True
        else:
            return False
    
    def contiene(self, group):
        if group.gid == self.gid:
            return True
        else:
            return False
        
    def __repr__(self):
        return "Groups(%r,%r)" % (self.gid,self.uid)



    
class User(Base):
    __tablename__ = 'USER'
    uid = Column(Integer, primary_key=True, autoincrement=True, unique=True, index=True)
    username = Column(String(20), nullable=False, unique=True, index=True)
    admin = Column(Boolean, unique=False, default=False)
    password= Column(String(16), nullable=False)
    description = Column(String(80), nullable=False)
    hours = Column(CHAR(24), default=(chr(0x00)*24))
    usuarios = relationship("Groups", backref="USER")
    
    
    def __repr__(self):
        return "User(%r,%r,%r,%r,%r, %r)" % (self.uid,self.username,self.admin,self.password,self.description,
                                             ':'.join(x.encode('hex') for x in self.hours))


class Group(Base):
    __tablename__ = 'GROUP'
    #__table_args__ = ({'autoload':True},)
    gid = Column(Integer, primary_key=True, autoincrement=True, unique=True, index=True)
    groupname = Column(String(20), nullable=False, unique=True, index=True)
    description = Column(String(80), nullable=False)    
    grupos = relationship("Groups", backref="GROUP")
    
    def __repr__(self):
        return "Group(%r,%r,%r)" % (self.gid, self.groupname, self.description)
    
if __name__ == "__main__":
    
    db=Database()
    ed_user = User(username='ed', password='Ed Jones', description='ed')
    
    try:
        db.session.add(ed_user)
        db.session.commit()
    except:
        db.session.rollback()
        
    storedUser=db.findUserByUsername('ed')
    print(db.setUserAdmin(storedUser))
    print(db.unsetUserAdmin(storedUser))
    storedUser=db.findUserByUsername('ed')
    storedUser.password='patata'
    print(db.changeUserPassword(storedUser))
    storedUser.description='cambio de descripcion'
    print(db.changeUserDescription(storedUser))

    newGroup = Group(groupname='nuevo_grupo', description='nuevo grupo de prueba')
    print(db.addGroup(newGroup))
    newGroup.description='otra descripcion'
    print(db.changeGroupDescription(newGroup))
    
    '''
    mytestGroup=Group(groupname='josi', description='Josi User ')
    storedGRP=db.addGroup(mytestGroup)
    print(mytestGroup)
    print(storedGRP)
    '''
    '''
    for idx in range(4096): # esto va desde 0..MAXUSERS, debiendo fallar en el numero MAXUSERS
        mytestUsr=User(username='josi'+str(idx), password='password', description='Josi User '+str(idx))
        result=db.addUser(mytestUsr)
        print(result)
        
        if result != None:
            print("success idx "+str(idx))                print("aborted")

            print(mytestUsr)
            print(result)
    '''    
    '''
    for instance in db.findUser("ep"):
        print("....%r" % inUSERstance)
    
    for instance in db.findGroup("%e"):
        print("....%r" % instance)
    print("----")
    for instance in db.getAllUser():
        print("....%r" % instance)
    print("----")        USER
    for instance in db.getAllGroups():
        print("....%r" % instance)
    print("----")        
    '''
    
    '''
        for instance in db.findUser(u"ñ"):
        print("....%r" % instance)
    
    for instance in db.findGroup("b"):
        print("....%r" % instance)
        
    print("-----")
    print(db.findUserByUID(1))
    print(db.findUserByUsername('ed'))
    print("-----")
    print(db.findGroupByGID(8))
    print("-----")
    print(db.findGroupByGroupname('e'))
    print(db.getLowestUnusedUIDfromUsers())
    otherUser = User(username='josi3', password='password', description='Josi User')
    result=db.addUser(otherUser)
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
    #(Groups(1,3), INSERT INTO "GROUP" VALUES(33,'e','e');User(1,'ed','Ed Jones','edspassword'), Group(3,'b','b','b'))
    
    '''