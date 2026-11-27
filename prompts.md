# Todos los prompts del workshop (copiar y pegar)

Prompts en orden de uso. Cada uno está pensado para pegarse tal cual en el chat de Genie One.
Las respuestas esperadas (datos demo) están validadas en [`datos/validation_results.md`](datos/validation_results.md).

---

## Bloque 1 — Primeros pasos

```text
¿Qué datos de cobranza tengo disponibles y qué puedo preguntarte?
```
```text
¿Cuántos deudores hay en la cartera y cuál es el saldo total en mora?
```
```text
Muéstrame el saldo en mora por campaña en un gráfico de barras.
```
```text
Ahora ordénalo de mayor a menor y agrega el número de deudores por campaña.
```

## Bloque 2 — Cartera

```text
Dame un resumen de la cartera en mora: número de deudores, saldo total, capital y días de mora promedio.
```
```text
¿Cómo se reparte el saldo en mora por campaña? Muéstralo como tabla y como gráfico.
```
```text
¿Cuál es el saldo en mora por región, de mayor a menor? ¿Qué región concentra más cartera?
```
```text
Distribúyeme la cartera por tramo de mora (subcampaña) con saldo y número de deudores.
```
```text
¿Cuánta provisión tenemos constituida y qué porcentaje del capital representa (tasa de cobertura)?
```
```text
Muéstrame los 10 deudores con mayor saldo en mora, con su región, campaña y días de mora.
```
```text
¿Cuántos deudores tienen productos de consumo, comercial e hipotecario?
```
```text
¿Qué estrategia de cobro se está aplicando a los deudores de más de 180 días de mora?
```
```text
Compara el saldo en mora de la regional Valle contra Bogotá y dime la diferencia en porcentaje.
```
```text
¿Cuántos clientes están castigados y cuánto capital representan?
```

## Bloque 3 — Gestiones y promesas

```text
¿Cuántas gestiones de cobranza se registraron en los últimos 90 días y cómo se reparten por canal (voz, digital, campo)?
```
```text
¿Cuál es la tasa de contacto efectivo? Es decir, qué porcentaje de las gestiones logró contacto con el TITULAR frente a tercero o sin contacto.
```
```text
¿Cuáles son los principales motivos de no pago que reportan los deudores? Ordénalos de mayor a menor.
```
```text
¿Cuántas promesas de pago hay y cuál es la tasa de cumplimiento por estado (cumplida, incumplida, parcial, vigente)? Incluye el valor prometido en cada estado.
```
```text
Del total prometido, ¿qué porcentaje corresponde a promesas ya cumplidas?
```
```text
Dame el top 10 de asesores por número de promesas cumplidas, con su tasa de cumplimiento. Solo asesores con 5 o más promesas.
```
```text
¿Qué grupo de cobranza (call center interno, outsourcing, abogados externos) tiene mejor tasa de cumplimiento de promesas?
```

## Bloque 4 — Memoria y personalización

```text
Recuerda que soy gerente de la regional Valle y que, salvo que diga lo contrario, quiero ver siempre las cifras de mi regional y en millones de COP.
```
```text
¿Cómo va mi cartera en mora este corte?
```
```text
¿Qué memorias tienes guardadas sobre mí?
```
```text
Actualiza mi memoria: ahora cubro las regionales Valle y Eje Cafetero.
```
```text
Olvida la memoria sobre la moneda, prefiero verlo sin convertir.
```
```text
¿Recuerdas el análisis de promesas por asesor que hicimos antes? Retomémoslo y ahora desglósalo por región.
```

## Bloque 5 — Skills

```text
Crea una skill llamada "briefing-cartera-semanal" que genere un briefing ejecutivo del estado de la cartera.
Debe incluir: (1) saldo total en mora y nº de deudores, (2) desglose por campaña, (3) top 3 regiones por saldo,
(4) tasa de cobertura (provisión/capital), (5) los 5 deudores de mayor saldo y (6) 3 alertas accionables.
Usa la tabla tbl_vreporteedadcartera, cifras en millones de COP y preséntalo con títulos y viñetas.
```
```text
/briefing-cartera-semanal
```
```text
/analisis-promesas-pago
```
```text
/seguimiento-juridico
```
```text
Edita la skill briefing-cartera-semanal para que además compare el saldo de esta semana con el corte anterior y marque en rojo las regiones que empeoraron.
```

## Bloque 6 — Documentos y artifacts

```text
Redacta un documento de una página con el resumen ejecutivo de la cartera de este corte: situación general, riesgo por región, cobertura de provisión y 3 recomendaciones. Que sea claro para el comité directivo.
```
```text
Crea una presentación de 3 láminas sobre el estado de la cobranza: (1) foto de cartera por campaña, (2) contactabilidad y cumplimiento de promesas, (3) estado del cobro jurídico. Audiencia: comité directivo.
```
```text
Agrega una lámina con el saldo en mora por región en un gráfico de barras.
```
```text
¿Qué región sube más respecto al promedio en esta lámina?
```

## Bloque 7 — Tareas programadas

```text
Envíame cada lunes a las 7:00 a.m. un briefing de la cartera en mora: saldo total, desglose por campaña, top 3 regiones y la tasa de cobertura. En millones de COP.
```
```text
Programa /briefing-cartera-semanal para que corra todos los lunes a las 7:00 a.m. (hora Bogotá) y me lo envíe por correo.
```
```text
@briefing-cartera-lunes córrelo ahora y muéstrame el resultado.
```

## Bloque 8 — Conectores, agentes y cierre

```text
Usa Slack para publicar en el canal #comite-cobranza un resumen de 3 líneas de la cartera en mora de esta semana.
```
```text
Redacta un correo para el equipo regional del Valle con las 3 alertas de cartera más importantes de este corte.
```
```text
Guarda este análisis de cobranza como un agente para poder reutilizarlo. Que incluya las definiciones de campaña, la tasa de cobertura y el cruce de promesas con cartera.
```
```text
Agrega la tabla obligaciones_cobis a mi agente de cobranza.
```
