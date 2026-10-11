import json
from crud import insert_document

def load_json_to_db(file_path):
    print(f"Loading data from {file_path}...")
    try:
        with open(file_path, 'r', encoding='utf-8') as f:
            data = json.load(f)           
            if isinstance(data, list):
                for item in data:
                    item["source_type"] = "json_imported"
                    insert_document("burger_info", item)
            else:
                data["source_type"] = "json_imported"
                insert_document("burger_info", data)
                
        print("JSON data successfully loaded to Astra DB!")
    except Exception as e:
        print(f"Error loading JSON: {e}")

if __name__ == "__main__":
    load_json_to_db(r"C:\Users\ABC Shop-eg\Downloads\burger_info.json")
    