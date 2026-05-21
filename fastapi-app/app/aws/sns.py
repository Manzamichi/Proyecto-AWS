import json

from app.aws.session import session
from app.config import settings

lambda_client = session.client("lambda")
sns_client = session.client("sns")


def enviar_notificacion_alumno(alumno) -> bool:
    """
    Flujo principal: invoca la Lambda, que publica en SNS.
    Fallback: si la Lambda no está configurada o falla, publica directo en SNS.
    """
    payload = {
        "alumnoId": alumno.id,
        "nombres": alumno.nombres,
        "apellidos": alumno.apellidos,
        "matricula": alumno.matricula,
        "promedio": alumno.promedio,
    }

    if settings.LAMBDA_FUNCTION_NAME:
        try:
            resp = lambda_client.invoke(
                FunctionName=settings.LAMBDA_FUNCTION_NAME,
                InvocationType="RequestResponse",
                Payload=json.dumps(payload).encode("utf-8"),
            )
            if resp.get("StatusCode") == 200:
                body = resp["Payload"].read().decode("utf-8")
                print(f"Lambda invocada OK: {body}")
                return True
            print(f"Lambda devolvió status {resp.get('StatusCode')}")
        except Exception as e:
            print(f"Error al invocar Lambda, fallback directo: {e}")

    return _publicar_directo(payload)


def _publicar_directo(payload: dict) -> bool:
    if not settings.SNS_TOPIC_ARN:
        print("Error: SNS_TOPIC_ARN no está configurado")
        return False
    try:
        mensaje = (
            "Calificaciones del alumno\n"
            f"Nombre: {payload['nombres']} {payload['apellidos']}\n"
            f"Matrícula: {payload['matricula']}\n"
            f"Promedio: {payload['promedio']}"
        )
        sns_client.publish(
            TopicArn=settings.SNS_TOPIC_ARN,
            Subject="Calificaciones de alumno",
            Message=mensaje,
        )
        print("Mensaje publicado directamente en SNS (fallback).")
        return True
    except Exception as e:
        print(f"Error al publicar en SNS: {e}")
        return False
