from uuid import UUID

from app.config import settings
from app.utils.repository import AbstractCloudRepository


class CloudService:
    def __init__(self, cloud_repo: AbstractCloudRepository):
        self.cloud_repo: AbstractCloudRepository = cloud_repo()

    async def upload_image(self, user_id: UUID, img_file) -> str:
        with img_file as file:
            await self.cloud_repo.upload_file(str(user_id), file)
        return settings.aws.s3.get_url(str(user_id))
