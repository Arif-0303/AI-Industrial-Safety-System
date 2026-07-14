from pydantic import BaseModel, EmailStr, Field


# =====================================================
# Register
# =====================================================

class UserRegister(BaseModel):
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
# Forgot Password
# =====================================================

class ForgotPasswordRequest(BaseModel):
    email: EmailStr


# =====================================================
# Reset Password
# =====================================================

class ResetPasswordRequest(BaseModel):
    token: str
    new_password: str = Field(..., min_length=6)


# =====================================================
# Refresh Token
# =====================================================

class RefreshTokenRequest(BaseModel):
    refresh_token: str


# =====================================================
# Logout
# =====================================================

class LogoutResponse(BaseModel):
    message: str


# =====================================================
# User Update
# =====================================================

class UserUpdate(BaseModel):
    name: str
    email: EmailStr
    role: str
    is_active: bool


# =====================================================
# User Response
# =====================================================

class UserResponse(BaseModel):
    id: int
    name: str
    email: EmailStr
    role: str

    class Config:
        from_attributes = True


# =====================================================
# Token Response
# =====================================================

class TokenResponse(BaseModel):
    access_token: str
    refresh_token: str
    token_type: str
    user: UserResponse


# =====================================================
# Generic Message Response
# =====================================================

class MessageResponse(BaseModel):
    message: str