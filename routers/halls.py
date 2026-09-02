
from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session

from database import get_db
from schemas import HallCreate, HallResponse, HallUpdate, HallStatusUpdate
from crud import create_hall, get_halls, update_hall, update_hall_status
from security import get_current_user
from models import User, UserRole, FunctionHall


router = APIRouter(prefix="/halls", tags=["Halls"])


@router.post("/", response_model=HallResponse)
def create_new_hall(
    hall: HallCreate,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    if current_user.role != UserRole.HALL_OWNER:
        raise HTTPException(
            status_code=403,
            detail="Only hall owners can create halls"
        )

    return create_hall(
        db,
        hall,
        owner_id=current_user.id
    )


@router.get("/", response_model=list[HallResponse])
def list_halls(
    db: Session = Depends(get_db)
):
    return get_halls(db)


@router.patch("/{hall_id}", response_model=HallResponse)
def update_hall_details(
    hall_id: int,
    hall: HallUpdate,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    if current_user.role != UserRole.HALL_OWNER:
        raise HTTPException(
            status_code=403,
            detail="Only hall owners can update halls"
        )

    existing_hall = db.query(FunctionHall).filter(
        FunctionHall.id == hall_id
    ).first()

    if not existing_hall:
        raise HTTPException(
            status_code=404,
            detail="Hall not found"
        )

    if existing_hall.owner_id != current_user.id:
        raise HTTPException(
            status_code=403,
            detail="You can only update your own hall"
        )

    updated_hall = update_hall(
        db,
        hall_id,
        hall.model_dump(exclude_unset=True)
    )

    return updated_hall


@router.patch("/{hall_id}/status", response_model=HallResponse)
def update_hall_status_endpoint(
    hall_id: int,
    status: HallStatusUpdate,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    if current_user.role != UserRole.HALL_OWNER:
        raise HTTPException(
            status_code=403,
            detail="Only hall owners can change hall status"
        )

    hall = db.query(FunctionHall).filter(
        FunctionHall.id == hall_id
    ).first()

    if not hall:
        raise HTTPException(
            status_code=404,
            detail="Hall not found"
        )

    if hall.owner_id != current_user.id:
        raise HTTPException(
            status_code=403,
            detail="You can only change the status of your own hall"
        )

    return update_hall_status(
        db,
        hall_id,
        status.is_active
    )
