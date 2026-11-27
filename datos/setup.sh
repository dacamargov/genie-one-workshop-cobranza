#!/usr/bin/env bash
# Crea TODO el workshop desde cero: esquema, tablas, metadatos, validación y Genie Agent.
# Idempotente. Ajusta PROFILE/WAREHOUSE/CATALOG/SCHEMA en load.py si usas otro entorno.
set -euo pipefail
cd "$(dirname "$0")"

PROFILE="${DATABRICKS_PROFILE:-fevm-dacamargovws}"
WAREHOUSE="${DATABRICKS_WAREHOUSE:-61200af9c31dec2e}"
CATALOG="${WORKSHOP_CATALOG:-dacamargovws_catalog}"
SCHEMA="${WORKSHOP_SCHEMA:-bancoomeva}"
N_CLIENTES="${N_CLIENTES:-500}"

echo "==> 0/5  Creando esquema ${CATALOG}.${SCHEMA} (si no existe)"
databricks api post /api/2.0/sql/statements -p "$PROFILE" --json \
  "{\"warehouse_id\":\"${WAREHOUSE}\",\"statement\":\"CREATE SCHEMA IF NOT EXISTS ${CATALOG}.${SCHEMA}\",\"wait_timeout\":\"30s\"}" >/dev/null

echo "==> 1/5  Generando ${N_CLIENTES} clientes sintéticos (CSV)"
python3 generate.py "$N_CLIENTES"

echo "==> 2/5  Creando las 17 tablas en ${CATALOG}.${SCHEMA}"
python3 load.py

echo "==> 3/5  Agregando metadatos de negocio (ontología)"
python3 prep_metadata.py

echo "==> 4/5  Validando los prompts del workshop"
python3 validate_prompts.py

echo "==> 5/5  Creando el Genie Agent 'Cobranza Bancoomeva'"
python3 create_genie_agent.py

echo "==> LISTO. Comparte el Genie Agent con los participantes y arranca por 01-primeros-pasos.md"
