from sqlmodel import SQLModel, Field, Relationship

from typing import Optional

class ShowtimeSeat(SQLModel, table=True):

    id: Optional[int] = Field(default=None, primary_key=True)

    showtime_id: int = Field(foreign_key="showtime.id")
    seat_id: int = Field(foreign_key="seat.id")

    is_reserved: bool = Field(default=False)

    showtime: "Showtime" = Relationship(back_populates="seats")
    seat: "Seat" = Relationship(back_populates="showtime_seats")