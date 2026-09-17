from fastapi import FastAPI
from routers import bookings, users, halls
from fastapi.middleware.cors import CORSMiddleware

app = FastAPI(title="Function Hall Booking System")

app.add_middleware(
    CORSMiddleware,
    allow_origins=[
    "http://localhost:5173",
    "http://127.0.0.1:5173",],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


@app.get("/")
def root():
    return {"message": "Function Hall Booking System API is running 🚀"}


app.include_router(users.router)
app.include_router(halls.router)
app.include_router(bookings.router)

