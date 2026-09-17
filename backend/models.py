import enum
from sqlalchemy import Column, Integer, String, Boolean, Date, DateTime, ForeignKey, Enum, Numeric
from sqlalchemy.orm import relationship
from datetime import datetime

from database import Base


class UserRole(str, enum.Enum):
    CUSTOMER = "customer"
    HALL_OWNER = "hall_owner"
    


class BookingStatus(str, enum.Enum):
    PENDING = "pending"
    CONFIRMED = "confirmed"
    CANCELLED = "cancelled"
    COMPLETED = "completed"


class User(Base):
    __tablename__ = "users"

    id = Column(Integer, primary_key=True, index=True)
    name = Column(String, nullable=False)
    email = Column(String, unique=True, index=True, nullable=False)
    password_hash = Column(String, nullable=False)
    role = Column(Enum(UserRole), default=UserRole.CUSTOMER, nullable=False)
    is_active = Column(Boolean, default=True, nullable=False)

    bookings = relationship("Booking", back_populates="user")
    notifications = relationship("Notification", back_populates="user")
    halls_owned = relationship("FunctionHall", back_populates="owner")


class FunctionHall(Base):
    __tablename__ = "function_halls"

    id = Column(Integer, primary_key=True, index=True)
    name = Column(String, nullable=False)
    address = Column(String, nullable=False)
    city = Column(String, nullable=False, index=True)
    capacity = Column(Integer, nullable=False)
    price_per_day = Column(Numeric(10, 2), nullable=False)
    description = Column(String, nullable=True)

    owner_id = Column(Integer, ForeignKey("users.id"), nullable=False)

    owner = relationship("User", back_populates="halls_owned")
    bookings = relationship("Booking", back_populates="hall")
    is_active = Column(Boolean, default=True, nullable=False)


class Booking(Base):
    __tablename__ = "bookings"

    id = Column(Integer, primary_key=True, index=True)

    user_id = Column(Integer, ForeignKey("users.id"), nullable=False)
    hall_id = Column(Integer, ForeignKey("function_halls.id"), nullable=False)

    start_date = Column(Date, nullable=False)
    end_date = Column(Date, nullable=False)

    status = Column(Enum(BookingStatus), default=BookingStatus.PENDING, nullable=False)

    created_at = Column(DateTime, default=datetime.utcnow)

    user = relationship("User", back_populates="bookings")
    hall = relationship("FunctionHall", back_populates="bookings")


class Notification(Base):
    __tablename__ = "notifications"

    id = Column(Integer, primary_key=True, index=True)

    user_id = Column(Integer, ForeignKey("users.id"), nullable=False)

    message = Column(String, nullable=False)
    is_read = Column(Boolean, default=False, nullable=False)
    created_at = Column(DateTime, default=datetime.utcnow)

    user = relationship("User", back_populates="notifications")