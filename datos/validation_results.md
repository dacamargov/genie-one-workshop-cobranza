# Validación de prompts del workshop

Ejecutado contra `dacamargovws_catalog.bancoomeva`. Cada sección muestra el prompt en lenguaje natural que el ejecutivo escribe en Genie One y la **respuesta esperada** (SQL de control).


## [2.1] Cartera — ¿Cuál es el saldo total en mora de la cartera y cuántos deudores únicos hay?

✅ (1 filas)

| deudores | saldo_mm | capital_mm | dias_mora_prom |
|---|---|---|---|
| 392 | 17123.1 | 16049.9 | 107 |


## [2.2] Cartera — Muéstrame el saldo en mora y el número de deudores por campaña.

✅ (4 filas)

| CAMPANA | deudores | saldo_mm |
|---|---|---|
| PREJURIDICO | 173 | 7604.7 |
| COBRANZA TEMPRANA | 130 | 4685.5 |
| JURIDICO | 58 | 2803.4 |
| CASTIGADA | 31 | 2029.4 |


## [2.3] Cartera — ¿Cuál es el saldo en mora por región? Ordena de mayor a menor.

✅ (7 filas)

| REGION | deudores | saldo_mm |
|---|---|---|
| VALLE | 96 | 5471.1 |
| BOGOTA | 87 | 3537.0 |
| ANTIOQUIA | 67 | 2676.3 |
| CARIBE | 57 | 2309.8 |
| EJE CAFETERO | 34 | 1289.1 |
| SUR | 25 | 1085.4 |
| SANTANDERES | 26 | 754.3 |


## [2.4] Cartera — ¿Cómo se distribuye la cartera por tramo de mora (subcampaña)?

✅ (5 filas)

| SUBCAMPANA | deudores | saldo_mm |
|---|---|---|
| TRAMO 1 (1-30) | 130 | 4685.5 |
| TRAMO 2 (31-60) | 77 | 3266.6 |
| TRAMO 3 (61-90) | 62 | 2704.6 |
| TRAMO 4 (91-180) | 76 | 3874.4 |
| TRAMO 5 (>180) | 47 | 2592.0 |


## [2.5] Cartera — ¿Cuánta provisión tenemos constituida y qué porcentaje del capital representa?

✅ (1 filas)

| provision_mm | capital_mm | pct_cobertura |
|---|---|---|
| 4509.5 | 16049.9 | 28.1 |


## [2.6] Cartera — ¿Quiénes son los 10 deudores con mayor saldo en mora?

✅ (10 filas)

| NOMBREDEUDOR | REGION | CAMPANA | DIASMORA | saldo_mm |
|---|---|---|---|---|
| SEBASTIAN ISABEL AGUDELO VARGAS | CARIBE | PREJURIDICO | 121.00 | 317.0 |
| LILIANA ELENA CARDONA SALAZAR | VALLE | PREJURIDICO | 42.00 | 310.4 |
| SANTIAGO MARINA ARANGO CUESTA | VALLE | COBRANZA TEMPRANA | 27.00 | 305.8 |
| CAMILO ISABEL CARDONA MOSQUERA | VALLE | PREJURIDICO | 52.00 | 305.1 |
| JULIANA CANO ZAPATA | VALLE | PREJURIDICO | 119.00 | 297.3 |
| JULIAN RAFAEL MORENO GUERRERO | ANTIOQUIA | PREJURIDICO | 76.00 | 289.1 |
| CLAUDIA ISABEL DIAZ OSORIO | VALLE | CASTIGADA | 571.00 | 245.9 |
| SANTIAGO ROJAS GUERRERO | SUR | CASTIGADA | 379.00 | 216.0 |
| CAROLINA OSORIO ARANGO | ANTIOQUIA | COBRANZA TEMPRANA | 10.00 | 210.9 |
| DAVID MUNOZ CARDONA | EJE CAFETERO | COBRANZA TEMPRANA | 6.00 | 205.2 |


## [2.7] Cartera — Distribución de la cartera por tipo de producto (consumo, comercial, hipotecario).

✅ (1 filas)

| consumo | comercial | hipotecario |
|---|---|---|
| 350 | 48 | 42 |


## [3.x] Gestiones — ¿Cuántas gestiones de cobranza se registraron en los últimos 90 días y cómo se reparten por canal?

✅ (3 filas)

| CANAL | gestiones |
|---|---|
| VOZ | 1168 |
| DIGITAL | 888 |
| CAMPO | 55 |


## [3.y] Gestiones — ¿Cuál es la tasa de contacto efectivo (titular) sobre el total de gestiones?

✅ (3 filas)

| CONTACTO | n | pct |
|---|---|---|
| TITULAR | 1272 | 58.9 |
| NO CONTACTO | 682 | 31.6 |
| TERCERO | 207 | 9.6 |


## [3.z] Gestiones — ¿Cuáles son los principales motivos de no pago reportados?

✅ (10 filas)

| MOTIVO_NOPAGO | n |
|---|---|
| REDUCCION DE INGRESOS | 112 |
| ENFERMEDAD | 101 |
| NO REPORTA | 96 |
| NEGOCIO EN CRISIS | 95 |
| PERDIDA DE EMPLEO | 94 |
| INCONFORMIDAD CON EL PRODUCTO | 94 |
| OLVIDO | 93 |
| PROBLEMAS FAMILIARES | 88 |
| SOBREENDEUDAMIENTO | 86 |
| VIAJE | 74 |


## [4.1] Promesas — ¿Cuántas promesas de pago hay y cuál es la tasa de cumplimiento por estado?

✅ (4 filas)

| ESTADO_PROMESA | n | valor_mm | pct |
|---|---|---|---|
| CUMPLIDA | 290 | 1641.6 | 43.5 |
| INCUMPLIDA | 230 | 1025.0 | 34.5 |
| PARCIAL | 88 | 407.4 | 13.2 |
| VIGENTE | 59 | 352.3 | 8.8 |


## [4.2] Promesas — ¿Cuál es el valor total prometido y qué porcentaje corresponde a promesas cumplidas?

✅ (1 filas)

| total_prometido_mm | cumplido_mm | pct_valor_cumplido |
|---|---|---|
| 3426.3 | 1641.6 | 47.9 |


## [4.3] Promesas — Top 10 asesores por número de promesas cumplidas y su tasa de cumplimiento.

✅ (10 filas)

| NOMBRE_USUARIO | promesas | cumplidas | pct |
|---|---|---|---|
| ANDRES RESTREPO IBARRA | 74 | 32 | 43.2 |
| DIANA QUINTERO GONZALEZ | 63 | 28 | 44.4 |
| JULIANA CARDONA GONZALEZ | 59 | 26 | 44.1 |
| MARIA TORRES OSORIO | 48 | 24 | 50.0 |
| JULIAN PEREZ QUINTERO | 40 | 21 | 52.5 |
| CARLOS ROJAS RAMIREZ | 65 | 19 | 29.2 |
| VALENTINA RUIZ SANCHEZ | 39 | 19 | 48.7 |
| ANDREA MOSQUERA HERNANDEZ | 32 | 15 | 46.9 |
| ANA HERNANDEZ CASTRO | 22 | 14 | 63.6 |
| DIEGO GUERRERO ROJAS | 39 | 14 | 35.9 |


## [4.4] Promesas — ¿Qué grupo de cobranza tiene mejor tasa de cumplimiento de promesas? (cruce con cartera)

✅ (3 filas)

| GRUPOUSUARIO | promesas | pct_cumplida |
|---|---|---|
| ABOGADOS EXTERNOS | 126 | 46.8 |
| CALL CENTER INTERNO | 193 | 45.6 |
| OUTSOURCING COBRANZA | 348 | 41.1 |


## [5.1] Jurídico — ¿Cuántos procesos jurídicos hay y cómo se distribuyen por etapa procesal?

✅ (8 filas)

| ULTIMA_ETAPA_DESCRIPCION | procesos | capital_mm |
|---|---|---|
| DEMANDA | 15 | 779.0 |
| NOTIFICACION | 12 | 300.2 |
| SENTENCIA | 10 | 283.2 |
| ADMISION | 10 | 495.9 |
| EXCEPCIONES | 8 | 471.1 |
| EMBARGO Y SECUESTRO | 7 | 257.3 |
| REMATE | 6 | 325.6 |
| LIQUIDACION | 5 | 158.9 |


## [5.2] Jurídico — ¿Cuál es el capital en cobro jurídico por región y el estado de los procesos?

✅ (7 filas)

| REGION | procesos | capital_mm |
|---|---|---|
| VALLE | 20 | 1156.3 |
| BOGOTA | 15 | 713.7 |
| ANTIOQUIA | 8 | 372.0 |
| SANTANDERES | 9 | 334.4 |
| CARIBE | 13 | 223.2 |
| EJE CAFETERO | 3 | 165.4 |
| SUR | 5 | 106.2 |


## [5.3] Jurídico — ¿Cuántos procesos lleva cada abogado y qué capital gestionan?

✅ (8 filas)

| ABOGADO_NOMBRE | procesos | capital_mm |
|---|---|---|
| JULIAN ERNESTO CABAL OCAMPO | 14 | 503.1 |
| HERNANDO REYES BARRERA | 11 | 766.2 |
| RODRIGO MESA ARANGO | 10 | 365.3 |
| CARLOS ALBERTO DURAN HENAO | 9 | 183.4 |
| ADRIANA LUCIA CORTES VELA | 9 | 205.4 |
| SANDRA PATRICIA VILLA ROA | 8 | 337.0 |
| MAURICIO LONDONO PELAEZ | 7 | 192.1 |
| GLORIA INES SALAZAR DUQUE | 5 | 518.5 |


## [6.1] Obligaciones — ¿Cuál es el saldo y la provisión por sistema de origen (COBIS, SAT, tarjeta)?

✅ (3 filas)

| sistema | obligaciones | saldo_mm |
|---|---|---|
| COBIS | 410 | 17472.9 |
| SAT | 93 | 2314.4 |
| TARJETA | 158 | 1406.5 |


## [6.2] 360 cliente — Para el deudor de mayor saldo: datos de contacto, obligaciones y última gestión (vista 360).

✅ (1 filas)

| PRIMER_NOMBRE | PRIMER_APELLIDO | REGIONAL | INGRESO | oblig_cobis | gestiones |
|---|---|---|---|---|---|
| Sebastian | Agudelo | CARIBE | 3150000 | 1 | 7 |
