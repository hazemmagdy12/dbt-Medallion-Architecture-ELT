from os import getenv
from dotenv import load_dotenv
from astrapy import DataAPIClient

load_dotenv()

def get_db_connection():
    client = DataAPIClient()
    db = client.get_database(
        "https://401d1dfc-b4ce-4ae7-9351-fff6ed33ba9b-us-east-2.apps.astra.datastax.com",
        token=getenv("ASTRA_DB_TOKEN"),
        keyspace="BURGER"
    )
    return db

db = get_db_connection()