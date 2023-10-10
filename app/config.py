from pydantic_settings import BaseSettings
from pydantic import Field


class DbSettings(BaseSettings):
    postgres_user: str = Field("postgres", env="DB_USER") 
    postgres_pass: str = Field("postgres",env="DB_PASS") 
    postgres_port: str = Field("5432",env="DB_PORT") 
    postgres_host: str = Field("db",env="DB_HOST") 
    postgres_name: str = Field("postgres",env="DB_NAME") 


class AuthSettings(BaseSettings):
    jwt_secret_key: str = Field("JWT_SECRET_KEY", env="JWT_SECRET_KEY") 
    jwt_refresh_secret_key: str = Field("JWT_REFRESH_SECRET_KEY", env="JWT_REFRESH_SECRET_KEY") 
    algorithm: str = Field("HS256", env="ALGORITHM") 
    access_token_expire_minutes: int = 30
    refresh_token_expire_minutes: int = 60 * 24 * 7


class Settings(BaseSettings):
    project_name: str = Field("User management", env="PROJECT_NAME") 
    db: DbSettings = DbSettings()
    auth: AuthSettings = AuthSettings()


settings = Settings()