from fastapi import HTTPException
from Intuit.MyBook.src.database.postgres import get_postgres_conn, get_postgres_cursor
from Intuit.MyBook.src.models.invoice import Invoice

async def create_invoice(invoice: Invoice):
    conn = get_postgres_conn()
    cursor = get_postgres_cursor(conn)
    try:
        # Insert invoice data
        cursor.execute(
            """
            INSERT INTO invoices (user_id, total_amount, currency, issue_date, due_date)
            VALUES (%s, %s, %s, %s, %s)
            RETURNING id
            """,
            (invoice.user_id, invoice.total_amount, invoice.currency, invoice.issue_date, invoice.due_date)
        )
        invoice_id = cursor.fetchone()['id']

        # Insert invoice items
        for item in invoice.items:
            cursor.execute(
                """
                INSERT INTO invoice_items (invoice_id, product_id, quantity, unit_price)
                VALUES (%s, %s, %s, %s)
                """,
                (invoice_id, item.product_id, item.quantity, item.unit_price)
            )

        conn.commit()
        return {"id": invoice_id, **invoice.dict()}
    except Exception as e:
        conn.rollback()
        raise HTTPException(status_code=400, detail=str(e))
    finally:
        cursor.close()
        conn.close()

async def get_invoice(invoice_id: int):
    conn = get_postgres_conn()
    cursor = get_postgres_cursor(conn)
    try:
        # Fetch invoice data
        cursor.execute("SELECT * FROM invoices WHERE id = %s", (invoice_id,))
        invoice = cursor.fetchone()
        if not invoice:
            raise HTTPException(status_code=404, detail="Invoice not found")

        # Fetch invoice items
        cursor.execute("SELECT * FROM invoice_items WHERE invoice_id = %s", (invoice_id,))
        items = cursor.fetchall()

        return {
            "invoice_id": invoice['id'],
            "user_id": invoice['user_id'],
            "items": [{
                "product_id": item['product_id'],
                "quantity": item['quantity'],
                "unit_price": item['unit_price']
            } for item in items],
            "total_amount": invoice['total_amount'],
            "currency": invoice['currency'],
            "issue_date": invoice['issue_date'].isoformat(),
            "due_date": invoice['due_date'].isoformat()
        }
    except Exception as e:
        raise HTTPException(status_code=400, detail=str(e))
    finally:
        cursor.close()
        conn.close()
