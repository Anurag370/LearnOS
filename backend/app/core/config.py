from functools import lru_cache

from pydantic_settings import BaseSettings, SettingsConfigDict

class Settings(BaseSettings):
    app_name:str = "LearnOS"
    app_env:str = "development"
    debug:bool = True

    database_url:str

    secret_key:str
    jwt_algorithm:str = "HS256"

    cors_origins:str = "http://localhost:3000"

    api_v1_prefix:str = "/api/v1"

    model_config = SettingsConfigDict(
        env_file = "../.env",
        env_file_encoding = "utf-8",
        extra = "ignore"
    )

    @property
    def cors_origins_list(self) -> list[str]:
        return [
            origin.strip() for origin in self.cors_origins.split(',') if origin.strip()
        ]

@lru_cache
def get_settings() -> Settings:
    return Settings() # type: ignore

settings = get_settings()