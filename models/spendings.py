from typing import List

from pydantic import BaseModel


class Spending(BaseModel):
    id: int
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