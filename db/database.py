from motor.motor_asyncio import AsyncIOMotorClient
import os
from dotenv import load_dotenv


load_dotenv()

def get_db_client():
    MONGO_URL = os.getenv("MONGO_URL")
    client = AsyncIOMotorClient(MONGO_URL)
    return client

# Get database
db = get_db_client().hasken_rayuwa


# Collections
states_collection = db.states
filmshow_collection = db.filmshows
discipleship_collection = db.discipleships
users_collection = db.users
links_collection = db.links
blogs_collection = db.blogs

async def get_db():
    try:
        yield db
    finally:
        pass

