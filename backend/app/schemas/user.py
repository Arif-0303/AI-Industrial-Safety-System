from pydantic import BaseModel, EmailStr, Field
from typing import List


# =====================================================
# Create User
# =====================================================

class UserCreate(BaseModel):
    name: str = Field(..., min_length=2, max_length=100)
    email: EmailStr
    password: str = Field(..., min_length=6)
    role: str = "worker"


# =====================================================
# Login
# =====================================================

class UserLogin(BaseModel):
    email: EmailStr
    password: str


# =====================================================
# Update User
# =====================================================

class UserUpdate(BaseModel):
    name: str
    email: EmailStr
    role: str
    is_active: bool


# =====================================================
# Assign Role
# =====================================================

class RoleUpdate(BaseModel):
    role: str


# =====================================================
# Search User
# =====================================================

class UserSearch(BaseModel):
    keyword: str


# =====================================================
# User Response
# =====================================================

class UserResponse(BaseModel):
    id: int
    name: str
    email: EmailStr
    role: str
    is_active: bool

    class Config:
        from_attributes = True


# =====================================================
# Pagination Response
# =====================================================

class PaginatedUsersResponse(BaseModel):
    page: int
    page_size: int
    total_users: int
    total_pages: int
    users: List[UserResponse]


# =====================================================
# User Statistics
# =====================================================

class UserStatisticsResponse(BaseModel):
    total_users: int
    active_users: int
    inactive_users: int
    admins: int
    safety_officers: int
    workers: int


# =====================================================
# Dashboard Response
# =====================================================

class AdminDashboardResponse(BaseModel):
    user_statistics: UserStatisticsResponse
    recent_users: List[UserResponse]


# =====================================================
# Generic Message
# =====================================================

class MessageResponse(BaseModel):
    message: str