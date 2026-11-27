# Bloque 0 — Preparación del facilitador (pre-trabajo)

> Esto se hace **antes** del workshop. No cuenta dentro de las 2 horas.
> Tiempo estimado: 20–30 minutos.

El objetivo es que, cuando los ejecutivos entren a Genie One, puedan hacer preguntas y obtener
respuestas correctas de inmediato. Para eso dejamos listas tres cosas: **los datos**, **el contexto de negocio**
(ontología) y, de forma recomendada, un **Genie Agent** sobre las tablas.

---

## 0.1 Verificar los datos (5 min)

Las 17 tablas ya están creadas en `dacamargovws_catalog.bancoomeva`. Verifícalo en el workspace
[`fevm-dacamargovws`](https://fevm-dacamargovws.cloud.databricks.com/?o=7474652595969633):

```sql
SELECT table_name
FROM dacamargovws_catalog.information_schema.tables
WHERE table_schema = 'bancoomeva'
ORDER BY table_name;
-- Debe devolver 17 tablas.
```

Si necesitas recrearlas (o reproducir con datos reales en otro esquema), usa los scripts de [`datos/`](datos/):

```bash
cd datos
python3 generate.py 500      # CSV sintéticos
python3 load.py              # crea las 17 tablas (ajusta PROFILE/WAREHOUSE/CATALOG/SCHEMA en el script)
```

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

## 0.3 (Recomendado) Crear un Genie Agent sobre las tablas (10 min)

Genie One primero busca un **Genie Agent** relevante para la pregunta y, si lo encuentra, lo usa para responder
([ver "How chat works"](https://docs.databricks.com/aws/en/genie-one/chat)). Un Agent curado mejora mucho la precisión.

1. En el workspace, ve a **Genie** y crea un nuevo **Genie Space / Agent** llamado **`Cobranza Bancoomeva`**.
2. Agrega como fuentes las 4 tablas de reportes (son las que usa el workshop):
   - `dacamargovws_catalog.bancoomeva.tbl_vreporteedadcartera`
   - `dacamargovws_catalog.bancoomeva.tbl_vreportegestiones`
   - `dacamargovws_catalog.bancoomeva.tbl_vreportepromesas`
   - `dacamargovws_catalog.bancoomeva.tbl_vreporteprocesosjuridicos`
   - *(Opcional)* las tablas `cliente`, `obligaciones_cobis`, `obligaciones_tarcred` para la "vista 360".
3. En **General instructions** del Agent, pega el contenido de [`genie-space-instructions.md`](genie-space-instructions.md).
4. Agrega estas **Example SQL queries** (ayudan a Genie a aprender los cruces):

```sql
-- Saldo en mora por campaña
SELECT CAMPANA, COUNT(*) AS deudores, SUM(SALDO) AS saldo
FROM tbl_vreporteedadcartera GROUP BY CAMPANA ORDER BY saldo DESC;

-- Tasa de cumplimiento de promesas por estado
SELECT ESTADO_PROMESA, COUNT(*) AS promesas, SUM(VALOR_PROMESA) AS valor
FROM tbl_vreportepromesas GROUP BY ESTADO_PROMESA;

-- Gestiones cruzadas con cartera (ojo con el tipo de la cédula)
SELECT c.GRUPOUSUARIO, COUNT(*) AS gestiones
FROM tbl_vreportegestiones g
JOIN tbl_vreporteedadcartera c
  ON CAST(g.ID_DEUDOR AS BIGINT) = CAST(c.IDENTIFICACION AS BIGINT)
GROUP BY c.GRUPOUSUARIO;
```

5. **Comparte** el Agent con los participantes (CAN VIEW / CAN RUN) para que lo vean en Genie One.

> **Nota técnica importante — la cédula:** en las tablas de reportes la llave del cliente tiene **tipos distintos**:
> `IDENTIFICACION`, `CEDULA` y `CLIENTE_IDENTIFICACION` son texto o número según la tabla. Para cruzarlas hay que
> hacer `CAST(... AS BIGINT)` en ambos lados. Esto se dejó documentado en los comentarios de columna y en los
> ejemplos del Agent para que Genie lo haga bien. (Es el mismo comportamiento que tendrán los datos reales.)

## 0.4 Checklist final antes de empezar

- [ ] Las 17 tablas existen y tienen datos (`SELECT COUNT(*)` > 0).
- [ ] `prep_metadata.py` ejecutado (columnas con descripción).
- [ ] Genie Agent `Cobranza Bancoomeva` creado y compartido (recomendado).
- [ ] Cada participante puede abrir Genie One y tiene `CAN USE` sobre un SQL Warehouse.
- [ ] Proyectar pantalla para la demo en vivo.

👉 Siguiente: [01-primeros-pasos.md](01-primeros-pasos.md)
