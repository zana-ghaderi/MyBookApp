from pydantic import BaseModel, EmailStr


class User(BaseModel):
    email: EmailStr
    password: str
    first_name: str
    last_name: str
    locale: str  # For language preference
    currency: str  # For preferred currency
