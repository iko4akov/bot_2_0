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

# CREATE_USER_COMMAND = """
# DO $$
# BEGIN
#     IF NOT EXISTS (SELECT FROM pg_catalog.pg_roles WHERE rolname = '{username}') THEN
#         EXECUTE format('CREATE USER %I WITH PASSWORD %L', '{username}', '{password}');
#     END IF;
# END
# $$;
# """
#
# CHECK_DB_COMMAND = """
#     DO $$
#     BEGIN
#         IF EXISTS (SELECT FROM pg_database WHERE datname = '{dbname}') THEN
#             RAISE NOTICE EXECUTE format ("Database already exists %'", '{dbname}')
#     END
# """
#
# CREATE_DB_COMMAND = """
# DO $$
# BEGIN
#     IF NOT EXISTS (SELECT FROM pg_database WHERE datname = '{dbname}') THEN
#         EXECUTE format('CREATE DATABASE %I OWNER %L', '{dbname}', '{username}');
#     END IF;
# END
# $$;
# """

# Команды для создания пользователя и базы данных
CREATE_USER_COMMAND = """
DO $$
BEGIN
    IF NOT EXISTS (SELECT FROM pg_catalog.pg_roles WHERE rolname = '{username}') THEN
        EXECUTE format('CREATE USER %I WITH PASSWORD %L', '{username}', '{password}');
    END IF;
END
$$;
"""

CREATE_DB_COMMAND = """
DO $$
BEGIN
    IF NOT EXISTS (SELECT FROM pg_database WHERE datname = '{dbname}') THEN
        RAISE NOTICE 'Creating database: %', '{dbname}';
    END IF;
END
$$;
"""

CREATE_DB_RAW_COMMAND = "CREATE DATABASE {dbname} OWNER {username};"