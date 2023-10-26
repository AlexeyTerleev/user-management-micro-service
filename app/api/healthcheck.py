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



