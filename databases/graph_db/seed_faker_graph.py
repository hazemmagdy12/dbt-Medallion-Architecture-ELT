from faker import Faker
import random
from database import db 

fake = Faker()

def seed_graph_with_faker():
    print(" Cleaning old Graph Data...")
    db.run_query("MATCH (n) DETACH DELETE n")

    print(" Inserting Standard Menu Items (Burgers & Sides)...")
    menu_items = [
        {"id": "b1", "name": "Classic Burger", "price": 5.99, "type": "Burger"},
        {"id": "b2", "name": "Cheese Burger", "price": 6.99, "type": "Burger"},
        {"id": "b3", "name": "Double Trouble", "price": 8.99, "type": "Burger"},
        {"id": "b4", "name": "Spicy Chicken", "price": 7.50, "type": "Burger"},
        {"id": "s1", "name": "Curly Fries", "price": 2.99, "type": "Side"},
        {"id": "s2", "name": "Onion Rings", "price": 3.50, "type": "Side"}
    ]
    
    for item in menu_items:
        query = f"""
        MERGE (i:{item['type']} {{id: $id}})
        SET i.name = $name, i.price = $price
        """
        db.run_query(query, item)

    print(" Generating 50 Fake Users and their Purchase Relationships...")
    items_ids = [item["id"] for item in menu_items]
    
    for _ in range(50):
        user_id = fake.uuid4()
        user_name = fake.first_name()
        
        create_user_query = "MERGE (u:User {id: $id}) SET u.name = $name"
        db.run_query(create_user_query, {"id": user_id, "name": user_name})
        
        num_purchases = random.randint(1, 5)
        purchased_items = random.sample(items_ids, num_purchases)
        
        for item_id in purchased_items:
            relation_query = """
            MATCH (u:User {id: $user_id})
            MATCH (i {id: $item_id}) 
            CREATE (u)-[:BOUGHT]->(i)
            """
            db.run_query(relation_query, {"user_id": user_id, "item_id": item_id})

    print(" Graph Database is now seeded with complex Faker relationships!")

if __name__ == "__main__":
    seed_graph_with_faker()