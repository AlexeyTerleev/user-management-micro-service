from pydantic import BaseModel
from pydantic_settings import BaseSettings, SettingsConfigDict


class S3(BaseModel):
    S3_BUCKET: str

    def get_url(self, file_name):
        return f"http://localhost:4566/{self.S3_BUCKET}/{file_name}"


class AWS(BaseModel):
    AWS_URL: str
    AWS_ACCESS_KEY_ID: str
    AWS_SECRET_ACCESS_KEY: str
    AWS_REGION_NAME: str
    s3: S3


class RedisSettings(BaseModel):
    REDIS_HOST: str
    REDIS_PORT: str
    REDIS_PASS: str


class DbSettings(BaseModel):
    DB_USER: str
    DB_PASS: str
    DB_HOST: str
    DB_PORT: str
    DB_NAME: str

    def get_url(self):
        return f"postgresql+asyncpg://{self.DB_USER}:{self.DB_PASS}@{self.DB_HOST}:{self.DB_PORT}/{self.DB_NAME}"


class AuthSettings(BaseModel):
    JWT_SECRET_KEY: str
    JWT_REFRESH_SECRET_KEY: str
    ALGORITHM: str

    access_token_expire_minutes: int = 1
    refresh_token_expire_minutes: int = 60 * 24 * 7


class Settings(BaseSettings):
    model_config = SettingsConfigDict(env_file=".env")

    PROJECT_NAME: str = "User Management"
    MODE: str

    db: DbSettings
    auth: AuthSettings
    redis: RedisSettings
    aws: AWS


settings = Settings()
