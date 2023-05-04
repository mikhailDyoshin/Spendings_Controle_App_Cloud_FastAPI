import asyncio

import httpx
import pytest

from database.connection import Settings
from main import app
from models.spendings import Spending
from models.users import User


@pytest.fixture(scope="session")
def event_loop():
    loop = asyncio.get_event_loop()
    yield loop
    loop.close()


async def init_db():
    """
        Creates a new database instance for testing.
    """
    test_settings = Settings()
    test_settings.DATABASE_URL = "mongodb://localhost:27017/testdb"

    await test_settings.initialize_database()


@pytest.fixture(scope="session")
async def default_client():
    await init_db()
    async with httpx.AsyncClient(app=app, base_url="http://app") as client:
        yield client

        # Clean up resources at the end of the session
        await Spending.find_all().delete()
        await User.find_all().delete()
