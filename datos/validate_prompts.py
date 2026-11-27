#!/usr/bin/env python3
"""Valida cada prompt del workshop ejecutando el SQL equivalente contra los datos.
Genera validation_results.md con la 'respuesta esperada' de cada pregunta."""
import sys, os
sys.argv = ["x"]
import load  # reutiliza load.sql / conexion

FQ = "dacamargovws_catalog.bancoomeva"
HERE = os.path.dirname(os.path.abspath(__file__))

# (id, modulo, pregunta en lenguaje natural, sql de validacion)
CHECKS = [
 ("2.1", "Cartera", "¿Cuál es el saldo total en mora de la cartera y cuántos deudores únicos hay?",
  f"SELECT COUNT(*) deudores, ROUND(SUM(SALDO)/1e6,1) saldo_mm, ROUND(SUM(CAPITAL)/1e6,1) capital_mm, ROUND(AVG(DIASMORA),0) dias_mora_prom FROM {FQ}.tbl_vreporteedadcartera"),
 ("2.2", "Cartera", "Muéstrame el saldo en mora y el número de deudores por campaña.",
  f"SELECT CAMPANA, COUNT(*) deudores, ROUND(SUM(SALDO)/1e6,1) saldo_mm FROM {FQ}.tbl_vreporteedadcartera GROUP BY 1 ORDER BY 3 DESC"),
 ("2.3", "Cartera", "¿Cuál es el saldo en mora por región? Ordena de mayor a menor.",
  f"SELECT REGION, COUNT(*) deudores, ROUND(SUM(SALDO)/1e6,1) saldo_mm FROM {FQ}.tbl_vreporteedadcartera GROUP BY 1 ORDER BY 3 DESC"),
 ("2.4", "Cartera", "¿Cómo se distribuye la cartera por tramo de mora (subcampaña)?",
  f"SELECT SUBCAMPANA, COUNT(*) deudores, ROUND(SUM(SALDO)/1e6,1) saldo_mm FROM {FQ}.tbl_vreporteedadcartera GROUP BY 1 ORDER BY 1"),
 ("2.5", "Cartera", "¿Cuánta provisión tenemos constituida y qué porcentaje del capital representa?",
  f"SELECT ROUND(SUM(PROVISION)/1e6,1) provision_mm, ROUND(SUM(CAPITAL)/1e6,1) capital_mm, ROUND(100*SUM(PROVISION)/SUM(CAPITAL),1) pct_cobertura FROM {FQ}.tbl_vreporteedadcartera"),
 ("2.6", "Cartera", "¿Quiénes son los 10 deudores con mayor saldo en mora?",
  f"SELECT NOMBREDEUDOR, REGION, CAMPANA, DIASMORA, ROUND(SALDO/1e6,1) saldo_mm FROM {FQ}.tbl_vreporteedadcartera ORDER BY SALDO DESC LIMIT 10"),
 ("2.7", "Cartera", "Distribución de la cartera por tipo de producto (consumo, comercial, hipotecario).",
  f"SELECT SUM(CASE WHEN CONSUMO='SI' THEN 1 ELSE 0 END) consumo, SUM(CASE WHEN COMERCIAL='SI' THEN 1 ELSE 0 END) comercial, SUM(CASE WHEN HIPOTECARIO='SI' THEN 1 ELSE 0 END) hipotecario FROM {FQ}.tbl_vreporteedadcartera"),
 ("3.x", "Gestiones", "¿Cuántas gestiones de cobranza se registraron en los últimos 90 días y cómo se reparten por canal?",
  f"SELECT CANAL, COUNT(*) gestiones FROM {FQ}.tbl_vreportegestiones WHERE FECHA_GESTION >= DATEADD(day,-90,current_date()) GROUP BY 1 ORDER BY 2 DESC"),
 ("3.y", "Gestiones", "¿Cuál es la tasa de contacto efectivo (titular) sobre el total de gestiones?",
  f"SELECT CONTACTO, COUNT(*) n, ROUND(100.0*COUNT(*)/SUM(COUNT(*)) OVER(),1) pct FROM {FQ}.tbl_vreportegestiones GROUP BY 1 ORDER BY 2 DESC"),
 ("3.z", "Gestiones", "¿Cuáles son los principales motivos de no pago reportados?",
  f"SELECT MOTIVO_NOPAGO, COUNT(*) n FROM {FQ}.tbl_vreportegestiones WHERE MOTIVO_NOPAGO IS NOT NULL GROUP BY 1 ORDER BY 2 DESC"),
 ("4.1", "Promesas", "¿Cuántas promesas de pago hay y cuál es la tasa de cumplimiento por estado?",
  f"SELECT ESTADO_PROMESA, COUNT(*) n, ROUND(SUM(VALOR_PROMESA)/1e6,1) valor_mm, ROUND(100.0*COUNT(*)/SUM(COUNT(*)) OVER(),1) pct FROM {FQ}.tbl_vreportepromesas GROUP BY 1 ORDER BY 2 DESC"),
 ("4.2", "Promesas", "¿Cuál es el valor total prometido y qué porcentaje corresponde a promesas cumplidas?",
  f"SELECT ROUND(SUM(VALOR_PROMESA)/1e6,1) total_prometido_mm, ROUND(SUM(CASE WHEN ESTADO_PROMESA='CUMPLIDA' THEN VALOR_PROMESA ELSE 0 END)/1e6,1) cumplido_mm, ROUND(100.0*SUM(CASE WHEN ESTADO_PROMESA='CUMPLIDA' THEN VALOR_PROMESA ELSE 0 END)/SUM(VALOR_PROMESA),1) pct_valor_cumplido FROM {FQ}.tbl_vreportepromesas"),
 ("4.3", "Promesas", "Top 10 asesores por número de promesas cumplidas y su tasa de cumplimiento.",
  f"SELECT NOMBRE_USUARIO, COUNT(*) promesas, SUM(CASE WHEN ESTADO_PROMESA='CUMPLIDA' THEN 1 ELSE 0 END) cumplidas, ROUND(100.0*SUM(CASE WHEN ESTADO_PROMESA='CUMPLIDA' THEN 1 ELSE 0 END)/COUNT(*),1) pct FROM {FQ}.tbl_vreportepromesas GROUP BY 1 HAVING COUNT(*)>=5 ORDER BY cumplidas DESC LIMIT 10"),
 ("4.4", "Promesas", "¿Qué grupo de cobranza tiene mejor tasa de cumplimiento de promesas? (cruce con cartera)",
  f"SELECT c.GRUPOUSUARIO, COUNT(*) promesas, ROUND(100.0*SUM(CASE WHEN p.ESTADO_PROMESA='CUMPLIDA' THEN 1 ELSE 0 END)/COUNT(*),1) pct_cumplida FROM {FQ}.tbl_vreportepromesas p JOIN {FQ}.tbl_vreporteedadcartera c ON CAST(p.CEDULA AS STRING)=c.IDENTIFICACION GROUP BY 1 ORDER BY pct_cumplida DESC"),
 ("5.1", "Jurídico", "¿Cuántos procesos jurídicos hay y cómo se distribuyen por etapa procesal?",
  f"SELECT ULTIMA_ETAPA_DESCRIPCION, COUNT(*) procesos, ROUND(SUM(CAPITAL)/1e6,1) capital_mm FROM {FQ}.tbl_vreporteprocesosjuridicos GROUP BY 1 ORDER BY 2 DESC"),
 ("5.2", "Jurídico", "¿Cuál es el capital en cobro jurídico por región y el estado de los procesos?",
  f"SELECT REGION, COUNT(*) procesos, ROUND(SUM(CAPITAL)/1e6,1) capital_mm FROM {FQ}.tbl_vreporteprocesosjuridicos GROUP BY 1 ORDER BY 3 DESC"),
 ("5.3", "Jurídico", "¿Cuántos procesos lleva cada abogado y qué capital gestionan?",
  f"SELECT ABOGADO_NOMBRE, COUNT(*) procesos, ROUND(SUM(CAPITAL)/1e6,1) capital_mm FROM {FQ}.tbl_vreporteprocesosjuridicos GROUP BY 1 ORDER BY 2 DESC"),
 ("6.1", "Obligaciones", "¿Cuál es el saldo y la provisión por sistema de origen (COBIS, SAT, tarjeta)?",
  f"""SELECT 'COBIS' sistema, COUNT(*) obligaciones, ROUND(SUM(SALDO)/1e6,1) saldo_mm FROM {FQ}.obligaciones_cobis
      UNION ALL SELECT 'TARJETA', COUNT(*), ROUND(SUM(SALDO)/1e6,1) FROM {FQ}.obligaciones_tarcred
      UNION ALL SELECT 'SAT', COUNT(*), ROUND(SUM(SALDO)/1e6,1) FROM {FQ}.obligaciones_sat
      ORDER BY saldo_mm DESC"""),
 ("6.2", "360 cliente", "Para el deudor de mayor saldo: datos de contacto, obligaciones y última gestión (vista 360).",
  f"""WITH top AS (SELECT IDENTIFICACION FROM {FQ}.tbl_vreporteedadcartera ORDER BY SALDO DESC LIMIT 1)
      SELECT c.PRIMER_NOMBRE, c.PRIMER_APELLIDO, c.REGIONAL, c.INGRESO,
             (SELECT COUNT(*) FROM {FQ}.obligaciones_cobis o WHERE o.NIT=c.DOCUMENTO) oblig_cobis,
             (SELECT COUNT(*) FROM {FQ}.tbl_vreportegestiones g WHERE CAST(g.ID_DEUDOR AS BIGINT)=CAST(c.DOCUMENTO AS BIGINT)) gestiones
      FROM {FQ}.cliente c JOIN top ON c.DOCUMENTO=top.IDENTIFICACION"""),
]


def render(res):
    cols = res["manifest"]["schema"]["columns"]
    data = res["result"].get("data_array", []) or []
    names = [c["name"] for c in cols]
    lines = ["| " + " | ".join(names) + " |", "|" + "|".join(["---"] * len(names)) + "|"]
    for row in data[:12]:
        lines.append("| " + " | ".join("" if v is None else str(v) for v in row) + " |")
    return "\n".join(lines), len(data)


def main():
    out = ["# Validación de prompts del workshop\n",
           f"Ejecutado contra `{FQ}`. Cada sección muestra el prompt en lenguaje natural que el ejecutivo escribe en Genie One y la **respuesta esperada** (SQL de control).\n"]
    ok = 0
    for cid, mod, pregunta, sql in CHECKS:
        try:
            res = load.sql(sql)
            table, n = render(res)
            status = "✅" if n > 0 else "⚠️ sin filas"
            if n > 0:
                ok += 1
            out.append(f"\n## [{cid}] {mod} — {pregunta}\n\n{status} ({n} filas)\n\n{table}\n")
            print(f"{status} [{cid}] {mod}: {n} filas")
        except Exception as e:
            out.append(f"\n## [{cid}] {mod} — {pregunta}\n\n❌ ERROR: {e}\n")
            print(f"❌ [{cid}] {mod}: {e}")
    open(os.path.join(HERE, "validation_results.md"), "w").write("\n".join(out))
    print(f"\n{ok}/{len(CHECKS)} prompts devuelven datos. -> validation_results.md")


if __name__ == "__main__":
    main()
