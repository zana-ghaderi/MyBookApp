from pydantic import BaseModel
from typing import Optional
from datetime import datetime

class Sale(BaseModel):
    user_id: int
    total_amount: float
    invoice_id: Optional[int] = None
    sale_date: Optional[datetime] = None  # Make this optional