from pydantic import BaseModel, Field

class Product(BaseModel):
    name: str
    description: str
    price: float
    sku: str
    currency: str = Field(..., example="USD")  # Add currency field
