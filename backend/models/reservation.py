from sqlmodel import SQLModel, Field, Relationship

from typing import Optional
from enum import Enum

class ReservationStatus(str, Enum):
    ACTIVE = "active"
    CANCELLED = "cancelled"
    EXPIRED = "expired"


class Reservation(SQLModel, table=True):
    id: Optional[int] = Field(default=None, primary_key=True)
    user_id: int = Field(foreign_key="user.id")
    showtime_id: int = Field(foreign_key="showtime.id")
    seats_reserved: int = Field(default=1)
    status: ReservationStatus = Field(default=ReservationStatus.ACTIVE)

    user: Optional["User"] = Relationship(back_populates="reservations")
    showtime: Optional["Showtime"] = Relationship(back_populates="reservations")