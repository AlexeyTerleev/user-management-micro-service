from fastapi import FastAPI

from app.api.routers import all_routers
from app.config import settings


app = FastAPI(
    title=settings.project_name
)

for router in all_routers:
    app.include_router(router)
