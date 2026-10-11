import json
import os
from database import db 

def seed_mockaroo_to_graph():
    json_file = r"C:\Users\ABC Shop-eg\Downloads\graph_mockaroo.json"

    if not os.path.exists(json_file):
        print(f" File not found: {json_file}")
        return

    with open(json_file, 'r', encoding='utf-8') as file:
        mockaroo_data = json.load(file)

    print(f" Found {len(mockaroo_data)} records. Uploading to Neo4j using UNWIND...")

    cypher_query = """
    UNWIND $data_list AS row
    
    // أولاً: التأكد إن اليوزر موجود، لو مش موجود اعمله
    MERGE (u:User {name: row.user_name})
    
    // ثانياً: البحث عن العنصر اللي اشتراه (برجر أو طبق جانبي)
    WITH u, row
    MATCH (i {id: row.item_id})
    
    // ثالثاً: إنشاء علاقة الشراء وإضافة تاريخ الشراء عليها كـ Property
    CREATE (u)-[:BOUGHT {date: row.purchase_date}]->(i)
    """

    try:
        db.run_query(cypher_query, {"data_list": mockaroo_data})
        print(" All Mockaroo data successfully converted to Graph Nodes and Relationships!")
    except Exception as e:
        print(f" Error executing Cypher query: {e}")

if __name__ == "__main__":
    seed_mockaroo_to_graph()