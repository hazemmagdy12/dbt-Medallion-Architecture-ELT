import random
from faker import Faker
from datetime import timezone
from crud import setup_table

fake = Faker()

def seed_user_activity(num_records=300):
    table = setup_table()
    
    actions = ["view_menu", "view_item", "add_to_cart", "remove_from_cart", "checkout"]
    burger_ids = ["b1", "b2", "b3", "b4", "b5", "b6"]
    
    print(f" Starting to seed {num_records} activities into Cassandra (Astra DB)...")
    
    for i in range(num_records):

        user_id = f"user_{random.randint(1, 50)}" 
        
        action = random.choices(
            actions, 
            weights=[0.4, 0.3, 0.15, 0.05, 0.1], 
            k=1
        )[0]
        
        burger_id = random.choice(burger_ids) if action in ["view_item", "add_to_cart", "remove_from_cart"] else "N/A"
        
        random_days_ago = random.randint(0, 30)
        random_time = fake.date_time_between(start_date=f'-{random_days_ago}d', end_date='now', tzinfo=timezone.utc)
        
        table.insert_one({
            "user_id": user_id,
            "activity_time": random_time,
            "action": action,
            "burger_id": burger_id
        })
        
        if (i + 1) % 100 == 0:
            print(f" Inserted {i + 1} records...")

    print(" Seeding complete! Wide-Column table is now full.")

if __name__ == "__main__":
    seed_user_activity(300)