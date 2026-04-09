from fastapi import  Depends, HTTPException,status
from app.models.user import Role
from app.core.security import get_current_user


def require_super_admin(user=Depends(get_current_user)):
    if user.role != Role.SUPER_ADMIN:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="You do not have permission to perform this action"
        )
    return user