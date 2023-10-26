from pydantic import Field
from pydantic_settings import BaseSettings


class S3(BaseSettings):
    url: str = Field("http://localstack:4566", env="S3_URL")
    access_key_id: str = Field("S3_ACCESS_KEY_ID", env="S3_ACCESS_KEY_ID")
    secret_access_key: str = Field("S3_SECRET_ACCESS_KEY", env="S3_SECRET_ACCESS_KEY")
    region_name: str = Field("eu-central-1", env="S3_REGION_NAME")
    bucket: str = Field("bucket", env="S3_BUCKET")


class RedisSettings(BaseSettings):
    host: str = Field("redis", env="REDIS_HOST")
    port: str = Field("6379", env="REDIS_PORT")
    password: str = Field("password", env="REDIS_PASS")


class DbSettings(BaseSettings):
    user: str = Field("postgres", env="DB_USER")
    password: str = Field("postgres", env="DB_PASS")
    host: str = Field("db", env="DB_HOST")
    port: str = Field("5432", env="DB_PORT")
    name: str = Field("postgres", env="DB_NAME")

    def get_url(self):
        return f"postgresql+asyncpg://{self.user}:{self.password}@{self.host}:{self.port}/{self.name}"


class AuthSettings(BaseSettings):
    jwt_secret_key: str = Field("JWT_SECRET_KEY", env="JWT_SECRET_KEY")
    jwt_refresh_secret_key: str = Field(
        "JWT_REFRESH_SECRET_KEY", env="JWT_REFRESH_SECRET_KEY"
    )
    algorithm: str = Field("HS256", env="ALGORITHM")
    access_token_expire_minutes: int = 30
    refresh_token_expire_minutes: int = 60 * 24 * 7


class Settings(BaseSettings):
    project_name: str = Field("User management", env="PROJECT_NAME")
    db: DbSettings = DbSettings()
    auth: AuthSettings = AuthSettings()
    redis: RedisSettings = RedisSettings()
    s3: S3 = S3()


settings = Settings()
