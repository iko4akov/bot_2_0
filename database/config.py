from settings.config import POSTGRES_ADMIN_USER, POSTGRES_HOST, POSTGRES_PORT, POSTGRES_ADMIN_DB, POSTGRES_USER, \
    POSTGRES_PASS, POSTGRES_DB

# URL for connect to DB
admin_url_db = f"postgresql+asyncpg://" \
               f"{POSTGRES_ADMIN_USER}@" \
               f"{POSTGRES_HOST}:" \
               f"{POSTGRES_PORT}/" \
               f"{POSTGRES_ADMIN_DB}"


bot_url_db = f"postgresql+asyncpg://" \
               f"{POSTGRES_USER}:" \
               f"{POSTGRES_PASS}@" \
               f"{POSTGRES_HOST}:" \
               f"{POSTGRES_PORT}/" \
               f"{POSTGRES_DB}"


#Commands create DB
CHECK_USER_COMMAND = "SELECT 1 FROM pg_catalog.pg_roles WHERE rolname = :username"
CREATE_USER_COMMAND = "CREATE USER {username} WITH PASSWORD '{password}';"

CHECK_DB_COMMAND = "SELECT 1 FROM pg_database WHERE datname = :dbname"
CREATE_DB_COMMAND = "CREATE DATABASE {dbname} OWNER {username};"
