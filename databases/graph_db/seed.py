from nosql.graph_db.database import db

def seed_database():
    print(" Seeding Graph Database with Burgers and Users...")
    
    print(" Cleaning old data...")
    clear_query = "MATCH (n) DETACH DELETE n"
    db.run_query(clear_query)
    
    print(" Inserting new nodes and relationships...")
    insert_query = """
    CREATE (b1:Burger {id: 'b1', name: 'Classic Burger', price: 5.99})
    CREATE (b2:Burger {id: 'b2', name: 'Cheese Burger', price: 6.99})
    CREATE (s1:Side {id: 's1', name: 'Curly Fries', price: 2.99})
    
    CREATE (u1:User {id: 'u1', name: 'Hazem'})
    CREATE (u2:User {id: 'u2', name: 'Ahmed'})
    
    CREATE (u1)-[:BOUGHT]->(b1)
    CREATE (u1)-[:BOUGHT]->(s1)
    CREATE (u2)-[:BOUGHT]->(b1)
    CREATE (u2)-[:BOUGHT]->(b2)
    """
    db.run_query(insert_query)
    
    print("Graph populated successfully!")

if __name__ == "__main__":
    seed_database()