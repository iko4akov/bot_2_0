import os
from dotenv import load_dotenv

load_dotenv()


# Settings parser
API_ID = os.getenv("APP_API_ID")
API_HASH = os.getenv("APP_API_HASH")
CHANNELS = [
    "@kosmo_off",
    "@okkosport"
]
