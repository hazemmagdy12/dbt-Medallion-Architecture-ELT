import random
from cart_services import add_to_cart

USERS = [f"user_{i}" for i in range(1, 51)]

MENU_ITEMS = ["b1", "b2", "b3", "b4", "s1", "s2"]

def seed_redis_with_fake_carts():
    print(" Generating 50 active shopping carts in Redis...")
    
    total_items = 0
    for user_id in USERS:
        num_different_items = random.randint(1, 3)
        chosen_items = random.sample(MENU_ITEMS, num_different_items)
        
        for burger_id in chosen_items:
            quantity = random.randint(1, 4)
            
            add_to_cart(user_id, burger_id, quantity)
            total_items += 1
            
    print("=" * 50)
    print(f" Successfully created active carts for {len(USERS)} users.")
    print(f"Total unique items sitting in Redis carts right now: {total_items}")
    print("Hurry up! You have 1800 seconds before these carts vanish!")
    print("=" * 50)

if __name__ == "__main__":
    seed_redis_with_fake_carts()