from fastapi import HTTPException
from Intuit.MyBook.src.database.postgres import get_postgres_conn, get_postgres_cursor
from Intuit.MyBook.src.models.product import Product
import logging

logger = logging.getLogger(__name__)

async def create_product(product: Product):
    conn = get_postgres_conn()
    cursor = get_postgres_cursor(conn)
    try:
        cursor.execute(
            "INSERT INTO products (name, description, price, sku, currency) VALUES (%s, %s, %s, %s, %s) RETURNING id",
            (product.name, product.description, product.price, product.sku, product.currency)
        )
        product_id = cursor.fetchone()['id']
        conn.commit()
        return {"id": product_id, **product.dict()}
    except Exception as e:
        conn.rollback()
        logger.error(f"Error creating product: {e}")
        raise HTTPException(status_code=400, detail=f"Error creating product: {str(e)}")
    finally:
        cursor.close()
        conn.close()

async def get_product(product_id: int):
    conn = get_postgres_conn()
    cursor = get_postgres_cursor(conn)
    try:
        cursor.execute("SELECT * FROM products WHERE id = %s", (product_id,))
        product = cursor.fetchone()
        if product:
            return product
        else:
            raise HTTPException(status_code=404, detail="Product not found")
    finally:
        cursor.close()
        conn.close()
