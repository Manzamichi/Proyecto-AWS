import boto3

from app.config import settings


def get_boto3_session():
    """
    Crea una sesión boto3.

    Si hay claves en el entorno (key/secret/sessionToken del botón AWS Details),
    las usa. Si no, boto3 cae a la cadena por defecto (IAM Role del EC2).
    """
    if settings.AWS_ACCESS_KEY_ID and settings.AWS_SECRET_ACCESS_KEY:
        return boto3.Session(
            aws_access_key_id=settings.AWS_ACCESS_KEY_ID,
            aws_secret_access_key=settings.AWS_SECRET_ACCESS_KEY,
            aws_session_token=settings.AWS_SESSION_TOKEN or None,
            region_name=settings.AWS_REGION,
        )
    return boto3.Session(region_name=settings.AWS_REGION)


session = get_boto3_session()
