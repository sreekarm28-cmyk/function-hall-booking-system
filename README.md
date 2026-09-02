# Function Hall Booking System

A backend API for managing function halls and bookings. The system supports customer registration, hall management, booking management, authentication, role-based access control, and booking status management.

## 🚀 Features

* User registration and login
* JWT-based authentication
* Role-based access control
* Customer and Hall Owner roles
* Function hall creation and management
* Activate/deactivate function halls
* Create and manage bookings
* Booking availability and date-overlap checking
* 10-minute hold for pending bookings
* Booking confirmation, cancellation, and completion
* Automatic cancellation of active bookings when a customer is deactivated
* PostgreSQL database
* Alembic database migrations
* Interactive Swagger API documentation

## 🛠️ Tech Stack

* Python
* FastAPI
* SQLAlchemy
* PostgreSQL
* Pydantic
* Alembic
* JWT
* Passlib / bcrypt
* Uvicorn

## 📂 Project Structure

```text
function_hall/
├── migrations/
├── routers/
│   ├── __init__.py
│   ├── users.py
│   ├── halls.py
│   └── bookings.py
├── .env
├── .gitignore
├── alembic.ini
├── create_owner.py
├── crud.py
├── database.py
├── main.py
├── models.py
├── schemas.py
├── security.py
└── requirements.txt
```

## ⚙️ Setup

### 1. Clone the repository

```bash
git clone <your-github-repository-url>
cd function_hall
```

### 2. Create a virtual environment

```bash
python -m venv venv
```

Activate it on Windows:

```bash
venv\Scripts\activate
```

### 3. Install dependencies

```bash
pip install -r requirements.txt
```

## 🔐 Environment Variables

Create a `.env` file in the project root:

```env
DATABASE_URL=your_postgresql_database_url
SECRET_KEY=your_secret_key
```

Do not commit the `.env` file to GitHub.

## 🗄️ Database Setup

The project uses Alembic for database migrations.

Run:

```bash
alembic upgrade head
```

To create a new migration after changing the models:

```bash
alembic revision --autogenerate -m "your migration message"
```

Then apply it:

```bash
alembic upgrade head
```

## ▶️ Run the Application

Start the FastAPI server:

```bash
uvicorn main:app --reload
```

The API will be available at:

```text
http://127.0.0.1:8000
```

## 📖 API Documentation

FastAPI provides interactive Swagger documentation at:

```text
http://127.0.0.1:8000/docs
```

You can use Swagger to register users, log in, create halls, create bookings, and test the available endpoints.

## 👥 User Roles

### Customer

Customers can:

* Register and log in
* View available halls
* Create bookings
* View their bookings
* Cancel their bookings

### Hall Owner

Hall owners can:

* Create function halls
* Update their halls
* Activate/deactivate their halls
* View bookings for their halls
* Confirm bookings
* Cancel bookings
* Complete bookings

## 🔄 Booking Lifecycle

```text
PENDING
   │
   ├──→ CONFIRMED
   │       │
   │       └──→ COMPLETED
   │
   └──→ CANCELLED
```

Pending bookings temporarily hold a hall for a limited period. Confirmed bookings prevent overlapping bookings for the same hall.

## 🔒 Authentication

The API uses JWT bearer authentication.

After logging in, the client receives an access token:

```text
Authorization: Bearer <access_token>
```

Protected endpoints require a valid access token.

## 📡 Main API Endpoints

### Users

```text
POST   /users/register
POST   /users/login
GET    /users/me
GET    /users/
PATCH  /users/{user_id}/status
```

### Function Halls

```text
GET    /halls/
POST   /halls/
PATCH  /halls/{hall_id}
PATCH  /halls/{hall_id}/status
```

### Bookings

```text
POST   /bookings/
GET    /bookings/
PATCH  /bookings/{booking_id}/confirm
PATCH  /bookings/{booking_id}/cancel
PATCH  /bookings/{booking_id}/complete
```

## 🧠 Important Business Rules

* Only authenticated users can access protected endpoints.
* Hall owners can modify only their own halls.
* Hall owners can manage bookings belonging to their own halls.
* Inactive halls cannot receive new bookings.
* A booking cannot have an end date before its start date.
* Overlapping active bookings are prevented.
* Pending bookings are held for a limited period.
* Deactivating a customer cancels their pending and confirmed bookings.
* Inactive users cannot access protected endpoints.

## 🚧 Future Improvements

* Email notifications
* Payment integration
* Booking history and reports
* Advanced hall search and filtering
* Frontend application
* Docker containerization
* Cloud deployment
* Automated testing
* CI/CD pipeline

## 📌 Project Status

The core backend functionality is implemented and tested. Dockerization and cloud deployment are planned as the next steps.
