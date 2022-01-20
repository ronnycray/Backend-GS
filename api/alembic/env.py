import asyncio
import pkgutil
import importlib
from logging.config import fileConfig

import services
from services.config import get_settings
from services.database import BaseModel

from sqlalchemy import engine_from_config
from sqlalchemy import pool
from sqlalchemy.ext.asyncio import AsyncEngine

from alembic import context


# initialize all the modules
for loader, module_name, is_pkg in pkgutil.walk_packages(services.__path__, services.__name__ + '.'):
    if is_pkg:
        # TODO: use logging
        try:
            print(f"Trying to import {module_name + '.models'}")
            importlib.import_module(module_name + '.models')
        except ModuleNotFoundError as e:
            print(f"Failed to import {module_name + '.models'}, error: {e}")
        else:
            print(f"Imported {module_name + '.models'}")


# this is the Alembic Config object, which provides
# access to the values within the .ini file in use.
config = context.config
# this will overwrite the ini-file sqlalchemy.url path
# with the path given in the config of the main code
print("DATABSE URL:", get_settings().database_url)
config.set_main_option("sqlalchemy.url", get_settings().database_url)

# Interpret the config file for Python logging.
# This line sets up loggers basically.
fileConfig(config.config_file_name)

# add your model's MetaData object here
# for 'autogenerate' support
# from myapp import mymodel
# target_metadata = mymodel.Base.metadata
target_metadata = BaseModel.metadata

# other values from the config, defined by the needs of env.py,
# can be acquired:
# my_important_option = config.get_main_option("my_important_option")
# ... etc.


def process_revision_directives(context, revision, directives):
    if config.cmd_opts.autogenerate:
        script = directives[0]
        if script.upgrade_ops.is_empty():
            directives[:] = []


def run_migrations_offline():
    """Run migrations in 'offline' mode.
    This configures the context with just a URL
    and not an Engine, though an Engine is acceptable
    here as well.  By skipping the Engine creation
    we don't even need a DBAPI to be available.
    Calls to context.execute() here emit the given string to the
    script output.
    """
    url = config.get_main_option("sqlalchemy.url")
    context.configure(
        url=url,
        target_metadata=target_metadata,
        literal_binds=True,
        dialect_opts={"paramstyle": "named"},
    )

    with context.begin_transaction():
        context.run_migrations()


def do_run_migrations(connection):
    context.configure(connection=connection, target_metadata=target_metadata)

    with context.begin_transaction():
        context.run_migrations()


async def run_migrations_online():
    """Run migrations in 'online' mode.
    In this scenario we need to create an Engine
    and associate a connection with the context.
    """
    connectable = AsyncEngine(
        engine_from_config(
            config.get_section(config.config_ini_section),
            prefix="sqlalchemy.",
            poolclass=pool.NullPool,
            future=True,
        )
    )

    async with connectable.connect() as connection:
        await connection.run_sync(do_run_migrations)


if context.is_offline_mode():
    run_migrations_offline()
else:
    asyncio.run(run_migrations_online())
