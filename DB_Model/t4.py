from sqlalchemy import *
from sqlalchemy.orm import *

#accessing a database
db = create_engine('sqlite:///blah.db')

#metadata object used for binding
metadata = MetaData(db)

# creating a table
users_table = Table('USERS', metadata,
    Column('uid', Integer, primary_key=True),
    Column('name', String(40))
    )

#metadata.engine.echo = True
#try:
users_table.create()
#except e:
#    pass
#    print 'TABLE \'users\' already exists.'

# loading definitions automatically
users_table = Table('users', metadata, autoload=True)

# printing a column
print list(users_table.columns)[0].name

#create a holding class
class User(object):
    def __repr__(self):
        return '%s(%r,%r)' % (
            self.__class__.__name__,self.user_name,self.user_id)

    def wager(self):
                return 'betting on it'

# map the holding class to the table definition
mapper(User, users_table)

#create an instance of the class
u1 = User()

#see, it automatically maps class and fields.  Slick.
print u1.uid
print u1.wager()