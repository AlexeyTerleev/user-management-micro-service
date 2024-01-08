from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

from app.api.routers import all_routers
from app.config import settings

app = FastAPI(title=settings.PROJECT_NAME)

origins = [
    "http://localhost",
    "http://localhost:5173",
]

app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

for router in all_routers:
    app.include_router(router)
