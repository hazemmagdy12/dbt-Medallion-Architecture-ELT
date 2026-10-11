import random
from faker import Faker
from crud import insert_document

fake = Faker()

def generate_faker_burgers(num_records=30):
    ingredients_pool = ["beef", "chicken", "swiss cheese", "cheddar", "truffle mayo", "mushrooms", "lettuce", "tomato", "bacon", "onions", "jalapeno"]
    burger_names = ["Classic Burger", "Truffle Mushroom Burger", "Spicy Chicken", "Double BBQ", "Veggie Delight", "Mega Bacon Burger"]
    
    print(f"Generating {num_records} records using Faker...")
    
    for _ in range(num_records):
        document_data = {
            "source_type": "faker_generated",
            "burger_id": f"b_fk_{fake.unique.random_int(min=100, max=999)}",
            "name": random.choice(burger_names),
            "price": round(random.uniform(6.0, 22.0), 2),
            "ingredients": random.sample(ingredients_pool, random.randint(2, 5)),
            "is_spicy": fake.boolean(),
            "customer_info": {
                "name": fake.name(),
                "email": fake.email(),
                "city": fake.city()
            },
            "order_date": fake.date_time_this_year().isoformat()
        }
        insert_document("burger_info", document_data)
        
    print("Faker data generation complete!")

if __name__ == "__main__":
    generate_faker_burgers()