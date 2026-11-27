# Bloque 2 — Preguntas de negocio sobre la cartera (25 min)

🎯 **Meta:** responder las preguntas que un comité de cobranza hace todas las semanas, en segundos y sin SQL.

📄 Doc: [Chat en Genie One](https://docs.databricks.com/aws/en/genie-one/chat). Tabla base: `tbl_vreporteedadcartera`.

> Todas las respuestas esperadas provienen de los datos demo y están validadas en
> [`datos/validation_results.md`](datos/validation_results.md).

---

## 2.1 Foto general de la cartera (4 min)

```text
Dame un resumen de la cartera en mora: número de deudores, saldo total, capital y días de mora promedio.
```

**Esperado:** 392 deudores · saldo ~17.123 MM COP · capital ~16.050 MM COP · ~107 días de mora promedio.

## 2.2 Composición por campaña (3 min)

```text
¿Cómo se reparte el saldo en mora por campaña? Muéstralo como tabla y como gráfico.
```

**Esperado:** PREJURIDICO 173 deudores / 7.605 MM · COBRANZA TEMPRANA 130 / 4.685 MM · JURIDICO 58 / 2.803 MM · CASTIGADA 31 / 2.029 MM.

## 2.3 Dónde está el riesgo: por región (3 min)

```text
¿Cuál es el saldo en mora por región, de mayor a menor? ¿Qué región concentra más cartera?
```

**Esperado:** VALLE (~5.471 MM) es la mayor, seguida de BOGOTA (~3.537 MM) y ANTIOQUIA (~2.676 MM).

## 2.4 Altura de mora (3 min)

```text
Distribúyeme la cartera por tramo de mora (subcampaña) con saldo y número de deudores.
```

**Esperado:** del TRAMO 1 (1-30) al TRAMO 5 (>180). El TRAMO 1 concentra más deudores (~130) pero hay ~47 deudores con más de 180 días.

## 2.5 Provisión y cobertura (3 min)

```text
¿Cuánta provisión tenemos constituida y qué porcentaje del capital representa (tasa de cobertura)?
```

**Esperado:** provisión ~4.509 MM COP ≈ **28,1%** del capital.

## 2.6 Top deudores (3 min)

```text
Muéstrame los 10 deudores con mayor saldo en mora, con su región, campaña y días de mora.
```

**Esperado:** una tabla encabezada por deudores con saldo individual > 200 MM COP (varios en VALLE).

## 2.7 Por tipo de producto (3 min)

```text
¿Cuántos deudores tienen productos de consumo, comercial e hipotecario?
```

**Esperado:** consumo ~350 · comercial ~48 · hipotecario ~42.

## 2.8 Reto para los participantes (3 min)

Deja que cada quien pregunte lo suyo. Ejemplos para destrabar:

```text
¿Qué estrategia de cobro se está aplicando a los deudores de más de 180 días de mora?
```
```text
Compara el saldo en mora de la regional Valle contra Bogotá y dime la diferencia en porcentaje.
```
```text
¿Cuántos clientes están castigados y cuánto capital representan?
```

> 💡 **Tip de facilitación:** si una respuesta no cuadra, abre la **citación** y revisa el SQL. Suele ser un tema
> de cómo está formulada la pregunta; reformula agregando la métrica exacta (ej. "usa el campo SALDO en COP").

---

### ✅ Cierre del bloque

Los ejecutivos ya pueden sacar la **foto semanal de cartera** (saldo, campaña, región, mora, provisión, top deudores) sin depender de un analista.

👉 Siguiente: [03-gestiones-promesas.md](03-gestiones-promesas.md)
