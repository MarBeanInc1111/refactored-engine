# Import necessary modules
import asyncio
from dotenv import load_dotenv
import pydantic
from motor.motor_asyncio import AsyncIOMotorClient
from database.database import create_tables, drop_tables

# Load environment variables from .env file
load_dotenv()

# Connect to the database
client = AsyncIOMotorClient(pydantic.BaseSettings().MONGO_URL)
db = client.my_database

# Drop and create tables in the database
async def main():
    await drop_tables(db) # Drops all existing tables in the database
    await create_tables(db) # Creates all necessary tables in the database

# Run the main function asynchronously
asyncio.run(main())

