from pydantic import BaseModel, Field

class FinancialReport(BaseModel):
    company_id: int
    report_type: str
    data: dict
    currency: str = Field(..., example="USD")  # Add currency field
    timestamp: str = Field(..., example="2024-09-12T12:34:56Z")  # Add timestamp field
