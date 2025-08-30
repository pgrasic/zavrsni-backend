import sys
import os

# Add the parent directory of 'src' to sys.path to allow absolute imports like 'src.models.user'
# This ensures that when you import src.models.*, Python knows where 'src' is.
# Assuming env.py is in alembic/env.py, and src is in the project root.
# Example: C:\Users\User\Desktop\Zavrsni\Backend\zavrsni-backend\alembic\env.py
# So, os.path.dirname(__file__) is ...\alembic
# os.path.dirname(os.path.dirname(__file__)) is ...\zavrsni-backend
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))


from logging.config import fileConfig

from sqlalchemy import engine_from_config
from sqlalchemy import pool

from alembic import context

# this is the Alembic Config object, which provides
# access to the values within the .ini file in use.
config = context.config

# Interpret the config file for Python logging.
if config.config_file_name is not None:
    fileConfig(config.config_file_name)

from dotenv import load_dotenv
load_dotenv()

# ====================================================================
# CRITICAL SECTION FOR ALMBIC MODEL DISCOVERY
# --------------------------------------------------------------------

# 1. Import your 'Base' object correctly.
#    Assuming 'src/models/base.py' contains `Base = declarative_base()`.
#    We need to import *that specific Base instance*.
from src.models.base import Base # <--- This is the crucial change!

# 2. Import all your model modules AFTER Base is defined/imported.
#    This makes sure that when your models do `from .base import Base`,
#    they are getting the same Base object whose metadata we want to inspect.
#    By importing them here, their table definitions get registered with Base.metadata.
import src.models.user
import src.models.lijek
import src.models.djelatna_tvar
import src.models.vezne_tablice
import src.models.kategorije
# Add any other model imports here as you create them.

# 3. Set target_metadata to the metadata of the SINGLE Base instance.
target_metadata = Base.metadata

# Print to confirm models are being registered
print("Tables in Base metadata:", target_metadata.tables.keys())

# ====================================================================


def get_url():
    DB_USER = os.getenv("DB_USER")
    DB_PASSWORD = os.getenv("DB_PASSWORD")
    DB_HOST = os.getenv("DB_HOST", "localhost")
    DB_PORT = os.getenv("DB_PORT", "5432")
    DB_NAME = os.getenv("DB_NAME")
    return f"postgresql+psycopg2://{DB_USER}:{DB_PASSWORD}@{DB_HOST}:{DB_PORT}/{DB_NAME}"

def run_migrations_offline() -> None:
    url = get_url()
    context.configure(
        url=url,
        target_metadata=target_metadata,
        literal_binds=True,
        dialect_opts={"paramstyle": "named"},
    )
    with context.begin_transaction():
        context.run_migrations()


def run_migrations_online() -> None:
    connectable = engine_from_config(
        {"sqlalchemy.url": get_url()},
        prefix="sqlalchemy.",
        poolclass=pool.NullPool,
    )
    with connectable.connect() as connection:
        context.configure(
            connection=connection, target_metadata=target_metadata
        )
        with context.begin_transaction():
            context.run_migrations()


if context.is_offline_mode():
    run_migrations_offline()
else:
    run_migrations_online()