from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session

from database import get_db
from schemas import UserCreate, UserResponse, Token ,UserStatusUpdate
from crud import get_user_by_email, create_user,get_users, update_user_status
from security import verify_password, create_access_token, get_current_user
from models import User, UserRole
from fastapi.security import OAuth2PasswordRequestForm

router = APIRouter(prefix="/users", tags=["Users"])


@router.post("/register", response_model=UserResponse)
def register(user: UserCreate, db: Session = Depends(get_db)):
    existing_user = get_user_by_email(db, user.email)
    if existing_user:
        raise HTTPException(status_code=400, detail="Email already registered")

    new_user = create_user(db, user)
    return new_user


@router.post("/login", response_model=Token)
def login(
    form_data: OAuth2PasswordRequestForm = Depends(),
    db: Session = Depends(get_db)
):
    user = get_user_by_email(db, form_data.username)

    if not user or not verify_password(form_data.password, user.password_hash):
        raise HTTPException(status_code=401, detail="Invalid email or password")

    access_token = create_access_token(data={"sub": str(user.id)})

    return {
        "access_token": access_token,
        "token_type": "bearer"
    }


@router.get("/me", response_model=UserResponse)
def read_current_user(current_user: User = Depends(get_current_user)):
    return current_user

@router.get("/", response_model=list[UserResponse])
def list_users(
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    if current_user.role != UserRole.HALL_OWNER:
        raise HTTPException(
            status_code=403,
            detail="Only hall owners can view users"
        )

    return get_users(db)




@router.patch("/{user_id}/status", response_model=UserResponse)
def update_user_status_endpoint(
    user_id: int,
    status: UserStatusUpdate,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    if current_user.role != UserRole.HALL_OWNER:
        raise HTTPException(
            status_code=403,
            detail="Only hall owners can change user status"
        )

    if current_user.id == user_id:
        raise HTTPException(
            status_code=400,
            detail="Owner cannot change their own status"
        )

    user = update_user_status(db, user_id, status.is_active)

    if not user:
        raise HTTPException(
            status_code=404,
            detail="User not found"
        )

    return user
