from sqlalchemy import create_engine
from sqlalchemy import Column, Integer, String
from sqlalchemy.orm import sessionmaker
from user_model import User

class DbUserRepository:
    def __init__(self,path):
        engine = create_engine(path)
        Session = sessionmaker(bind=engine)
        self.session = Session()

    def create(self,data):
        user = User(name=data["name"])
        self.session.add(user)
        self.session.commit()
        return user.id

    def get(self,user_id):
        user = self.session.query(User).get(user_id)
        return {"name":user.name}

    def set(self,user_id,data):
        user = self.session.query(User).get(user_id)
        user.name = data["name"]
        self.session.commit()
