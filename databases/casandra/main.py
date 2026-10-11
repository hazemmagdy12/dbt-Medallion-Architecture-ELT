import time
from nosql.casandra.crud import setup_table, log_user_activity, get_user_history, update_user_activity, delete_user_activity

def main():    
    table = setup_table()
    
    print("\n--- Simulating User Activity ---")
    log_user_activity(table, user_id="user_123", action="view_item", burger_id="b1")
    time.sleep(1) 
    log_user_activity(table, user_id="user_123", action="add_to_cart", burger_id="b1")
    
    print("\n--- Displaying User History ---")
    cursor = table.find({"user_id": "user_123"})
    activities = list(cursor) 
    
    for row in activities:
        print(f"- Time: {row['activity_time']}, Action: {row['action']}, Item: {row['burger_id']}")
    
    
    if len(activities) > 0:
        oldest_activity_time = activities[-1]['activity_time']
        
        print("\n--- Updating Activity ---")

        update_user_activity(table, "user_123", oldest_activity_time, "view_item_and_liked")
        
        print("\n--- Deleting Activity ---")

        newest_activity_time = activities[0]['activity_time']
        delete_user_activity(table, "user_123", newest_activity_time)
        
        print("\n--- History After Update & Delete ---")
        get_user_history(table, "user_123")

    print("\n Phase 3 Full CRUD completed successfully!")

if __name__ == "__main__":
    main()