from sqlmodel import SQLModel


class ReservationCreate(SQLModel):
    showtime_id: int
    seats: int = 1


class ReservationRead(SQLModel):
    id: int
    showtime_id: int
    seats_reserved: int
