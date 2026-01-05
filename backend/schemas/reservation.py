from sqlmodel import SQLModel
from typing import List


class ReservationCreate(SQLModel):
    showtime_id: int
    seat_ids: List[int]


class ReservationRead(SQLModel):
    id: int
    showtime_id: int
    seats_reserved: int
