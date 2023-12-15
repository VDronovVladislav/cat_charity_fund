from typing import Optional
from datetime import datetime

from pydantic import BaseModel, PositiveInt, Field


class CharityProjectCreate(BaseModel):
    name: str = Field(None, min_length=1, max_length=100)
    description: str
    full_amount: PositiveInt


class CharityProjecUpdate(BaseModel):
    name: Optional[str] = Field(None, min_length=1, max_length=100)
    description: Optional[str]
    full_amount: Optional[PositiveInt]


class CharityProjectDB(CharityProjectCreate):
    id: int
    invested_amount: int
    fully_invested: bool
    create_date: datetime
    close_date: Optional[datetime]

    class Config:
        orm_mode = True