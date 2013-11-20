from sqlalchemy import Column, Integer, String, create_engine
from sqlalchemy.orm import Session
from sqlalchemy.ext.declarative import declarative_base

Base = declarative_base()

class MyClass(Base):
    __tablename__ = 'mytable'
    id = Column(Integer, primary_key=True)

    @mapped_column(String)
    def _name(self, value):
        return "The name is: " + value

e = create_engine('sqlite://',echo=True)
Base.metadata.create_all(e)

s = Session(e)
s.add(MyClass(name="myname"))
s.commit()

print s.query(MyClass).first().name
