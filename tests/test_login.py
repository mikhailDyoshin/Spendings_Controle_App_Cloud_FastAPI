import httpx
import pytest


@pytest.mark.asyncio
async def test_sign_user_up(default_client: httpx.AsyncClient) -> None:
    """
        The function tests the sign-up route.
    """

    # request data
    payload = {
        "email": "testuser@mymail.com",
        "password": "testpassword",
    }

    headers = {
        "accept": "application/json",
        "Content-Type": "application/json"
    }

    # expected response
    test_response = {
        "message": "User created successfully!"
    }

    # initiate the request
    response = await default_client.post("/user/signup", json=payload, headers=headers)

    # compare the responses to be sure whether the request was successful
    assert response.status_code == 200
    assert response.json() == test_response


@pytest.mark.asyncio
async def test_user_exists(default_client: httpx.AsyncClient) -> None:
    """
        The function tests the "user-already-exists" conflict.
    """

    # request data
    payload = {
        "email": "testuser@mymail.com",
        "password": "testpassword",
    }

    headers = {
        "accept": "application/json",
        "Content-Type": "application/json"
    }

    # expected detail
    detail = "User with supplied username exists"

    # initiate the request
    response = await default_client.post("/user/signup", json=payload, headers=headers)

    # assert the response
    assert response.status_code == 409
    assert response.json()['detail'] == detail


@pytest.mark.asyncio
async def test_sign_user_in(default_client: httpx.AsyncClient) -> None:
    """
        The function tests the sign-in route.
    """
    # request data
    payload = {
        "username": "testuser@mymail.com",
        "password": "testpassword"
    }

    headers = {
        "accept": "application/json",
        "Content-Type": "application/x-www-form-urlencoded"
    }

    # initiate the request
    response = await default_client.post("/user/signin", data=payload, headers=headers)

    # compare the responses to be sure whether the request was successful
    assert response.status_code == 200
    assert response.json()["token_type"] == "Bearer"


@pytest.mark.asyncio
async def test_sign_in_non_existent_user(default_client: httpx.AsyncClient) -> None:
    """
        The function tests the sign-in route.
    """
    # request data
    payload = {
        "username": "wrong@mymail.com",
        "password": "testpassword"
    }

    headers = {
        "accept": "application/json",
        "Content-Type": "application/x-www-form-urlencoded"
    }

    detail = "User with supplied email does not exist"

    # initiate the request
    response = await default_client.post("/user/signin", data=payload, headers=headers)

    # compare the responses to be sure whether the request was successful
    assert response.status_code == 404
    assert response.json()["detail"] == detail


@pytest.mark.asyncio
async def test_sign_user_in_wrong_password(default_client: httpx.AsyncClient) -> None:
    """
        The function tests the sign-in route.
    """
    # request data
    payload = {
        "username": "testuser@mymail.com",
        "password": "wrongpassword"
    }

    headers = {
        "accept": "application/json",
        "Content-Type": "application/x-www-form-urlencoded"
    }

    detail = 'Invalid details passed.'

    # initiate the request
    response = await default_client.post("/user/signin", data=payload, headers=headers)

    # compare the responses to be sure whether the request was successful
    assert response.status_code == 401
    assert response.json()["detail"] == detail
    