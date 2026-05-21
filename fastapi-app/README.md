# Guía de despliegue en AWS — Segunda Entrega (FastAPI)

Orden recomendado de creación: **S3 → DynamoDB → SNS → Lambda → RDS → EC2**.
Toma capturas de: **EC2, RDS, SNS topic y la tabla DynamoDB** (lo pide el PDF).
Crea **todos** los recursos en la misma región (normalmente `us-east-1`).

---

## Arquitectura del proyecto

```
fastapi-app/
├── app/
│   ├── main.py            # FastAPI + routers + manejadores de error (400/500)
│   ├── config.py          # settings desde .env
│   ├── database.py        # engine SQLAlchemy, get_db, init_db
│   ├── models/            # ORM: Alumno (password, fotoPerfilUrl), Profesor
│   ├── schemas/           # Pydantic v2 (validaciones de la entrega 1)
│   ├── routers/           # endpoints alumnos y profesores
│   └── aws/               # session boto3, s3, sns, dynamo
├── lambda/lambda_function.py
├── requirements.txt
├── .env.example
├── deploy.sh / sicei.service
└── reset_db.py
```

Endpoints implementados:

```
GET    /alumnos                         GET    /profesores
GET    /alumnos/{id}                     GET    /profesores/{id}
POST   /alumnos                          POST   /profesores
PUT    /alumnos/{id}                     PUT    /profesores/{id}
DELETE /alumnos/{id}                     DELETE /profesores/{id}
POST   /alumnos/{id}/fotoPerfil          (S3, multipart/form-data, campo "foto")
POST   /alumnos/{id}/email               (Lambda -> SNS)
POST   /alumnos/{id}/session/login       (DynamoDB)
POST   /alumnos/{id}/session/verify
POST   /alumnos/{id}/session/logout
```

---

## 0. Credenciales del laboratorio

Lab → **AWS Details → AWS CLI**. Copia `aws_access_key_id`, `aws_secret_access_key`
y `aws_session_token` al `.env`. **Caducan** al reiniciar el lab: si algo falla,
vuelve a copiarlos y reinicia el servicio.

---

## 1. S3 — bucket público

1. **S3 → Create bucket**. Nombre único, p. ej. `sicei-fotos-<matricula>`. Región `us-east-1`.
2. **Object Ownership**: **ACLs enabled** (el código sube con `ACL: public-read`).
3. **Block Public Access**: **desmarca** "Block all public access" y confirma.
4. Crea el bucket.
5. (Recomendado) **Permissions → Bucket policy**:

```json
{
  "Version": "2012-10-17",
  "Statement": [{
    "Sid": "PublicReadGetObject",
    "Effect": "Allow",
    "Principal": "*",
    "Action": "s3:GetObject",
    "Resource": "arn:aws:s3:::sicei-fotos-<matricula>/*"
  }]
}
```

`.env` → `S3_BUCKET_NAME`. Prueba: sube foto con `POST /alumnos/{id}/fotoPerfil`,
copia la URL devuelta y ábrela en el navegador.

---

## 2. DynamoDB — tabla `sesiones-alumnos`

1. **DynamoDB → Create table**. Table name: `sesiones-alumnos` (exacto).
2. **Partition key**: `sessionString` — String. Sin sort key.
3. Capacidad **On-demand**. Create.

> El código busca por `sessionString` (`get_item`), por eso es la partition key.
> Los atributos `id` (UUID), `fecha`, `alumnoId`, `active` se guardan por item.

Captura de la tabla creada.

---

## 3. SNS — topic

1. **SNS → Topics → Create topic**. Tipo **Standard**. Nombre `notificaciones-alumnos`.
2. Copia el **ARN** → `.env` (`SNS_TOPIC_ARN`) y variable de entorno de la Lambda.

> El profe se suscribe en la revisión. Para tus pruebas, crea una suscripción
> **Email** con tu correo y confírmala.

Captura del topic.

---

## 4. Lambda — `notificar-alumno`

1. **Lambda → Create function → Author from scratch**. Name `notificar-alumno`.
2. Runtime **Python 3.12**. Execution role: usa rol existente **LabRole**.
3. Pega `lambda/lambda_function.py` en el editor → **Deploy**.
4. **Configuration → Environment variables** → `SNS_TOPIC_ARN` con el ARN del paso 3.
5. (Opcional) **Test** con:

```json
{ "alumnoId": 1, "nombres": "Juan", "apellidos": "Perez",
  "matricula": "A12345", "promedio": 9.5 }
```

`.env` → `LAMBDA_FUNCTION_NAME=notificar-alumno`.

> `POST /alumnos/{id}/email` invoca esta Lambda; la Lambda publica en SNS.
> Si falla, el código hace fallback y publica directo en SNS (usa `SNS_TOPIC_ARN` del `.env`).

---

## 5. RDS — MySQL en subnet pública

1. **RDS → Create database**. Standard create, motor **MySQL**, template Free tier.
2. DB identifier `sicei-db`. Master username `admin` + password.
3. Instancia más pequeña (`db.t3.micro` / `db.t4g.micro`).
4. **Connectivity**:
   - **Public access: Yes**.
   - Security group con **inbound TCP 3306** desde tu IP y desde el SG del EC2
     (o `0.0.0.0/0` solo para la entrega).
5. **Additional configuration → Initial database name**: `sicei`.
6. Create. Espera a **Available** y copia el **Endpoint**.

`.env`: `DB_HOST` (endpoint), `DB_USER=admin`, `DB_PASSWORD`, `DB_PORT=3306`, `DB_NAME=sicei`.

> Las tablas `alumnos` y `profesores` se crean solas al arrancar (lifespan → `init_db`).

Captura de la instancia RDS.

---

## 6. EC2 — servidor

1. **EC2 → Launch instance**. AMI Amazon Linux 2023, `t2.micro`/`t3.micro`.
2. Key pair para SSH.
3. **Security group inbound**:
   - SSH (22) desde tu IP.
   - **Custom TCP 8080** desde `0.0.0.0/0`. (`Constants.URL = http://localhost:8080`; el revisor lo apunta a tu DNS público).
4. Launch. Copia la **IP/DNS público**.

Captura del EC2.

### Subir y arrancar

```bash
# Desde tu máquina:
scp -i tu-key.pem -r fastapi-app ec2-user@<IP_EC2>:~/
ssh -i tu-key.pem ec2-user@<IP_EC2>

# En el EC2:
cd fastapi-app
cp .env.example .env
nano .env                 # rellena valores reales

# Opción A: arranque rápido en puerto 8080 (foreground)
bash deploy.sh

# Opción B: servicio (recomendado) — bind al puerto 8080
python3 -m venv venv && source venv/bin/activate
pip install -r requirements.txt && deactivate
sudo cp sicei.service /etc/systemd/system/sicei.service
sudo systemctl daemon-reload
sudo systemctl enable --now sicei
sudo systemctl status sicei
```

### Resetear la base de datos antes de las pruebas

```bash
source venv/bin/activate
python reset_db.py
```

---

## 7. Verificación

```bash
curl -X POST http://<IP_EC2>:8080/alumnos \
  -H "Content-Type: application/json" \
  -d '{"nombres":"Juan","apellidos":"Perez","matricula":"A1","promedio":9.5,"password":"secret"}'

curl http://<IP_EC2>:8080/alumnos
```

Checklist del PDF:

- [ ] RDS conectada al EC2 — datos persisten al reiniciar.
- [ ] Bucket S3 público — la URL de la foto abre en el navegador.
- [ ] Topic SNS — llega correo al suscriptor.
- [ ] Tabla DynamoDB `sesiones-alumnos`.
- [ ] Lambda `notificar-alumno` existe y se invoca.
- [ ] Corre 100% sobre AWS.
- [ ] Capturas de EC2, RDS, SNS, DynamoDB.

---

## Contrato del autotest (rama database)

El script Java de revisión (`AlumnosApiTest`, `ProfesoresApiTest`, `S3ApiTest`,
`SessionApiTest`) tiene particularidades que este proyecto ya respeta:

- **Usa el puerto 8080** (`Constants.URL = http://localhost:8080`). La app corre en 8080.
- **El POST NO envía `id`; lo genera la DB** y el test lo extrae de la respuesta
  (`.path("id")`) para los GET/PUT/DELETE posteriores. El POST devuelve el `id`.
- **El CRUD SÍ envía `password`** (string aleatorio de 10). Se guarda y se compara en login.
- **`POST /alumnos/{id}/email`** → 200 + JSON; con id inexistente → 404.
- **`POST /alumnos/{id}/fotoPerfil`** (multipart, campo `foto`) → 200 + JSON con
  `fotoPerfilUrl`. La URL **debe contener `s3.amazonaws.com`** y un **HEAD a la URL
  devuelve 200** (objeto público vía ACL public-read).
- **Sesiones**: login → `sessionString` de 128; password incorrecto → 400; verify de
  sesión inválida → 400; logout invalida la sesión (verify posterior → 400).
- **405** en `DELETE /alumnos|/profesores` y **404** en rutas inexistentes (FastAPI por defecto).
- **400** ante tipos incorrectos (`matricula` numérica, `horasClase` float negativo,
  `nombres` null). Cubierto por `StrictStr` + validadores + handler de `RequestValidationError`.

### Correr los tests localmente

```bash
# Con la app corriendo en localhost:8080:
cd sicei-autotest-database
mvn clean test
# Reporte: target/site/surefire-report.html
```

---

## Depuración

- **boto3 no autentica**: credenciales del lab caducadas. Recópialas al `.env` y
  `sudo systemctl restart sicei`.
- **No conecta a RDS desde local**: revisa SG (3306) y Public access = Yes.
- **El autotest no alcanza la API**: confirma inbound 8080 en el SG del EC2 y que
  uvicorn/gunicorn escucha en `0.0.0.0:8080`.
- **HEAD a la foto falla**: el objeto debe ser público (ACL public-read) y el bucket
  sin Block Public Access; la URL debe contener `s3.amazonaws.com`.
- **Foto no abre en navegador**: ACLs habilitadas y Block Public Access desactivado.
