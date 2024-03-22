# Import necessary modules
import asyncio
from dotenv import load_dotenv
import pydantic
from motor.motor_asyncio import AsyncIOMotorClient
from database.database import create_tables, drop_tables

# Load environment variables from .env file
load_dotenv()

# Connect to the database
class DatabaseConfig(pydantic.BaseSettings):
    MONGO_URL: str

db_config = DatabaseConfig()
client = AsyncIOMotorClient(db_config.MONGO_URL)
db = client.my_database

# Drop and create tables in the database
async def main():
    try:
        await drop_tables(db) # Drops all existing tables in the database
    except Exception as e:
        print(f"Error dropping tables: {e}")
    
    try:
        await create_tables(db) # Creates all necessary tables in the database
    except Exception as e:
        print(f"Error creating tables: {e}")

# Run the main function asynchronously
try:
    asyncio.run(main())
except KeyboardInterrupt:
    print("Shutting down...")
    client.close()
    await client.wait_closed()
