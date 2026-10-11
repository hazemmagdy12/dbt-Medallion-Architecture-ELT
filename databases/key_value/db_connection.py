import os
from dotenv import load_dotenv
import redis
load_dotenv()

def get_redis_conniction():
    r= redis.Redis(
        host=os.getenv("REDIS_HOST"),
        port=os.getenv("REDIS_PORT"),
        password=os.getenv("REDIS_PASSWORD"),
        decode_responses=True
    )
    return r
if __name__ == "__main__":
    try:
        r_db = get_redis_conniction()
        r_db.ping() 
        print("Connected to Redis successfully!")
    except Exception as e:
        print(f"Error connecting to Redis: {e}")