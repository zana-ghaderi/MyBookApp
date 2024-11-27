from fastapi import FastAPI

from Intuit.MyBook.src.models.invoice import Invoice
from Intuit.MyBook.src.services import invoice_service
from src.models.user import User
from src.models.product import Product
from src.models.sale import Sale
from src.models.inventory import InventoryItem
from src.models.customer_profile import CustomerProfile
from src.models.financial_report import FinancialReport
from src.services import user_service, product_service, sales_service, inventory_service, customer_profile_service, financial_report_service

app = FastAPI()

# non-blocking
# concurrency
# scalability
@app.post("/users/")
async def create_user(user: User):
    return await user_service.create_user(user)

@app.get("/users/{user_id}")
async def get_user(user_id: int):
    return await user_service.get_user(user_id)

@app.post("/products/")
async def create_product(product: Product):
    return await product_service.create_product(product)

@app.get("/products/{product_id}")
async def get_product(product_id: int):
    return await product_service.get_product(product_id)

@app.post("/sales/")
async def create_sale(sale: Sale):
    return await sales_service.create_sale(sale)

@app.post("/inventory/")
async def update_inventory(item: InventoryItem):
    return await inventory_service.update_inventory(item)

@app.post("/customer-profiles/")
async def create_customer_profile(profile: CustomerProfile):
    return await customer_profile_service.create_customer_profile(profile)

@app.get("/customer-profiles/{user_id}")
async def get_customer_profile(user_id: int):
    return await customer_profile_service.get_customer_profile(user_id)

@app.post("/financial-reports/")
async def create_financial_report(report: FinancialReport):
    return await financial_report_service.create_financial_report(report)

@app.get("/financial-reports/{company_id}")
async def get_financial_reports(company_id: int):
    return await financial_report_service.get_financial_reports(company_id)

@app.post("/invoices/")
async def create_invoice(invoice: Invoice):
    return await invoice_service.create_invoice(invoice)

@app.get("/invoices/{invoice_id}")
async def get_invoice(invoice_id: int):
    return await invoice_service.get_invoice(invoice_id)

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000)