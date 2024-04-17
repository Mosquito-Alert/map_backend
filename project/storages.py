import os

from storages.backends.s3boto3 import S3Boto3Storage, S3StaticStorage
from storages.utils import setting

class StaticRootS3Boto3Storage(S3StaticStorage):
    location = os.path.join(setting("AWS_LOCATION", ""), "static")
    default_acl = "public-read"


class MediaRootS3Boto3Storage(S3Boto3Storage):
    location = os.path.join(setting("AWS_LOCATION", ""), "media")
    file_overwrite = False
    default_acl = "public-read"