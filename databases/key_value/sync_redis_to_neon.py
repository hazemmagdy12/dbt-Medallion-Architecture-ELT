import os
import json
import psycopg2
from psycopg2.extras import execute_values
from dotenv import load_dotenv
from db_connection import get_redis_conniction

load_dotenv()
NEON_DB_URL = os.getenv("NEON_DB_URL")

def extract_redis_carts_and_load_neon():
    if not NEON_DB_URL:
        print(" Error: NEON_DB_URL is missing from .env file!")
        return

    redis_client = None
    conn = None

    try:

        print(" Scanning Redis for active shopping carts before they expire...")
        redis_client = get_redis_conniction()
        
        cart_keys = redis_client.keys("cart:*")
        
        if not cart_keys:
            print("No active carts found in Redis! The 1800 seconds might be up, or the Faker script didn't run.")
            return
            
        redis_records = []
        for key in cart_keys:
            user_id = key.split(":")[1]
            
            cart_data = redis_client.hgetall(key)
            
            payload = {
                "user_id": user_id,
                "cart_items": cart_data
            }
            redis_records.append(payload)
            
        print(f" Snatched {len(redis_records)} active carts from Redis successfully!")

        print(" Connecting to Neon PostgreSQL...")
        conn = psycopg2.connect(NEON_DB_URL)
        cursor = conn.cursor()

        print(" Creating Bronze Layer Table for Redis Carts...")
        create_table_query = """
        CREATE SCHEMA IF NOT EXISTS burger_app;
        
        CREATE TABLE IF NOT EXISTS burger_app.raw_redis_carts (
            id SERIAL PRIMARY KEY,
            cart_payload JSONB,
            captured_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
        );
        """
        cursor.execute(create_table_query)
        conn.commit()

        print(" Loading Cart data into Neon (Bulk Insert)...")
        insert_query = "INSERT INTO burger_app.raw_redis_carts (cart_payload) VALUES %s"
        
        values_to_insert = [(json.dumps(record),) for record in redis_records]
        
        execute_values(cursor, insert_query, values_to_insert)
        
        conn.commit()
        print(" Redis carts successfully rescued and dumped into Neon's Bronze Layer!")

    except Exception as e:
        print(f" Error during sync: {e}")
    finally:
        if conn:
            cursor.close()
            conn.close()
            print(" Neon Database connection closed safely.")

if __name__ == "__main__":
    extract_redis_carts_and_load_neon()