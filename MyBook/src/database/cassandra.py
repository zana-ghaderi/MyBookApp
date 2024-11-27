
from Intuit.MyBook.src.config.config import CASSANDRA_CONFIG
from cassandra.cluster import Cluster

def get_cassandra_session():
    cluster = Cluster(
        CASSANDRA_CONFIG["contact_points"],
        port=CASSANDRA_CONFIG["port"]
    )
    return cluster.connect(CASSANDRA_CONFIG["keyspace"])
