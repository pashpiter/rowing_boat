from sqlmodel import SQLModel, Field


class PassengerBase(SQLModel):
    name: str


class Passenger(PassengerBase, table=True):
    id: int | None = Field(default=None, primary_key=True)
    boat_id: int | None = Field(default=1, foreign_key='boat.id')


class PassengerRead(PassengerBase):
    pass
