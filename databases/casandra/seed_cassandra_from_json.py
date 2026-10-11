import json
import os
from datetime import datetime, timezone
from crud import setup_table

def seed_mockaroo_to_cassandra():

    json_file = r"C:\Users\ABC Shop-eg\Downloads\MOCK_DATA.json"
    
    if not os.path.exists(json_file):
        print(" File 'MOCK_DATA.json' not found!")
        return

    with open(json_file, 'r', encoding='utf-8') as f:
        data = json.load(f)
        
    print(f" Found {len(data)} records. Fixing dates and connecting to Cassandra...")
    
    table = setup_table()
    
    for i, record in enumerate(data):

        raw_time = record.get("activity_time")
        if raw_time:
            try:
                parsed_date = datetime.strptime(raw_time, "%m/%d/%Y")
                record["activity_time"] = parsed_date.replace(tzinfo=timezone.utc).isoformat()
            except ValueError:
                pass # لو في مشكلة في قراءة التاريخ سيبه زي ما هو

        table.insert_one(record)     
        if (i + 1) % 20 == 0:
            print(f" Inserted {i + 1} records into Cassandra...")
            
    print(" All Mockaroo data is now live in Cassandra!")

if __name__ == "__main__":
    seed_mockaroo_to_cassandra()