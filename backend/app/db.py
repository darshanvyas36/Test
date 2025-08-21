from motor.motor_asyncio import AsyncIOMotorClient, AsyncIOMotorDatabase
from .core.config import MONGO_CONNECTION_STRING, DATABASE_NAME

class DBMeta(type):
    _instances = {}
    def __call__(cls, *args, **kwargs):
        if cls not in cls._instances:
            cls._instances[cls] = super(DBMeta, cls).__call__(*args, **kwargs)
        return cls._instances[cls]

class DatabaseClient(metaclass=DBMeta):
    client: AsyncIOMotorClient = None
    db: AsyncIOMotorDatabase = None

db_client = DatabaseClient()

async def connect_to_mongo():
    """
    Establishes the connection to the MongoDB database using an async client.
    """
    print("Connecting to async MongoDB...")
    try:
        db_client.client = AsyncIOMotorClient(MONGO_CONNECTION_STRING)
        db_client.db = db_client.client[DATABASE_NAME]
        await db_client.client.admin.command('ping')
        print("Successfully connected to async MongoDB!")
    except Exception as e:
        print(f"Error connecting to async MongoDB: {e}")
        raise

def close_mongo_connection():
    """
    Closes the connection to the MongoDB database.
    """
    if db_client.client:
        print("Closing async MongoDB connection...")
        db_client.client.close()
        print("Async MongoDB connection closed.")

def get_database() -> AsyncIOMotorDatabase:
    """
    Returns the database instance.
    """
    if db_client.db is None:
        raise Exception("Database not connected. The application might not have started correctly.")
    return db_client.db
