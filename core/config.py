from typing import Any, Annotated, Literal
from pydantic_settings import BaseSettings, SettingsConfigDict
from pydantic import BeforeValidator, PostgresDsn, computed_field, AnyHttpUrl
from pydantic_core import MultiHostUrl



def parse_cors(v: Any) -> list[str] | str:
    if isinstance(v, str) and not v.startswith("["):
        return [i.strip() for i in v.split(",")]
    elif isinstance(v, list | str):
        return v
    raise ValueError(v)

class Settings(BaseSettings):
    # load env
    
    model_config = SettingsConfigDict(env_file=".env", env_file_encoding="utf-8") # noqa

    ENVIRONMENT: Literal["local", "staging", "production"] = "local"
    TITLE: str
    DESCRIPTION: str 
    API_VERSION: str
    ADMIN_USERNAME: str
    ADMIN_PASSWORD: str
    CLOUDINARY_CLOUD_NAME: str
    CLOUDINARY_API_KEY: str
    CLOUDINARY_API_SECRET: str
    DATABASE_URL: str 
    DOCS_URL: str
    BACKEND_CORS_ORIGINS: Annotated[
        list[AnyHttpUrl] | str, BeforeValidator(parse_cors)
    ] = [] 
    POSTGRES_SERVER: str
    # POSTGRES_PORT: int
    POSTGRES_USER: str
    POSTGRES_PASSWORD: str
    
    POSTGRES_DB: str

    @computed_field  # type: ignore[misc]
    @property
    def SQL_DATABASE_URI(self) -> PostgresDsn:
        HostUrl = self.DATABASE_URL
        
        # MultiHostUrl.build(
        #         scheme="postgresql",
        #         username=self.POSTGRES_USER,
        #         password=self.POSTGRES_PASSWORD,
        #         host=self.POSTGRES_SERVER,
        #         # port=self.POSTGRES_PORT,
        #         # path=self.POSTGRES_DB,
        #     )
    
        
        print(HostUrl)
        
        return HostUrl
    
    SMTP_TLS: bool = True
    SMTP_SSL: bool = False
    SMTP_PORT: int = 587
    SMTP_HOST: str | None = None
    SMTP_USER: str | None = None
    SMTP_PASSWORD: str | None = None
    # TODO: update type to EmailStr when sqlmodel supports it
    EMAILS_FROM_EMAIL: str | None = None
    EMAILS_FROM_NAME: str | None = None

settings = Settings()
