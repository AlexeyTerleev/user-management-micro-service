
from fastapi import APIRouter

router = APIRouter(
    prefix="/healthcheck",
    tags=["Healthcheck"],
)


@router.get("", status_code=204)
async def healthcheck():
    ...
