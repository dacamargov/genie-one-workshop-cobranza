# Bloque 7 — Tareas programadas (10 min)

🎯 **Meta:** que un reporte clave llegue **solo**, por correo y como un hilo de chat, sin que nadie tenga que pedirlo.

📄 Doc: [Tareas programadas en Genie One](https://docs.databricks.com/aws/en/genie-one/scheduled-tasks).

---

## 7.1 Crear una tarea desde el chat (5 min)

Una **tarea programada** corre a una hora definida y publica el resultado en un hilo de chat. Además te envía un
correo con el resultado, sus visualizaciones y un **PDF adjunto**.

Pídela en lenguaje natural:

```text
Envíame cada lunes a las 7:00 a.m. un briefing de la cartera en mora: saldo total, desglose por campaña,
top 3 regiones y la tasa de cobertura. En millones de COP.
```

Genie puede hacer **preguntas aclaratorias** (hora, zona horaria, si filtras por región) y luego crea la tarea
en la sección **Schedules**. Si instalaste la skill del Bloque 5, puedes apoyarte en ella:

```text
Programa /briefing-cartera-semanal para que corra todos los lunes a las 7:00 a.m. (hora Bogotá) y me lo envíe por correo.
```

> 💡 Las **skills que instalaste** están disponibles en las tareas programadas, así que la corrida recurrente aplica el mismo formato.

## 7.2 Crear una tarea manualmente (2 min)

1. En la barra lateral, **Schedules** → flecha junto a **+ Create in chat** → **Create manually**.
2. Llena **Title, Instructions, Connections, Schedule y Timezone** → **Create**.

## 7.3 Gestionar y ejecutar ya (3 min)

- **Ver/editar/borrar:** haz clic en la tarea dentro de **Schedules**. Cada corrida abre un hilo de chat.
- **Correr ahora:** al crearla, usa **Run now** para no esperar al horario (ideal para la demo en vivo).
- **Referenciar en el chat:** menciona la tarea con `@` en una nueva pregunta.

```text
@briefing-cartera-lunes córrelo ahora y muéstrame el resultado.
```

---

### ✅ Cierre del bloque

El reporte semanal de cartera ahora es **automático**: llega el lunes a las 7:00 a.m. al correo del comité.

👉 Siguiente: [08-conectores-agentes-cierre.md](08-conectores-agentes-cierre.md)
