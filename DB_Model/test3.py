from sqlalchemy import *

Base = declarative_base()

class Users(Base):
    __tablename__ = 'USERS'
    uid = Column(Integer, primary_key=True)
    name = Column(String(20), nullable=False),
    password_hash = Column(String(80)),
    description = Column(String(80)),


    @mapped_column(String)
    def _name(self, value):
        return "The name is: " + value

e = create_engine('sqlite://',echo=True)
Base.metadata.create_all(e)

s = Session(e)
s.add(MyClass(name="proxy.db"))
s.commit()

print s.query(Users).first().name