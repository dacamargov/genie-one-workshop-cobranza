# Bloque 0 — Preparación del facilitador: crear todo desde cero (pre-trabajo)

> Esto se hace **antes** del workshop. No cuenta dentro de las 2 horas.
> Tiempo estimado: 20–30 minutos.

Este bloque crea **todo desde cero**: el esquema, las 17 tablas con datos sintéticos, el contexto de negocio
(ontología) y el **Genie Agent** sobre las tablas. Todo está automatizado en los scripts de [`datos/`](datos/).

## 0.0 Camino rápido: un solo comando (recomendado)

Desde la raíz del repo:

```bash
cd datos
./setup.sh      # genera datos, crea esquema+tablas, agrega metadatos, valida y crea el Genie Agent
```

El script es idempotente y al final imprime la **URL del Genie Agent**. Si prefieres ir paso a paso, usa las
secciones siguientes. Antes de empezar, ajusta `PROFILE / WAREHOUSE / CATALOG / SCHEMA_UC` en
[`datos/load.py`](datos/load.py) si usas otro entorno (por defecto apuntan a `fevm-dacamargovws` y
`dacamargovws_catalog.bancoomeva`).

---

## 0.1 Crear el esquema y las tablas (8 min)

```bash
cd datos

# (si el esquema no existe todavía)
databricks api post /api/2.0/sql/statements -p fevm-dacamargovws --json \
  '{"warehouse_id":"61200af9c31dec2e","statement":"CREATE SCHEMA IF NOT EXISTS dacamargovws_catalog.bancoomeva"}'

python3 generate.py 500      # genera los CSV sintéticos (ajusta el nº de clientes)
python3 load.py              # sube a un Volume y crea las 17 tablas con los tipos del esquema
```

Verifica el resultado:

```sql
SELECT table_name
FROM dacamargovws_catalog.information_schema.tables
WHERE table_schema = 'bancoomeva'
ORDER BY table_name;
-- Debe devolver 17 tablas.
```

> Para reproducir con **datos reales**, carga tablas con los mismos nombres y columnas
> (ver [`datos/schema.json`](datos/schema.json)) en tu propio catálogo/esquema y continúa igual.

## 0.2 Cargar el contexto de negocio / ontología (5 min)

Genie One responde apoyándose en **Genie Ontology**: comentarios de tablas y columnas, métricas, dominios, etc.
([ver Chat › Genie Ontology](https://docs.databricks.com/aws/en/genie-one/chat)). Ya dejamos descripciones
de negocio en las columnas clave de las 4 tablas de reportes. Para re-aplicarlas:

```bash
cd datos
python3 prep_metadata.py     # agrega COMMENT a 46 columnas clave
```

> **Por qué importa:** con buenos comentarios, cuando un ejecutivo pregunta *"¿cuánto saldo en mora hay en jurídico?"*,
> Genie entiende que `CAMPANA = 'JURIDICO'` y que `SALDO` está en COP. Sin contexto, las respuestas son menos precisas.

## 0.3 Crear el Genie Agent desde cero (10 min)

Genie One primero busca un **Genie Agent** relevante para la pregunta y, si lo encuentra, lo usa para responder
([ver "How chat works"](https://docs.databricks.com/aws/en/genie-one/chat)). Un Agent curado mejora mucho la precisión.

### Opción A — por script (recomendado)

El script [`datos/create_genie_agent.py`](datos/create_genie_agent.py) crea el Agent **`Cobranza Bancoomeva`** de cero
vía la API de Genie (`POST /api/2.0/genie/spaces`): agrega las 6 tablas, las instrucciones de negocio y 5 consultas
de ejemplo ya validadas.

```bash
cd datos
python3 create_genie_agent.py
# Imprime el space_id y la URL del Agent recién creado.
```

> Requisitos: `CAN USE` en un SQL Warehouse **Pro o Serverless** y **Databricks Assistant** habilitado.
> Para registrarlo en otra carpeta, exporta `GENIE_PARENT_PATH=/Users/tu-correo` antes de ejecutar.

### Opción B — por interfaz (UI)

1. En el workspace, ve a **Genie** y crea un nuevo **Genie Space / Agent** llamado **`Cobranza Bancoomeva`**.
2. Agrega como fuentes las 4 tablas de reportes (+ opcionalmente `cliente` y `obligaciones_cobis` para la "vista 360"):
   `tbl_vreporteedadcartera`, `tbl_vreportegestiones`, `tbl_vreportepromesas`, `tbl_vreporteprocesosjuridicos`.
3. En **General instructions**, pega el contenido de [`genie-space-instructions.md`](genie-space-instructions.md).
4. Agrega **Example SQL queries** (las mismas del script). Por ejemplo:

```sql
-- Tasa de cumplimiento de promesas por grupo (ojo con el tipo de la cédula)
SELECT c.GRUPOUSUARIO, COUNT(*) AS promesas,
       ROUND(100.0*SUM(CASE WHEN p.ESTADO_PROMESA='CUMPLIDA' THEN 1 ELSE 0 END)/COUNT(*),1) AS pct_cumplida
FROM tbl_vreportepromesas p
JOIN tbl_vreporteedadcartera c ON CAST(p.CEDULA AS BIGINT) = CAST(c.IDENTIFICACION AS BIGINT)
GROUP BY c.GRUPOUSUARIO ORDER BY pct_cumplida DESC;
```

### Compartir y validar

- **Comparte** el Agent con los participantes: ábrelo en Genie y pulsa **Share** (CAN VIEW / CAN RUN).
- Este Agent ya fue probado de punta a punta. Respuestas verificadas:
  - *"¿Cuál es el saldo total en mora y cuántos deudores hay?"* → **17.123 millones de COP, 392 deudores**.
  - *"¿Qué grupo de cobranza tiene mejor cumplimiento de promesas?"* → **ABOGADOS EXTERNOS, 46,8%** (usando el cruce con `CAST`).

> **Nota técnica importante — la cédula:** en las tablas de reportes la llave del cliente tiene **tipos distintos**:
> `IDENTIFICACION`, `CEDULA` y `CLIENTE_IDENTIFICACION` son texto o número según la tabla. Para cruzarlas hay que
> hacer `CAST(... AS BIGINT)` en ambos lados. Esto se dejó documentado en los comentarios de columna y en los
> ejemplos del Agent para que Genie lo haga bien. (Es el mismo comportamiento que tendrán los datos reales.)

## 0.4 Checklist final antes de empezar

- [ ] El esquema `dacamargovws_catalog.bancoomeva` existe.
- [ ] Las 17 tablas existen y tienen datos (`SELECT COUNT(*)` > 0).
- [ ] `prep_metadata.py` ejecutado (columnas con descripción).
- [ ] Genie Agent `Cobranza Bancoomeva` creado (`create_genie_agent.py`) y **compartido** con los participantes.
- [ ] `validate_prompts.py` en verde (19/19 prompts devuelven datos).
- [ ] Cada participante puede abrir Genie One y tiene `CAN USE` sobre un SQL Warehouse.
- [ ] Proyectar pantalla para la demo en vivo.

👉 Siguiente: [01-primeros-pasos.md](01-primeros-pasos.md)
