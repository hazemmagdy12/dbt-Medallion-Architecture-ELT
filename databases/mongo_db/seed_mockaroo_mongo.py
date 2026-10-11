import json
import os
from database import get_database
from models import BurgerModel
from pymongo.errors import BulkWriteError

def seed_mongo_with_mockaroo():
    json_file = r"C:\Users\ABC Shop-eg\Downloads\mongo.json"
    
    if not os.path.exists(json_file):
        print(f" File not found: {json_file}")
        return

    with open(json_file, 'r', encoding='utf-8') as file:
        mockaroo_data = json.load(file)
        
    print(f"Found {len(mockaroo_data)} records in Mockaroo file.")

    valid_data = []
    for item in mockaroo_data:
        if "ingredients[]" in item:
            item["ingredients"] = item.pop("ingredients[]")
            
        raw_ing = item.get("ingredients")
        if isinstance(raw_ing, str):
            item["ingredients"] = [raw_ing, "Special Burger Sauce"]
        elif not raw_ing:
            item["ingredients"] = ["Beef Patty", "Cheese"]

        try:
            burger_obj = BurgerModel(**item)
            valid_data.append(burger_obj.model_dump())
        except Exception as e:
            print(f" Skipping invalid record. Validation error: {e}")

    if not valid_data:
        print(" No valid data to insert.")
        return

    try:
        db = get_database()
        burger_collection = db["burgers"]
        
        print(" Inserting Mockaroo data into MongoDB...")
        result = burger_collection.insert_many(valid_data)
        
        print(f" Successfully inserted {len(result.inserted_ids)} Mockaroo burgers into MongoDB!")
        
    except BulkWriteError as bwe:
        print(f" Bulk write error: {bwe.details}")
    except Exception as e:
        print(f" Error: {e}")
if __name__ == "__main__":
    seed_mongo_with_mockaroo()