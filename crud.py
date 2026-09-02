from datetime import datetime, timedelta
from sqlalchemy.orm import Session
from models import User, FunctionHall, Booking, BookingStatus, UserRole
from schemas import UserCreate, HallCreate, BookingCreate
from security import hash_password


def get_user_by_email(db: Session, email: str) -> User | None:
    return db.query(User).filter(User.email == email).first()


def create_user(db: Session, user: UserCreate) -> User:
    hashed_pw = hash_password(user.password)

    new_user = User(
        name=user.name,
        email=user.email,
        password_hash=hashed_pw,
        role=UserRole.CUSTOMER,
    )

    db.add(new_user)
    db.commit()
    db.refresh(new_user)

    return new_user


def create_hall(db: Session, hall: HallCreate, owner_id: int) -> FunctionHall:
    new_hall = FunctionHall(**hall.model_dump(), owner_id=owner_id)
    db.add(new_hall)
    db.commit()
    db.refresh(new_hall)
    return new_hall


def get_halls(db: Session):
    return db.query(FunctionHall).all()


HOLD_MINUTES = 10


def is_hall_available(db: Session, hall_id: int, start_date, end_date) -> bool:
    hold_cutoff = datetime.utcnow() - timedelta(minutes=HOLD_MINUTES)

    conflicting = db.query(Booking).filter(
        Booking.hall_id == hall_id,
        Booking.start_date <= end_date,
        Booking.end_date >= start_date,
        (
            (Booking.status == BookingStatus.CONFIRMED) |
            ((Booking.status == BookingStatus.PENDING) & (Booking.created_at >= hold_cutoff))
        )
    ).first()

    return conflicting is None


def create_booking(db: Session, booking: BookingCreate, user_id: int) -> Booking:
    new_booking = Booking(
        user_id=user_id,
        hall_id=booking.hall_id,
        start_date=booking.start_date,
        end_date=booking.end_date,
        status=BookingStatus.PENDING,
    )
    db.add(new_booking)
    db.commit()
    db.refresh(new_booking)
    return new_booking

def get_users(db: Session):
    return db.query(User).all()

def update_user_status(db: Session, user_id: int, is_active: bool):
    user = db.query(User).filter(User.id == user_id).first()

    if not user:
        return None

    user.is_active = is_active

    # When a customer is deactivated,
    # cancel their pending and confirmed bookings.
    if not is_active:
        db.query(Booking).filter(
            Booking.user_id == user_id,
            Booking.status.in_([
                BookingStatus.PENDING,
                BookingStatus.CONFIRMED
            ])
        ).update(
            {Booking.status: BookingStatus.CANCELLED},
            synchronize_session=False
        )

    db.commit()
    db.refresh(user)

    return user

    

def cancel_booking(db: Session, booking_id: int):
    booking = db.query(Booking).filter(Booking.id == booking_id).first()

    if not booking:
        return None

    booking.status = BookingStatus.CANCELLED

    db.commit()
    db.refresh(booking)

    return booking

def get_my_bookings(db: Session, user_id: int):
    return db.query(Booking).filter(
        Booking.user_id == user_id
    ).all()


def get_owner_bookings(db: Session, owner_id: int):
    return (
        db.query(Booking)
        .join(FunctionHall)
        .filter(FunctionHall.owner_id == owner_id)
        .all()
    )

def update_hall(db: Session, hall_id: int, hall_data: dict):
    hall = db.query(FunctionHall).filter(
        FunctionHall.id == hall_id
    ).first()

    if not hall:
        return None

    for key, value in hall_data.items():
        setattr(hall, key, value)

    db.commit()
    db.refresh(hall)

    return hall


def confirm_booking(db: Session, booking_id: int):
    booking = db.query(Booking).filter(
        Booking.id == booking_id
    ).first()

    if not booking:
        return None

    booking.status = BookingStatus.CONFIRMED

    db.commit()
    db.refresh(booking)

    return booking


def complete_booking(db: Session, booking_id: int):
    booking = db.query(Booking).filter(
        Booking.id == booking_id
    ).first()

    if not booking:
        return None

    booking.status = BookingStatus.COMPLETED

    db.commit()
    db.refresh(booking)

    return booking

def update_hall_status(db: Session, hall_id: int, is_active: bool):
    hall = db.query(FunctionHall).filter(
        FunctionHall.id == hall_id
    ).first()

    if not hall:
        return None

    hall.is_active = is_active

    db.commit()
    db.refresh(hall)

    return hall