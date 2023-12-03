# User Management Microservice

### This is web microservice for managing users based on FastAPI. 

## Stack:
- FastAPI (with Pydantic, SQLAlchemy, Alembic, PyJWT)
- Lint with black and isort
- Databases:
    - PostgreSQL
    - Redis
- Cloud Services:
    - AWS SES
    - AWS S3
- Tests with PyTest
- CI / CD with GitHub Actions

## Install

```bash
git clone https://github.com/AlexeyTerleev/user-management-micro-service.git
```

## Run
### Create .env file:
```
export DB='{"DB_USER": "postgres", "DB_PASS": "postgres", "DB_HOST": "db", "DB_PORT": "5432", "DB_NAME": "postgres"}'
export AUTH='{"JWT_SECRET_KEY": "JWT_SECRET_KEY", "JWT_REFRESH_SECRET_KEY": "JWT_REFRESH_SECRET_KEY", "ALGORITHM": "HS256"}'
export REDIS='{"REDIS_HOST": "redis", "REDIS_PORT": "6379", "REDIS_PASS": "password"}'
export AWS='{"AWS_URL": "http://localstack:4566", "AWS_ACCESS_KEY_ID": "AWS_ACCESS_KEY_ID", "AWS_SECRET_ACCESS_KEY": "AWS_SECRET_ACCESS_KEY", "AWS_REGION_NAME": "eu-central-1", "s3": {"S3_BUCKET": "bucket"}}'
export MODE=DEV
```
### Create conteiners
```bash
docker-compose up
```
### Go to http://localhost:8000/docs