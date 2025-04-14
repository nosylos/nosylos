import os

import boto3
from django.conf import settings


def upload_image(image, filename):
    if settings.ENVIRONMENT == "local":
        file_path = os.path.abspath(
            os.path.join("media", filename.split("/")[-1])
        )
        with open(file_path, "wb") as f:
            f.write(image.read())
        return

    s3_client = boto3.client("s3")
    s3_client.upload_fileobj(
        image,
        settings.IMAGE_BUCKET_NAME,
        filename,
    )
