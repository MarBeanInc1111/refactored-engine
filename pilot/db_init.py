# Import necessary modules
from dotenv import load_dotenv # Loads environment variables from .env file
import pydantic # Used for data validation
from motor.motor_asyncio import AsyncIOMotorClient # MongoDB driver for AsyncIO
from database.database import create_tables, drop_tables # Database management functions

# Load environment variables from .env file
load_dotenv()

# Drop and create tables in the database
drop_tables() # Drops all existing tables in the database
create_tables() # Creates all necessary tables in the database
