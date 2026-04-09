from sqlalchemy import Column, Integer, String,Enum
from app.core.database import Base
import enum



class Role(enum.Enum):
    SUPER_ADMIN = "super_admin"
    FRANCHISE="franchise"

class User(Base):
    __tablename__ = "users"

    id = Column(Integer, primary_key=True, index=True)
    email = Column(String, unique=True, index=True)
    password = Column(String)
    role = Column(Enum(Role), default=Role.SUPER_ADMIN)

