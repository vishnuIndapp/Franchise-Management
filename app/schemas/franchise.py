from pydantic import BaseModel,EmailStr,Field
from typing import Optional




class FranchiseBase(BaseModel):
    name: str = Field(..., min_length=3)
    email: EmailStr
    phone: str = Field(..., min_length=10, max_length=15)
    address: Optional[str] = None



class FranchiseCreate(FranchiseBase):
    password: str = Field(..., min_length=6,max_length=72)
    franchise_code: str = Field(..., min_length=3, max_length=20)


class FranchiseUpdate(BaseModel):
    name: Optional[str] = Field(None, min_length=3)
    email: Optional[EmailStr] = None
    phone: Optional[str] = Field(None, min_length=10, max_length=15)
    address: Optional[str] = None
    password: Optional[str] = Field(default=None, min_length=6, max_length=72)


class FranchiseResponse(FranchiseBase):
    id: int
    franchise_code: str

    model_config = { "from_attributes": True }


class FranchiseListResponse(BaseModel):
    total: int
    page : int
    limit : int
    data: list[FranchiseResponse]
    
