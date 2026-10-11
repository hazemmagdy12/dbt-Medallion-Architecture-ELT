from database import db

def insert_document(collection_name, document_data):
    collection = db.get_collection(collection_name)
    result = collection.insert_one(document_data)
    print(result.inserted_id)

def read_document(collection_name, filter_query={}):
    collection = db.get_collection(collection_name)
    result = collection.find(filter_query)
    print(collection_name)
    for doc in result:
        print(doc)
    print("-----------------------------------")

def update_document(collection_name, filter_query, updated_data):
    collection = db.get_collection(collection_name)
    result = collection.update_one(filter_query, {"$set": updated_data})
    print(result.update_info)

def delete_document(collection_name, filter_query):
    collection = db.get_collection(collection_name)
    result = collection.delete_one(filter_query)
    print(result.deleted_count)

def get_all_documents(collection_name):
    collection = db.get_collection(collection_name)
    result=collection.find()
    return list(result)

def get_documents_in_batches(collection_name, batch_size=1000):
    collection = db.get_collection(collection_name)
    cursor = collection.find() 
    batch = [] 
    for doc in cursor:
        batch.append(doc) # حط السطر في الجردل
        if len(batch) == batch_size:
            yield batch  # ييلد: يعني "خد الجردل ده يا باشا، وأنا هوقف شغل واستناك"
            batch = []   # أول ما ترجعلي، هفضي الجردل عشان أملاه من جديد للفة الجاية           
    if batch:
        yield batch