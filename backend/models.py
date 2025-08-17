from pydantic import BaseModel, Field, EmailStr
from typing import List, Optional
from datetime import datetime
import uuid

# Contact Models
class ContactCreate(BaseModel):
    name: str = Field(..., min_length=2, max_length=100)
    email: EmailStr
    phone: Optional[str] = Field(None, max_length=20)
    message: str = Field(..., min_length=10, max_length=1000)

class Contact(BaseModel):
    id: str = Field(default_factory=lambda: str(uuid.uuid4()))
    name: str
    email: str
    phone: Optional[str] = None
    message: str
    created_at: datetime = Field(default_factory=datetime.utcnow)
    status: str = Field(default="new")  # new, contacted, resolved

    class Config:
        json_encoders = {
            datetime: lambda v: v.isoformat()
        }

# Property Models  
class PropertyCreate(BaseModel):
    title: str = Field(..., min_length=5, max_length=200)
    price: str = Field(..., min_length=1, max_length=50)
    location: str = Field(..., min_length=5, max_length=200)
    bedrooms: int = Field(..., ge=1, le=20)
    parking: int = Field(..., ge=0, le=10)
    area: str = Field(..., min_length=1, max_length=50)
    type: str = Field(..., pattern="^(For Sale|For Rent|Investment)$")
    image: str = Field(..., min_length=10)
    description: Optional[str] = Field(None, max_length=2000)
    features: Optional[List[str]] = None

class PropertyUpdate(BaseModel):
    title: Optional[str] = Field(None, min_length=5, max_length=200)
    price: Optional[str] = Field(None, min_length=1, max_length=50)
    location: Optional[str] = Field(None, min_length=5, max_length=200)
    bedrooms: Optional[int] = Field(None, ge=1, le=20)
    parking: Optional[int] = Field(None, ge=0, le=10)
    area: Optional[str] = Field(None, min_length=1, max_length=50)
    type: Optional[str] = Field(None, pattern="^(For Sale|For Rent|Investment)$")
    image: Optional[str] = Field(None, min_length=10)
    description: Optional[str] = Field(None, max_length=2000)
    features: Optional[List[str]] = None
    status: Optional[str] = Field(None, pattern="^(active|sold|rented)$")

class Property(BaseModel):
    id: str = Field(default_factory=lambda: str(uuid.uuid4()))
    title: str
    price: str
    location: str
    bedrooms: int
    parking: int
    area: str
    type: str  # For Sale, For Rent, Investment
    image: str
    description: Optional[str] = None
    features: Optional[List[str]] = None
    status: str = Field(default="active")  # active, sold, rented
    created_at: datetime = Field(default_factory=datetime.utcnow)
    updated_at: datetime = Field(default_factory=datetime.utcnow)

    class Config:
        json_encoders = {
            datetime: lambda v: v.isoformat()
        }

# Response Models
class ContactResponse(BaseModel):
    success: bool
    message: str
    contact_id: Optional[str] = None

class PropertyResponse(BaseModel):
    success: bool
    message: str
    property_id: Optional[str] = None