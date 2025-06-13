import os
from dotenv import load_dotenv

load_dotenv()

# API Key
API_KEY = os.getenv("API_KEY")

# DB Configuration
DB_HOST = os.getenv("DB_HOST")
DB_USER = os.getenv("DB_USER")
DB_PASSWORD = os.getenv("DB_PASSWORD")
DB_NAME = os.getenv("DB_NAME")

# Table Names
TABLE_FIRE_STATION = os.getenv("TABLE_FIRE_STATION")
TABLE_WILDFIRE = os.getenv("TABLE_WILDFIRE")
TABLE_MAPPING = os.getenv("TABLE_MAPPING")
