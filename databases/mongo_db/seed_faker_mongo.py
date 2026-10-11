import random
from faker import Faker
from pymongo.errors import BulkWriteError, OperationFailure
from database import get_database
from models import BurgerModel

fake = Faker()

BURGER_ADJECTIVES = ["Smash", "Classic", "Spicy", "Double", "Truffle", "BBQ", "Crispy", "Ultimate"]
BURGER_NOUNS = ["Burger", "Melt", "Delight", "Stack", "Bite", "Patty"]
POSSIBLE_INGREDIENTS = [
    "Beef Patty", "Chicken Breast", "Cheddar Cheese", "Swiss Cheese", 
    "Lettuce", "Tomato", "Onions", "Caramelized Onions", "Pickles", 
    "Jalapenos", "Bacon", "Mayo", "Ketchup", "Mustard", "BBQ Sauce", "Truffle Oil"
]

def generate_fake_burgers(num_records: int = 50):
    """
    دالة لتوليد داتا وهمية مطابقة تماماً للـ BurgerModel باستخدام Faker.
    """
    print(f" Generating {num_records} fake burger records...")
    fake_burgers = []
    
    for _ in range(num_records):
        name = f"{random.choice(BURGER_ADJECTIVES)} {random.choice(BURGER_NOUNS)}"
        
        num_ingredients = random.randint(2, 6)
        ingredients = random.sample(POSSIBLE_INGREDIENTS, num_ingredients)
        
        price = round(random.uniform(5.50, 24.99), 2)
        
        is_available = random.choices([True, False], weights=[0.85, 0.15])[0]
        
        try:
            burger_obj = BurgerModel(
                name=name,
                ingredients=ingredients,
                price=price,
                is_available=is_available
            )
            fake_burgers.append(burger_obj.model_dump())
            
        except Exception as validation_error:
            print(f" Validation error skipped: {validation_error}")
            
    return fake_burgers

def seed_mongo_with_faker():
    """
    دالة الاتصال بقاعدة بيانات MongoDB وإدخال البيانات المولدّة.
    """
    print(" Connecting to MongoDB...")
    try:
        db = get_database()
        burger_collection = db["burgers"]
        
        print(" Cleaning old data from 'burgers' collection...")
        burger_collection.delete_many({})
        
        data_to_insert = generate_fake_burgers(500)
        
        if not data_to_insert:
            print(" No valid data generated to insert.")
            return

        print(" Inserting data into MongoDB...")
        result = burger_collection.insert_many(data_to_insert)
        
        print(f" BOOM! Successfully inserted {len(result.inserted_ids)} burgers into MongoDB!")

    except BulkWriteError as bwe:
        print(f" Bulk write error occurred: {bwe.details}")
    except OperationFailure as op_err:
        print(f" Authentication or permission error: {op_err}")
    except Exception as e:
        print(f" An unexpected error occurred: {e}")

if __name__ == "__main__":
    seed_mongo_with_faker()