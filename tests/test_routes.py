import httpx
import pytest

from auth.jwt_handler import create_access_token
from models.spendings import Spending


@pytest.fixture(scope="module")
async def access_token() -> str:
    """
        The fixture creates a token 
        while testing CRUD-routes.
        Since the routes are protected, 
        it's necessary to generate an access token
        while testing them.
    """
    return create_access_token("testuser@mymail.com")


@pytest.fixture(scope="module")
async def access_token_other() -> str:
    """
        The fixture creates a token 
        while testing CRUD-routes.
        Since only creator has an access to his data, 
        it's neccessary to generate 
        the second access token 
        to check the feature.
    """
    return create_access_token("testuserOther@mymail.com")


@pytest.fixture(scope="module")
async def mock_spending() -> Spending:
    """
        The fixture is needed to test the get-requests. 
        It posts an event that will be requested 
        by the tests that check READ endpoints.
    """
    new_spending = Spending(
        _id="64511f71dbad5f6828103501",
        creator="testuser@mymail.com",
        date="2023-04-28",
        food=112.15,
        transport=10.11,
        shopping=1010.50,
        total=1132.0
    )

    await Spending.insert_one(new_spending)

    yield new_spending


@pytest.mark.asyncio
async def test_get_spendings(default_client: httpx.AsyncClient, mock_spending: Spending, access_token: str) -> None:

    headers = {
        "Content-Type": "application/json",
        "Authorization": f"Bearer {access_token}"
    }

    response = await default_client.get("/spending/", headers=headers)

    assert response.status_code == 200
    assert response.json()[0]["_id"] == str(mock_spending.id)


@pytest.mark.asyncio
async def test_get_spending(default_client: httpx.AsyncClient, mock_spending: Spending, access_token: str) -> None:
    url = f"/spending/{str(mock_spending.id)}"

    headers = {
        "Content-Type": "application/json",
        "Authorization": f"Bearer {access_token}"
    }

    response = await default_client.get(url, headers=headers)

    assert response.status_code == 200
    assert response.json()["creator"] == mock_spending.creator
    assert response.json()["_id"] == str(mock_spending.id)


@pytest.mark.asyncio
async def test_get_spending_wrong_user(default_client: httpx.AsyncClient, mock_spending: Spending, access_token_other: str) -> None:
    url = f"/spending/{str(mock_spending.id)}"

    headers = {
        "Content-Type": "application/json",
        "Authorization": f"Bearer {access_token_other}"
    }

    response = await default_client.get(url, headers=headers)

    assert response.status_code == 400


@pytest.mark.asyncio
async def test_post_spending(default_client: httpx.AsyncClient, access_token: str) -> None:
    payload = {
        "_id": "64511f71dbad5f6829103501",
        "creator": "testuser@mymail.com",
        "date": "2023-04-28",
        "food": 112.15,
        "transport":  10.11,
        "shopping": 1010.50,
        "total": 1132.0,
    }

    headers = {
        "Content-Type": "application/json",
        "Authorization": f"Bearer {access_token}"
    }

    test_response = {
        "message": "Record created successfully"
    }

    response = await default_client.post("/spending/new", json=payload, headers=headers)

    assert response.status_code == 200
    assert response.json() == test_response


@pytest.mark.asyncio
async def test_get_spending_count(default_client: httpx.AsyncClient, access_token: str) -> None:

    headers = {
        "Content-Type": "application/json",
        "Authorization": f"Bearer {access_token}"
    }

    response = await default_client.get("/spending/", headers=headers)

    # The list of events: [{event1_dict}, {event2_dict}]
    spendings = response.json()

    assert response.status_code == 200
    assert len(spendings) == 2


@pytest.mark.asyncio
async def test_get_spending_count_wrong_user(default_client: httpx.AsyncClient, access_token_other: str) -> None:

    headers = {
        "Content-Type": "application/json",
        "Authorization": f"Bearer {access_token_other}"
    }

    response = await default_client.get("/spending/", headers=headers)

    # The list of events: [{event1_dict}, {event2_dict}]
    spendings = response.json()

    assert response.status_code == 200
    assert len(spendings) == 0


@pytest.mark.asyncio
async def test_update_spending(default_client: httpx.AsyncClient, mock_spending: Spending, access_token: str) -> None:
    test_payload = {
        "date": "2023-03-05"
    }

    headers = {
        "Content-Type": "application/json",
        "Authorization": f"Bearer {access_token}"
    }

    url = f"/spending/{str(mock_spending.id)}"

    response = await default_client.put(url, json=test_payload, headers=headers)

    assert response.status_code == 200
    assert response.json()["date"] == test_payload["date"]


@pytest.mark.asyncio
async def test_update_spending_wrong_user(default_client: httpx.AsyncClient, mock_spending: Spending, access_token_other: str) -> None:
    test_payload = {
        "date": "2023-03-05"
    }

    headers = {
        "Content-Type": "application/json",
        "Authorization": f"Bearer {access_token_other}"
    }

    url = f"/spending/{str(mock_spending.id)}"

    response = await default_client.put(url, json=test_payload, headers=headers)

    assert response.status_code == 400


@pytest.mark.asyncio
async def test_delete_spending_wrong_user(default_client: httpx.AsyncClient, mock_spending: Spending, access_token_other: str) -> None:
    test_response = {
        "message": "Record deleted successfully"
    }

    headers = {
        "Content-Type": "application/json",
        "Authorization": f"Bearer {access_token_other}"
    }

    url = f"/spending/{mock_spending.id}"

    response = await default_client.delete(url, headers=headers)

    assert response.status_code == 400


@pytest.mark.asyncio
async def test_delete_spending(default_client: httpx.AsyncClient, mock_spending: Spending, access_token: str) -> None:
    test_response = {
        "message": "Record deleted successfully"
    }

    headers = {
        "Content-Type": "application/json",
        "Authorization": f"Bearer {access_token}"
    }

    url = f"/spending/{mock_spending.id}"

    response = await default_client.delete(url, headers=headers)

    assert response.status_code == 200
    assert response.json() == test_response


@pytest.mark.asyncio
async def test_delete_spending_againg(default_client: httpx.AsyncClient, mock_spending: Spending, access_token: str) -> None:
    test_response = {
        "message": "Record deleted successfully"
    }

    headers = {
        "Content-Type": "application/json",
        "Authorization": f"Bearer {access_token}"
    }

    url = f"/spending/{mock_spending.id}"

    response = await default_client.delete(url, headers=headers)

    assert response.status_code == 404


@pytest.mark.asyncio
async def test_get_spending_again(default_client: httpx.AsyncClient, mock_spending: Spending, access_token: str) -> None:
    url = f"/spending/{mock_spending.id}"

    headers = {
        "Content-Type": "application/json",
        "Authorization": f"Bearer {access_token}"
    }

    response = await default_client.get(url, headers=headers)

    assert response.status_code == 404


@pytest.mark.asyncio
async def test_update_non_existent_spending(default_client: httpx.AsyncClient, mock_spending: Spending, access_token: str) -> None:
    test_payload = {
        "date": "2023-03-05"
    }

    headers = {
        "Content-Type": "application/json",
        "Authorization": f"Bearer {access_token}"
    }

    url = f"/spending/{str(mock_spending.id)}"

    response = await default_client.put(url, json=test_payload, headers=headers)

    assert response.status_code == 404
