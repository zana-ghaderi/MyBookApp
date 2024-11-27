
from Intuit.MyBook.src.models.user import User
from Intuit.MyBook.src.services import user_service
import pytest
import uuid

@pytest.mark.asyncio
async def test_create_user():
    print("Running create user test")
    unique_email = f"test_{uuid.uuid4()}@example.com"
    user = User(email=unique_email, password="password", first_name="Test", last_name="User", locale="en-US", currency="USD")
    result = await user_service.create_user(user)
    assert "id" in result
    assert result["email"] == user.email
    assert result["first_name"] == user.first_name
    assert result["last_name"] == user.last_name
    assert result["locale"] == user.locale
    assert result["currency"] == user.currency


@pytest.mark.asyncio
async def test_get_user():
    print("Running get user test")
    # First, create a user
    unique_email = f"test_{uuid.uuid4()}@example.com"
    user = User(email=unique_email, password="password", first_name="Test", last_name="User", locale="en-US", currency="USD")
    created_user = await user_service.create_user(user)

    # Now, try to get the user
    result = await user_service.get_user(created_user["id"])
    assert result["id"] == created_user["id"]
    assert result["email"] == created_user["email"]
    assert result["first_name"] == created_user["first_name"]
    assert result["last_name"] == created_user["last_name"]
    assert result["locale"] == created_user["locale"]
    assert result["currency"] == created_user["currency"]