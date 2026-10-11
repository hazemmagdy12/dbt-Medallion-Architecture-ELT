import os
import json
import psycopg2
from psycopg2.extras import execute_values
from dotenv import load_dotenv
from neo4j import GraphDatabase

load_dotenv()

NEON_DB_URL = os.getenv("NEON_DB_URL")
NEO4J_URI = os.getenv("NEO4J_URI")
NEO4J_USERNAME = os.getenv("NEO4J_USERNAME") 
NEO4J_PASSWORD = os.getenv("NEO4J_PASSWORD")

def extract_neo4j_and_load_neon():
    if not NEON_DB_URL or not NEO4J_URI or not NEO4J_USERNAME or not NEO4J_PASSWORD:
        print("Error: Missing Database Credentials in .env file!")
        return

    neo4j_driver = None
    conn = None

    try:
        neo4j_driver = GraphDatabase.driver(NEO4J_URI, auth=(NEO4J_USERNAME, NEO4J_PASSWORD))
        
        extract_query = """
        MATCH (u:User)-[r:BOUGHT]->(i)
        RETURN u.name AS user_name, r.date AS purchase_date, i.id AS item_id
        """
        
        neo4j_records = []
        with neo4j_driver.session() as session:
            result = session.run(extract_query)
            for record in result:
                neo4j_records.append({
                    "user_name": record["user_name"],
                    "purchase_date": record["purchase_date"],
                    "item_id": record["item_id"]
                })

        if not neo4j_records:
            print("No data found in Neo4j. Did you run the graph seed script?")
            return

        print(f" Extracted {len(neo4j_records)} relationships (User -> BOUGHT -> Item) successfully!")

        conn = psycopg2.connect(NEON_DB_URL)
        cursor = conn.cursor()

        create_table_query = """
        CREATE SCHEMA IF NOT EXISTS burger_app;
        
        CREATE TABLE IF NOT EXISTS burger_app.raw_neo4j_graph (
            id SERIAL PRIMARY KEY,
            graph_payload JSONB,
            synced_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
        );
        """
        cursor.execute(create_table_query)
        conn.commit()

        print("Loading Graph data into Neon (Bulk Insert)...")
        insert_query = "INSERT INTO burger_app.raw_neo4j_graph (graph_payload) VALUES %s"
        
        values_to_insert = [(json.dumps(record),) for record in neo4j_records]
        
        execute_values(cursor, insert_query, values_to_insert)
        
        conn.commit()
        print(" Neo4j data sync complete! Check 'raw_neo4j_graph' in Neon.")

    except Exception as e:
        print(f" Error during sync: {e}")
    finally:
        if neo4j_driver:
            neo4j_driver.close()
        if conn:
            cursor.close()
            conn.close()

if __name__ == "__main__":
    extract_neo4j_and_load_neon()