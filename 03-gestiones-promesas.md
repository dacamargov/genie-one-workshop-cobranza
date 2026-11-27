# Bloque 3 — Gestiones, contactabilidad y promesas de pago (20 min)

🎯 **Meta:** medir la **operación** de cobranza: cuánto se gestiona, con qué efectividad y cuánto se recupera vía promesas.

📄 Doc: [Chat en Genie One](https://docs.databricks.com/aws/en/genie-one/chat).
Tablas: `tbl_vreportegestiones`, `tbl_vreportepromesas`.

---

## 3.1 Volumen de gestiones por canal (3 min)

```text
¿Cuántas gestiones de cobranza se registraron en los últimos 90 días y cómo se reparten por canal (voz, digital, campo)?
```

**Esperado:** VOZ ~1.168 · DIGITAL ~888 · CAMPO ~55.

## 3.2 Contactabilidad / contacto efectivo (3 min)

```text
¿Cuál es la tasa de contacto efectivo? Es decir, qué porcentaje de las gestiones logró contacto con el TITULAR
frente a tercero o sin contacto.
```

**Esperado:** TITULAR ~58,9% · NO CONTACTO ~31,6% · TERCERO ~9,6%.

## 3.3 Motivos de no pago (3 min)

```text
¿Cuáles son los principales motivos de no pago que reportan los deudores? Ordénalos de mayor a menor.
```

**Esperado:** encabezan REDUCCION DE INGRESOS, ENFERMEDAD, NEGOCIO EN CRISIS, PERDIDA DE EMPLEO.

## 3.4 Promesas de pago y cumplimiento (4 min)

```text
¿Cuántas promesas de pago hay y cuál es la tasa de cumplimiento por estado (cumplida, incumplida, parcial, vigente)?
Incluye el valor prometido en cada estado.
```

**Esperado:** CUMPLIDA ~43,5% · INCUMPLIDA ~34,5% · PARCIAL ~13,2% · VIGENTE ~8,8% (sobre ~667 promesas).

```text
Del total prometido, ¿qué porcentaje corresponde a promesas ya cumplidas?
```

**Esperado:** de ~3.426 MM COP prometidos, ~**47,9%** corresponde a promesas cumplidas.

## 3.5 Desempeño por asesor (4 min)

```text
Dame el top 10 de asesores por número de promesas cumplidas, con su tasa de cumplimiento. Solo asesores con 5 o más promesas.
```

**Esperado:** un ranking con tasas de cumplimiento entre ~29% y ~64%.

## 3.6 Desempeño por grupo de cobranza (3 min)

```text
¿Qué grupo de cobranza (call center interno, outsourcing, abogados externos) tiene mejor tasa de cumplimiento de promesas?
```

**Esperado:** ABOGADOS EXTERNOS (~46,8%) y CALL CENTER INTERNO (~45,6%) por encima de OUTSOURCING (~41,1%).

> 💡 Este cruce une **promesas** con **cartera** por la cédula. Es el tipo de pregunta que normalmente requiere un analista;
> aquí el ejecutivo la resuelve solo. Si Genie falla el cruce, recuérdale: *"cruza por la cédula convirtiendo ambos campos a número"*.

---

### ✅ Cierre del bloque

Ya se cubre el **ciclo operativo**: gestiones → contactabilidad → promesas → cumplimiento, con cortes por asesor y por grupo.

👉 Siguiente: [04-memoria-personalizacion.md](04-memoria-personalizacion.md)
