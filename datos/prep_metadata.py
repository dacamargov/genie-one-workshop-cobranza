#!/usr/bin/env python3
"""Preparacion de metadatos (ontologia): agrega COMMENT a las columnas clave de las
tablas de reportes para que Genie One entienda el negocio y responda con precision."""
import sys, os
sys.argv = ["x"]
import load

FQ = "dacamargovws_catalog.bancoomeva"

COMMENTS = {
 "tbl_vreporteedadcartera": {
   "IDENTIFICACION": "Documento de identidad (cedula) del deudor. Llave del cliente.",
   "NOMBREDEUDOR": "Nombre completo del deudor.",
   "REGION": "Regional comercial donde esta asignado el deudor.",
   "CIUDAD": "Ciudad del deudor.",
   "ESTADO": "Estado de la cartera del deudor: ACTIVO, EN COBRO JURIDICO o CASTIGADO.",
   "CAMPANA": "Etapa de cobranza: COBRANZA TEMPRANA, PREJURIDICO, JURIDICO o CASTIGADA.",
   "SUBCAMPANA": "Tramo de altura de mora (ej. TRAMO 1 (1-30), TRAMO 5 (>180)).",
   "SALDO": "Saldo total adeudado por el deudor en pesos colombianos (COP).",
   "CAPITAL": "Capital adeudado en COP.",
   "MORA": "Valor total en mora en COP.",
   "PROVISION": "Provision contable constituida sobre la deuda en COP.",
   "DIASMORA": "Dias de mora (altura de mora) del deudor.",
   "GRUPOUSUARIO": "Grupo de cobranza responsable: CALL CENTER INTERNO, OUTSOURCING COBRANZA o ABOGADOS EXTERNOS.",
   "NOMBREUSUARIO": "Nombre del asesor de cobranza asignado.",
   "NOMBREABOGADO": "Nombre del abogado asignado (cuando aplica cobro juridico).",
   "ESTRATEGIA": "Estrategia de cobro definida para el deudor.",
   "CONSUMO": "SI/NO: el deudor tiene productos de consumo.",
   "COMERCIAL": "SI/NO: el deudor tiene productos comerciales.",
   "HIPOTECARIO": "SI/NO: el deudor tiene productos hipotecarios.",
   "CUOTA": "Valor de la cuota mensual en COP.",
 },
 "tbl_vreportegestiones": {
   "ID_DEUDOR": "Documento de identidad (cedula) del deudor gestionado. Cruza con tbl_vreporteedadcartera.IDENTIFICACION.",
   "FECHA_GESTION": "Fecha y hora en que se realizo la gestion de cobranza.",
   "USUARIO": "Login del asesor que realizo la gestion.",
   "ACCION": "Tipo de gestion: LLAMADA SALIENTE, WHATSAPP, SMS, EMAIL, VISITA, etc.",
   "RESPUESTA": "Resultado de la gestion (ej. PROMESA DE PAGO, NO CONTESTA, SE NIEGA A PAGAR).",
   "CONTACTO": "Con quien se logro el contacto: TITULAR, TERCERO o NO CONTACTO.",
   "MOTIVO_NOPAGO": "Motivo de no pago declarado por el deudor.",
   "CANAL": "Canal de la gestion: VOZ, DIGITAL o CAMPO.",
 },
 "tbl_vreportepromesas": {
   "CEDULA": "Documento de identidad (cedula) del deudor que hace la promesa. Cruza con tbl_vreporteedadcartera.IDENTIFICACION.",
   "NOMBRE_CLIENTE": "Nombre del deudor.",
   "VALOR_PROMESA": "Valor prometido a pagar en COP.",
   "FECHA_PROMESA": "Fecha pactada para el pago.",
   "ESTADO_PROMESA": "Estado de la promesa: VIGENTE, CUMPLIDA, INCUMPLIDA o PARCIAL.",
   "NOMBRE_USUARIO": "Nombre del asesor que tomo la promesa.",
   "REGIONAL": "Regional del deudor.",
   "CAMPANA": "Etapa de cobranza en la que se tomo la promesa.",
   "ZONA": "Zona geografica de cobranza.",
 },
 "tbl_vreporteprocesosjuridicos": {
   "CLIENTE_IDENTIFICACION": "Documento de identidad (cedula) del demandado. Cruza con tbl_vreporteedadcartera.IDENTIFICACION.",
   "CLIENTE_NOMBRE": "Nombre del demandado.",
   "REGION": "Regional del proceso.",
   "CAPITAL": "Capital en cobro juridico en COP.",
   "ABOGADO_NOMBRE": "Nombre del abogado externo a cargo del proceso.",
   "PROCESO": "Tipo de proceso judicial (ej. EJECUTIVO SINGULAR).",
   "PROCESO_ESTADO": "Estado del proceso: ACTIVO, SUSPENDIDO, TERMINADO POR PAGO, etc.",
   "PROCESO_JUZGADO": "Juzgado donde cursa el proceso.",
   "ULTIMA_ETAPA_DESCRIPCION": "Etapa procesal actual (DEMANDA, NOTIFICACION, SENTENCIA, EMBARGO Y SECUESTRO, REMATE, etc.).",
 },
}


def main():
    n = 0
    for tbl, cols in COMMENTS.items():
        for col, cmt in cols.items():
            load.sql(f"ALTER TABLE {FQ}.{tbl} ALTER COLUMN `{col}` COMMENT '{cmt}'")
            n += 1
        print(f"OK {tbl}: {len(cols)} columnas comentadas", flush=True)
    print(f"Total {n} columnas con descripcion de negocio.")


if __name__ == "__main__":
    main()
