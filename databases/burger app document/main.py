from crud import insert_document, read_document, update_document, delete_document
#ملف التجربه
if __name__ == "__main__":
    print("Starting Burger App Data Store Operations...\n")

    document_data = {
        "burger_id": "b3",
        "name": "Truffle Mushroom Burger",
        "price": 14.00,
        "ingredients": ["beef", "swiss cheese", "truffle mayo", "mushrooms"],
        "visited": False
    }

    insert_document("burger_info", document_data)

    my_filter = {"burger_id": "b3"}
    
    read_document("burger_info", my_filter)

    update_document("burger_info", my_filter, {"price": 16.50})

    read_document("burger_info", my_filter)

    delete_document("burger_info" , my_filter)