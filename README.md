# Workshop Genie One

Workshop hands-on para usar [Genie One](https://docs.databricks.com/aws/en/genie-one/) para responder preguntas,
automatizar reportes y tomar acciones sobre la **cartera de cobranza**, en lenguaje natural y **sin escribir SQL**.

El recorrido es el siguiente:

1. El facilitador crea una sola vez un **Genie Agent** sobre las tablas de cobranza (sección 3).
2. A partir de ahí, cada participante va **bajando por esta página** y copiando/pegando los prompts tal cual: primero
   preguntas de negocio sobre la cartera, gestiones y promesas; luego memoria, *skills*, documentos, presentaciones,
   tareas programadas y conectores.

> 📊 **Datos reales, mismo esquema.** Este workshop se corre sobre **tus propias tablas** de cobranza (las mismas que
> ya tienes en producción). No se generan datos: solo apuntas el Genie Agent a tu catálogo y esquema. Las cifras de
> "respuesta esperada" que aparecen abajo son de un entorno de ejemplo y sirven solo como referencia de **cómo debe
> verse** una buena respuesta.

---

## 1. Prerrequisitos

| Requisito | Detalle |
|---|---|
| **Workspace Databricks** | Con **Unity Catalog** y **Genie One** habilitados. |
| **SQL Warehouse** | Cada participante necesita `CAN USE` sobre un warehouse **Pro o Serverless**. Genie One usa **Auto** por defecto. |
| **Entitlement** | *Workspace access* o *Databricks SQL access* (no basta *consumer* para crear skills/agents). |
| **Databricks Assistant** | Habilitado (requisito de Genie). |
| **Tus tablas de cobranza** | Las 17 tablas del esquema (ver sección 2) cargadas en un catálogo/esquema sobre el que tengas acceso. |

> 👤 **Facilitador:** haz la sección 3 **antes** del workshop y comparte el Genie Agent con los participantes.

---

## 2. Las tablas del workshop

El workshop se apoya sobre todo en **4 tablas de reportes** de cobranza. Todas comparten la **cédula del cliente**
como llave para cruzarlas.

| Tabla | Qué contiene |
|---|---|
| `tbl_vreporteedadcartera` | Edad de cartera: un registro por deudor en mora (saldo, días de mora, campaña, asesor). |
| `tbl_vreportegestiones` | Gestiones de cobro (llamadas, WhatsApp, SMS, visitas) con su resultado. |
| `tbl_vreportepromesas` | Promesas de pago con valor, fecha y estado. |
| `tbl_vreporteprocesosjuridicos` | Procesos jurídicos: juzgado, radicado, abogado y etapa procesal. |

Tablas maestras y de productos (opcionales, para la "vista 360"): `cliente`, `direccion`, `correo`,
`tbl_telefono_wsac`, `referencia_cliente`, `referencia_codeudores`, `cuentas_pasivo`, `garantias`,
`pagos_prestamos`, `obligaciones_cobis`, `obligaciones_sat`, `obligaciones_sat_amparadas`, `obligaciones_tarcred`.

> ⚠️ **La cédula tiene tipos distintos por tabla:** `IDENTIFICACION` (texto) en cartera, `ID_DEUDOR` (número) en
> gestiones, `CEDULA` (número) en promesas, `CLIENTE_IDENTIFICACION` (texto) en jurídico, `DOCUMENTO` (texto) en
> cliente. Para cruzarlas hay que convertir **ambos lados** con `CAST(... AS BIGINT)`. Esto queda resuelto en las
> instrucciones del Genie Agent (sección 3).

---

## 3. Preparación: crear el Genie Agent (facilitador)

Genie One primero busca un **Genie Agent** relevante y, si lo encuentra, lo usa para responder
([cómo funciona el chat](https://docs.databricks.com/aws/en/genie-one/chat)). Un Agent curado mejora mucho la precisión.

> 👤 **Esta sección la hace solo el facilitador, una sola vez.** Los participantes **no** pasan por aquí: empiezan en
> la sección 4 y en todo el workshop solo escriben en lenguaje natural, nunca código.

**Pasos (una sola vez):**

1. En la barra lateral abre **Genie** y crea un nuevo agente (**New**).
2. Aparece la pantalla **"What should your Genie Agent do?"** con dos opciones: describirlo en lenguaje natural o
   **seleccionar las tablas manualmente**. Ambas funcionan; para este ejercicio lo haremos **seleccionando las tablas
   manualmente**, pero también puedes crearlo describiendo las tablas en lenguaje natural. Nombra el agente **`Cobranza`**.
3. Al seleccionar las tablas, primero **busca el catálogo y el esquema donde están tus tablas** y ábrelos; allí
   selecciona tus 4 tablas de reportes (y opcionalmente `cliente` y `obligaciones_cobis` para la vista 360). Con tu
   catálogo y esquema reales, las tablas son:

```text
<catalogo>.<esquema>.tbl_vreporteedadcartera
<catalogo>.<esquema>.tbl_vreportegestiones
<catalogo>.<esquema>.tbl_vreportepromesas
<catalogo>.<esquema>.tbl_vreporteprocesosjuridicos
<catalogo>.<esquema>.cliente
<catalogo>.<esquema>.obligaciones_cobis
```

4. En **General instructions** del agente, pega este texto:

```text
Eres un asistente de análisis para el área de cobranza de un banco. Respondes preguntas sobre la cartera en mora,
las gestiones de cobro, las promesas de pago y los procesos jurídicos.

Reglas de negocio:
- Los valores monetarios (SALDO, CAPITAL, MORA, PROVISION, VALOR_PROMESA, CUOTA) están en pesos colombianos (COP).
  Reporta cifras grandes en millones de COP, redondeadas.
- La campaña (CAMPANA) es la etapa de cobranza, de menor a mayor severidad:
  COBRANZA TEMPRANA -> PREJURIDICO -> JURIDICO -> CASTIGADA.
- DIASMORA es la altura de mora del deudor; SUBCAMPANA es el tramo de días de mora.
- Tasa de cobertura = SUM(PROVISION) / SUM(CAPITAL).
- Contacto efectivo = gestiones con CONTACTO = 'TITULAR'.
- Tasa de cumplimiento de promesas = promesas con ESTADO_PROMESA = 'CUMPLIDA' / total de promesas.
- LLAVE DEL CLIENTE (cédula) con tipos distintos por tabla: tbl_vreporteedadcartera.IDENTIFICACION (STRING),
  tbl_vreportegestiones.ID_DEUDOR (DECIMAL), tbl_vreportepromesas.CEDULA (LONG),
  tbl_vreporteprocesosjuridicos.CLIENTE_IDENTIFICACION (STRING), cliente.DOCUMENTO (STRING).
  Para cruzar estas tablas convierte AMBOS lados con CAST(... AS BIGINT).

Estilo: responde en español, tono ejecutivo y conciso. Cuando sea útil muestra una tabla o una visualización
(barras para rankings, torta para distribuciones) e incluye el total y el detalle.
```

5. **Guarda** y **comparte** el agente con los participantes: ábrelo y pulsa **Share** (CAN VIEW / CAN RUN).

> 🧑‍💻 Con las instrucciones de negocio del paso 4 es suficiente para el workshop. Opcionalmente, si el facilitador
> quiere afinar aún más la precisión, el panel del agente permite agregar **consultas de ejemplo** desde la misma
> interfaz de Genie. No es necesario para el ejercicio y los participantes nunca ven ni escriben código.

> ✅ Valida el agente preguntándole *"¿Cuál es el saldo total en mora y cuántos deudores hay?"*: debe responder con el
> total y usar `tbl_vreporteedadcartera`. Prueba también *"¿Qué grupo de cobranza cumple mejor las promesas?"* para
> confirmar que hace bien el cruce con `CAST`.

---

## 4. Primeros pasos en el chat

📄 [Chat en Genie One](https://docs.databricks.com/aws/en/genie-one/chat).

Abre Genie One y haz clic en **New chat** (o usa el modo **Ask**). El compute está en **Auto**: no hay que configurar nada.

> ⚠️ **Importante — dónde escribir.** Todo el workshop (secciones 4 a 11) se hace en el chat de **Genie One**
> (**New chat / Ask**), **no** dentro del room del Genie Agent "Cobranza". Genie One usa el Agent **por detrás** para
> responder tus preguntas de datos, pero las funciones de skills, memoria, documentos, presentaciones y tareas
> programadas viven en Genie One. Si escribes dentro del room del Agent, esas funciones no estarán disponibles.

Copia este primer prompt:

```text
¿Qué datos de cobranza tengo disponibles y qué puedo preguntarte?
```

Ahora pega este:

```text
¿Cuántos deudores hay en la cartera y cuál es el saldo total en mora?
```

**Verifica la respuesta:** haz clic en el ícono de **citación** para ver de qué tabla salió el dato y el SQL que ejecutó.
Las respuestas están gobernadas y corren con *tus* permisos de Unity Catalog.

Pide una visualización:

```text
Muéstrame el saldo en mora por campaña en un gráfico de barras.
```

Refínala sin empezar de nuevo:

```text
Ahora ordénalo de mayor a menor y agrega el número de deudores por campaña.
```

> Respuesta esperada (entorno de ejemplo): PREJURIDICO, COBRANZA TEMPRANA, JURIDICO y CASTIGADA, ordenadas por saldo.

---

## 5. Preguntas de negocio sobre la cartera

Tres preguntas, cada una con gráfico y un insight de negocio. Copia una, mira la respuesta y conversa el hallazgo
antes de pasar a la siguiente.

**a) ¿Dónde está concentrado el riesgo? — por etapa de cobranza**

```text
Muéstrame el saldo en mora por campaña (cobranza temprana, prejurídico, jurídico y castigada) en un gráfico de barras, con el porcentaje que representa cada etapa sobre el total de la cartera. Dime en qué etapa está concentrado el riesgo.
```

> 💡 *Insight:* revela cuánto de la cartera ya escaló a etapas severas (jurídico/castigada) frente a la mora temprana,
> que es la más recuperable.

**b) ¿Qué regiones debemos priorizar? — concentración geográfica**

```text
¿Qué regiones concentran la cartera en mora? Muéstrame el saldo por región en un gráfico de barras ordenado de mayor a menor, e indícame qué porcentaje del total representan las 3 regiones más altas.
```

> 💡 *Insight:* si pocas regiones concentran la mayoría del saldo, ahí deben ir los recursos de cobranza.

**c) ¿Qué tan vieja y cubierta está la cartera? — altura de mora y provisión**

```text
Muéstrame cómo se distribuye el saldo en mora por altura de mora (días de mora) en un gráfico, resáltame cuánto saldo está en mora de más de 180 días y dime qué porcentaje del capital tenemos cubierto con la provisión.
```

> 💡 *Insight:* une antigüedad de la deuda y cobertura; alta mora vieja con baja provisión es una señal de alerta.

---

## 6. Gestiones, contactabilidad y promesas de pago

Tres preguntas que cuentan la historia de la operación: cuánto trabajamos, cuánto recuperamos y quién lo hace mejor.

**a) ¿Estamos contactando a la gente? — productividad y contactabilidad**

```text
Muéstrame las gestiones de cobranza de los últimos 90 días repartidas por canal (voz, digital, campo) en un gráfico, y dime qué porcentaje del total logró contacto efectivo con el titular.
```

> 💡 *Insight:* mide el esfuerzo (volumen por canal) contra el resultado (contacto efectivo). Una contactabilidad baja
> explica buena parte de la mora.

**b) ¿Cuánto estamos recuperando? — promesas de pago**

```text
Muéstrame las promesas de pago por estado (cumplida, incumplida, parcial, vigente) en un gráfico, con el valor prometido en cada estado, y dime la tasa de cumplimiento y qué porcentaje del valor prometido ya se cumplió.
```

> 💡 *Insight:* la tasa de cumplimiento y el valor efectivamente recuperado son el mejor termómetro de la gestión.

**c) ¿Quién cobra mejor? — efectividad por equipo**

```text
¿Qué grupo de cobranza (call center interno, outsourcing, abogados externos) tiene mejor tasa de cumplimiento de promesas? Muéstralo en un gráfico de barras ordenado de mayor a menor.
```

> 💡 *Insight:* compara el desempeño de los equipos internos frente a los externos para decidir dónde reforzar.
> Si Genie necesita ayuda con el cruce, pídele *"cruza por la cédula convirtiendo ambos campos a número"*.

---

## 7. Memoria y personalización

📄 [Personalizar Genie One](https://docs.databricks.com/aws/en/genie-one/personalization).

Genie One guarda memorias **privadas** cuando se lo pides. Crea una:

```text
Recuerda que soy gerente de la regional Valle y que, salvo que diga lo contrario, quiero ver siempre las cifras de mi regional y en millones de COP.
```

Ahora pregunta "a secas" y observa que ya filtra por tu regional:

```text
¿Cómo va mi cartera en mora este corte?
```

Gestiona tus memorias:

```text
¿Qué memorias tienes guardadas sobre mí?
```

```text
Actualiza mi memoria: ahora cubro las regionales Valle y Eje Cafetero.
```

```text
Olvida la memoria sobre la moneda, prefiero verlo sin convertir.
```

Retoma una conversación anterior:

```text
¿Recuerdas el análisis de promesas por asesor que hicimos antes? Retomémoslo y ahora desglósalo por región.
```

---

## 8. Skills: automatizar análisis repetibles

📄 [Skills en Genie One](https://docs.databricks.com/aws/en/genie-one/skills).

Una **Skill** le enseña a Genie una tarea repetible con un formato fijo. La invocas con `/` y puedes compartirla con tu
equipo. En este repo hay 3 skills listas en [`skills/`](skills/).

> ⚠️ Recuerda: las skills son de **Genie One** (su chat propio), no del room del Agent. Haz todo esto desde Genie One
> (**New chat / Ask**). Si pides crear una skill dentro del room del Agent "Cobranza", verás un mensaje de que *"no se
> pueden guardar skills en esta plataforma"*: es porque el room del Agent no es Genie One.

**Opción 1 (recomendada) — subir una skill ya preparada.** En la navegación izquierda de Genie One, **Customizations →
Skills → + New → Upload Skills**, y sube una carpeta de [`skills/`](skills/) (por ejemplo `briefing-cartera-semanal`).
Es el camino más confiable porque no depende de que la creación por chat esté habilitada. Luego invócala escribiendo `/`:

```text
/briefing-cartera-semanal
```

```text
/analisis-promesas-pago
```

```text
/seguimiento-juridico
```

**Opción 2 — crear una skill dictándola** (si tu workspace tiene la creación de skills por chat habilitada). En un
**New chat** de Genie One copia este prompt:

```text
Crea una skill llamada "briefing-cartera-semanal" que genere un briefing ejecutivo del estado de la cartera.
Debe incluir: (1) saldo total en mora y nº de deudores, (2) desglose por campaña, (3) top 3 regiones por saldo,
(4) tasa de cobertura (provisión/capital), (5) los 5 deudores de mayor saldo y (6) 3 alertas accionables.
Cifras en millones de COP y preséntalo con títulos y viñetas.
```

Genie la guarda en `/Workspace/Users/{tu-correo}/.assistant/skills/` y la invocas igual con `/briefing-cartera-semanal`.

> 💡 **Si tu workspace aún no tiene skills habilitadas**, no te detengas: pega el mismo texto del briefing como una
> pregunta normal (sin la parte "Crea una skill llamada…", empezando por "Dame un briefing ejecutivo…") y Genie lo
> genera al instante. Pierdes solo el poder invocarlo luego con `/`.

**Editar una skill:**

```text
Edita la skill briefing-cartera-semanal para que además compare el saldo de esta semana con el corte anterior y marque las regiones que empeoraron.
```

**Compartir con el equipo:** **Customizations → Skills**, selecciona la skill → **Share** → elige catálogo y esquema y
agrega usuarios/grupos. (Requiere los previews *Enhanced Unity AI Gateway* y *Unity Gateway skills in Genie*, que
habilita un admin; ver la [doc de Skills](https://docs.databricks.com/aws/en/genie-one/skills).)

---

## 9. Documentos y presentaciones

📄 [Documentos](https://docs.databricks.com/aws/en/genie-one/documents) · [Artifacts](https://docs.databricks.com/aws/en/genie-one/artifacts).

**Redactar un documento ejecutivo** — después de analizar la cartera:

```text
Redacta un documento de una página con el resumen ejecutivo de la cartera de este corte: situación general, riesgo por región, cobertura de provisión y 3 recomendaciones. Que sea claro para el comité directivo.
```

Se abre en un panel editable, con citaciones, historial de versiones y comentarios. Compártelo con **Share** (quien edite
necesita *CAN EDIT*).

**Crear una presentación (artifact)** — *(Beta; un admin debe activar Artifacts en Previews)*:

```text
Crea una presentación de 3 láminas sobre el estado de la cobranza: (1) foto de cartera por campaña, (2) contactabilidad y cumplimiento de promesas, (3) estado del cobro jurídico. Audiencia: comité directivo.
```

Refínala en el mismo hilo:

```text
Agrega una lámina con el saldo en mora por región en un gráfico de barras.
```

Pregúntale a una lámina (**Ask Genie**): selecciona un gráfico y pega:

```text
¿Qué región sube más respecto al promedio en esta lámina?
```

> ⚠️ Un artifact guarda una **instantánea** de los datos: quien pueda verlo ve esa data aunque no tenga acceso a las
> tablas de origen. Revisa con quién lo compartes.

---

## 10. Tareas programadas

📄 [Tareas programadas](https://docs.databricks.com/aws/en/genie-one/scheduled-tasks).

Una tarea programada corre sola a una hora y te manda el resultado por **correo** (con PDF) y como hilo de chat.

```text
Envíame cada lunes a las 7:00 a.m. (hora Bogotá) un briefing de la cartera en mora: saldo total, desglose por campaña, top 3 regiones y la tasa de cobertura. En millones de COP.
```

Si ya instalaste la skill, apóyate en ella:

```text
Programa /briefing-cartera-semanal para que corra todos los lunes a las 7:00 a.m. (hora Bogotá) y me lo envíe por correo.
```

Córrela en vivo para la demo (o desde **Schedules → Run now**):

```text
@briefing-cartera-lunes córrelo ahora y muéstrame el resultado.
```

También puedes crearla manualmente en **Schedules → Create → Create manually** (Title, Instructions, Connections,
Schedule, Timezone).

---

## 11. Conectores (MCP), Genie Agent reutilizable y cierre

📄 [Conectar apps externas con MCP](https://docs.databricks.com/aws/en/genie-one/external-sources) ·
[Crear un Genie Agent desde un chat](https://docs.databricks.com/aws/en/genie-one/create-agent-from-chat).

**Conectar una app** (Slack, Gmail, Google Drive, Microsoft 365, Jira, GitHub…): en la home, ícono **+** de la barra →
**Connectors** → elige la app → **Sign in**. Luego:

```text
Usa Slack para publicar en el canal #comite-cobranza un resumen de 3 líneas de la cartera en mora de esta semana.
```

```text
Redacta un correo para el equipo regional del Valle con las 3 alertas de cartera más importantes de este corte.
```

**Guardar el trabajo como un Genie Agent reutilizable:**

```text
Guarda este análisis de cobranza como un agente para poder reutilizarlo. Que incluya las definiciones de campaña, la tasa de cobertura y el cruce de promesas con cartera.
```

**Cierre — lo que cada participante se lleva:** preguntar y verificar con citaciones; analizar cartera, gestiones,
promesas y jurídico sin SQL; *skills* para estandarizar reportes; documentos y presentaciones para comité; tareas
automáticas por correo; y conectores para actuar en Slack/correo.

**Tarea para después:** (1) crea tu propia skill para el reporte que más repites, (2) prográmalo para que te llegue cada
semana, (3) comparte tu mejor skill con el equipo.

---

## 12. Estructura del repo

```
genie-one-workshop-hands-on/
├── README.md                              # este workshop completo, de arriba a abajo
└── skills/
    ├── briefing-cartera-semanal/SKILL.md  # briefing ejecutivo semanal de cartera
    ├── analisis-promesas-pago/SKILL.md    # cumplimiento de promesas y asesores
    └── seguimiento-juridico/SKILL.md      # estado del cobro jurídico
```

Documentación de Genie One:
[Genie One](https://docs.databricks.com/aws/en/genie-one/) ·
[Chat](https://docs.databricks.com/aws/en/genie-one/chat) ·
[Skills](https://docs.databricks.com/aws/en/genie-one/skills) ·
[Scheduled tasks](https://docs.databricks.com/aws/en/genie-one/scheduled-tasks) ·
[Personalization](https://docs.databricks.com/aws/en/genie-one/personalization) ·
[Documents](https://docs.databricks.com/aws/en/genie-one/documents) ·
[Artifacts](https://docs.databricks.com/aws/en/genie-one/artifacts) ·
[MCP](https://docs.databricks.com/aws/en/genie-one/external-sources) ·
[Crear un Genie Agent](https://docs.databricks.com/aws/en/genie-one/create-agent-from-chat).

> Datos de ejemplo sintéticos. El esquema es real, para reproducir el workshop con datos propios.
