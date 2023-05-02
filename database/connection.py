from typing import Any, List, Optional

from beanie import init_beanie, PydanticObjectId
from models.spendings import Spending
from models.users import User
from motor.motor_asyncio import AsyncIOMotorClient
from pydantic import BaseSettings, BaseModel


class Settings(BaseSettings):
    DATABASE_URL: Optional[str] = None

    async def initialize_database(self):
        client = AsyncIOMotorClient(self.DATABASE_URL)
        await init_beanie(database=client.get_default_database(), 
                          document_models=[Spending, User])


    class Config:
        # The environment that stores DATABASE_URL
        env_file = ".env"


class Database:
    """
        The class defines all CRUD operations in a MongoDB instance.
    """
    def __init__(self, model):
        self.model = model


    # Create
    async def save(self, document) -> None:
        """
            Adds a record to the database collection.
        """
        await document.create()
        return None


    # Read
    async def get(self, id: PydanticObjectId) -> Any:
        """
            Takes document's id and returns a document instead.
        """
        # Getting document by its id
        doc = await self.model.get(id)

        # Checking if the document exists
        if doc:
            return doc
        else:
            return False


    async def get_all(self) -> List[Any]:
        """
            Returns all existing documents in the database.
        """
        # Forming the list that stores all existing documents.
        docs = await self.model.find_all().to_list()
        return docs


    # Update
    async def update(self, id: PydanticObjectId, body: BaseModel) -> Any:
        doc_id = id

        # Parsing the updated request body into a dictionary
        des_body = body.dict()
        # Filtering the dictionary to remove None values
        des_body = {key: value for key, value in des_body.items() if value is not None}

        # Forming the query
        update_query = {"$set": {field: value for field, value in des_body.items()}}

        # Getting document with supplied ID
        doc = await self.get(doc_id)

        # Checking the document's presence
        if not doc:
            return False

        # Updating the document using Beanie's update() method
        await doc.update(update_query)

        return doc


    # Delete
    async def delete(self, id: PydanticObjectId) -> bool:
        doc = await self.get(id)

        if not doc:
            return False

        await doc.delete()

        return True