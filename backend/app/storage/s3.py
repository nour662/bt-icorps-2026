import boto3
from botocore.config import Config
from app.core.config import settings

# initializing the s3 client
def get_s3_client():
    print("S3_ENDPOINT runtime:", settings.S3_ENDPOINT)
    is_minio = bool(settings.S3_ENDPOINT)
    client = boto3.client(
        "s3",
        endpoint_url=settings.S3_ENDPOINT or None,
        aws_access_key_id=settings.S3_ACCESS_KEY or None,
        aws_secret_access_key=settings.S3_SECRET_KEY or None,
        region_name=settings.AWS_REGION,
        config=Config(
            signature_version="s3v4",
            s3={"addressing_style" : "path"} if is_minio else None,
        ),
    )
    return client


def ensure_bucket_exists():
    s3 = get_s3_client()
    bucket = settings.S3_BUCKET_NAME
    bucket_names = []
    if (s3.list_buckets() != None):
        for b in s3.list_buckets().get("Buckets", []):
            bucket_names.append(b["Name"])
    if bucket not in bucket_names:
        s3.create_bucket(Bucket=bucket)

def load_pdf_from_s3(key):
    s3 = get_s3_client()
    obj = s3.get_object(
        Bucket=settings.S3_BUCKET_NAME,
        Key=key
    )
    text = obj["Body"].read()
    return text
