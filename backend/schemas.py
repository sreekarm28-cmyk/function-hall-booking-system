from decimal import Decimal
from datetime import date, datetime

from pydantic import BaseModel, EmailStr, model_validator

from models import UserRole, BookingStatus


class UserCreate(BaseModel):
    name: str
    email: EmailStr
    password: str


class UserResponse(BaseModel):
    id: int
    name: str
    email: EmailStr
    role: UserRole
    is_active: bool

    class Config:
        from_attributes = True


class Token(BaseModel):
    access_token: str
    token_type: str = "bearer"


class HallCreate(BaseModel):
    name: str
    address: str
    city: str
    capacity: int
    price_per_day: Decimal
    description: str | None = None


class HallResponse(BaseModel):
    id: int
    name: str
    address: str
    city: str
    capacity: int
    price_per_day: Decimal
    owner_id: int
    is_active: bool

    class Config:
        from_attributes = True


class BookingCreate(BaseModel):
    hall_id: int
    start_date: date
    end_date: date

    @model_validator(mode="after")
    def validate_dates(self):
        if self.end_date < self.start_date:
            raise ValueError("End date cannot be before start date")
        return self


class BookingResponse(BaseModel):
    id: int
    user_id: int
    hall_id: int
    start_date: date
    end_date: date
    status: BookingStatus
    created_at: datetime

    class Config:
        from_attributes = True


class UserStatusUpdate(BaseModel):
    is_active: bool


class HallUpdate(BaseModel):
    name: str | None = None
    address: str | None = None
    city: str | None = None
    capacity: int | None = None
    price_per_day: Decimal | None = None
    description: str | None = None


class HallStatusUpdate(BaseModel):
    is_active: bool