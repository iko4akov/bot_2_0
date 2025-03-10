from settings.config import POSTGRES_ADMIN_USER, POSTGRES_HOST, POSTGRES_PORT, POSTGRES_ADMIN_DB, POSTGRES_USER, \
    POSTGRES_PASS, POSTGRES_DB


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

# create_user_command = f"CREATE USER {POSTGRES_USER} WITH PASSWORD '{POSTGRES_PASS}';"
#
# create_db_command = f"CREATE DATABASE {POSTGRES_DB} OWNER {POSTGRES_USER};"

CREATE_USER_COMMAND = """
DO $$
BEGIN
    IF NOT EXISTS (SELECT FROM pg_catalog.pg_roles WHERE rolname = '{username}') THEN
        CREATE USER "{username}" WITH PASSWORD '{password}';
    END IF;
END
$$;
"""

CREATE_DB_COMMAND = """
DO $$
BEGIN
    IF NOT EXISTS (SELECT FROM pg_database WHERE datname = '{dbname}') THEN
        CREATE DATABASE "{dbname}" OWNER "{username}";
    END IF;
END
$$;
"""
