import motor.motor_asyncio
from core.config import settings
mongo_client = motor.motor_asyncio.AsyncIOMotorClient('mongos', 27017)

def get_database() -> motor.motor_asyncio.AsyncIOMotorDatabase:
    return mongo_client.get_database(settings.mongo.INITDB_DATABASE)

