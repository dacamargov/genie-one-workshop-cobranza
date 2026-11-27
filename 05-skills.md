# Bloque 5 — Skills: automatizar análisis repetibles (20 min)

🎯 **Meta:** convertir un análisis que se hace "siempre igual" en una **Skill** que cualquiera invoca con un `/`, y compartirla con el equipo.

📄 Doc: [Skills en Genie One](https://docs.databricks.com/aws/en/genie-one/skills).

---

## ¿Qué es una Skill?

Una Skill le enseña a Genie One una **tarea repetible** con un formato de salida definido. Genie la carga sola cuando
detecta que es relevante, o la invocas manualmente escribiendo `/` seguido del nombre. Por defecto es privada;
puedes **compartirla con tu equipo**. Una Skill es texto (archivos `SKILL.md`), no admite binarios.

En este workshop creamos 3 skills de cobranza (ya preparadas en [`skills/`](skills/)):

| Skill | Para qué sirve |
|---|---|
| [`briefing-cartera-semanal`](skills/briefing-cartera-semanal/SKILL.md) | Briefing ejecutivo semanal del estado de la cartera. |
| [`analisis-promesas-pago`](skills/analisis-promesas-pago/SKILL.md) | Análisis de promesas: cumplimiento, asesores y recuperación. |
| [`seguimiento-juridico`](skills/seguimiento-juridico/SKILL.md) | Estado del cobro jurídico por etapa, abogado y región. |

---

## 5.1 Crear una Skill desde el chat (5 min)

La forma más simple: **pedirle a Genie que la cree**. Copia y pega:

```text
Crea una skill llamada "briefing-cartera-semanal" que genere un briefing ejecutivo del estado de la cartera.
Debe incluir: (1) saldo total en mora y nº de deudores, (2) desglose por campaña, (3) top 3 regiones por saldo,
(4) tasa de cobertura (provisión/capital), (5) los 5 deudores de mayor saldo y (6) 3 alertas accionables.
Usa la tabla tbl_vreporteedadcartera, cifras en millones de COP y preséntalo con títulos y viñetas.
```

Genie crea la skill y la guarda en tu workspace en `/Workspace/Users/{tu-correo}/.assistant/skills/`.

## 5.2 Invocar una Skill (3 min)

Escribe `/` y selecciona la skill (o deja que Genie la cargue sola cuando sea relevante):

```text
/briefing-cartera-semanal
```

**Esperado:** un briefing estructurado con el saldo (~17.123 MM), el desglose por campaña, el top de regiones
(Valle, Bogotá, Antioquia), la cobertura (~28%) y alertas.

## 5.3 Subir una Skill ya preparada (4 min)

En vez de dictarla, puedes **subir** un `SKILL.md`. Usa los de este repo:

1. En la navegación izquierda, **Customizations → Skills**.
2. **+ New → Upload Skills**.
3. Sube la carpeta de una skill (ej. [`skills/analisis-promesas-pago/`](skills/analisis-promesas-pago/)) o su `SKILL.md`.
4. Si ya existe una con el mismo nombre, Genie pide confirmar antes de reemplazar.

Pruébala:

```text
/analisis-promesas-pago
```

> Las skills subidas siguen la [especificación de Agent Skills](https://docs.databricks.com/aws/en/genie-one/skills)
> y se guardan en tu carpeta `/.assistant/skills/`.

## 5.4 Editar una Skill (2 min)

```text
Edita la skill briefing-cartera-semanal para que además compare el saldo de esta semana con el corte anterior
y marque en rojo las regiones que empeoraron.
```

Revisa los cambios en el panel lateral. También puedes abrirla en **Customizations → Skills → (tu skill) → Edit with Genie**
u **Open in workspace editor**.

## 5.5 Compartir una Skill con el equipo (4 min)

> ⚠️ Requiere dos previews activos (los habilita un admin): *Enhanced Unity AI Gateway* (cuenta) y
> *Unity Gateway skills in Genie* (workspace). Ver la [doc de Skills](https://docs.databricks.com/aws/en/genie-one/skills).

1. **Customizations → Skills**, selecciona la skill y haz clic en **Share**.
2. En **Publish to**, elige catálogo y esquema (necesitas `USE CATALOG`, `USE SCHEMA` y `CREATE VOLUME`).
3. Agrega los usuarios/grupos y el nivel de acceso general. **Done**.

Quien la recibe la ve junto a sus skills y la **instala** para usarla (necesita `READ VOLUME` en ese esquema).
Las skills instaladas también quedan disponibles en las **tareas programadas** (Bloque 7).

> 💡 **Mensaje para ejecutivos:** una skill bien hecha estandariza "cómo se mide" en toda el área. El briefing de cartera
> se ve igual lo pida quien lo pida, y eso elimina discusiones de "¿de dónde salió ese número?".

---

### ✅ Cierre del bloque

El equipo ya sabe crear skills (dictándolas o subiéndolas), invocarlas con `/`, editarlas y compartirlas.

👉 Siguiente: [06-documentos-artifacts.md](06-documentos-artifacts.md)
