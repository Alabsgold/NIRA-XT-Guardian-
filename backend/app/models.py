from sqlalchemy import Boolean, Column, ForeignKey, Integer, String, DateTime, Enum, Text
from sqlalchemy.orm import relationship
from sqlalchemy.sql import func
import enum
from .database import Base

class UserRole(str, enum.Enum):
    PARENT = "parent"
    ADMIN = "admin"

class User(Base):
    __tablename__ = "users"

    id = Column(Integer, primary_key=True, index=True)
    email = Column(String, unique=True, index=True)
    hashed_password = Column(String)
    role = Column(Enum(UserRole), default=UserRole.PARENT)
    created_at = Column(DateTime(timezone=True), server_default=func.now())

    families = relationship("Family", back_populates="owner")

class Family(Base):
    __tablename__ = "families"

    id = Column(Integer, primary_key=True, index=True)
    name = Column(String)
    owner_id = Column(Integer, ForeignKey("users.id"))
    
    # Policy settings
    block_adult = Column(Boolean, default=False)
    block_phishing = Column(Boolean, default=True)
    block_scam = Column(Boolean, default=True)

    owner = relationship("User", back_populates="families")
    profiles = relationship("ChildProfile", back_populates="family")
    blocklist = relationship("BlocklistEntry", back_populates="family")
    events = relationship("EventLog", back_populates="family")

class ChildProfile(Base):
    __tablename__ = "child_profiles"

    id = Column(Integer, primary_key=True, index=True)
    name = Column(String)
    family_id = Column(Integer, ForeignKey("families.id"))
    
    family = relationship("Family", back_populates="profiles")

class BlocklistType(str, enum.Enum):
    BLOCK = "block"
    ALLOW = "allow"

class BlocklistEntry(Base):
    __tablename__ = "blocklist_entries"

    id = Column(Integer, primary_key=True, index=True)
    domain = Column(String, index=True)
    entry_type = Column(Enum(BlocklistType), default=BlocklistType.BLOCK)
    family_id = Column(Integer, ForeignKey("families.id"))

    family = relationship("Family", back_populates="blocklist")

class EventLog(Base):
    __tablename__ = "event_logs"

    id = Column(Integer, primary_key=True, index=True)
    family_id = Column(Integer, ForeignKey("families.id"), nullable=True)
    domain = Column(String, index=True)
    blocked = Column(Boolean)
    reason = Column(String)
    client_ip = Column(String)
    timestamp = Column(DateTime(timezone=True), server_default=func.now())

    family = relationship("Family", back_populates="events")

class OverrideRequest(Base):
    __tablename__ = "override_requests"

    id = Column(Integer, primary_key=True, index=True)
    family_id = Column(Integer, ForeignKey("families.id"))
    domain = Column(String)
    status = Column(String, default="pending") # pending, approved, rejected
    token = Column(String, unique=True, index=True)
    created_at = Column(DateTime(timezone=True), server_default=func.now())
