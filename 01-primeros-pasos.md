# Bloque 1 — Primeros pasos en el chat (15 min)

🎯 **Meta:** que cada participante abra Genie One, haga su primera pregunta y aprenda a **confiar y verificar** la respuesta.

📄 Doc de referencia: [Chat en Genie One](https://docs.databricks.com/aws/en/genie-one/chat).

---

## 1.1 Abrir el chat (3 min)

1. Entra a Genie One en el workspace [`fevm-dacamargovws`](https://fevm-dacamargovws.cloud.databricks.com/?o=7474652595969633).
2. En la barra lateral, haz clic en **New chat** (o usa el modo **Ask** en la barra de búsqueda).
3. El compute está en **Auto** por defecto: Genie elige el mejor SQL Warehouse. No tienes que configurar nada.

> ℹ️ Para usar el chat necesitas permiso `CAN USE` sobre al menos un SQL Warehouse.

## 1.2 Tu primera pregunta (4 min)

Copia y pega:

```text
¿Qué datos de cobranza tengo disponibles y qué puedo preguntarte?
```

Luego:

```text
¿Cuántos deudores hay en la cartera y cuál es el saldo total en mora?
```

**Respuesta esperada (datos demo):** ~**392 deudores** y un saldo en mora de **~17.123 millones de COP**
(capital ~16.050 millones; mora promedio ~107 días).

## 1.3 Verificar la respuesta con citaciones (4 min)

Genie One responde apoyándose en **Genie Ontology** (tablas, columnas, métricas). Cada respuesta trae **citaciones**
que muestran de dónde salió el dato.

1. Haz clic en el ícono de **citación** de la respuesta anterior.
2. Observa qué tabla usó (`tbl_vreporteedadcartera`) y, si está disponible, el SQL que ejecutó.

> 💡 **Mensaje para ejecutivos:** las respuestas están **gobernadas** y se ejecutan con *tus* permisos de Unity Catalog.
> Siempre puedes abrir la citación para auditar el número antes de usarlo en un comité.

## 1.4 Pedir una visualización (4 min)

```text
Muéstrame el saldo en mora por campaña en un gráfico de barras.
```

- Genie genera la gráfica. Haz clic en el ícono de la esquina inferior derecha para **expandirla** en el panel lateral.
- Prueba refinar sin volver a empezar:

```text
Ahora ordénalo de mayor a menor y agrega el número de deudores por campaña.
```

**Respuesta esperada:** PREJURIDICO (~7.605 MM), COBRANZA TEMPRANA (~4.685 MM), JURIDICO (~2.803 MM), CASTIGADA (~2.029 MM).

---

### ✅ Cierre del bloque

Los participantes ya saben: abrir un chat, preguntar en lenguaje natural, **verificar con citaciones** y pedir gráficos.

👉 Siguiente: [02-preguntas-cartera.md](02-preguntas-cartera.md)
