from sqlmodel import SQLModel


class SeatAvailabilitySchema(SQLModel):
    seat_id: int
    row: int
    number: int
    is_reserved: bool
