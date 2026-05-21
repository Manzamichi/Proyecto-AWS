import json
import os

import boto3

# La Lambda usa su rol de ejecución (LabRole en AWS Academy).
sns_client = boto3.client("sns")

SNS_TOPIC_ARN = os.environ["SNS_TOPIC_ARN"]


def lambda_handler(event, context):
    """
    Recibe la info del alumno y publica una notificación en el topic SNS.

    event esperado:
      { "alumnoId": 1, "nombres": "Juan", "apellidos": "Perez",
        "matricula": "A12345", "promedio": 9.5 }
    """
    if isinstance(event, str):
        event = json.loads(event)
    if "body" in event and isinstance(event["body"], str):
        event = json.loads(event["body"])

    nombres = event.get("nombres", "")
    apellidos = event.get("apellidos", "")
    matricula = event.get("matricula", "")
    promedio = event.get("promedio", "")

    mensaje = (
        "Calificaciones del alumno\n"
        f"Nombre: {nombres} {apellidos}\n"
        f"Matrícula: {matricula}\n"
        f"Promedio: {promedio}"
    )

    sns_client.publish(
        TopicArn=SNS_TOPIC_ARN,
        Subject="Calificaciones de alumno",
        Message=mensaje,
    )

    return {"statusCode": 200, "body": json.dumps({"mensaje": "Notificación publicada en SNS"})}
