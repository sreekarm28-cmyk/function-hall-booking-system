from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session

from database import get_db
from schemas import BookingCreate, BookingResponse
from crud import (
    cancel_booking,
    confirm_booking,
    complete_booking,
    create_booking,
    is_hall_available,
    get_my_bookings,
    get_owner_bookings,
)
from security import get_current_user
from models import Booking, BookingStatus, User, UserRole, FunctionHall


router = APIRouter(prefix="/bookings", tags=["Bookings"])


@router.post("/", response_model=BookingResponse)
def create_new_booking(
    booking: BookingCreate,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user),
):
    hall = db.query(FunctionHall).filter(
        FunctionHall.id == booking.hall_id
    ).first()

    if not hall:
        raise HTTPException(
            status_code=404,
            detail="Hall not found",
        )

    if not hall.is_active:
        raise HTTPException(
            status_code=400,
            detail="Hall is currently inactive",
        )

    if not is_hall_available(
        db,
        booking.hall_id,
        booking.start_date,
        booking.end_date,
    ):
        raise HTTPException(
            status_code=409,
            detail="Hall is not available for these dates",
        )

    return create_booking(
        db,
        booking,
        user_id=current_user.id,
    )


@router.get("/", response_model=list[BookingResponse])
def get_bookings(
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user),
):
    if current_user.role == UserRole.HALL_OWNER:
        return get_owner_bookings(db, current_user.id)

    return get_my_bookings(db, current_user.id)


@router.patch("/{booking_id}/confirm", response_model=BookingResponse)
def confirm_booking_by_owner(
    booking_id: int,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user),
):
    if current_user.role != UserRole.HALL_OWNER:
        raise HTTPException(
            status_code=403,
            detail="Only hall owners can confirm bookings",
        )

    booking = db.query(Booking).filter(
        Booking.id == booking_id
    ).first()

    if not booking:
        raise HTTPException(
            status_code=404,
            detail="Booking not found",
        )

    hall = db.query(FunctionHall).filter(
        FunctionHall.id == booking.hall_id
    ).first()

    if hall.owner_id != current_user.id:
        raise HTTPException(
            status_code=403,
            detail="You can only confirm bookings for your own halls",
        )

    if booking.status != BookingStatus.PENDING:
        raise HTTPException(
            status_code=400,
            detail="Only pending bookings can be confirmed",
        )

    return confirm_booking(db, booking_id)


@router.patch("/{booking_id}/cancel", response_model=BookingResponse)
def cancel_booking_endpoint(
    booking_id: int,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user),
):
    booking = db.query(Booking).filter(
        Booking.id == booking_id
    ).first()

    if not booking:
        raise HTTPException(
            status_code=404,
            detail="Booking not found",
        )

    if current_user.role == UserRole.CUSTOMER:
        if booking.user_id != current_user.id:
            raise HTTPException(
                status_code=403,
                detail="You can only cancel your own bookings",
            )

    elif current_user.role == UserRole.HALL_OWNER:
        hall = db.query(FunctionHall).filter(
            FunctionHall.id == booking.hall_id
        ).first()

        if hall.owner_id != current_user.id:
            raise HTTPException(
                status_code=403,
                detail="You can only cancel bookings for your own halls",
            )

    if booking.status in [
        BookingStatus.CANCELLED,
        BookingStatus.COMPLETED,
    ]:
        raise HTTPException(
            status_code=400,
            detail="Booking cannot be cancelled",
        )

    return cancel_booking(db, booking_id)


@router.patch("/{booking_id}/complete", response_model=BookingResponse)
def complete_booking_by_owner(
    booking_id: int,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user),
):
    if current_user.role != UserRole.HALL_OWNER:
        raise HTTPException(
            status_code=403,
            detail="Only hall owners can complete bookings",
        )

    booking = db.query(Booking).filter(
        Booking.id == booking_id
    ).first()

    if not booking:
        raise HTTPException(
            status_code=404,
            detail="Booking not found",
        )

    hall = db.query(FunctionHall).filter(
        FunctionHall.id == booking.hall_id
    ).first()

    if hall.owner_id != current_user.id:
        raise HTTPException(
            status_code=403,
            detail="You can only complete bookings for your own halls",
        )

    if booking.status != BookingStatus.CONFIRMED:
        raise HTTPException(
            status_code=400,
            detail="Only confirmed bookings can be completed",
        )

    return complete_booking(db, booking_id)