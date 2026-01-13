# import boto3
# from botocore.config import Config
# from app.core.config import settings

# initializing the s3 client
def get_s3_client():
    client = boto3.client(
        "s3",
        endpoint_url=settings.S3_ENDPOINT,
        aws_access_key_id=settings.S3_ACCESS_KEY,
        aws_secret_access_key=settings.S3_SECRET_KEY,
        region_name="us-east-1",
        config=Config(signature_version="s3v4"),
    )
#     return client


def ensure_bucket_exists():
    s3 = get_s3_client()
    bucket = settings.S3_BUCKET_NAME
    bucket_names = []
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
