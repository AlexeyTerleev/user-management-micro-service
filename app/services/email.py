import boto3

from app.config import settings


class EmailService:
    def __init__(self):
        self.client = boto3.client(
            "ses",
            endpoint_url=settings.aws.url,
            aws_access_key_id=settings.aws.access_key_id,
            aws_secret_access_key=settings.aws.secret_access_key,
            region_name=settings.aws.region_name,
        )

    async def send_reset_password_url(self, email, url) -> dict:
        response = self.client.send_email(
            Source="alexey.terleev@innowise-group.com",
            Destination={"ToAddresses": [email]},
            Message={
                "Subject": {"Data": "Reset Password"},
                "Body": {
                    "Html": {
                        "Charset": "UTF-8",
                        "Data": f'To reset yout password follow the link: <a class="ulink" href="{url}">Reset Password</a>.',
                    }
                },
            },
        )
        return response
