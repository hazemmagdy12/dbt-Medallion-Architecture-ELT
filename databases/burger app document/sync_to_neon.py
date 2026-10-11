import os
import json
import psycopg2
from dotenv import load_dotenv
from crud import get_all_documents 
from psycopg2.extras import execute_batch
load_dotenv()

NEON_DB_URL = os.getenv("NEON_DB_URL")

def extract_and_load():

    if not NEON_DB_URL:
        print(" Error: NEON_DB_URL is missing from .env file!")
        return

    try:

        print("Extracting data from DataStax Astra DB...")
        datastax_records = get_all_documents("burger_info")
        print(f" Extracted {len(datastax_records)} records successfully!")

        print("Connecting to Neon PostgreSQL...")
        conn = psycopg2.connect(NEON_DB_URL)
        cursor = conn.cursor()

        print("Creating Schema and Bronze Layer Table...")
        create_table_query = """
        CREATE SCHEMA IF NOT EXISTS burger_app;
        
        CREATE TABLE IF NOT EXISTS burger_app.raw_burger_orders (
            id SERIAL PRIMARY KEY,
            order_data JSONB,
            synced_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
        );
        """
        cursor.execute(create_table_query)
        conn.commit()

        print("Loading data into Neon in Batches...")
        insert_query = "INSERT INTO burger_app.raw_burger_orders (order_data) VALUES (%s)"

        records_to_insert = [[json.dumps(record)] for record in datastax_records]

        execute_batch(cursor, insert_query, records_to_insert, page_size=1000)

        conn.commit()
        cursor.close()
        conn.close()
        print(" Data sync complete! Welcome to the Bronze Layer.")

    except Exception as e:
        print(f" Error during sync: {e}")

if __name__ == "__main__":
    extract_and_load()