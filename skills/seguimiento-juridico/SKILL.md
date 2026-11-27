---
name: seguimiento-juridico
description: Resume el estado del cobro jurídico de la cartera. Úsala cuando pidan "estado jurídico", "procesos judiciales de cobranza", "seguimiento a abogados" o "cartera en cobro jurídico". Reporta procesos por etapa procesal, capital en juego, carga por abogado y por región, y alertas de procesos estancados.
---

# Seguimiento del cobro jurídico

Da visibilidad ejecutiva sobre los procesos judiciales de recuperación de cartera.

## Fuente de datos

Usa `tbl_vreporteprocesosjuridicos`. Valores monetarios (`CAPITAL`) en **millones de COP**.

Campos clave: `ULTIMA_ETAPA_DESCRIPCION` (etapa procesal: DEMANDA, ADMISION, NOTIFICACION, EXCEPCIONES, SENTENCIA,
LIQUIDACION, EMBARGO Y SECUESTRO, REMATE), `PROCESO_ESTADO`, `ABOGADO_NOMBRE`, `REGION`,
`PROCESO_FECHA_ULTIMA_ACTUALIZACION`.

## Qué calcular

1. **Procesos por etapa procesal:** nº de procesos y capital por `ULTIMA_ETAPA_DESCRIPCION`.
2. **Capital en cobro jurídico por región**, ordenado de mayor a menor.
3. **Carga por abogado:** nº de procesos y capital que gestiona cada `ABOGADO_NOMBRE`.
4. **Estado de los procesos:** cuántos ACTIVO, SUSPENDIDO, TERMINADO POR PAGO, TERMINADO POR DESISTIMIENTO.
5. **Alertas:** procesos sin actualización reciente (`PROCESO_FECHA_ULTIMA_ACTUALIZACION` antigua) o con alto capital en etapas iniciales.

## Formato de salida

- Título: **"Seguimiento del cobro jurídico"**.
- Tablas para etapas, regiones y abogados; incluye totales.
- Una **lectura ejecutiva** de 1 párrafo: dónde está concentrado el capital y qué procesos requieren atención.
- 2–3 **alertas** con acción sugerida (ej. escalar procesos estancados en etapa de notificación).
- Español, tono ejecutivo. No muestres SQL salvo que lo pidan.

## Parámetros opcionales

- Filtra por **región** o **abogado** si el usuario lo indica.
