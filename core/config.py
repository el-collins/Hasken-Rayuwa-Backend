from typing import Any, Annotated, Literal
from pydantic_settings import BaseSettings, SettingsConfigDict
from pydantic import BeforeValidator, computed_field, AnyHttpUrl
from dotenv import load_dotenv


def parse_cors(v: Any) -> list[str] | str:
    if isinstance(v, str) and not v.startswith("["):
        return [i.strip() for i in v.split(",")]
    elif isinstance(v, list | str):
        return v
    raise ValueError(v)


# Load environment variables from .env file
load_dotenv()


class Settings(BaseSettings):
    # load env

    model_config = SettingsConfigDict(
        env_file=".env", env_file_encoding="utf-8"
    )  # noqa

    ENVIRONMENT: Literal["local", "staging", "production"] = "local"
    LOCAL_DATABASE_URL: str = "sqlite:///./dev.db"
    REMOTE_DATABASE_URL: str
    TITLE: str
    DESCRIPTION: str
    API_VERSION: str
    ADMIN_USERNAME: str
    ADMIN_PASSWORD: str
    CLOUDINARY_CLOUD_NAME: str
    CLOUDINARY_API_KEY: str
    CLOUDINARY_API_SECRET: str
    DOCS_URL: str
    BACKEND_CORS_ORIGINS: Annotated[
        list[AnyHttpUrl] | str, BeforeValidator(parse_cors)
    ] = []

    @computed_field
    @property
    def SQL_DATABASE_URI(self) -> str:
        if self.ENVIRONMENT == "local":
            print("Using local database")
            return self.LOCAL_DATABASE_URL
        else:
            return self.REMOTE_DATABASE_URL

    SMTP_TLS: bool = True
    SMTP_SSL: bool = False
    SMTP_PORT: int = 587
    SMTP_HOST: str | None = None
    SMTP_USER: str | None = None
    SMTP_PASSWORD: str | None = None
    # TODO: update type to EmailStr when sqlmodel supports it
    EMAILS_FROM_EMAIL: str | None = None
    EMAILS_FROM_NAME: str | None = None


settings = Settings()  # type: ignore
