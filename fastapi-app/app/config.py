import os

from dotenv import load_dotenv

load_dotenv()


class Settings:
    # Base de datos RDS (MySQL)
    DB_USER: str = os.getenv("DB_USER", "")
    DB_PASSWORD: str = os.getenv("DB_PASSWORD", "")
    DB_HOST: str = os.getenv("DB_HOST", "")
    DB_PORT: str = os.getenv("DB_PORT", "3306")
    DB_NAME: str = os.getenv("DB_NAME", "")

    # Override directo (útil para tests con SQLite)
    DATABASE_URL: str = os.getenv("DATABASE_URL", "")

    # AWS
    AWS_REGION: str = os.getenv("AWS_REGION", os.getenv("REGION_NAME", "us-east-1"))
    AWS_ACCESS_KEY_ID: str = os.getenv("AWS_ACCESS_KEY_ID", "")
    AWS_SECRET_ACCESS_KEY: str = os.getenv("AWS_SECRET_ACCESS_KEY", "")
    AWS_SESSION_TOKEN: str = os.getenv("AWS_SESSION_TOKEN", "")

    S3_BUCKET_NAME: str = os.getenv("S3_BUCKET_NAME", "")
    SNS_TOPIC_ARN: str = os.getenv("SNS_TOPIC_ARN", "")
    LAMBDA_FUNCTION_NAME: str = os.getenv("LAMBDA_FUNCTION_NAME", "")

    DYNAMO_TABLE: str = os.getenv("DYNAMO_TABLE", "sesiones-alumnos")

    @property
    def sqlalchemy_uri(self) -> str:
        if self.DATABASE_URL:
            return self.DATABASE_URL
        return (
            f"mysql+pymysql://{self.DB_USER}:{self.DB_PASSWORD}"
            f"@{self.DB_HOST}:{self.DB_PORT}/{self.DB_NAME}"
        )


settings = Settings()
