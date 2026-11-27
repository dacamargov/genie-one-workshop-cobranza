#!/usr/bin/env python3
"""Sube los CSV sinteticos a un Volume de UC y crea las 17 tablas con los tipos del Excel (schema.json)."""
import json, os, subprocess, sys, time

PROFILE = "fevm-dacamargovws"
WAREHOUSE = "61200af9c31dec2e"
CATALOG, SCHEMA_UC = "dacamargovws_catalog", "bancoomeva"
VOLUME = "workshop_raw"
HERE = os.path.dirname(os.path.abspath(__file__))
DATA = os.path.join(HERE, "data")
SCHEMA = json.load(open(os.path.join(HERE, "schema.json")))

TYPE = {"STRING": "STRING", "DECIMAL": "DECIMAL(18,2)", "TIMESTAMP": "TIMESTAMP", "DATE": "DATE", "INT": "INT",
        "LONG": "BIGINT", "DOUBLE": "DOUBLE", "FLOAT": "FLOAT"}
COMMENTS = {
    "tbl_vreporteedadcartera": "Reporte de edad de cartera: un registro por deudor en mora (saldo, capital, dias de mora, campana, asesor/abogado asignado y datos de contacto). DATOS SINTETICOS.",
    "tbl_vreportegestiones": "Gestiones de cobranza (llamadas, WhatsApp, SMS, email, visitas) realizadas sobre cada deudor, con respuesta y motivo de no pago. DATOS SINTETICOS.",
    "tbl_vreporteprocesosjuridicos": "Procesos juridicos de cobro: juzgado, radicado, abogado, etapa y sub-etapa procesal. DATOS SINTETICOS.",
    "tbl_vreportepromesas": "Promesas de pago registradas en la gestion de cobranza, con valor, fecha y estado (vigente, cumplida, incumplida, parcial). DATOS SINTETICOS.",
    "cliente": "Informacion demografica, laboral y de calificacion del cliente (un registro por documento). DATOS SINTETICOS.",
    "correo": "Correos electronicos del cliente. DATOS SINTETICOS.",
    "cuentas_pasivo": "Cuentas de pasivo del cliente (ahorros, corriente, CDT) con saldo y estado. DATOS SINTETICOS.",
    "direccion": "Direcciones del cliente (residencia, comercial, correspondencia). DATOS SINTETICOS.",
    "garantias": "Garantias (hipoteca/prenda) asociadas a las obligaciones, con avaluo y valor actual. DATOS SINTETICOS.",
    "obligaciones_cobis": "Obligaciones de credito del sistema COBIS (libranza, consumo, vehiculo, hipotecario, comercial, educativo). DATOS SINTETICOS.",
    "obligaciones_sat": "Obligaciones de credito del sistema SAT. DATOS SINTETICOS.",
    "obligaciones_sat_amparadas": "Obligaciones SAT amparadas (con amparador). DATOS SINTETICOS.",
    "obligaciones_tarcred": "Obligaciones de tarjeta de credito. DATOS SINTETICOS.",
    "pagos_prestamos": "Pagos recibidos sobre prestamos. DATOS SINTETICOS.",
    "referencia_cliente": "Referencias personales, familiares y comerciales del cliente. DATOS SINTETICOS.",
    "referencia_codeudores": "Codeudores asociados a cada obligacion. DATOS SINTETICOS.",
    "tbl_telefono_wsac": "Telefonos del cliente (celular, fijo, trabajo). DATOS SINTETICOS.",
}


def run(cmd, **kw):
    r = subprocess.run(cmd, capture_output=True, text=True, **kw)
    if r.returncode != 0:
        raise RuntimeError(f"{' '.join(cmd)}\n{r.stdout}\n{r.stderr}")
    return r.stdout


def sql(stmt):
    body = json.dumps({"warehouse_id": WAREHOUSE, "statement": stmt, "wait_timeout": "50s", "on_wait_timeout": "CONTINUE"})
    out = json.loads(run(["databricks", "api", "post", "/api/2.0/sql/statements", "--json", body, "-p", PROFILE]))
    while out["status"]["state"] in ("PENDING", "RUNNING"):
        time.sleep(3)
        out = json.loads(run(["databricks", "api", "get", f"/api/2.0/sql/statements/{out['statement_id']}", "-p", PROFILE]))
    if out["status"]["state"] != "SUCCEEDED":
        raise RuntimeError(f"SQL fallo: {out['status']}\n{stmt[:400]}")
    return out


def main():
    fq = f"{CATALOG}.{SCHEMA_UC}"
    sql(f"CREATE VOLUME IF NOT EXISTS {fq}.{VOLUME} COMMENT 'CSV sinteticos del workshop Genie One'")
    vol = f"/Volumes/{CATALOG}/{SCHEMA_UC}/{VOLUME}"
    for t in SCHEMA:
        name = t["table"]
        src = os.path.join(DATA, f"{name}.csv")
        run(["databricks", "fs", "cp", src, f"dbfs:{vol}/{name}.csv", "--overwrite", "-p", PROFILE])
        read_schema = ", ".join(f"`{c['name']}` STRING" for c in t["columns"])
        cols = ", ".join(f"TRY_CAST(`{c['name']}` AS {TYPE[c['type']]}) AS `{c['name']}`" if c["type"] != "STRING" else f"`{c['name']}`" for c in t["columns"])
        sql(f"DROP TABLE IF EXISTS {fq}.{name}")
        sql(f"CREATE TABLE {fq}.{name} COMMENT '{COMMENTS[name]}' AS SELECT {cols} FROM read_files('{vol}/{name}.csv', format => 'csv', header => true, schema => '{read_schema}')")
        n = sql(f"SELECT COUNT(*) FROM {fq}.{name}")["result"]["data_array"][0][0]
        print(f"OK {name:32s} {n:>6s} filas", flush=True)


if __name__ == "__main__":
    main()
