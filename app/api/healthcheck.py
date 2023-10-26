from fastapi import APIRouter, File, UploadFile, HTTPException, Depends
import boto3
from app.config import settings
from app.services.cloud import CloudService
from app.api.dependencies import cloud_service
from typing import Annotated
from app.schemas.users import UserOutSchema
from app.utils.oauth_bearer import get_current_unblocked_user
router = APIRouter(
    prefix="/healthcheck",
    tags=["Healthcheck"],
)


@router.get("", status_code=204)
async def healthcheck():
    ...

@router.post("/upload")
async def upload(
    file: UploadFile,
    user: Annotated[UserOutSchema, Depends(get_current_unblocked_user)],
    cloud_service: Annotated[CloudService, Depends(cloud_service)]
):
    try:
        contents = file.file.read()
        file.file.seek(0)
        path = await cloud_service.upload_image(user.id, file.file)
    finally:
        file.file.close()
    return path


