#!/usr/bin/env bash
# Despliegue de la app FastAPI en EC2 (Amazon Linux 2023 o Ubuntu).
# Uso: bash deploy.sh
set -euo pipefail

APP_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
cd "$APP_DIR"

echo "==> Instalando Python si falta"
if command -v dnf >/dev/null 2>&1; then
  sudo dnf install -y python3 python3-pip
elif command -v apt-get >/dev/null 2>&1; then
  sudo apt-get update -y && sudo apt-get install -y python3 python3-pip python3-venv
fi

echo "==> Entorno virtual"
python3 -m venv venv
source venv/bin/activate
pip install --upgrade pip
pip install -r requirements.txt

if [ ! -f .env ]; then
  echo "ERROR: falta .env. Ejecuta: cp .env.example .env y edítalo."
  exit 1
fi

echo "==> Arrancando uvicorn en el puerto 8080"
exec venv/bin/uvicorn app.main:app --host 0.0.0.0 --port 8080
