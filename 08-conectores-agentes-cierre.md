# Bloque 8 — Conectores (MCP), Genie Agent y cierre (5 min)

🎯 **Meta:** mostrar que Genie One no solo **lee datos**, también **actúa** en otras herramientas, y dejar un activo reutilizable.

📄 Docs: [Conectar apps externas con MCP](https://docs.databricks.com/aws/en/genie-one/external-sources) ·
[Crear un Genie Agent desde un chat](https://docs.databricks.com/aws/en/genie-one/create-agent-from-chat).

---

## 8.1 Conectores externos con MCP (demo, 2 min)

Con **MCP** cada usuario conecta apps con sus propias credenciales (Slack, Gmail, Google Drive, Microsoft 365,
Atlassian/Jira, GitHub, etc.). Genie puede **consultar** y **actuar** (ej. redactar un correo, publicar en Slack).

**Conectar una app:** en la home de Genie One, ícono **+** de la barra de búsqueda → **Connectors** → elige la app → **Sign in**.

Ejemplo de acción una vez conectado Slack:

```text
Usa Slack para publicar en el canal #comite-cobranza un resumen de 3 líneas de la cartera en mora de esta semana.
```

Ejemplo con correo (el conector de Gmail/Outlook **redacta** borradores, no envía):

```text
Redacta un correo para el equipo regional del Valle con las 3 alertas de cartera más importantes de este corte.
```

> ℹ️ Los conectores corren bajo **Unity Gateway** con los permisos de cada usuario; si una herramienta no se activa sola,
> pídele explícitamente *"usa Slack"* o *"usa Google Drive"*.

## 8.2 Guardar el trabajo como un Genie Agent (2 min)

Si una conversación acumuló contexto valioso (métricas, definiciones, formato), guárdala como **Genie Agent** reutilizable:

```text
Guarda este análisis de cobranza como un agente para poder reutilizarlo. Que incluya las definiciones de campaña,
la tasa de cobertura y el cruce de promesas con cartera.
```

También: menú **•••** bajo una respuesta → **Create Agent**. Luego puedes editarlo en lenguaje natural:

```text
Agrega la tabla obligaciones_cobis a mi agente de cobranza.
```

## 8.3 Cierre y próximos pasos (1 min)

**Lo que cada ejecutivo se lleva hoy:**

- Preguntar en lenguaje natural y **verificar** con citaciones.
- Analizar cartera, gestiones, promesas y jurídico sin SQL.
- **Skills** para estandarizar reportes y compartirlos.
- **Documentos** y **presentaciones** listos para comité.
- **Tareas programadas** que llegan solas por correo.
- **Conectores** para actuar en Slack/correo y **Agents** reutilizables.

**Tarea para después del workshop:**

1. Crea tu propia skill para el reporte que más repites.
2. Programa ese reporte para que te llegue cada semana.
3. Reproduce el workshop con **tus datos reales** siguiendo [`datos/`](datos/) y [`00-preparacion-facilitador.md`](00-preparacion-facilitador.md).

> 🙌 ¡Gracias! Dudas y feedback al facilitador.
