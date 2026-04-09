from sqlalchemy.orm import Session
from app.models.user import User
from app.core.security import hash_password
from app.models.franchise import Franchise



def get_user_profile(db: Session, user: User):
    franchise = db.query(Franchise).filter(Franchise.email == user.email).first()

    return {
        "id": user.id,
        "email": user.email,
        "role": user.role.value,
        "name": franchise.name if franchise else None,
        "phone": franchise.phone if franchise else None,
        "address": franchise.address if franchise else None,
        "franchise_code": franchise.franchise_code if franchise else None
    }


def update_user_profile(db: Session, user: User, data):

    if data.password:
        user.password = hash_password(data.password)

    franchise= db.query(Franchise).filter(Franchise.email == user.email).first()
    if franchise:
        if data.name:
            franchise.name = data.name
        if data.phone:
            franchise.phone = data.phone
        if data.address:
            franchise.address = data.address
    
    db.commit()
    return {
        "id": user.id,
        "email": user.email,
        "role": user.role.value,
        "name": franchise.name if franchise else None,
        "phone": franchise.phone if franchise else None,
        "address": franchise.address if franchise else None,
    }