
from datetime import datetime
from pydantic import BaseModel, EmailStr
from typing import Optional, List, Dict, Any

class GeoJSONFeature(BaseModel):
    type: str
    properties: Dict[str, Any]
    geometry: Dict[str, Any]

class GeoJSONUpload(BaseModel):
    type: str
    name: str
    crs: Optional[Dict[str, Any]]
    features: List[GeoJSONFeature]

class GroupedRoadFeature(BaseModel):
    updated_at: Optional[datetime]
    is_current: bool
    customer_id: int
    geometry_points: int

class UserCreate(BaseModel):
    username: str
    email: EmailStr
    password: str

class UserOut(BaseModel):
    id: int
    username: str
    email: EmailStr

    class Config:
        from_attributes = True

class UserLogin(BaseModel):
    email: EmailStr
    password: str

class TokenOut(BaseModel):
    access_token: str
    token_type: str
    user_id: int