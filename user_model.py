from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy import create_engine
from sqlalchemy import Column, Integer, String

Base = declarative_base()

class User(Base):
    __tablename__ = 'users'

    id = Column(Integer, primary_key=True)
    name = Column(String)

    def __repr__(self):
        return "<User(id={0:d} name='{1:s}')>".format(self.id,self.name)

if __name__=="__main__":
    engine = create_engine('sqlite:///test.db', echo=True)
    Base.metadata.create_all(engine)
