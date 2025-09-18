import os
from files.domain.use_cases import FilesUseCases
from authentication.persistence.redis_token_repo import RedisTokenRepository
from files.persistence.memory_file_repo import InMemoryFileRepo
from files.persistence.s3_storage_repo import S3StorageRepository

_token_repo = RedisTokenRepository(url=os.getenv("REDIS_URL", "redis://redis:6379/0"))
_storage = S3StorageRepository(
    bucket=os.getenv("S3_BUCKET", "my-bucket"),
    region=os.getenv("AWS_REGION", "us-east-1"),
    endpoint_url=os.getenv("S3_ENDPOINT", "http://minio:9000")
)
_file_repo = InMemoryFileRepo()
_files_uc = FilesUseCases(_token_repo, _file_repo, _storage)

def get_files_uc():
    return _files_uc
