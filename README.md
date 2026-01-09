# Movie Reservation System

Movie Reservation System is a backend service that allows users to reserve movie for a specific showtimes.

Project based on <https://roadmap.sh/projects/movie-reservation-system> challenge

## How to Run the Project

Requirements

- Python 3.8+
- PostgreSQL
- pip
- virtualenv (recommended)

---

### 1. Clone the repository

```bash
git clone https://github.com/your-username/movie-reservation-system.git
cd movie-reservation-system

```

### 2. Create and activate a virtual environment

```bash
python -m venv venv
```

Linux / macOS

```bash
source venv/bin/activate
```

Windows

```bash
venv\Scripts\activate
```

### 3. Install dependencies

```bash
pip install -r requirements.txt
```

### 4. Configure environment variables

Create a .env file in the project root:

```env
POSTGRES_DB=
POSTGRES_USER=
POSTGRES_PASSWORD=
DB_HOST=
DB_PORT=

SECRET_KEY=
REFRESH_SECRET_KEY=

ALGORITHM=HS256
ACCESS_TOKEN_EXPIRE_MINUTES=60
```

### 5. Apply database migrations

```bash
alembic upgrade head
```

### 6. Run development server

```bash
fastapi dev main.py
```

## Features

User Authentication

- User registration and login

- JWT based authentication stored in cookies

- Role-based access:

    User - can browse movies and reserve seats

    Admin - can manage movies and showtimes

 Movie Management (Admin only)

- Admin can create, update, and delete movies

- Each movie includes:
    title,
    description,
    poster image,
    genre

- Manage movie showtimes

Showtimes

- Movies can have multiple showtimes

- Each showtime has its own set of seats

- Showtimes are scheduled by date and time

- Users can get all seats for specific showtime

- Users can get all available seats for specific showtime

- Users can view showtime

- Users can filter showtimes by movie_id, hall_number and starts_at query

Showtimes(Admin only)

- Admin can create showtime

- Admin can edit showtime

- Admin can cancel showtime

Reservations

- Users can view their reservations

- Users can reserve one or multiple seats for a showtime

- Users can cancel upcoming reservations

- The system prevents seat overbooking

Reservations(Admin only)

- Admins can view all reservations for a specific showtime

- Admin can view reservations for a specific user
