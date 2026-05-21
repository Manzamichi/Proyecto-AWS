import secrets
import time
import uuid

from app.aws.session import session
from app.config import settings

dynamodb = session.resource("dynamodb")
table = dynamodb.Table(settings.DYNAMO_TABLE)


def create_session(alumno_id: int) -> str:
    """
    Crea una sesión y devuelve el sessionString (128 caracteres hex).
    Esquema del item:
      sessionString (string, PK)
      id            (string, UUID)
      fecha         (number, Unix timestamp)
      alumnoId      (number)
      active        (boolean)
    """
    session_string = secrets.token_hex(64)  # 64 bytes -> 128 caracteres hex

    item = {
        "sessionString": session_string,
        "id": str(uuid.uuid4()),
        "fecha": int(time.time()),
        "alumnoId": int(alumno_id),
        "active": True,
    }
    table.put_item(Item=item)
    return session_string


def get_session(session_string: str):
    response = table.get_item(Key={"sessionString": session_string})
    return response.get("Item")


def deactivate_session(session_string: str):
    table.update_item(
        Key={"sessionString": session_string},
        UpdateExpression="SET active = :a",
        ExpressionAttributeValues={":a": False},
    )
