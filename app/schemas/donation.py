from typing import Optional
from datetime import datetime

from pydantic import BaseModel, PositiveInt, validator


class DonationCreate(BaseModel):
    full_amount: PositiveInt
    comment: Optional[str]


class DonationLowDB(DonationCreate):
    id: int
    create_date: datetime

    @validator("create_date", pre=True, always=True)
    def set_create_date(cls, value):
        return value or datetime.now()

    class Config:
        orm_mode = True


class DonationDB(DonationLowDB):
    invested_amount: int
    fully_invested: bool
    close_date: Optional[datetime]
    user_id: Optional[int]