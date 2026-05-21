import uuid

from app.aws.session import session
from app.config import settings

s3_client = session.client("s3")


def _public_url(bucket: str, key: str) -> str:
    if settings.AWS_REGION == "us-east-1":
        return f"https://{bucket}.s3.amazonaws.com/{key}"
    return f"https://s3.amazonaws.com/{bucket}/{key}"


def upload_file_to_s3(file_obj, filename: str, content_type: str, alumno_id: int):
    bucket = settings.S3_BUCKET_NAME
    if not bucket:
        print("Error: S3_BUCKET_NAME no está configurado")
        return None

    try:
        ext = filename.rsplit(".", 1)[-1] if filename and "." in filename else "jpg"
        key = f"alumnos/{alumno_id}/{uuid.uuid4().hex}.{ext}"

        s3_client.upload_fileobj(
            file_obj,
            bucket,
            key,
            ExtraArgs={
                "ACL": "public-read",
                "ContentType": content_type or "application/octet-stream",
            },
        )
        url = _public_url(bucket, key)
        print(f"Archivo subido a {bucket}/{key}")
        return url
    except Exception as e:
        print(f"Error al subir archivo a S3: {e}")
        return None
