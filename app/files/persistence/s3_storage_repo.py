import boto3
from .storage_repo import StorageRepository

class S3StorageRepository(StorageRepository):
    def __init__(self, bucket: str, region: str | None = None, endpoint_url: str | None = None):
        self.s3 = boto3.client("s3", region_name=region, endpoint_url=endpoint_url)
        self.bucket = bucket

    def put(self, key, stream, content_type):
        self.s3.upload_fileobj(stream, self.bucket, key, ExtraArgs={"ContentType": content_type})

    def get_presigned_url(self, key, expires_seconds=900):
        return self.s3.generate_presigned_url(
            "get_object", Params={"Bucket": self.bucket, "Key": key}, ExpiresIn=expires_seconds
        )

    def get_object(self, key: str) -> bytes:
        obj = self.s3.get_object(Bucket=self.bucket, Key=key)
        return obj["Body"].read()

    def delete(self, key):
        self.s3.delete_object(Bucket=self.bucket, Key=key)
