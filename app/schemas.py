from datetime import datetime
from typing import Union
from pydantic import BaseModel, HttpUrl, field_validator


class URLSchema(BaseModel):
    id: int
    original_url: str
    alias: str
    is_active: bool
    expires_at: datetime
    count: int = 0

    class Config:
        from_attributes = True


class URLCreate(BaseModel):
    original_url: Union[HttpUrl, str]


class UserCreate(BaseModel):
    email: str
    password: str

    @field_validator('password')
    def validate_password(cls, v):
        if len(v) < 8:
            raise ValueError("Password must be at least 8 characters long")

        return v


class AliasSchema(BaseModel):
    alias: str
