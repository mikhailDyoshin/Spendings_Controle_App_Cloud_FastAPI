from typing import List

from fastapi import APIRouter, Body, HTTPException, status
from models.spendings import Spending

event_router = APIRouter(
    tags=["Events"]
)

spendings = []


@event_router.get("/", response_model=List[Spending])
async def retrieve_all_spendings() -> List[Spending]:
    return spendings


@event_router.get("/{id}", response_model=Spending)
async def retrieve_event(id: int) -> Spending:
    for spending in spendings:
        if spending.id == id:
            return spending
    raise HTTPException(
        status_code=status.HTTP_404_NOT_FOUND,
        detail="Record with supplied ID does not exist"
    )


@event_router.post("/new")
async def create_event(body: Spending = Body(...)) -> dict:
    spendings.append(body)
    return {
        "message": "Record created successfully"
    }


@event_router.delete("/{id}")
async def delete_event(id: int) -> dict:
    for event in spendings:
        if event.id == id:
            spendings.remove(event)
            return {
                "message": "Record deleted successfully"
            }

    raise HTTPException(
        status_code=status.HTTP_404_NOT_FOUND,
        detail="Record with supplied ID does not exist"
    )