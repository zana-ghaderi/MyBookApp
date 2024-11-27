from confluent_kafka import Producer
import json

from Intuit.MyBook.src.config.config import KAFKA_CONFIG


def get_kafka_producer():
    return Producer(KAFKA_CONFIG)

def delivery_report(err, msg):
    if err is not None:
        print(f'Message delivery failed: {err}')
    else:
        print(f'Message delivered to {msg.topic()} [{msg.partition()}]')

def produce_kafka_message(producer, topic, key, value):
    producer.produce(
        topic,
        key=key,
        value=json.dumps(value),
        callback=delivery_report
    )
    producer.flush()