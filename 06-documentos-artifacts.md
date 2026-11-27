# Bloque 6 — Documentos y presentaciones (artifacts) (15 min)

🎯 **Meta:** convertir una conversación en un **documento** compartible y en una **presentación (slides)** sin salir de Genie One.

📄 Docs: [Documentos](https://docs.databricks.com/aws/en/genie-one/documents) · [Artifacts](https://docs.databricks.com/aws/en/genie-one/artifacts).

---

## 6.1 Redactar un documento ejecutivo (6 min)

Un **documento** es texto editable que se abre en un panel tipo lienzo, con historial de versiones y comentarios.

Después de analizar la cartera (Bloque 2), pide:

```text
Redacta un documento de una página con el resumen ejecutivo de la cartera de este corte: situación general,
riesgo por región, cobertura de provisión y 3 recomendaciones. Que sea claro para el comité directivo.
```

- El documento se abre en el panel lateral. Edítalo con la barra de herramientas.
- Haz clic en una **citación** para ver de dónde salió cada cifra.
- Abre el **historial de versiones** y agrega un **comentario**.

**Compartir:** botón **Share** del documento → agrega usuarios/grupos (necesitan al menos *CAN EDIT* para editar) o copia el enlace.

## 6.2 Crear una presentación / artifact (6 min)

> ⚠️ Artifacts está en **Beta**: un admin del workspace debe activarlo en **Previews**. Ver la [doc de Artifacts](https://docs.databricks.com/aws/en/genie-one/artifacts).

Un **artifact** es una página visual (ej. un deck de slides) con gráficos y una **instantánea** de los datos.

```text
Crea una presentación de 3 láminas sobre el estado de la cobranza: (1) foto de cartera por campaña,
(2) contactabilidad y cumplimiento de promesas, (3) estado del cobro jurídico. Audiencia: comité directivo.
```

Luego refínala en el mismo hilo:

```text
Agrega una lámina con el saldo en mora por región en un gráfico de barras.
```

- El artifact aparece en el hilo; haz clic para abrirlo. Modos **View / Edit / Data**.
- En **Edit** puedes mover elementos, insertar texto o gráficos. Guarda solo (muestra "Saving…/Saved").
- Prueba **Ask Genie** sobre una lámina: selecciona un gráfico y pregunta.

```text
¿Qué región sube más respecto al promedio en esta lámina?
```

## 6.3 Compartir un artifact (3 min)

> ⚠️ **Dato clave de gobierno:** un artifact guarda una **instantánea** de los datos. Quien pueda verlo ve esa data,
> **aunque no tenga acceso a las tablas de origen**. Revisa con quién lo compartes.

1. Abre el artifact → **Share**.
2. Elige permiso (**Can read** / **Can edit**) y alcance (*solo personas con acceso* o *todo el workspace*).

> 💡 Compartir un **chat** no comparte sus artifacts; el artifact se comparte aparte.

---

### ✅ Cierre del bloque

De la conversación al entregable: un **one-pager** para el comité y un **deck** presentable, en minutos.

👉 Siguiente: [07-tareas-programadas.md](07-tareas-programadas.md)
