from sqlalchemy.orm import Session
from app.models.franchise import Franchise
from app.models.user import User, Role
from app.core.security import hash_password
from fastapi import HTTPException
from app.utils.redis import r
import json
from app.core.config import settings


CACHE_EXPIRY = settings.CACHE_EXPIRY



def create_franchise_user(db: Session,data):


    existing_user = db.query(User).filter(User.email == data.email).first()
    if existing_user:
        raise HTTPException(status_code=400, detail="Email already registered")
    existing_phone = db.query(Franchise).filter(Franchise.phone == data.phone).first()
    if existing_phone:
        raise HTTPException(status_code=400, detail="Phone already exists")
    existing_code = db.query(Franchise).filter(Franchise.franchise_code == data.franchise_code).first()
    if existing_code:
        raise HTTPException(status_code=400, detail="Franchise code already exists")

    user=User(
        email=data.email,
        password=hash_password(data.password),
        role=Role.FRANCHISE
    )
    db.add(user)
    db.flush()  

    franchise=Franchise(
        name=data.name,
        email=data.email,
        phone=data.phone,
        address=data.address,
        franchise_code=data.franchise_code
    )
    db.add(franchise)
    db.commit()
    db.refresh(franchise)
    return franchise



def get_franchises(db: Session,search: str,page: int, limit: int):

    cache_key = f"franchise:{search}:{page}:{limit}"

    cached_data = r.get(cache_key)
    if cached_data:
        return json.loads(cached_data)
    

    query = db.query(Franchise)
    if search:
        query=query.filter(
            (Franchise.name.ilike(f"%{search}%")) |
            (Franchise.email.ilike(f"%{search}%")) |
            (Franchise.phone.ilike(f"%{search}%")) |
            (Franchise.franchise_code.ilike(f"%{search}%"))
        )
    total = query.count()
    data = query.offset((page-1)*limit).limit(limit).all()
    result = {
        "total": total,
        "data": [
            {
                "id": f.id,
                "name": f.name,
                "email": f.email,
                "phone": f.phone,
                "address": f.address,
                "franchise_code": f.franchise_code
            }
            for f in data
        ]
    }
    r.setex(cache_key, CACHE_EXPIRY, json.dumps(result))


    return result



def get_franchise_by_id(db: Session, franchise_id: int):
    return db.query(Franchise).filter(Franchise.id == franchise_id).first()


def update_franchise(db: Session, franchise_id: int, data):
    franchise = db.query(Franchise).filter(Franchise.id == franchise_id).first()
    if not franchise:
        raise HTTPException(status_code=404, detail="Franchise not found")
    
    for key, value in data.dict(exclude_unset=True).items():
        setattr(franchise, key, value)
    
    db.commit()
    db.refresh(franchise)
    return franchise

def delete_franchise(db: Session, franchise_id: int):
    franchise=db.query(Franchise).filter(Franchise.id == franchise_id).first()
    if not franchise:
        raise HTTPException(status_code=404, detail="Franchise not found")
    
    db.delete(franchise)
    db.commit()
    return "success"