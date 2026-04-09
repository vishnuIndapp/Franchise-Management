from sqlalchemy import Column, Integer, String
from app.core.database import Base

class Franchise(Base):
    __tablename__ = "franchises"

    id = Column(Integer, primary_key=True, index=True)
    name = Column(String)
    email= Column(String, unique=True)
    phone= Column(String, unique=True)
    address= Column(String)
    franchise_code= Column(String, unique=True)