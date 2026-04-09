from sqlalchemy.orm import Session
from passlib.context import CryptContext
from app.models.user import User, Role
from app.utils.jwt import create_access_token,create_refresh_token
from app.core.security import verify_password






def login_user(db: Session, email: str, password: str, franchise_code: str = None):
    try:
        user = db.query(User).filter(User.email == email).first()
    except Exception as e:
        print("DB ERROR:", str(e))
        raise
    if not user:
        return None
    if not verify_password(password, user.password):
        return None
    
    if user.role == Role.FRANCHISE:
        from app.models.franchise import Franchise
        franchise = db.query(Franchise).filter(Franchise.email == email, Franchise.franchise_code == franchise_code).first()
        if not franchise:
            return None
    token= create_access_token(data={"user_id": user.id, "email": user.email, "role": user.role.value})
    refresh_token = create_refresh_token(data={"user_id": user.id})
    return {
        "access_token": token,
        "refresh_token": refresh_token,
        "role": user.role.value
    }



def get_users(db: Session):
    return db.query(User).all()
    