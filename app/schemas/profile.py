from pydantic import BaseModel,EmailStr,Field
from typing import Optional


class ProfileResponse(BaseModel):
    id: int
    email: EmailStr
    role: str
    name: Optional[str] = None
    phone: Optional[str] = None
    address: Optional[str] = None
    franchise_code: Optional[str] = None

    model_config = { "from_attributes": True }




class ProfileUpdate(BaseModel):
    name: Optional[str] = Field(None, min_length=3)
    phone: Optional[str] = Field(None, min_length=10, max_length=15)
    address: Optional[str] = None
    password: Optional[str] = Field(default=None, min_length=6, max_length=72)