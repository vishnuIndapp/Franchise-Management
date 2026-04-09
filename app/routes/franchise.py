from fastapi import APIRouter, Depends, HTTPException,Query,status
from sqlalchemy.orm import Session

from app.core.database import get_db
from app.schemas.franchise import FranchiseCreate, FranchiseResponse,FranchiseListResponse,FranchiseUpdate
from app.services.franchise_service import create_franchise_user,get_franchises,get_franchise_by_id,update_franchise,delete_franchise
from app.dependencies.role_checker import require_super_admin


router = APIRouter()


@router.post("/", response_model=FranchiseResponse)
def create(data:FranchiseCreate,db: Session = Depends(get_db), user=Depends(require_super_admin)):
    return create_franchise_user(db, data)


@router.get("/", response_model=FranchiseListResponse)
def list_franchises(
    search: str = Query(None, description="Search term for name, email, phone, or franchise code"),
    page: int = Query(1, ge=1, description="Page number"),
    limit: int = Query(10, ge=1, le=100, description="Number of items per page"),
    db: Session = Depends(get_db)):

    result=get_franchises(db, search, page, limit)

    return {
        "total": result["total"],
        "page": page,
        "limit": limit,
        "data": result["data"]
    }


@router.get("/{franchise_id}", response_model=FranchiseResponse)
def get_one(franchise_id: int, db: Session = Depends(get_db)):
    franchise = get_franchise_by_id(db, franchise_id)
    if not franchise:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Franchise not found")
    return franchise



@router.put("/{franchise_id}", response_model=FranchiseResponse)
def update(franchise_id: int,
                              data: FranchiseUpdate,
                              db: Session = Depends(get_db),
                              user=Depends(require_super_admin)):
    franchise=update_franchise(db, franchise_id, data)

    if not franchise:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Franchise not found")
    
    return franchise

@router.delete("/{franchise_id}")
def delete(franchise_id: int, db: Session = Depends(get_db), user=Depends(require_super_admin)):
    
    success = delete_franchise(db, franchise_id)

    if not success:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Franchise not found")
    
    return {"detail": "Franchise deleted successfully"}
