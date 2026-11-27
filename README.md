# Workshop Genie One para Ejecutivos — Inteligencia de Cobranza

Workshop práctico de **2 horas** para que ejecutivos y líderes de negocio aprendan a usar
[Genie One](https://docs.databricks.com/aws/en/genie-one/) para responder preguntas de negocio,
automatizar reportes y tomar acciones, **sin escribir una sola línea de SQL**.

El caso de uso es la **gestión de cobranza de un banco** (datos de ejemplo inspirados en un modelo tipo Bancoomeva):
cartera en mora, gestiones de cobro, promesas de pago y procesos jurídicos.

> **Datos 100% sintéticos.** Ningún nombre, cédula, teléfono, correo o cifra corresponde a una persona o entidad real.
> El esquema sí es real, para que cada área pueda reproducir el workshop con **sus propios datos** usando las mismas tablas.

---

## Objetivos de aprendizaje

Al terminar, cada participante podrá:

1. Hacer preguntas de negocio en lenguaje natural y **verificar** las respuestas con citaciones.
2. Analizar la cartera, las gestiones, las promesas de pago y el cobro jurídico desde el chat.
3. Enseñarle a Genie One tareas repetibles con **Skills** y compartirlas con su equipo.
4. Generar **documentos** ejecutivos y **presentaciones (slides/artifacts)** a partir de una conversación.
5. Programar **tareas automáticas** que llegan por correo (ej. un briefing diario de cartera).
6. Conectar aplicaciones externas (Slack, correo, Jira) con **MCP** y crear un **Genie Agent** reutilizable.

---

## Público y requisitos

- **Público:** ejecutivos, gerentes de cobranza, líderes de riesgo y de operaciones. No requiere conocimientos técnicos.
- **Permisos mínimos por participante:** entitlement *Workspace access* o *Databricks SQL access* y permiso `CAN USE` sobre al menos un SQL Warehouse (requisito de Genie One chat — ver [doc de Chat](https://docs.databricks.com/aws/en/genie-one/chat)).
- **Datos:** las 17 tablas del esquema en `dacamargovws_catalog.bancoomeva` (ya creadas; ver [`datos/`](datos/)).
- **Compute:** Genie One usa **Auto** por defecto; no hace falta elegir warehouse manualmente.

---

## Agenda (2 horas)

| # | Tiempo | Bloque | Archivo |
|---|--------|--------|---------|
| 0 | *Pre-trabajo* | Preparación del facilitador (datos, metadatos y Genie Space) | [00-preparacion-facilitador.md](00-preparacion-facilitador.md) |
| 1 | 0:00 – 0:15 | Primeros pasos en el chat | [01-primeros-pasos.md](01-primeros-pasos.md) |
| 2 | 0:15 – 0:40 | Preguntas de negocio sobre la cartera | [02-preguntas-cartera.md](02-preguntas-cartera.md) |
| 3 | 0:40 – 1:00 | Gestiones, contactabilidad y promesas de pago | [03-gestiones-promesas.md](03-gestiones-promesas.md) |
| 4 | 1:00 – 1:10 | Memoria y personalización | [04-memoria-personalizacion.md](04-memoria-personalizacion.md) |
| 5 | 1:10 – 1:30 | Skills: automatizar análisis repetibles | [05-skills.md](05-skills.md) |
| 6 | 1:30 – 1:45 | Documentos y presentaciones (artifacts) | [06-documentos-artifacts.md](06-documentos-artifacts.md) |
| 7 | 1:45 – 1:55 | Tareas programadas | [07-tareas-programadas.md](07-tareas-programadas.md) |
| 8 | 1:55 – 2:00 | Conectores (MCP), Genie Agent y cierre | [08-conectores-agentes-cierre.md](08-conectores-agentes-cierre.md) |

- **Todos los prompts listos para copiar/pegar** están en [`prompts.md`](prompts.md).
- **Skills listas para subir** están en [`skills/`](skills/).

---

## Las 17 tablas del workshop

En `dacamargovws_catalog.bancoomeva`. Comparten la **cédula del cliente** como llave para cruzarlas.

**Reportes de cobranza** (origen `silver_prod.awss3_wsac`):

| Tabla | Qué contiene |
|---|---|
| `tbl_vreporteedadcartera` | Edad de cartera: un registro por deudor en mora (saldo, días de mora, campaña, asesor). |
| `tbl_vreportegestiones` | Gestiones de cobro (llamadas, WhatsApp, SMS, visitas) con su resultado. |
| `tbl_vreportepromesas` | Promesas de pago con valor, fecha y estado. |
| `tbl_vreporteprocesosjuridicos` | Procesos jurídicos: juzgado, radicado, abogado y etapa procesal. |

**Datos maestros y productos** (origen `refine_prod.wsac`): `cliente`, `direccion`, `correo`, `tbl_telefono_wsac`,
`referencia_cliente`, `referencia_codeudores`, `cuentas_pasivo`, `garantias`, `pagos_prestamos`,
`obligaciones_cobis`, `obligaciones_sat`, `obligaciones_sat_amparadas`, `obligaciones_tarcred`.

---

## Reproducir con datos reales

El esquema es el mismo que usan las áreas en producción. Para reproducir el workshop con datos propios,
basta con cargar tablas con **los mismos nombres y columnas** (ver [`datos/schema.json`](datos/schema.json))
en un catálogo/esquema propio y repetir los mismos pasos. Los scripts de [`datos/`](datos/) regeneran todo:

```bash
cd datos
python3 generate.py 500      # genera CSV sintéticos (ajusta el nº de clientes)
python3 load.py              # sube a un Volume y crea las 17 tablas
python3 prep_metadata.py     # agrega descripciones de negocio a las columnas clave
python3 validate_prompts.py  # valida que cada prompt del workshop devuelva datos
```

> Resultado de la última validación: **19/19 prompts** devuelven datos coherentes. Ver [`datos/validation_results.md`](datos/validation_results.md).

---

## Créditos y documentación

Workshop basado en la documentación oficial de Genie One:
[Chat](https://docs.databricks.com/aws/en/genie-one/chat) ·
[Skills](https://docs.databricks.com/aws/en/genie-one/skills) ·
[Scheduled tasks](https://docs.databricks.com/aws/en/genie-one/scheduled-tasks) ·
[Personalization](https://docs.databricks.com/aws/en/genie-one/personalization) ·
[Documents](https://docs.databricks.com/aws/en/genie-one/documents) ·
[Artifacts](https://docs.databricks.com/aws/en/genie-one/artifacts) ·
[MCP](https://docs.databricks.com/aws/en/genie-one/external-sources) ·
[Crear un Genie Agent](https://docs.databricks.com/aws/en/genie-one/create-agent-from-chat).
