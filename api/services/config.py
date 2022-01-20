from pydantic import BaseSettings
from functools import lru_cache
import os

print(os.environ)


class Settings(BaseSettings):
    app_url: str = os.environ.get(key='API_URL', default='http://127.0.0.1:8000')
    database_url: str = os.environ.get(
        key='DATABASE_URL',
        default="postgresql+asyncpg://dev_user:11991199@postgres:5436/dev_gainsystem_db"
    )
    secret_key = os.environ.get(
        key='SECRET_KEY',
        default="mC*A`a!UOOgRX8'(8K'iTf.=FX&Zbr3`l@YcadME}4AoM5]eBJnVqyA:%L0KTh<"
    )
    echo_db: bool = True if os.environ.get(key='ECHO_DB') == 'True' else False
    access_token_expire_minutes: int = os.environ.get(key='ACCESS_TOKEN_EXPIRE_MINUTES', default=30)
    refresh_token_expire_minutes: int = os.environ.get(key='REFRESH_TOKEN_EXPIRE_MINUTES', default=43200)
    algorithm: str = os.environ.get(key='ALGORITHM', default='HS256')
    bytes_refresh_token: int = int(os.environ.get(key='BYTES_REFRESH_TOKEN', default=100))
    length_google_uid = 40
    limit_entropy = 0.5
    length_device_id = 100


@lru_cache()
def get_settings() -> Settings:
    return Settings()
