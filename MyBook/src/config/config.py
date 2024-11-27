
POSTGRES_CONFIG = {
    "dbname": "mybook_db",
    "user": "zana",
    "password": "mybook_password",
    "host": "localhost",
    "port": "5432"
}

CASSANDRA_CONFIG = {
    "contact_points": ["localhost"],
    "port": 9042,
    "keyspace": "mybook"
}

KAFKA_CONFIG = {
    'bootstrap.servers': 'localhost:9092',
    'client.id': 'mybook-producer'
}

REDIS_CONFIG = {
    'host': 'localhost',
    'port': '6379',
    'db': '0'
}
