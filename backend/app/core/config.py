from functools import lru_cache

from pydantic_settings import BaseSettings, SettingsConfigDict

class Settings(BaseSettings):
    app_name:str = "LearnOS"
    app_env:str = "development"
    debug:bool = True

    database_url:str

    secret_key:str
    jwt_algorithm:str = "HS256"

    model_config = SettingsConfigDict(
        env_file = "../.env",
        env_file_encoding = "utf-8",
        extra = "ignore"
    )


@lru_cache
def get_settings() -> Settings:
    return Settings() # type: ignore

settings = get_settings()