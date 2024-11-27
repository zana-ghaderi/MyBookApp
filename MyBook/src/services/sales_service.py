from fastapi import HTTPException
from Intuit.MyBook.src.database.postgres import get_postgres_conn, get_postgres_cursor
from Intuit.MyBook.src.kafka.kafka_producer import get_kafka_producer, produce_kafka_message
from Intuit.MyBook.src.models.sale import Sale
import logging

logger = logging.getLogger(__name__)

async def create_sale(sale: Sale):
    conn = get_postgres_conn()
    cursor = get_postgres_cursor(conn)
    try:
        cursor.execute(
            "INSERT INTO sales (user_id, total_amount, invoice_id) VALUES (%s, %s, %s) RETURNING id, sale_date",
            (sale.user_id, sale.total_amount, sale.invoice_id)
        )
        result = cursor.fetchone()
        sale_id = result['id']
        sale_date = result['sale_date']
        conn.commit()

        # Publish event to Kafka for real-time processing
        kafka_producer = get_kafka_producer()
        produce_kafka_message(
            kafka_producer,
            'sales-topic',
            str(sale_id),  # Use sale_id as the key
            {
                'sale_id': sale_id,
                'user_id': sale.user_id,
                'total_amount': float(sale.total_amount),
                'invoice_id': sale.invoice_id,
                'sale_date': sale_date.isoformat()
            }
        )

        return {
            "id": sale_id,
            "user_id": sale.user_id,
            "total_amount": float(sale.total_amount),
            "invoice_id": sale.invoice_id,
            "sale_date": sale_date
        }
    except Exception as e:
        conn.rollback()
        logger.error(f"Error creating sale: {e}")
        raise HTTPException(status_code=400, detail=f"Error creating sale: {str(e)}")
    finally:
        cursor.close()
        conn.close()