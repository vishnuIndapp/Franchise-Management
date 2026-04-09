from fastapi import APIRouter, Depends, HTTPException, status
from fastapi import APIRouter, Depends, HTTPException, status

from app.core.database import get_db
from app.core.security import get_current_user
from app.schemas.profile import ProfileResponse, ProfileUpdate
from app.services.profile_service import get_user_profile,update_user_profile


router = APIRouter()


@router.get("/", response_model=ProfileResponse)
def read_profile(user=Depends(get_current_user), 
                 db=Depends(get_db),
                 current_user=Depends(get_current_user)):
    return get_user_profile(db, current_user)


@router.put("/", response_model=ProfileResponse)
def update_profile(data: ProfileUpdate, 
                   user=Depends(get_current_user), 
                   db=Depends(get_db),
                   current_user=Depends(get_current_user)):
    updated= update_user_profile(db, current_user, data)
    if not updated:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="User not found")
    return updated