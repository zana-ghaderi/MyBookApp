from pydantic import BaseModel, Field

class InventoryItem(BaseModel):
    product_id: int
    quantity: int
    location: str = Field(..., example="Warehouse A")
    currency: str = Field(..., example="USD")  # Add currency field