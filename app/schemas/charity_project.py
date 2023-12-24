from typing import Optional
from datetime import datetime

from pydantic import BaseModel, PositiveInt, Field, validator


class CharityProjectCreate(BaseModel):
    name: str = Field(..., min_length=1, max_length=100)
    description: str = Field(..., min_length=1)
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

    @validator("create_date", pre=True, always=True)
    def set_create_date(cls, value):
        return value or datetime.now()

    class Config:
        orm_mode = True