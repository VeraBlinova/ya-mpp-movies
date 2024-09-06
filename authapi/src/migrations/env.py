import asyncio
from logging.config import fileConfig

from alembic import context
from sqlalchemy import pool
from sqlalchemy.engine import Connection
from sqlalchemy.ext.asyncio import async_engine_from_config
from sqlmodel import SQLModel ## Updated: Import SQLModel

## Updated: Import authapi models
from models.role import Role
from models.user import User
from models.history import History

from core.config import settings as authapi_settings ## Updated: Import authapi_settings

# Alembic Config object
config = context.config
## Updated: get pg url from authapi_settings instead of url hardcoded in alembic.ini
config.set_main_option('sqlalchemy.url', authapi_settings.db.url)

# Logger setup
if config.config_file_name is not None:
    fileConfig(config.config_file_name)

# Models MetaData
target_metadata = SQLModel.metadata ## Updated: add authapi models metadata



def run_migrations_offline() -> None:
    """Run migrations in 'offline' mode.

    This configures the context with just a URL
    and not an Engine, though an Engine is acceptable
    here as well.  By skipping the Engine creation
    we don't even need a DBAPI to be available.

    Calls to context.execute() here emit the given string to the
    script output.

    """
    url = config.get_main_option('sqlalchemy.url')
    context.configure(
        url=url,
        target_metadata=target_metadata,
        literal_binds=True,
        dialect_opts={'paramstyle': 'named'},
        include_schemas=True,  # Added to create tables in custom schema
    )

    with context.begin_transaction():
        context.execute(
            f'create schema if not exists {target_metadata.schema};'
        )   # Added to create tables in custom schema
        context.execute(
            f'set search_path to {target_metadata.schema}'
        )   # Added to create tables in custom schema
        context.run_migrations()


def do_run_migrations(connection: Connection) -> None:
    context.configure(connection=connection, target_metadata=target_metadata)

    with context.begin_transaction():
        context.run_migrations()


async def run_async_migrations() -> None:
    """In this scenario we need to create an Engine
    and associate a connection with the context.

    """

    connectable = async_engine_from_config(
        config.get_section(config.config_ini_section, {}),
        prefix='sqlalchemy.',
        poolclass=pool.NullPool,
    )

    async with connectable.connect() as connection:
        await connection.run_sync(do_run_migrations)

    await connectable.dispose()


def run_migrations_online() -> None:
    """Run migrations in 'online' mode."""

    asyncio.run(run_async_migrations())


if context.is_offline_mode():
    run_migrations_offline()
else:
    run_migrations_online()
