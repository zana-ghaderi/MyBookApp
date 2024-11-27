import json
import uuid
from fastapi import HTTPException
from Intuit.MyBook.src.database.cassandra import get_cassandra_session
from Intuit.MyBook.src.kafka.kafka_producer import get_kafka_producer, produce_kafka_message
from Intuit.MyBook.src.models.customer_profile import CustomerProfile

async def create_customer_profile(profile: CustomerProfile):
    session = get_cassandra_session()
    try:
        profile_id = uuid.uuid4()
        # Create profile in Cassandra
        session.execute(
            """
            INSERT INTO customer_profiles (id, user_id, preferences)
            VALUES (%s, %s, %s)
            """,
            (profile_id, profile.user_id, json.dumps(profile.preferences))
        )

        # Publish event to Kafka
        kafka_producer = get_kafka_producer()
        produce_kafka_message(
            kafka_producer,
            'customer-profiles-topic',
            str(profile_id),  # Use profile_id as the key
            {
                'id': str(profile_id),
                'user_id': profile.user_id,
                'preferences': profile.preferences
            }
        )

        return {"message": "Customer profile created successfully"}
    except Exception as e:
        raise HTTPException(status_code=400, detail=str(e))

async def get_customer_profile(user_id: int):
    session = get_cassandra_session()
    try:
        query = "SELECT * FROM customer_profiles WHERE user_id = %s ALLOW FILTERING"
        rows = session.execute(query, (user_id,))
        profile = rows.one()
        if profile:
            return {
                "id": str(profile.id),
                "user_id": profile.user_id,
                "preferences": json.loads(profile.preferences)
            }
        else:
            raise HTTPException(status_code=404, detail="Customer profile not found")
    except Exception as e:
        raise HTTPException(status_code=400, detail=str(e))
