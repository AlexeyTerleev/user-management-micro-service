from fastapi import FastAPI

from app.api.routers import all_routers


app = FastAPI(
    title="User management"
)

for router in all_routers:
    app.include_router(router)
