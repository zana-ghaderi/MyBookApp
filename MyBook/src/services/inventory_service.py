from fastapi import HTTPException
from datetime import datetime
import logging

from Intuit.MyBook.src.database.postgres import get_postgres_conn, get_postgres_cursor
from Intuit.MyBook.src.kafka.kafka_producer import get_kafka_producer, produce_kafka_message
from Intuit.MyBook.src.models.inventory import InventoryItem

logger = logging.getLogger(__name__)

async def update_inventory(item: InventoryItem):
    conn = get_postgres_conn()
    cursor = get_postgres_cursor(conn)
    kafka_producer = get_kafka_producer()

    try:
        cursor.execute(
            """
            INSERT INTO inventory (product_id, quantity, location, currency) 
            VALUES (%s, %s, %s, %s)
            ON CONFLICT (product_id) 
            DO UPDATE SET 
                quantity = inventory.quantity + EXCLUDED.quantity,
                location = EXCLUDED.location,
                currency = EXCLUDED.currency
            RETURNING *
            """,
            (item.product_id, item.quantity, item.location, item.currency)
        )
        updated_item = cursor.fetchone()
        conn.commit()

        # Publish event to Kafka for real-time insights
        produce_kafka_message(
            kafka_producer,
            'inventory-topic',
            str(item.product_id),  # Use product_id as the key
            {
                'product_id': item.product_id,
                'quantity': item.quantity,
                'location': item.location,
                'currency': item.currency,
                'timestamp': datetime.now().isoformat()
            }
        )

        return updated_item
    except Exception as e:
        conn.rollback()
        logger.error(f"Error updating inventory: {e}")
        raise HTTPException(status_code=400, detail="Error updating inventory")
    finally:
        cursor.close()
        conn.close()
