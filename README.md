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

5. Agrega estas **Example SQL queries** (ayudan a Genie a aprender los cruces). Reemplaza `<catalogo>.<esquema>`:

```sql
-- Saldo en mora por campaña
SELECT CAMPANA, COUNT(*) AS deudores, SUM(SALDO) AS saldo
FROM <catalogo>.<esquema>.tbl_vreporteedadcartera
GROUP BY CAMPANA ORDER BY saldo DESC;
```

```sql
-- Tasa de cumplimiento de promesas por grupo de cobranza (cruce por cédula)
SELECT c.GRUPOUSUARIO, COUNT(*) AS promesas,
       ROUND(100.0*SUM(CASE WHEN p.ESTADO_PROMESA='CUMPLIDA' THEN 1 ELSE 0 END)/COUNT(*),1) AS pct_cumplida
FROM <catalogo>.<esquema>.tbl_vreportepromesas p
JOIN <catalogo>.<esquema>.tbl_vreporteedadcartera c
  ON CAST(p.CEDULA AS BIGINT) = CAST(c.IDENTIFICACION AS BIGINT)
GROUP BY c.GRUPOUSUARIO ORDER BY pct_cumplida DESC;
```

```sql
-- Procesos jurídicos por etapa procesal
SELECT ULTIMA_ETAPA_DESCRIPCION, COUNT(*) AS procesos, SUM(CAPITAL) AS capital
FROM <catalogo>.<esquema>.tbl_vreporteprocesosjuridicos
GROUP BY ULTIMA_ETAPA_DESCRIPCION ORDER BY procesos DESC;
```

6. **Guarda** y **comparte** el agente con los participantes: ábrelo y pulsa **Share** (CAN VIEW / CAN RUN).

> ✅ Valida el agente preguntándole *"¿Cuál es el saldo total en mora y cuántos deudores hay?"*: debe responder con el
> total y usar `tbl_vreporteedadcartera`. Prueba también *"¿Qué grupo de cobranza cumple mejor las promesas?"* para
> confirmar que hace bien el cruce con `CAST`.

---

## 4. Primeros pasos en el chat

📄 [Chat en Genie One](https://docs.databricks.com/aws/en/genie-one/chat).

Abre Genie One y haz clic en **New chat** (o usa el modo **Ask**). El compute está en **Auto**: no hay que configurar nada.

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

Base: `tbl_vreporteedadcartera`. Copia y pega uno por uno.

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

**Reto libre** — que cada quien pregunte lo suyo. Ejemplos para destrabar:

```text
¿Qué estrategia de cobro se está aplicando a los deudores de más de 180 días de mora?
```

```text
Compara el saldo en mora de la regional Valle contra Bogotá y dime la diferencia en porcentaje.
```

```text
¿Cuántos clientes están castigados y cuánto capital representan?
```

> 💡 Si una respuesta no cuadra, abre la **citación** y revisa el SQL; suele ser la formulación. Reformula agregando la
> métrica exacta (p. ej. *"usa el campo SALDO en COP"*).

---

## 6. Gestiones, contactabilidad y promesas de pago

Tablas: `tbl_vreportegestiones`, `tbl_vreportepromesas`.

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

> 💡 La última pregunta cruza **promesas** con **cartera** por la cédula. Si Genie falla el cruce, recuérdale:
> *"cruza por la cédula convirtiendo ambos campos a número"*.

También puedes mirar el cobro jurídico:

```text
¿Cuántos procesos jurídicos hay y cómo se distribuyen por etapa procesal? Incluye el capital en cada etapa.
```

```text
¿Cuál es el capital en cobro jurídico por región y cuántos procesos lleva cada abogado?
```

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

**Crear una skill dictándola** — copia este prompt:

```text
Crea una skill llamada "briefing-cartera-semanal" que genere un briefing ejecutivo del estado de la cartera.
Debe incluir: (1) saldo total en mora y nº de deudores, (2) desglose por campaña, (3) top 3 regiones por saldo,
(4) tasa de cobertura (provisión/capital), (5) los 5 deudores de mayor saldo y (6) 3 alertas accionables.
Usa la tabla tbl_vreporteedadcartera, cifras en millones de COP y preséntalo con títulos y viñetas.
```

Genie la guarda en `/Workspace/Users/{tu-correo}/.assistant/skills/`. **Invócala** escribiendo `/`:

```text
/briefing-cartera-semanal
```

**Subir una skill ya preparada** (alternativa): en la navegación izquierda, **Customizations → Skills → + New → Upload
Skills**, y sube una carpeta de [`skills/`](skills/) (por ejemplo `analisis-promesas-pago`). Luego pruébala:

```text
/analisis-promesas-pago
```

```text
/seguimiento-juridico
```

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
