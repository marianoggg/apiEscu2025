from configs.db import engine, Base
from sqlalchemy import Column, Integer, String, DateTime, ForeignKey
from sqlalchemy.orm import sessionmaker, relationship
from pydantic import BaseModel
import datetime

# region Modelos SQLAlchemy
class User(Base):
    __tablename__ = "user"
    id = Column(Integer, primary_key =True)
    username = Column( String(50), nullable=False, unique=True)
    password = Column(String(40))
    id_userdetail = Column(Integer, ForeignKey("userdetail.id"))
    userdetail = relationship("UserDetail", uselist=False)
    payments= relationship("Payment", uselist=True, back_populates="user")
    pivoteusercareer = relationship("PivoteUserCareer", back_populates="user")

    def __init__(self, username, password):
        self.username = username
        self.password = password

class UserDetail(Base):
    __tablename__="userdetail"
    id = Column(Integer, primary_key =True)
    first_name = Column(String(50))
    last_name = Column(String(50))
    dni = Column(Integer)
    type = Column(String(50))
    email = Column(String(50), nullable=False, unique=True)

    def __init__(self, first_name, last_name, dni, type, email):
        self.first_name = first_name
        self.last_name = last_name
        self.dni = dni
        self.type = type
        self.email = email

class Career(Base):
    __tablename__="career"
    id = Column(Integer, primary_key=True)
    name = Column(String(50))

    def __init__(self, name):
        self.name= name

class Payment(Base):
    __tablename__="payment"
    id = Column(Integer, primary_key=True)
    id_career=Column(Integer, ForeignKey("career.id"))
    id_user=Column(Integer, ForeignKey("user.id"))
    amount = Column(Integer)
    affected_month = Column(DateTime)
    created_at = Column(DateTime, default=datetime.datetime.now())
    user = relationship("User", uselist=False, back_populates="payments")
    career = relationship("Career", uselist=False)

    def __init__(self, a, b, c, d):
        self.id_career = a
        self.id_user = b
        self.amount = c
        self.affected_month = d

class PivoteUserCareer(Base):
    __tablename__="pivote_user_career"
    id = Column(Integer, primary_key=True)
    id_career = Column(ForeignKey("career.id"))
    id_user = Column(ForeignKey("user.id"))
    career = relationship("Career", uselist=False)
    user = relationship("User", uselist=False, back_populates="pivoteusercareer")

    def __init__(self, id_user, id_career):
        self.id_user = id_user
        self.id_career = id_career
# endregion

# region Pydantic Models
class InputUser(BaseModel):
    username:str
    password:str
    firstname:str
    lastname:str
    dni:int
    type:str
    email:str

class InputLogin(BaseModel):
    username:str
    password:str

class InputUserDetail(BaseModel):
    first_name:str
    last_name:str
    dni:int
    type:str
    email:str

class InputCareer(BaseModel):
    name: str

class InputPayment(BaseModel):
    id_career: int
    id_user: int
    amount: int
    affected_month: datetime.date

class InputUserAddCareer(BaseModel):
    id_user: int
    id_career: int
# endregion

# region configuraciones 
Base.metadata.create_all(bind=engine)

Session = sessionmaker(bind=engine)

session = Session()
# endregion