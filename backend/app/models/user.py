"""
User database model.
Optional user management for future authentication features.
"""
from sqlmodel import SQLModel, Field, Relationship
from typing import Optional, List
from datetime import datetime
from uuid import uuid4


class UserBase(SQLModel):
    """Base schema for User"""
    email: str = Field(..., unique=True, index=True, description="User email address")
    full_name: Optional[str] = Field(None, description="User full name")
    is_active: bool = Field(default=True, description="Whether user account is active")


class User(UserBase, table=True):
    """
    User database model.
    
    Stores user information for future authentication and
    tracking of user-specific reports.
    """
    __tablename__ = "users"
    
    # Primary key
    id: Optional[str] = Field(
        default_factory=lambda: f"usr_{uuid4().hex[:12]}",
        primary_key=True,
        description="Unique user identifier"
    )
    
    # Timestamps
    created_at: datetime = Field(
        default_factory=datetime.utcnow,
        description="User creation timestamp"
    )
    updated_at: Optional[datetime] = Field(
        default=None,
        description="Last update timestamp"
    )
    
    # Relationships (for future use)
    # reports: List["ATSReport"] = Relationship(back_populates="user")
    
    class Config:
        """Pydantic config"""
        from_attributes = True


class UserCreate(UserBase):
    """Schema for creating a new user"""
    pass


class UserRead(UserBase):
    """Schema for reading a user"""
    id: str
    created_at: datetime
    updated_at: Optional[datetime] = None



