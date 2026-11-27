# Bloque 4 — Memoria y personalización (10 min)

🎯 **Meta:** que Genie One recuerde el contexto de cada ejecutivo para no repetirlo en cada conversación.

📄 Doc: [Personalizar Genie One](https://docs.databricks.com/aws/en/genie-one/personalization).

---

## 4.1 Crear una memoria (4 min)

Genie One guarda una memoria cuando se lo pides explícitamente. Las memorias son **privadas** de cada usuario.

```text
Recuerda que soy gerente de la regional Valle y que, salvo que diga lo contrario,
quiero ver siempre las cifras de mi regional y en millones de COP.
```

A partir de ahí, prueba una pregunta "a secas":

```text
¿Cómo va mi cartera en mora este corte?
```

**Esperado:** Genie responde ya filtrado por **Valle** y en **millones de COP**, sin que lo repitas. La respuesta
incluye una citación a la memoria usada (puedes darle 👍/👎).

## 4.2 Memoria sugerida (2 min)

A veces Genie detecta un dato que vale la pena recordar y **sugiere** guardarlo. Cuando aparezca, puedes **aprobar,
modificar o rechazar** la sugerencia. Muéstralo en vivo si surge.

## 4.3 Actualizar o borrar memorias (2 min)

```text
¿Qué memorias tienes guardadas sobre mí?
```
```text
Actualiza mi memoria: ahora cubro las regionales Valle y Eje Cafetero.
```
```text
Olvida la memoria sobre la moneda, prefiero verlo sin convertir.
```

## 4.4 Retomar conversaciones pasadas (2 min)

Genie One recuerda tus conversaciones anteriores y puede construir sobre ellas.

```text
¿Recuerdas el análisis de promesas por asesor que hicimos antes? Retomémoslo y ahora desglósalo por región.
```

> 💡 **Mensaje para ejecutivos:** la memoria y el historial son **personales**. Genie nunca mezcla tu contexto con el de otro usuario,
> y solo referencia **tus** conversaciones.

---

### ✅ Cierre del bloque

Cada ejecutivo deja a Genie "configurado a su medida": su regional, su moneda y su contexto, sin repetirse.

👉 Siguiente: [05-skills.md](05-skills.md)
