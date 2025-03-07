import os
from dotenv import load_dotenv

load_dotenv()


# For Bot
BOT_TOKEN=os.getenv('BOT_TOKEN')

# Settings parser
API_ID = os.getenv("APP_API_ID")
API_HASH = os.getenv("APP_API_HASH")

CHANNELS = [
    "@kosmo_off",
    "@okkosport"
]

# Database
POSTGRES_USER = os.getenv('POSTGRES_USER')
POSTGRES_PASS = os.getenv('POSTGRES_PASS')
POSTGRES_DB = os.getenv('POSTGRES_DB')
POSTGRES_HOST = os.getenv('POSTGRES_HOST')
POSTGRES_PORT = os.getenv('POSTGRES_PORT')

# Check admin
ADMINS = [os.getenv('ADMIN_TG1')]
