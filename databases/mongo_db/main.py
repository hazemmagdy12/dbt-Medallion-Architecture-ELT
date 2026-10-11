from fastapi import FastAPI
from database import get_database
from models import BurgerModel

app = FastAPI(title="Burger App API")

db = get_database()
burger_collection = db["burgers"]

@app.post("/burgers/")
def create_burger(burger: BurgerModel):
    burger_dict = burger.model_dump()
    
    result = burger_collection.insert_one(burger_dict)
    
    return {
        "message": "Burger added successfully", 
        "burger_id": str(result.inserted_id)
    }

@app.get("/burgers/")
def get_menu():
    cursor = burger_collection.find()
    
    menu = []
    for document in cursor:
        document["_id"] = str(document["_id"])
        menu.append(document)
        
    return {"menu": menu}