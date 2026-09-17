from database import SessionLocal
from models import User, UserRole
from security import hash_password


db = SessionLocal()

owner = User(
    name="Function Hall Owner",
    email="owner@functionhall.com",
    password_hash=hash_password("Owner@123"),
    role=UserRole.HALL_OWNER
)

db.add(owner)
db.commit()
db.refresh(owner)

print(f"Owner created with ID: {owner.id}")

db.close()