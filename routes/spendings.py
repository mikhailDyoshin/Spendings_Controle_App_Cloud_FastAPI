from typing import List
from fastapi import APIRouter, Body, HTTPException, status
from models.spendings import Spending, SpendingUpdate
from database.connection import Database
from beanie import PydanticObjectId


event_router = APIRouter(
    tags=["Events"]
)

spendings_database = Database(Spending)


@event_router.get("/", response_model=List[Spending])
async def retrieve_all_spendings() -> List[Spending]:
    spendings = await spendings_database.get_all()
    return spendings


@event_router.get("/{id}", response_model=Spending)
async def retrieve_event(id: PydanticObjectId) -> Spending:
    event = await spendings_database.get(id)
    
    if not event:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Record with supplied ID does not exist"
        )
    
    return event


@event_router.post("/new")
async def create_event(body: Spending) -> dict:
    await spendings_database.save(body)
    return {
        "message": "Record created successfully"
    }


@event_router.put("/{id}")
async def update_event(id: PydanticObjectId, body: SpendingUpdate) -> Spending:
    updated_spending = await spendings_database.update(id, body)
    if not updated_spending:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Event with supplied ID does not exist"
        )
    return updated_spending


@event_router.delete("/{id}")
async def delete_event(id: PydanticObjectId) -> dict:
    spending = await spendings_database.delete(id)

    if not spending:
        raise HTTPException(
        status_code=status.HTTP_404_NOT_FOUND,
        detail="Record with supplied ID does not exist"
        )

    return {
        "message": "Record deleted successfully"
    }
