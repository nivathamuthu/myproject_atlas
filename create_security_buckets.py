import os

from dotenv import load_dotenv
from minio import Minio


load_dotenv()


client = Minio(
    os.getenv("MINIO_ENDPOINT"),
    access_key=os.getenv("MINIO_ACCESS_KEY"),
    secret_key=os.getenv("MINIO_SECRET_KEY"),
    secure=os.getenv("MINIO_SECURE", "false").lower() == "true",
)


for env_name in (
    "MINIO_BUCKET_QUARANTINE",
    "MINIO_BUCKET_TRUSTED",
):
    bucket_name = os.getenv(env_name)

    if not bucket_name:
        raise RuntimeError(
            f"{env_name} is not configured."
        )

    if not client.bucket_exists(bucket_name):
        client.make_bucket(bucket_name)
        print(f"Created: {bucket_name}")
    else:
        print(f"Already exists: {bucket_name}")


print("Security buckets ready.")