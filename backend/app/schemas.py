from pydantic import BaseModel, EmailStr
from typing import List, Optional
from datetime import datetime
from .models import UserRole, BlocklistType

# Auth
class UserCreate(BaseModel):
    email: EmailStr
    password: str

class UserResponse(BaseModel):
    id: int
    email: EmailStr
    role: UserRole
    class Config:
        from_attributes = True

class Token(BaseModel):
    access_token: str
    token_type: str

# Family
class FamilyBase(BaseModel):
    name: str
    block_adult: bool = False
    block_phishing: bool = True
    block_scam: bool = True

class FamilyCreate(FamilyBase):
    pass

class FamilyResponse(FamilyBase):
    id: int
    owner_id: int
    class Config:
        from_attributes = True

# Blocklist
class BlocklistEntryCreate(BaseModel):
    domain: str
    entry_type: BlocklistType

class BlocklistEntryResponse(BlocklistEntryCreate):
    id: int
    class Config:
        from_attributes = True

# Policy (for Resolver)
class PolicyResponse(BaseModel):
    family_id: int
    block_adult: bool
    block_phishing: bool
    block_scam: bool
    blocklist: List[str]
    whitelist: List[str]

# Events
class EventCreate(BaseModel):
    domain: str
    blocked: bool
    reason: str
    client_ip: str
    family_id: Optional[int] = None

class EventResponse(EventCreate):
    id: int
    timestamp: datetime
    class Config:
        from_attributes = True

# Override
class OverrideRequestCreate(BaseModel):
    domain: str
    family_id: int

class OverrideRequestResponse(OverrideRequestCreate):
    id: int
    status: str
    token: str
    created_at: datetime
    class Config:
        from_attributes = True
