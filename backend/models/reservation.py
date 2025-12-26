from sqlmodel import SQLModel, Field, Relationship

from typing import Optional


class Reservation(SQLModel, table=True):
    id: Optional[int] = Field(default=None, primary_key=True)
    user_id: int = Field(foreign_key="user.id")
    showtime_id: int = Field(foreign_key="showtime.id")
    seats_reserved: int = Field(default=1)

    user: Optional["User"] = Relationship(back_populates="reservations")
    showtime: Optional["Showtime"] = Relationship(back_populates="reservations")