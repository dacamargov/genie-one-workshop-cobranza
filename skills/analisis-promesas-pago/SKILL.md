---
name: analisis-promesas-pago
description: Analiza las promesas de pago de la cobranza. Úsala cuando pidan "análisis de promesas", "cumplimiento de promesas de pago", "efectividad de asesores" o "cuánto se está recuperando". Calcula tasa de cumplimiento por estado, valor prometido vs cumplido, ranking de asesores y desempeño por grupo de cobranza.
---

# Análisis de promesas de pago

Evalúa qué tan bien está convirtiendo la operación de cobranza las promesas en recuperación real.

## Fuentes de datos

- `tbl_vreportepromesas`: promesas con `VALOR_PROMESA`, `ESTADO_PROMESA`, `NOMBRE_USUARIO`, `REGIONAL`, `CAMPANA`, `CEDULA`.
- `tbl_vreporteedadcartera`: para cruzar por grupo de cobranza (`GRUPOUSUARIO`).

Cédulas con tipos distintos: cruza `tbl_vreportepromesas.CEDULA` con `tbl_vreporteedadcartera.IDENTIFICACION`
convirtiendo ambos con `CAST(... AS BIGINT)`. Valores en **millones de COP**.

## Qué calcular

1. **Cumplimiento por estado:** nº de promesas y % por `ESTADO_PROMESA` (CUMPLIDA, INCUMPLIDA, PARCIAL, VIGENTE).
2. **Recuperación por valor:** valor total prometido y % del valor que corresponde a promesas CUMPLIDA.
3. **Top 10 asesores** (`NOMBRE_USUARIO`) por promesas cumplidas y su tasa de cumplimiento (mínimo 5 promesas).
4. **Desempeño por grupo de cobranza** (`GRUPOUSUARIO`): tasa de cumplimiento de CALL CENTER INTERNO vs OUTSOURCING COBRANZA vs ABOGADOS EXTERNOS.

## Formato de salida

- Título: **"Análisis de promesas de pago"**.
- Una tabla para el cumplimiento por estado y otra para el top de asesores.
- Un párrafo de **lectura ejecutiva**: dónde se está recuperando y dónde se está perdiendo valor.
- 2–3 **recomendaciones** accionables (ej. reforzar seguimiento a promesas vigentes próximas a vencer).
- Español, tono ejecutivo. No muestres SQL salvo que lo pidan.

## Parámetros opcionales

- Filtra por **región**, **campaña** o **rango de fechas** si el usuario lo indica.
