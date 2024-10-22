from motor.motor_asyncio import AsyncIOMotorClient
import os
from dotenv import load_dotenv
from bson import ObjectId


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

# Type definitions for MongoDB ObjectId handling
# PyObjectId = Annotated[str, BeforeValidator(str)]
# ObjectId = Annotated[
#     bson.ObjectId,
#     BeforeValidator(lambda x: bson.ObjectId(x) if isinstance(x, str) else x),
# ]

# Database helper functions
async def get_db():
    try:
        yield db
    finally:
        pass

async def get_or_create_entity(collection, filter_query, data):
    """
    Get an entity from MongoDB or create if it doesn't exist
    """
    entity = await collection.find_one(filter_query)
    if not entity:
        entity = await collection.insert_one(data)
        entity = await collection.find_one({"_id": entity.inserted_id})
    return entity

async def update_instance(collection, id, data):
    """
    Update a MongoDB document
    """
    update_result = await collection.update_one(
        {"_id": ObjectId(id)},
        {"$set": data}
    )
    return update_result