import datetime
import uuid  
from typing import Annotated, Optional
from pydantic import BaseModel, EmailStr, Field
from datetime import datetime


class TokenOtd(BaseModel):
    id: str


class VerifyRequest(BaseModel):
    token: str
    otp: str


class Reset(BaseModel):
    email: EmailStr


class ResetPassword(BaseModel):
    token: str
    password: str


class LoginDto(BaseModel):
    email: EmailStr
    password: Annotated[str, Field(min_length=6)]


class RegisterDto(BaseModel):
    first_name: Optional[str] = Field(None, max_length=55)
    last_name: Optional[str] = Field(None, max_length=55)
    phone_number: Optional[str] = Field(None, max_length=20)
    email: EmailStr
    password: Annotated[str, Field(min_length=6)]


class RefreshTokenDto(BaseModel):
    token: str


class Profile(BaseModel):
    first_name: Optional[str] = Field(None, max_length=55)
    last_name: Optional[str] = Field(None, max_length=55)
    phone_number: Optional[str] = Field(None, max_length=20)
    email: Optional[EmailStr] = None





class UserResponseDto(BaseModel):
    first_name: Optional[str] = Field(None, max_length=55)
    last_name: Optional[str] = Field(None, max_length=55)
    phone_number: Optional[str] = Field(None, max_length=20)
    email: EmailStr
    is_superuser: bool
    is_host: bool
    is_staff: bool
    created_at: datetime

    class Config:
        from_attributes = True


class RefreshToken(BaseModel):
    token: str