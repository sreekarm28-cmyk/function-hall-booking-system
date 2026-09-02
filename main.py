from fastapi import FastAPI
from routers import bookings, users, halls

app = FastAPI(title="Function Hall Booking System")


@app.get("/")
def root():
    return {"message": "Function Hall Booking System API is running"}


app.include_router(users.router)
app.include_router(halls.router)
app.include_router(bookings.router)

