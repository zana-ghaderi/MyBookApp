from pydantic import BaseModel, Field
from typing import List

class InvoiceItem(BaseModel):
    product_id: int
    quantity: int
    unit_price: float

class Invoice(BaseModel):
    user_id: int
    items: List[InvoiceItem]
    total_amount: float
    currency: str = Field(..., example="USD")
    issue_date: str = Field(..., example="2024-09-12T12:34:56Z")
    due_date: str = Field(..., example="2024-09-30T23:59:59Z")
