from typing import List, Optional
from pydantic import BaseModel
from beanie import Document


class Spending(Document):
    date: str
    food: float
    transport: float
    shopping: float
    total: float

    class Config:
        schema_extra = {
            "example": {
                "date": "2023-04-28",
                "food": 112.15,
                "transport":  10.11,
                "shopping": 1010.50,
                "total": 1132.0,
            }
        }

    class Settings:
        name="spendings"


class SpendingUpdate(BaseModel):
    date: Optional[str]
    food: Optional[float]
    transport: Optional[float]
    shopping: Optional[float]
    total: Optional[float]
