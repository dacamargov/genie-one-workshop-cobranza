---
name: briefing-cartera-semanal
description: Genera un briefing ejecutivo semanal del estado de la cartera de cobranza en mora. Úsala cuando pidan el "briefing de cartera", el "resumen semanal de cartera" o la "foto de cartera". Resume saldo, composición por campaña y región, cobertura de provisión, top deudores y alertas accionables, en millones de COP.
---

# Briefing semanal de cartera

Produce un informe ejecutivo del estado actual de la cartera en mora, listo para presentar en comité.

## Fuente de datos

Usa la tabla `tbl_vreporteedadcartera` (un registro por deudor en mora). Valores monetarios en **pesos colombianos (COP)**;
repórtalos en **millones de COP** redondeados a un decimal.

## Qué calcular

1. **Resumen general:** número de deudores, saldo total en mora, capital total y días de mora promedio (`AVG(DIASMORA)`).
2. **Composición por campaña** (`CAMPANA`): deudores y saldo por COBRANZA TEMPRANA, PREJURIDICO, JURIDICO y CASTIGADA, ordenado por saldo.
3. **Top 3 regiones** (`REGION`) por saldo en mora.
4. **Cobertura:** tasa de provisión = `SUM(PROVISION) / SUM(CAPITAL)`, en %.
5. **Top 5 deudores** por `SALDO`, con nombre, región, campaña y días de mora.
6. **Alertas accionables (3):** por ejemplo, regiones que concentran el riesgo, peso de la cartera castigada,
   o deudores de alto saldo con mora creciente. Cada alerta debe sugerir una acción.

## Formato de salida

- Título: **"Briefing de cartera — semana del {fecha}"**.
- Secciones con subtítulos en negrita y viñetas; incluye una tabla para la composición por campaña.
- Cierra con las 3 alertas en una lista numerada, cada una con una acción recomendada.
- Tono ejecutivo, en español, conciso. No muestres SQL salvo que lo pidan.

## Parámetros opcionales

- Si el usuario indica una **región** (o tiene una memoria con su regional), filtra todo el briefing a esa región.
- Si pide comparar con el **corte anterior**, incluye la variación del saldo por campaña.
