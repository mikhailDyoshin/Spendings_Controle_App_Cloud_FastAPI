from typing import List
from fastapi import APIRouter, Body, HTTPException, status, Depends
from models.spendings import Spending, SpendingUpdate
from database.connection import Database
from beanie import PydanticObjectId
from auth.authenticate import authenticate


event_router = APIRouter(
    tags=["Spendings"]
)

spendings_database = Database(Spending)


@event_router.get("/", response_model=List[Spending])
async def retrieve_all_spendings(user: str=Depends(authenticate)) -> List[Spending]:
    spendings = await spendings_database.get_all(user)
    return spendings


@event_router.get("/{id}", response_model=Spending)
async def retrieve_event(id: PydanticObjectId, user: str=Depends(authenticate)) -> Spending:
    spending = await spendings_database.get(id)

    if not spending:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Record with supplied ID does not exist"
        )

    if spending.creator != user:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Operation not allowed",
        )
    
    return spending


@event_router.post("/new")
async def create_event(body: Spending, user: str=Depends(authenticate)) -> dict:
    body.creator = user
    await spendings_database.save(body)
    return {
        "message": "Record created successfully"
    }


@event_router.put("/{id}")
async def update_event(id: PydanticObjectId, body: SpendingUpdate, user: str=Depends(authenticate)) -> Spending:
    
    # Check if the record exists
    spending = await spendings_database.get(id)
    if not spending:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Event with supplied ID does not exist"
        )
    
    # Check if the user who's trying to update a record is the record's creator
    if spending.creator != user:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Operation not allowed",
        )
    
    # Updating selected record
    updated_spending = await spendings_database.update(id, body)
    
    return updated_spending


@event_router.delete("/{id}")
async def delete_event(id: PydanticObjectId, user: str=Depends(authenticate)) -> dict:
    spending_to_delete = await spendings_database.get(id)

    if not spending_to_delete:
        raise HTTPException(
        status_code=status.HTTP_404_NOT_FOUND,
        detail="Record with supplied ID does not exist"
        )

    if spending_to_delete.creator != user:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Operation not allowed",
        )
    
    spending_deleted = await spendings_database.delete(id)

    if spending_deleted:

        return {
            "message": "Record deleted successfully"
        }
