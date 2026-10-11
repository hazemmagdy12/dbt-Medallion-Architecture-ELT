from db_connection import get_redis_conniction

redis_db = get_redis_conniction()

def add_to_cart(user_id, burger_id, quantity=1):

    cart_key = f"cart:{user_id}"
    
    redis_db.hincrby(cart_key, burger_id, quantity)
    
    redis_db.expire(cart_key, 1800)# العربيه هتتمسح بعد نص ساعه
    
    print(quantity, burger_id ,user_id)

################################################################################
def view_cart(user_id):
    cart_key = f"cart:{user_id}"
    
    cart_items = redis_db.hgetall(cart_key)
    
    if not cart_items:
        print(f"Empty cart:  {user_id}")
    else:
        print(user_id)
        for burger, qty in cart_items.items():
            print(f"item:{burger} quantty: {qty}")
#==========================================================================================
def remove_from_cart(user_id, burger_id):
    cart_key = f"cart:{user_id}"
    
    redis_db.hdel(cart_key, burger_id)
#=================================================================
def clear_cart(user_id):
    cart_key = f"cart:{user_id}"
    
    redis_db.delete(cart_key)


if __name__ == "__main__":
    add_to_cart("user_101", "burger_5", 2)

    add_to_cart("user_101", "burger_2", 1)
    
    view_cart("user_101")
    
    remove_from_cart("user_101", "burger_2")
    
    view_cart("user_101")
    
    clear_cart("user_101")
    
    view_cart("user_101")