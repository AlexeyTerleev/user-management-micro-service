from app.api.auth import router as auth_router
from app.api.healthcheck import router as healthcheck_router
from app.api.user import router as user_router

all_routers = [
    auth_router,
    user_router,
    healthcheck_router,
]
