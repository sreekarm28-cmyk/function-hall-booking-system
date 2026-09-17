from database import SessionLocal
from models import User
from security import hash_password

db = SessionLocal()

owner = db.query(User).filter(
    User.email == "owner@functionhall.com"
).first()

if owner:
    owner.password_hash = hash_password("Owner@12345")
    db.commit()
    print("Owner password reset successfully.")
else:
    print("Owner not found.")

db.close()