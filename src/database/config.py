from fastapi.security import APIKeyHeader, OAuth2PasswordBearer
import orjson
from sqlalchemy import create_engine
from sqlalchemy.ext.asyncio import create_async_engine

import pytz
import functools
import asyncio
from loguru import logger
import os
from dotenv import load_dotenv

load_dotenv(override=True)

INSTANCE_ID = 0
APP_TIMEZONE = "Europe/Moscow"

DATABASE_HOST = os.environ.get("DATABASE_HOST")
DATABASE_PORT = os.environ.get("DATABASE_PORT")
DATABASE_LOGIN = os.environ.get("DATABASE_LOGIN")
DATABASE_PASSWORD = os.environ.get("DATABASE_PASSWORD")
DATABASE_NAME = os.environ.get("DATABASE_NAME")

logger.info(f"postgresql+asyncpg://{DATABASE_LOGIN}:{DATABASE_PASSWORD}@{DATABASE_HOST}:{DATABASE_PORT}/{DATABASE_NAME}")

def database_url_asyncpg():
    return f"postgresql+asyncpg://{DATABASE_LOGIN}:{DATABASE_PASSWORD}@{DATABASE_HOST}:{DATABASE_PORT}/{DATABASE_NAME}"

app_timezone = pytz.timezone(APP_TIMEZONE)
database_engine = create_engine(
    f"postgresql+psycopg2://{DATABASE_LOGIN}:{DATABASE_PASSWORD}@{DATABASE_HOST}:{DATABASE_PORT}/{DATABASE_NAME}",
    json_serializer=orjson.dumps,
    json_deserializer=orjson.loads,
)
database_engine_async = create_async_engine(
    # f"postgresql+asyncpg://{DATABASE_LOGIN}:{DATABASE_PASSWORD}@{DATABASE_HOST}:{DATABASE_PORT}/{DATABASE_NAME}",
    database_url_asyncpg(),
    json_serializer=orjson.dumps,
    json_deserializer=orjson.loads,
)

def retry_async(num_attempts):
    def decorator(func):
        @functools.wraps(func)
        async def wrapper(*args, **kwargs):
            for try_index in range(num_attempts + 1):
                try:
                    return await func(*args, **kwargs)
                except Exception as e:
                    if try_index == num_attempts:
                        raise e
                    print(
                        f"Exception occurred: {e}. Retrying... ({try_index + 1}/{num_attempts})"
                    )
                    await asyncio.sleep(1)

        return wrapper

    return decorator
