from typing import List, Optional
from sqlmodel import SQLModel, Field, Relationship

class Seat(SQLModel, table=True):
    id: Optional[int] = Field(default=None, primary_key=True)
    row: int
    number: int

    showtime_seats: List["ShowtimeSeat"] = Relationship(
        back_populates="seat"
    )
