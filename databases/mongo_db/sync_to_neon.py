import os
import json
import psycopg2
from psycopg2.extras import execute_values
from dotenv import load_dotenv
from pymongo import MongoClient

load_dotenv()

NEON_DB_URL = os.getenv("NEON_DB_URL")
MONGO_URI = os.getenv("MONGO_URI", "mongodb://127.0.0.1:27017/")
MONGO_DB_NAME = "burger_app_db"

def extract_mongo_and_load_neon():
    if not NEON_DB_URL:
        print(" Error: NEON_DB_URL is missing from .env file!")
        return

    try:

        print(f" Extracting data from local MongoDB ({MONGO_DB_NAME} -> burgers)...")
        
        mongo_client = MongoClient(MONGO_URI)
        mongo_db = mongo_client[MONGO_DB_NAME]
        mongo_collection = mongo_db["burgers"]
        
        mongo_records = list(mongo_collection.find({}))
        
        if not mongo_records:
            print(" No data found in MongoDB. Please run the Mockaroo/Faker seed script first.")
            return

        for record in mongo_records:
            record["_id"] = str(record["_id"])

        print(f" Extracted and cleaned {len(mongo_records)} records from MongoDB successfully!")


        print(" Connecting to Neon PostgreSQL...")
        conn = psycopg2.connect(NEON_DB_URL)
        cursor = conn.cursor()

        print(" Creating Schema and Bronze Layer Table for MongoDB data...")
        create_table_query = """
        CREATE SCHEMA IF NOT EXISTS burger_app;
        
        CREATE TABLE IF NOT EXISTS burger_app.raw_mongo_burgers (
            id SERIAL PRIMARY KEY,
            mongo_payload JSONB,
            synced_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
        );
        """
        cursor.execute(create_table_query)
        conn.commit()

        print(" Loading data into Neon (Bulk Insert)...")
        insert_query = "INSERT INTO burger_app.raw_mongo_burgers (mongo_payload) VALUES %s"
        
        values_to_insert = [(json.dumps(record),) for record in mongo_records]
        
        execute_values(cursor, insert_query, values_to_insert)
        
        conn.commit()
        cursor.close()
        conn.close()
        print(" MongoDB data sync complete! Check 'raw_mongo_burgers' in Neon.")

    except Exception as e:
        print(f" Error during sync: {e}")

if __name__ == "__main__":
    extract_mongo_and_load_neon()