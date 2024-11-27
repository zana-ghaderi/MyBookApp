from pydantic import BaseModel, Field

class CustomerProfile(BaseModel):
    user_id: int
    preferences: dict
    locale: str = Field(..., example="en-US")  # Add locale field
