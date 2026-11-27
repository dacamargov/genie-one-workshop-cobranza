#!/usr/bin/env python3
"""Crea DESDE CERO el Genie Agent 'Cobranza Bancoomeva' sobre las tablas del workshop,
via la API de Genie (POST /api/2.0/genie/spaces). Reutiliza la conexion de load.py.

Uso:
    python3 create_genie_agent.py

Ajusta PROFILE / WAREHOUSE / CATALOG / SCHEMA en load.py si usas otro entorno.
Requiere: CAN USE en un SQL Warehouse Pro/Serverless y Databricks Assistant habilitado.
"""
import json, os, sys
sys.argv = ["x"]
import load

PROFILE = load.PROFILE
WAREHOUSE = load.WAREHOUSE
FQ = f"{load.CATALOG}.{load.SCHEMA_UC}"
PARENT_PATH = os.environ.get("GENIE_PARENT_PATH", "/Users/daniel.vargas@databricks.com")
TITLE = "Cobranza Bancoomeva"
DESCRIPTION = ("Explora en lenguaje natural la cartera en mora, las gestiones de cobro, las promesas de pago "
               "y los procesos juridicos de cobranza. Datos sinteticos para el workshop de Genie One.")

TABLES = [
 (f"{FQ}.tbl_vreporteedadcartera",
  "Edad de cartera: un registro por deudor en mora. Columnas clave: IDENTIFICACION (cedula), NOMBREDEUDOR, "
  "REGION, CAMPANA (COBRANZA TEMPRANA/PREJURIDICO/JURIDICO/CASTIGADA), SUBCAMPANA (tramo de mora), SALDO, "
  "CAPITAL, MORA, PROVISION (COP), DIASMORA, GRUPOUSUARIO, NOMBREUSUARIO, NOMBREABOGADO, ESTRATEGIA, "
  "CONSUMO/COMERCIAL/HIPOTECARIO (SI/NO)."),
 (f"{FQ}.tbl_vreportegestiones",
  "Gestiones de cobro. Columnas clave: ID_DEUDOR (cedula, DECIMAL), FECHA_GESTION, USUARIO (login asesor), "
  "ACCION (LLAMADA SALIENTE/WHATSAPP/SMS/EMAIL/VISITA), RESPUESTA, CONTACTO (TITULAR/TERCERO/NO CONTACTO), "
  "MOTIVO_NOPAGO, CANAL (VOZ/DIGITAL/CAMPO)."),
 (f"{FQ}.tbl_vreportepromesas",
  "Promesas de pago. Columnas clave: CEDULA (LONG), NOMBRE_CLIENTE, VALOR_PROMESA (COP), FECHA_PROMESA, "
  "ESTADO_PROMESA (VIGENTE/CUMPLIDA/INCUMPLIDA/PARCIAL), NOMBRE_USUARIO (asesor), REGIONAL, CAMPANA, ZONA."),
 (f"{FQ}.tbl_vreporteprocesosjuridicos",
  "Procesos juridicos de cobro. Columnas clave: CLIENTE_IDENTIFICACION (cedula), CLIENTE_NOMBRE, REGION, "
  "CAPITAL (COP), ABOGADO_NOMBRE, PROCESO, PROCESO_ESTADO, PROCESO_JUZGADO, ULTIMA_ETAPA_DESCRIPCION (etapa "
  "procesal: DEMANDA/ADMISION/NOTIFICACION/EXCEPCIONES/SENTENCIA/LIQUIDACION/EMBARGO Y SECUESTRO/REMATE)."),
 (f"{FQ}.cliente",
  "Datos maestros del cliente (un registro por DOCUMENTO/cedula): nombres, REGIONAL, INGRESO, PROFESION, "
  "ESTADO, calificaciones. Util para la vista 360 del deudor."),
 (f"{FQ}.obligaciones_cobis",
  "Obligaciones de credito del sistema COBIS (NIT=cedula): PRODUCTO, SALDO, CAPITAL_TOTAL, DIAS_DE_MORA, "
  "PROVISION, ESTADO. Para analizar deuda por producto."),
]

INSTRUCTIONS = [
 "Responde en espanol, con tono ejecutivo y conciso.",
 "- Los valores monetarios (SALDO, CAPITAL, MORA, PROVISION, VALOR_PROMESA, CUOTA) estan en pesos colombianos (COP). Reporta cifras grandes en millones de COP, redondeadas.",
 "- La campana (CAMPANA) es la etapa de cobranza, de menor a mayor severidad: COBRANZA TEMPRANA -> PREJURIDICO -> JURIDICO -> CASTIGADA.",
 "- DIASMORA es la altura de mora del deudor; SUBCAMPANA es el tramo de dias de mora.",
 "- Tasa de cobertura = SUM(PROVISION) / SUM(CAPITAL).",
 "- Contacto efectivo = gestiones con CONTACTO = 'TITULAR'.",
 "- Tasa de cumplimiento de promesas = promesas con ESTADO_PROMESA = 'CUMPLIDA' / total de promesas.",
 "- LLAVE DEL CLIENTE (cedula) con tipos distintos por tabla: tbl_vreporteedadcartera.IDENTIFICACION (STRING), "
 "tbl_vreportegestiones.ID_DEUDOR (DECIMAL), tbl_vreportepromesas.CEDULA (LONG), "
 "tbl_vreporteprocesosjuridicos.CLIENTE_IDENTIFICACION (STRING), cliente.DOCUMENTO (STRING), obligaciones_cobis.NIT (STRING). "
 "Para cruzar estas tablas convierte AMBOS lados con CAST(... AS BIGINT).",
 "- Cuando sea util, muestra una tabla o una visualizacion (barras para rankings, torta para distribuciones) e incluye el total y el detalle.",
]

EXAMPLES = [
 ("¿Cuál es el saldo total en mora y cuántos deudores hay?",
  f"SELECT COUNT(*) AS deudores, SUM(SALDO) AS saldo, SUM(CAPITAL) AS capital, ROUND(AVG(DIASMORA)) AS dias_mora_prom\nFROM {FQ}.tbl_vreporteedadcartera"),
 ("Saldo en mora por campaña, de mayor a menor.",
  f"SELECT CAMPANA, COUNT(*) AS deudores, SUM(SALDO) AS saldo\nFROM {FQ}.tbl_vreporteedadcartera\nGROUP BY CAMPANA ORDER BY saldo DESC"),
 ("Tasa de cumplimiento de promesas por estado, con valor prometido.",
  f"SELECT ESTADO_PROMESA, COUNT(*) AS promesas, SUM(VALOR_PROMESA) AS valor\nFROM {FQ}.tbl_vreportepromesas\nGROUP BY ESTADO_PROMESA ORDER BY promesas DESC"),
 ("¿Qué grupo de cobranza tiene mejor cumplimiento de promesas?",
  f"SELECT c.GRUPOUSUARIO, COUNT(*) AS promesas,\n       ROUND(100.0*SUM(CASE WHEN p.ESTADO_PROMESA='CUMPLIDA' THEN 1 ELSE 0 END)/COUNT(*),1) AS pct_cumplida\nFROM {FQ}.tbl_vreportepromesas p\nJOIN {FQ}.tbl_vreporteedadcartera c ON CAST(p.CEDULA AS BIGINT)=CAST(c.IDENTIFICACION AS BIGINT)\nGROUP BY c.GRUPOUSUARIO ORDER BY pct_cumplida DESC"),
 ("Procesos jurídicos por etapa procesal y capital en juego.",
  f"SELECT ULTIMA_ETAPA_DESCRIPCION, COUNT(*) AS procesos, SUM(CAPITAL) AS capital\nFROM {FQ}.tbl_vreporteprocesosjuridicos\nGROUP BY ULTIMA_ETAPA_DESCRIPCION ORDER BY procesos DESC"),
]


def uid(n):
    import hashlib
    return hashlib.md5(n.encode()).hexdigest()


def build_serialized_space():
    space = {
        "version": 2,
        "data_sources": {"tables": [{"identifier": ident, "description": [desc]} for ident, desc in sorted(TABLES)]},
        "instructions": {
            "text_instructions": [{"id": uid("instr-cobranza"), "content": [l + "\n" for l in INSTRUCTIONS]}],
            "example_question_sqls": sorted(({"id": uid(q), "question": [q], "sql": [sql]} for q, sql in EXAMPLES), key=lambda e: e["id"]),
        },
    }
    return json.dumps(space, ensure_ascii=False)


def main():
    body = {
        "warehouse_id": WAREHOUSE,
        "serialized_space": build_serialized_space(),
        "title": TITLE,
        "description": DESCRIPTION,
        "parent_path": PARENT_PATH,
    }
    tmp = "/tmp/_genie_cobranza_body.json"
    json.dump(body, open(tmp, "w"), ensure_ascii=False)
    out = load.run(["databricks", "api", "post", "/api/2.0/genie/spaces", "--json", f"@{tmp}", "-p", PROFILE])
    res = json.loads(out)
    sid = res.get("space_id")
    host = load.run(["databricks", "auth", "env", "-p", PROFILE]) if False else None
    print("Genie Agent creado:")
    print("  space_id:", sid)
    print("  title   :", res.get("title"))
    print("  URL     : https://fevm-dacamargovws.cloud.databricks.com/genie/rooms/%s?o=7474652595969633" % sid)
    print("\nSiguiente: en Genie, abre el Agent, pulsa 'Share' y compártelo con los participantes.")


if __name__ == "__main__":
    main()
