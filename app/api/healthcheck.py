from typing import Annotated

import boto3
from fastapi import APIRouter, Depends, File, HTTPException, UploadFile

from app.api.dependencies import cloud_service
from app.config import settings
from app.schemas.users import UserOutSchema
from app.services.cloud import CloudService
from app.utils.oauth_bearer import get_current_unblocked_user

router = APIRouter(
    prefix="/healthcheck",
    tags=["Healthcheck"],
)


@router.get("", status_code=204)
async def healthcheck():
    ...
