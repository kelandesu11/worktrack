from functools import lru_cache

from pydantic import AliasChoices, Field
from pydantic_settings import BaseSettings, SettingsConfigDict


class Settings(BaseSettings):
    database_url: str = Field(
        default="postgresql+psycopg://postgres:Km15578!@db:5432/worktrack",
        validation_alias=AliasChoices("database_url", "DATABASE_URL"),
    )
    jwt_secret_key: str = Field(
        default="change-me",
        validation_alias=AliasChoices("jwt_secret_key", "JWT_SECRET_KEY", "SECRET_KEY"),
    )
    jwt_algorithm: str = Field(
        default="HS256",
        validation_alias=AliasChoices("jwt_algorithm", "JWT_ALGORITHM", "ALGORITHM"),
    )
    access_token_expire_minutes: int = Field(
        default=60,
        validation_alias=AliasChoices("access_token_expire_minutes", "ACCESS_TOKEN_EXPIRE_MINUTES"),
    )
    refresh_token_expire_minutes: int = Field(
        default=10080,
        validation_alias=AliasChoices("refresh_token_expire_minutes", "REFRESH_TOKEN_EXPIRE_MINUTES"),
    )
    totp_issuer: str = Field(
        default="WorkTrack",
        validation_alias=AliasChoices("totp_issuer", "TOTP_ISSUER"),
    )
    app_name: str = Field(
        default="WorkTrack Backend",
        validation_alias=AliasChoices("app_name", "APP_NAME"),
    )
    app_version: str = Field(
        default="0.1.0",
        validation_alias=AliasChoices("app_version", "APP_VERSION"),
    )

    model_config = SettingsConfigDict(env_file=".env", extra="ignore")


@lru_cache
def get_settings() -> Settings:
    return Settings()