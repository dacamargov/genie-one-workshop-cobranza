#!/usr/bin/env python3
"""
Generador de datos SINTETICOS para el workshop de Genie One (cobranza - Bancoomeva).
Respeta exactamente las columnas/orden de schema.json (extraido del Excel).
Todas las tablas comparten la misma poblacion de clientes (coherencia referencial).
Solo libreria estandar. Uso: python3 generate.py [N_CLIENTES]
"""
import csv, json, os, random, sys, math
from datetime import date, datetime, timedelta

SEED = 42
N = int(sys.argv[1]) if len(sys.argv) > 1 else 500
random.seed(SEED)
HERE = os.path.dirname(os.path.abspath(__file__))
OUT = os.path.join(HERE, "data")
os.makedirs(OUT, exist_ok=True)
SCHEMA = {t["table"]: [c["name"] for c in t["columns"]] for t in json.load(open(os.path.join(HERE, "schema.json")))}

HOY = date(2026, 11, 25)
PROCESO = date(2026, 11, 24)
CORTE = date(2026, 10, 31)
CORTE_INT = 20261031

# ---------------------------------------------------------------- catalogos
NOMBRES_M = "Juan Carlos Andres Luis Jorge Camilo Santiago Felipe Diego Sebastian Mauricio Fernando Ricardo Alejandro Julian Oscar Hernan Miguel David Daniel".split()
NOMBRES_F = "Maria Ana Laura Paula Carolina Diana Andrea Natalia Claudia Sandra Luz Martha Liliana Juliana Camila Valentina Marcela Patricia Viviana Catalina".split()
SEG_NOMBRES = "Antonio Jose Alberto Eduardo Enrique Patricia Fernanda Lucia Marina Isabel Elena Rafael".split()
APELLIDOS = "Gomez Rodriguez Martinez Lopez Garcia Hernandez Gonzalez Perez Sanchez Ramirez Torres Diaz Vargas Castro Ruiz Ortiz Moreno Rojas Jimenez Munoz Salazar Cardona Restrepo Arango Quintero Mejia Cano Osorio Zapata Bedoya Henao Velez Agudelo Cuesta Mosquera Ospina Paz Guerrero Ibarra Pinzon".split()

REGIONALES = {
    "BOGOTA":       [("Bogota", "Cundinamarca"), ("Soacha", "Cundinamarca"), ("Chia", "Cundinamarca")],
    "ANTIOQUIA":    [("Medellin", "Antioquia"), ("Envigado", "Antioquia"), ("Bello", "Antioquia"), ("Rionegro", "Antioquia")],
    "VALLE":        [("Cali", "Valle del Cauca"), ("Palmira", "Valle del Cauca"), ("Tulua", "Valle del Cauca"), ("Buenaventura", "Valle del Cauca")],
    "CARIBE":       [("Barranquilla", "Atlantico"), ("Cartagena", "Bolivar"), ("Santa Marta", "Magdalena"), ("Monteria", "Cordoba")],
    "SANTANDERES":  [("Bucaramanga", "Santander"), ("Floridablanca", "Santander"), ("Cucuta", "Norte de Santander")],
    "EJE CAFETERO": [("Pereira", "Risaralda"), ("Manizales", "Caldas"), ("Armenia", "Quindio")],
    "SUR":          [("Pasto", "Narino"), ("Popayan", "Cauca"), ("Neiva", "Huila")],
}
REG_PESO = [("BOGOTA", 22), ("ANTIOQUIA", 18), ("VALLE", 22), ("CARIBE", 14), ("SANTANDERES", 9), ("EJE CAFETERO", 9), ("SUR", 6)]
CODIGO_REGIONAL = {r: 10 + i for i, r in enumerate(REGIONALES)}
ZONA_DE = {"BOGOTA": "CENTRO", "ANTIOQUIA": "NOROCCIDENTE", "VALLE": "SUROCCIDENTE", "CARIBE": "NORTE",
           "SANTANDERES": "NORORIENTE", "EJE CAFETERO": "OCCIDENTE", "SUR": "SUR"}
BARRIOS = ["El Poblado", "Chapinero", "Laureles", "San Fernando", "Prado", "Centro", "Cabecera", "Granada", "Usaquen", "Belen",
           "Ciudad Jardin", "Santa Barbara", "La Candelaria", "Bocagrande", "El Limonar"]
JUZGADOS_TIPO = ["Civil Municipal", "Civil del Circuito", "Pequenas Causas y Competencia Multiple"]

PRODUCTOS = {  # tabla -> lista (producto, linea)
    "cobis": [("CREDITO LIBRANZA", "LIB"), ("CREDITO CONSUMO", "CON"), ("CREDITO VEHICULO", "VEH"),
              ("CREDITO HIPOTECARIO", "HIP"), ("CREDITO COMERCIAL", "COM"), ("CREDITO EDUCATIVO", "EDU")],
    "sat": [("CREDITO SAT LIBRE INVERSION", "SAT1"), ("CREDITO SAT VEHICULO", "SAT2")],
    "sat_amparadas": [("CREDITO SAT AMPARADO", "SAA1")],
    "tarcred": [("TARJETA CREDITO CLASICA", "TC1"), ("TARJETA CREDITO GOLD", "TC2"), ("TARJETA CREDITO PLATINUM", "TC3")],
}
CLASIFICA_DE = {"LIB": "CONSUMO", "CON": "CONSUMO", "VEH": "CONSUMO", "HIP": "HIPOTECARIO", "COM": "COMERCIAL", "EDU": "CONSUMO",
                "SAT1": "CONSUMO", "SAT2": "CONSUMO", "SAA1": "CONSUMO", "TC1": "CONSUMO", "TC2": "CONSUMO", "TC3": "CONSUMO"}
DESTINOS = [("101", "LIBRE INVERSION"), ("102", "COMPRA DE VEHICULO"), ("103", "VIVIENDA"), ("104", "CAPITAL DE TRABAJO"),
            ("105", "EDUCACION"), ("106", "COMPRA DE CARTERA"), ("107", "REMODELACION")]
ORIGINADORES = [("BANCOOMEVA", "900406150"), ("COOMEVA", "890300625"), ("FIDUCIARIA COOMEVA", "805012921")]

ABOGADOS = [("1017201001", "Mauricio Londono Pelaez"), ("43870211", "Gloria Ines Salazar Duque"), ("79451030", "Hernando Reyes Barrera"),
            ("66812344", "Adriana Lucia Cortes Vela"), ("98765210", "Rodrigo Mesa Arango"), ("52100333", "Sandra Patricia Villa Roa"),
            ("1130622100", "Julian Ernesto Cabal Ocampo"), ("71650900", "Carlos Alberto Duran Henao")]
SUPERVISORES_ABOG = [("32456780", "Beatriz Elena Mazo Ruiz"), ("70123456", "Gustavo Adolfo Pineda Lara")]
GRUPOS = ["CALL CENTER INTERNO", "OUTSOURCING COBRANZA", "ABOGADOS EXTERNOS"]
USUARIOS = []  # (login, nombre, grupo)
_n = 0
for g, k in zip(GRUPOS, [8, 6, 4]):
    for i in range(k):
        _n += 1
        nm = f"{random.choice(NOMBRES_F + NOMBRES_M)} {random.choice(APELLIDOS)} {random.choice(APELLIDOS)}"
        USUARIOS.append((f"cob{_n:03d}", nm, g))
USU_INTERNOS = [u for u in USUARIOS if u[2] != "ABOGADOS EXTERNOS"]
USU_JUR = [u for u in USUARIOS if u[2] == "ABOGADOS EXTERNOS"]


# ---------------------------------------------------------------- helpers
def wch(pairs):
    items, weights = zip(*pairs)
    return random.choices(items, weights)[0]


def money(lo, hi, step=1000):
    return int(random.uniform(lo, hi) // step * step)


def rdate(d0, d1):
    return d0 + timedelta(days=random.randint(0, (d1 - d0).days))


def phone_cel():
    return "3" + random.choice("012") + "".join(random.choices("0123456789", k=8))


def phone_fijo():
    return random.choice(["601", "604", "602", "605", "607", "606"]) + "".join(random.choices("0123456789", k=7))


def fmt(v):
    if v is None:
        return ""
    if isinstance(v, datetime):
        return v.strftime("%Y-%m-%d %H:%M:%S")
    if isinstance(v, date):
        return v.isoformat()
    if isinstance(v, float):
        return f"{v:.4f}".rstrip("0").rstrip(".") if v != int(v) else str(int(v))
    return str(v)


TABLES = {k: [] for k in SCHEMA}


def add(table, **kw):
    cols = SCHEMA[table]
    bad = set(kw) - set(cols)
    assert not bad, f"{table}: columnas inexistentes {bad}"
    TABLES[table].append([fmt(kw.get(c)) for c in cols])


def add_common(table, d):
    add(table, **{k: v for k, v in d.items() if k in SCHEMA[table]})


def tramo(d):
    if d <= 30: return "TRAMO 1 (1-30)"
    if d <= 60: return "TRAMO 2 (31-60)"
    if d <= 90: return "TRAMO 3 (61-90)"
    if d <= 180: return "TRAMO 4 (91-180)"
    return "TRAMO 5 (>180)"


def prov_pct(d):
    return 0.01 if d == 0 else 0.03 if d <= 30 else 0.10 if d <= 60 else 0.25 if d <= 90 else 0.5 if d <= 180 else 1.0


def calif(d):
    return "A" if d == 0 else "B" if d <= 30 else "C" if d <= 90 else "D" if d <= 180 else "E"


# ---------------------------------------------------------------- poblacion
people = []
used = set()
for i in range(N):
    doc = random.randint(10_000_000, 1_199_999_999)
    while doc in used:
        doc = random.randint(10_000_000, 1_199_999_999)
    used.add(doc)
    sexo = random.choice(["M", "F"])
    pn = random.choice(NOMBRES_M if sexo == "M" else NOMBRES_F)
    sn = random.choice(SEG_NOMBRES) if random.random() < 0.4 else None
    a1, a2 = random.choice(APELLIDOS), random.choice(APELLIDOS)
    reg = wch(REG_PESO)
    ciudad, depto = random.choice(REGIONALES[reg])
    nac = rdate(date(1955, 1, 1), date(2002, 12, 31))
    # distribucion de mora: ~22% al dia, resto en tramos
    r = random.random()
    if r < 0.22: dm = 0
    elif r < 0.45: dm = random.randint(1, 30)
    elif r < 0.62: dm = random.randint(31, 60)
    elif r < 0.75: dm = random.randint(61, 90)
    elif r < 0.90: dm = random.randint(91, 180)
    else: dm = random.randint(181, 720)
    people.append(dict(doc=str(doc), tipo="CC" if random.random() < 0.94 else "CE", pn=pn, sn=sn, a1=a1, a2=a2, sexo=sexo,
                       nombre=" ".join(x for x in [pn, sn, a1, a2] if x), nac=nac, reg=reg, ciudad=ciudad, depto=depto,
                       mora=dm, ingreso=money(1_800_000, 14_000_000, 50_000), sucursal=f"OFICINA {ciudad.upper()}"
                       ))

# ---------------------------------------------------------------- CLIENTE / DIRECCION / CORREO / TELEFONO / REFERENCIAS
PROFESIONES = ["INGENIERO", "ABOGADO", "CONTADOR", "MEDICO", "DOCENTE", "ADMINISTRADOR", "COMERCIANTE", "ENFERMERO", "TECNICO", "INDEPENDIENTE"]
ACT_ECO = ["EDUCACION", "SALUD", "COMERCIO", "SERVICIOS FINANCIEROS", "CONSTRUCCION", "MANUFACTURA", "TRANSPORTE", "SECTOR PUBLICO", "TECNOLOGIA"]
EMPRESAS = ["COOMEVA EPS", "ALCALDIA MUNICIPAL", "CLINICA DEL OCCIDENTE", "SERVICIOS INTEGRALES SAS", "COLEGIO LA SALLE", "TRANSPORTES DEL VALLE",
            "CONSTRUCTORA ANDINA", "COMERCIALIZADORA NORTE", "UNIVERSIDAD REGIONAL", "INDEPENDIENTE"]
ESTADOS_CIVIL = ["SOLTERO", "CASADO", "UNION LIBRE", "SEPARADO", "VIUDO"]

for p in people:
    ing_bco = rdate(date(2008, 1, 1), date(2025, 12, 31))
    estado_cli = ("ACTIVO", "A")
    if p["mora"] > 360: estado_cli = ("CASTIGADO", "C")
    add("cliente", DOCUMENTO=p["doc"], CODIGO_TIPO_DOCUMENTO="1" if p["tipo"] == "CC" else "2",
        TIPO_DE_DOCUMENTO="CEDULA DE CIUDADANIA" if p["tipo"] == "CC" else "CEDULA DE EXTRANJERIA",
        PRIMER_NOMBRE=p["pn"], SEGUNDO_NOMBRE=p["sn"], PRIMER_APELLIDO=p["a1"], SEGUNDO_APELLIDO=p["a2"],
        FECHA_NACIMIENTO=p["nac"], SEXO=p["sexo"], ESTADO_CIVIL=random.choice(ESTADOS_CIVIL), PERSONAS_A_CARGO=random.randint(0, 4),
        PROFESION=random.choice(PROFESIONES), ACTIVIDAD_ECONOMICA=random.choice(ACT_ECO),
        TIPO_DE_INGRESO=random.choice(["SALARIO", "SALARIO", "HONORARIOS", "NEGOCIO PROPIO", "PENSION"]), INGRESO=p["ingreso"],
        EMPRESA=random.choice(EMPRESAS), PUESTO=random.choice(["ANALISTA", "AUXILIAR", "DIRECTOR", "PROFESIONAL", "OPERARIO", "GERENTE"]),
        FECHA_INGRESO=rdate(date(2005, 1, 1), date(2025, 6, 30)),
        CALIFICACION_CONSUMO=calif(p["mora"]), CALIFICACION_HIPOTECARIO="A" if p["mora"] < 30 else calif(p["mora"]),
        CALIFICACION_COMERCIAL="A" if p["mora"] < 60 else calif(p["mora"]), FECHA_DE_PROCESO=PROCESO,
        FECHA_CASTIGO=rdate(date(2025, 1, 1), date(2026, 9, 30)) if estado_cli[1] == "C" else None,
        CODIGO_REGIONAL=CODIGO_REGIONAL[p["reg"]], REGIONAL=p["reg"], FECHA_INGRESO_BCO=ing_bco,
        CODIGO_ESTADO=estado_cli[1], ESTADO=estado_cli[0], TIPO_CLIENTE=random.choice(["ASOCIADO", "ASOCIADO", "NO ASOCIADO"]),
        CODIGO_OFICINA_VINCULACION=f"{CODIGO_REGIONAL[p['reg']]}{random.randint(1, 9):02d}", OFICINA_VINCULACION=p["sucursal"],
        CORTE_CLIENTE=CORTE_INT)
    p["cod_tipo"] = "1" if p["tipo"] == "CC" else "2"
    # direcciones
    def dir_():
        return f"{random.choice(['CALLE', 'CARRERA', 'AVENIDA', 'DIAGONAL'])} {random.randint(1, 120)} # {random.randint(1, 99)}-{random.randint(1, 99)}"
    p["dir_res"], p["dir_com"] = dir_(), dir_()
    for tipo_d, d in [("RESIDENCIA", p["dir_res"]), ("COMERCIAL", p["dir_com"])] + ([("CORRESPONDENCIA", dir_())] if random.random() < 0.3 else []):
        add("direccion", DOCUMENTO=p["doc"], CODIGO_TIPO_DOCUMENTO=p["cod_tipo"], DIRECCION=d, TIPO_DE_DIRECCION=tipo_d, PAIS="COLOMBIA",
            DEPARTAMENTO=p["depto"].upper(), CIUDAD=p["ciudad"].upper(), APARTADO_AEREO=None, BARRIO=random.choice(BARRIOS).upper(),
            OBSERVACION=None, FECHA_DE_PROCESO=PROCESO)
    p["email"] = f"{p['pn'].lower()}.{p['a1'].lower()}{random.randint(1, 999)}@correo-ejemplo.com"
    add("correo", DOCUMENTO=p["doc"], CODIGO_TIPO_DOCUMENTO=p["cod_tipo"], EMAIL=p["email"], TIPO_DE_DIRECCION="PERSONAL",
        OBSERVACION=None, FECHA_DE_PROCESO=PROCESO)
    if random.random() < 0.35:
        add("correo", DOCUMENTO=p["doc"], CODIGO_TIPO_DOCUMENTO=p["cod_tipo"], EMAIL=f"{p['pn'].lower()}.{p['a1'].lower()}@empresa-ejemplo.com",
            TIPO_DE_DIRECCION="LABORAL", OBSERVACION=None, FECHA_DE_PROCESO=PROCESO)
    # telefonos
    p["cel"] = phone_cel()
    p["tel_res"], p["tel_fam"], p["tel_com"] = phone_fijo(), phone_cel(), phone_fijo()
    tels = [(p["cel"], "CELULAR", "PERSONAL"), (p["tel_res"], "FIJO", "RESIDENCIA"), (p["tel_com"], "FIJO", "TRABAJO")]
    if random.random() < 0.5: tels.append((p["tel_fam"], "CELULAR", "FAMILIAR"))
    for t, tp, cat in tels:
        add("tbl_telefono_wsac", DOCUMENTO=p["doc"], CODIGO_TIPO_DOCUMENTO=p["cod_tipo"], TIPO_DOCUMENTO="CEDULA DE CIUDADANIA" if p["tipo"] == "CC" else "CEDULA DE EXTRANJERIA",
            TELEFONO=t, TIPO=tp, CATEGORIA=cat, EXTENSION=None, INDICATIVO="57" if tp == "CELULAR" else "60" + t[2:3], CIUDAD=p["ciudad"].upper(), FECHA_DE_PROCESO=PROCESO)
    # referencias personales
    for k in range(random.randint(1, 3)):
        add("referencia_cliente", DOCUMENTO_UNICO_DE_IDENTIDAD=p["doc"], TIPO_DE_IDENTIFICACION=p["cod_tipo"],
            NOMBRE=f"{random.choice(NOMBRES_F + NOMBRES_M)} {random.choice(APELLIDOS)} {random.choice(APELLIDOS)}", DIRECCION=dir_(),
            TELEFONO=random.choice([phone_cel(), phone_fijo()]), TIPO_REFERENCIA=random.choice(["PERSONAL", "FAMILIAR", "COMERCIAL"]),
            CIUDAD=p["ciudad"].upper())
    # cuentas pasivo (ahorros / corriente / cdt)
    for k in range(random.choice([0, 1, 1, 2])):
        prod = random.choice(["CUENTA DE AHORROS", "CUENTA DE AHORROS", "CUENTA CORRIENTE", "CDT", "AHORRO PROGRAMADO"])
        add("cuentas_pasivo", FECHA_ACTUALIZACION=PROCESO, ENTIDAD="BANCOOMEVA", PRODUCTO=prod, NUMERO=str(random.randint(10**9, 10**10 - 1)),
            CUENTA=str(random.randint(10**9, 10**10 - 1)), SALDO=money(0, 25_000_000, 10_000), ESTADO=random.choice(["ACTIVA", "ACTIVA", "INACTIVA", "EMBARGADA"]),
            NUMERO_UNICO_IDENTIDAD=p["doc"], TIPO_DOCUMENTO=p["cod_tipo"], DEBITO_AUTOMATICO=random.choice([0, 1]))

# ---------------------------------------------------------------- OBLIGACIONES
oblig = []  # lista de dicts base
for p in people:
    n_ob = random.choices([1, 2, 3], [60, 30, 10])[0]
    for _ in range(n_ob):
        fam = wch([("cobis", 55), ("tarcred", 25), ("sat", 12), ("sat_amparadas", 8)])
        prod, linea = random.choice(PRODUCTOS[fam])
        clas = CLASIFICA_DE[linea]
        # la mora de la obligacion es la del cliente (la peor) o menor
        dm = p["mora"] if (not oblig or oblig[-1]["p"] is not p) else random.choice([0, p["mora"], max(0, p["mora"] - random.randint(0, 40))])
        if fam == "tarcred": monto = money(1_500_000, 25_000_000, 100_000)
        elif linea == "HIP": monto = money(80_000_000, 450_000_000, 1_000_000)
        elif linea == "VEH" or linea == "SAT2": monto = money(25_000_000, 110_000_000, 500_000)
        elif linea == "COM": monto = money(30_000_000, 250_000_000, 1_000_000)
        else: monto = money(3_000_000, 60_000_000, 100_000)
        plazo = 360 if linea == "HIP" else random.choice([36, 48, 60, 72, 84]) if fam != "tarcred" else 36
        pagadas = random.randint(2, plazo - 2)
        capital_total = int(monto * (1 - pagadas / plazo) * random.uniform(0.9, 1.0)) if fam != "tarcred" else int(monto * random.uniform(0.2, 0.95))
        cuotas_ven = math.ceil(dm / 30) if dm > 0 else 0
        cuota = int(max(60_000, (monto / plazo) * 1.35)) if fam != "tarcred" else int(max(50_000, capital_total * 0.05))
        cap_venc = min(capital_total, int(cuota * 0.7 * cuotas_ven)) if dm > 0 else 0
        int_venc = int(cuota * 0.3 * cuotas_ven) if dm > 0 else 0
        int_mor = int(cap_venc * 0.28 / 365 * dm) if dm > 0 else 0
        cargos = int(random.choice([0, 12_000, 25_000, 48_000])) if dm > 0 else 0
        saldo = capital_total + int_venc + int_mor + cargos
        mora_v = cap_venc + int_venc + int_mor
        dest = random.choice(DESTINOS)
        orig = random.choices(ORIGINADORES, [80, 15, 5])[0]
        tasa = round(random.uniform(14, 31), 2)
        apertura = rdate(date(2019, 1, 1), date(2026, 2, 28))
        oblig.append(dict(p=p, fam=fam, producto=prod, linea=linea, clas=clas, dm=dm, monto=monto, plazo=plazo, pagadas=pagadas,
                          capital=capital_total, cuotas_ven=cuotas_ven, cuota=cuota, cap_venc=cap_venc, int_venc=int_venc, int_mor=int_mor,
                          cargos=cargos, saldo=saldo, mora_v=mora_v, dest=dest, orig=orig, tasa=tasa, apertura=apertura,
                          vence=apertura + timedelta(days=int(plazo * 30.4)), prox=date(2026, 12, random.randint(1, 28)),
                          prov=int(capital_total * prov_pct(dm)), num=str(random.randint(10**9, 10**10 - 1)),
                          vendedor=str(random.randint(10**6, 10**7 - 1)), suc=random.choice(list(range(100, 140)))))
for o in oblig:
    p = o["p"]
    f = o["fam"]
    estado = "CASTIGADA" if o["dm"] > 360 else ("VIGENTE" if o["dm"] == 0 else "EN MORA")
    common = dict(NIT=p["doc"], ENTIDAD="BANCOOMEVA", NUMERO_DE_OBLIGACION=o["num"], PRODUCTO=o["producto"], CLASIFICA=o["clas"],
                  MONEDA="COP", DIAS_DE_MORA=o["dm"], TOTAL_A_PAGAR=o["mora_v"] + o["cuota"] if o["dm"] else o["cuota"],
                  MONTO_DESEMBOLSADO=o["monto"], ESTADO=estado, FECHA_DE_APERTURA=o["apertura"], FECHA_DE_VENCIMIENTO=o["vence"],
                  FECHA_DE_PROXIMO_PAGO=o["prox"], IDENTIFICACION_DEL_VENDEDOR=o["vendedor"], SALDO=o["saldo"], MORA=o["mora_v"],
                  CAPITAL_TOTAL=o["capital"], CAPITAL_VENCIDO=o["cap_venc"], INTERESES_VENCIDOS=o["int_venc"], INTERESES_MORATORIOS=o["int_mor"],
                  CARGOS_O_COMISIONES=o["cargos"], FECHA_DE_ACTUALIZACION=PROCESO, FINANCIACION_CAUSADA=int(o["capital"] * 0.01),
                  FINANCIACION_NO_CAUSADA=int(o["capital"] * 0.004), PROVISION=o["prov"], PROYECCION_PROVISION=int(o["capital"] * prov_pct(min(720, o["dm"] + 30))),
                  CUENTAS_POR_COBRAR=o["int_venc"] + o["int_mor"], MORA_AL_CORTE=o["mora_v"], MORA_AL_DIA=o["mora_v"],
                  DESTINO_ECONOMICO=o["dest"][1], CAPITAL_X_VENCER=o["capital"] - o["cap_venc"], CUOTAS_PACTADAS=o["plazo"],
                  CUOTAS_VENCIDAS=o["cuotas_ven"], CUOTAS_PAGADAS=o["pagadas"], TIPO_DOCUMENTO=p["cod_tipo"], CORTE=CORTE_INT,
                  ESTADO_OBL=estado, SRC_OBLIGA=f.upper(), SLDO_PRVK=o["prov"], SLDO_PRVI=int((o["int_venc"] + o["int_mor"]) * prov_pct(o["dm"])),
                  COD_DESTINOECONOMICO=o["dest"][0], INDICADOR_ORIGINADOR="S" if o["orig"][0] != "BANCOOMEVA" else "N",
                  NOMBRE_ORIGINADOR=o["orig"][0], NIT_ORIGINADOR=o["orig"][1], SISTEMA_PRODUCTO=1 if f == "cobis" else 2 if f == "sat" else 3 if f == "sat_amparadas" else 4,
                  CUOTA=o["cuota"], TASA_NOMINAL=o["tasa"], TASA_PROMEDIO_PONDERADA=o["tasa"] - 1.1, TASAAPLIP=o["tasa"] + 1.2,
                  LINEA_DE_CREDITO=o["linea"], SUCURSAL=o["suc"])
    if f == "cobis":
        d = {k: v for k, v in common.items()}
        d.update(NUM_CRED_ANT=None, CIUDAD_GARANTIA=p["ciudad"].upper() if o["linea"] in ("HIP", "VEH") else None,
                 CODIGO_ADMINISTRADOR=str(random.randint(100, 999)), CODIGO_PORTAFOLIO=random.choice(["P01", "P02", "P03"]), SEG_TITUL=random.choice([0, 1]),
                 SUCURSAL=p["sucursal"])
        d["LINEA_DE_CREDITO"] = o["linea"]
        add_common("obligaciones_cobis", d)
        o["garantia"] = o["linea"] in ("HIP", "VEH")
    elif f == "sat":
        common["SUCURSAL"] = o["suc"]
        common["LINEA_DE_CREDITO"] = random.randint(1, 9)
        add_common("obligaciones_sat", common)
    elif f == "sat_amparadas":
        common["SUCURSAL"] = p["sucursal"]
        add_common("obligaciones_sat_amparadas", dict(common, NIT_LLAVE=p["doc"] + "0", NIT_AMPARADOR=random.choice(["890300625", "900406150"]), P01NROCUOR=o["plazo"]))
    else:
        common["SUCURSAL"] = p["sucursal"]
        add_common("obligaciones_tarcred", common)
    # pagos de la obligacion (ultimos 6 meses; menos frecuentes si esta en mora)
    n_pagos = random.randint(3, 6) if o["dm"] < 30 else random.randint(0, 3)
    for k in range(n_pagos):
        fr = PROCESO - timedelta(days=30 * k + random.randint(0, 12))
        add("pagos_prestamos", FECHA_ACTUALIZACION=PROCESO, DOCUMENTO_UNICO_IDENTIDAD=p["doc"], TIPO_DOCUMENTO=p["cod_tipo"],
            SECUENCIA=str(random.randint(1, 99999)), FECHA_RECEPCION=fr, VALOR_PAGO=int(o["cuota"] * random.choice([1, 1, 1, 0.5, 2])))
    # garantias
    if f == "cobis" and o["linea"] in ("HIP", "VEH") or (f == "sat" and o["linea"] == "SAT2"):
        hip = o["linea"] == "HIP"
        val = int(o["monto"] * random.uniform(1.15, 1.6))
        add("garantias", DOCUMENTO_UNICO_DE_IDENTIDAD=p["doc"], NUMERO_UNICO_OBLIGACION=p["doc"] + o["num"][-4:], NUMERO_DE_OBLIGACION=o["num"],
            NUMERO_DE_GARANTIA=str(random.randint(10**7, 10**8 - 1)), ENTIDAD="BANCOOMEVA", LIN_NUM=str(random.randint(1, 5)), PRODUCTO=o["producto"],
            TIPO_DE_IDENTIFICACION=p["cod_tipo"], TIPO_DE_GARANTIA="HIPOTECA" if hip else "PRENDA",
            DESCRIPCION=("APARTAMENTO " if hip else "VEHICULO ") + (f"{random.randint(1, 20)}0{random.randint(1, 9)} {p['ciudad'].upper()}" if hip else random.choice(["MAZDA 3 2022", "CHEVROLET ONIX 2023", "RENAULT DUSTER 2021", "KIA SPORTAGE 2022"])),
            MONEDA="COP", FECHA_AVALUO=rdate(date(2023, 1, 1), date(2026, 6, 30)), FECHA_ACTUALIZACION=PROCESO, ESTADO="VIGENTE",
            FECHA_DE_VENCIMIENTO=o["vence"], VALOR=val, VALOR_ACTUAL=int(val * random.uniform(0.85, 1.05)), VALOR_C=val, VALOR_ACTUAL_C=int(val * random.uniform(0.85, 1.05)))
    # codeudores
    if random.random() < 0.28:
        cdoc = str(random.randint(10_000_000, 1_199_999_999))
        add("referencia_codeudores", DOCUMENTO_UNICO_DE_IDENTIDAD=p["doc"], NUMERO_DE_OBLIGACION=o["num"], PRODUCTO=o["producto"],
            NOMBRE=f"{random.choice(NOMBRES_F + NOMBRES_M)} {random.choice(APELLIDOS)} {random.choice(APELLIDOS)}", DIRECCION=f"CALLE {random.randint(1, 100)} # {random.randint(1, 80)}-{random.randint(1, 50)}",
            TIPO_DE_DIRECCION="RESIDENCIA", TELEFONO_DOMICILIO=phone_fijo(), TELEFONO_TRABAJO=phone_fijo(), TELEFONO_ADICIONAL=phone_cel(),
            RELACION=random.choice(["CONYUGE", "HIJO", "HERMANO", "AMIGO", "SOCIO"]), FECHA_DE_PROCESO=PROCESO, TIPO_DOCUMENTO="1",
            DOCUMENTO_CODEUDOR=cdoc, TIPO_DOCUMENTO_CODEUDOR="1")

# ---------------------------------------------------------------- CARTERA (edad de cartera) - un registro por deudor con mora
FRANJAS = ["06:00-08:00", "08:00-10:00", "10:00-12:00", "12:00-14:00", "14:00-16:00", "16:00-18:00", "18:00-20:00"]
by_person = {}
for o in oblig:
    by_person.setdefault(o["p"]["doc"], []).append(o)
deudores = []
for p in people:
    obs = by_person[p["doc"]]
    dm = max(o["dm"] for o in obs)
    if dm == 0:
        continue
    cap = sum(o["capital"] for o in obs)
    saldo = sum(o["saldo"] for o in obs)
    mora_v = sum(o["mora_v"] for o in obs)
    prov = sum(o["prov"] for o in obs)
    cv = max(o["cuotas_ven"] for o in obs)
    cuota = sum(o["cuota"] for o in obs)
    if dm <= 30: camp = "COBRANZA TEMPRANA"
    elif dm <= 90: camp = "PREJURIDICO"
    elif dm <= 360: camp = "JURIDICO" if random.random() < 0.65 else "PREJURIDICO"
    else: camp = "CASTIGADA"
    juridico = camp in ("JURIDICO",) or (camp == "CASTIGADA" and random.random() < 0.5)
    if juridico:
        usr = random.choice(USU_JUR); abog = random.choice(ABOGADOS); sup = random.choice(SUPERVISORES_ABOG)
    else:
        usr = random.choice(USU_INTERNOS if random.random() < 0.65 else [u for u in USU_INTERNOS if u[2] == "OUTSOURCING COBRANZA"])
        abog = sup = None
    p.update(camp=camp, subcamp=tramo(dm), dm=dm, capital=cap, saldo=saldo, mora_v=mora_v, prov=prov, cv=cv, usr=usr, abog=abog, sup=sup,
             juridico=juridico, cuota=cuota, franja=random.choice(FRANJAS),
             estado_cart="CASTIGADO" if dm > 360 else ("EN COBRO JURIDICO" if juridico else "ACTIVO"),
             estrategia=random.choice(["LLAMADA + WHATSAPP", "SMS MASIVO", "VISITA DOMICILIARIA", "ACUERDO DE PAGO", "REESTRUCTURACION", "COBRO JURIDICO"]) if not juridico else "COBRO JURIDICO")
    deudores.append(p)
    clas = {o["clas"] for o in obs}
    add("tbl_vreporteedadcartera", FECHAACTUALIZACION=datetime(2026, 11, 24, 6, 0, 0), IDENTIFICACION=p["doc"], NOMBREDEUDOR=p["nombre"].upper(),
        REGION=p["reg"], CIUDAD=p["ciudad"].upper(), SUCURSAL=p["sucursal"], ESTADO=p["estado_cart"],
        ESTADOCLIENTE="CASTIGADO" if dm > 360 else "MOROSO", CAMPANA=camp, SUBCAMPANA=p["subcamp"], GRUPOUSUARIO=usr[2],
        NOMBREUSUARIO=usr[1].upper(), ABOGADO=abog[0] if abog else None, NOMBREABOGADO=abog[1].upper() if abog else None,
        DIACORTE="31", SALDO=saldo, CAPITAL=cap, MORA=mora_v, PROVISION=prov, CUOTASVEN=cv, DIASMORA=dm,
        TELEFONORES=p["tel_res"], TELEFONOFAM=p["tel_fam"], TELEFONOCOM=p["tel_com"], TELEFONOCEL=p["cel"],
        DIRECCIONRES=p["dir_res"], DIRECCIONRESCIUDAD=p["ciudad"].upper(), DIRECCIONCOM=p["dir_com"], DIRECCIONCOMCIUDAD=p["ciudad"].upper(),
        DIRECCIONCORRESPONDENCIA=p["dir_res"], DIRECCIONCORRESPONDENCIACIUDAD=p["ciudad"].upper(), EMAIL=p["email"], ESTRATEGIA=p["estrategia"],
        CONSUMO="SI" if "CONSUMO" in clas else "NO", COMERCIAL="SI" if "COMERCIAL" in clas else "NO", HIPOTECARIO="SI" if "HIPOTECARIO" in clas else "NO",
        ABOGADO_SUPERVISOR=sup[0] if sup else None, NOMBRE_ABOGADO_SUPERVISOR=sup[1].upper() if sup else None, CUOTA=cuota,
        FRANJAMAYORCONTACTO=p["franja"], TELEFONOMAYORCONTACTO=p["cel"])

# ---------------------------------------------------------------- GESTIONES + PROMESAS
ACCIONES = [("LLAMADA SALIENTE", 50), ("WHATSAPP", 22), ("SMS", 12), ("EMAIL", 8), ("LLAMADA ENTRANTE", 5), ("VISITA", 3)]
RESP_CONTACTO = [("PROMESA DE PAGO", 24), ("COMPROMISO DE PAGO PARCIAL", 6), ("SOLICITA REESTRUCTURACION", 6), ("YA PAGO", 7), ("SE NIEGA A PAGAR", 6),
                 ("SOLICITA INFORMACION", 8), ("CONTACTO TERCERO", 10), ("NO CONTESTA", 20), ("NUMERO ERRADO", 4), ("BUZON DE VOZ", 9)]
MOTIVOS = ["PERDIDA DE EMPLEO", "REDUCCION DE INGRESOS", "ENFERMEDAD", "OLVIDO", "SOBREENDEUDAMIENTO", "PROBLEMAS FAMILIARES",
           "INCONFORMIDAD CON EL PRODUCTO", "VIAJE", "NEGOCIO EN CRISIS", "NO REPORTA"]
OBS = ["Cliente indica que paga en la proxima quincena", "Se envia estado de cuenta por correo", "Cliente solicita llamar en la tarde",
       "Se informa valor en mora y fecha limite de pago", "Cliente manifiesta dificultad economica transitoria", "Tercero informa que el titular esta de viaje",
       "Se ofrece alternativa de reestructuracion", "Cliente reconoce la deuda y pide link de pago", "Sin contacto efectivo, se programa nuevo intento"]
promesas_n = 0
for p in deudores:
    ng = random.randint(2, 9) if p["dm"] > 0 else 0
    for k in range(ng):
        fg = datetime.combine(PROCESO - timedelta(days=random.randint(0, 89)), datetime.min.time()) + timedelta(hours=random.randint(8, 19), minutes=random.randint(0, 59))
        accion = wch(ACCIONES)
        resp = wch(RESP_CONTACTO)
        contacto = "NO CONTACTO" if resp in ("NO CONTESTA", "NUMERO ERRADO", "BUZON DE VOZ") else ("TERCERO" if resp == "CONTACTO TERCERO" else "TITULAR")
        usr = p["usr"]
        add("tbl_vreportegestiones", ID_DEUDOR=p["doc"], FECHA_GESTION=fg, USUARIO=usr[0], ACCION=accion, RESPUESTA=resp, CONTACTO=contacto,
            TELEFONO=p["cel"] if random.random() < 0.7 else p["tel_fam"] if p["tel_fam"].startswith("3") else p["cel"], OBSERVACION_INT=random.choice(OBS),
            MOTIVO_NOPAGO=random.choice(MOTIVOS) if resp in ("SE NIEGA A PAGAR", "SOLICITA REESTRUCTURACION", "COMPROMISO DE PAGO PARCIAL", "PROMESA DE PAGO") else None,
            SUB_CAMPANA=p["subcamp"], CANAL="VOZ" if "LLAMADA" in accion else "DIGITAL" if accion in ("WHATSAPP", "SMS", "EMAIL") else "CAMPO",
            FECHA_INSER=fg.date(), FECHA_PROCESO=fg.date(), FECHA_CIERRE=fg.date() + timedelta(days=random.randint(0, 5)),
            USUARIO_CREA=usr[0], USUARIO_ACTUAL=usr[0])
        if resp in ("PROMESA DE PAGO", "COMPROMISO DE PAGO PARCIAL"):
            fp = fg + timedelta(days=random.randint(2, 15))
            if fp.date() > PROCESO: est = "VIGENTE"
            else: est = wch([("CUMPLIDA", 48), ("INCUMPLIDA", 37), ("PARCIAL", 15)])
            valor = int(p["mora_v"] * (random.uniform(0.3, 0.7) if resp.startswith("COMPROMISO") else random.uniform(0.8, 1.0)) // 1000 * 1000)
            promesas_n += 1
            add("tbl_vreportepromesas", USUARIO=usr[0], NOMBRE_USUARIO=usr[1].upper(), ZONA=ZONA_DE[p["reg"]], REGIONAL=p["reg"], CAMPANA=p["camp"],
                SUB_CAMPANA=p["subcamp"], CEDULA=p["doc"], NOMBRE_CLIENTE=p["nombre"].upper(), SUB_CAMPANA_1=p["subcamp"], VALOR_PROMESA=max(valor, 50000),
                FECHA_PROMESA=fp.replace(hour=0, minute=0, second=0), ESTADO_PROMESA=est, FECHA_GESTION=fg, CUOTAS_VEN=p["cv"], CORTE=CORTE_INT,
                USUARIO_GESTION=usr[0], ACCION=accion, RESPUESTA=resp, FECHA_INSER=fg, FECHA_PROCESO=datetime.combine(PROCESO, datetime.min.time()),
                FECHA_CIERRE=fp, USUARIO_CREA=usr[0], USUARIO_ACTUAL=usr[0])

# ---------------------------------------------------------------- PROCESOS JURIDICOS
ETAPAS = [("01", "DEMANDA", "RADICACION DE DEMANDA"), ("02", "ADMISION", "AUTO ADMISORIO"), ("03", "NOTIFICACION", "NOTIFICACION AL DEMANDADO"),
          ("04", "EXCEPCIONES", "TRASLADO DE EXCEPCIONES"), ("05", "SENTENCIA", "SENTENCIA / SEGUIR ADELANTE"), ("06", "LIQUIDACION", "LIQUIDACION DEL CREDITO"),
          ("07", "EMBARGO Y SECUESTRO", "MEDIDAS CAUTELARES"), ("08", "REMATE", "AVALUO Y REMATE")]
SUBETAPAS = {"01": ("0101", "Pendiente radicar"), "02": ("0201", "Pendiente auto admisorio"), "03": ("0301", "Citacion enviada"),
             "04": ("0401", "En traslado"), "05": ("0501", "Pendiente sentencia"), "06": ("0601", "Pendiente aprobacion"),
             "07": ("0701", "Oficio de embargo radicado"), "08": ("0801", "Fecha de remate fijada")}
for p in deudores:
    if not p["juridico"]:
        continue
    etapa = random.choice(ETAPAS)
    sub = SUBETAPAS[etapa[0]]
    creado = datetime.combine(rdate(date(2024, 6, 1), date(2026, 9, 30)), datetime.min.time()) + timedelta(hours=random.randint(8, 17))
    ult = min(datetime.combine(PROCESO, datetime.min.time()), creado + timedelta(days=random.randint(5, 300)))
    act = random.randint(1, 4); ina = random.randint(0, 3)
    ab = p["abog"]; usr = p["usr"]
    int_ab = random.choice(SUPERVISORES_ABOG)
    juz = f"Juzgado {random.randint(1, 25):02d} {random.choice(JUZGADOS_TIPO)} de {p['ciudad']}"
    radicado = f"{random.randint(11, 85)}{random.randint(1, 999):03d}{random.randint(31, 40)}{random.randint(1, 99):02d}{random.randint(1, 30):03d}{creado.year}{random.randint(0, 99999):05d}00"
    add("tbl_vreporteprocesosjuridicos", REGION=p["reg"], CLIENTE_IDENTIFICACION=p["doc"], CLIENTE_NOMBRE=p["nombre"].upper(), CLIENTE_ESTADO=p["estado_cart"],
        CLIENTE_CAMPANA=p["camp"], CLIENTE_SUB_CAMPANA_ACTUAL=p["subcamp"], CAPITAL=p["capital"], USUARIO_ACTUAL=usr[0], USUARIO_ACTUAL_NOMBRE=usr[1].upper(),
        ABOGADO=ab[0], ABOGADO_NOMBRE=ab[1].upper(), ABOGADO_INTERNO=int_ab[0], ABOGADO_INTERNO_NOMBRE=int_ab[1].upper(),
        PROCESO_USUARIO_CREACION=usr[0], PROCESO_USUARIO_CREACION_NOMBRE=usr[1].upper(), PROCESO="EJECUTIVO SINGULAR" if random.random() < 0.8 else "EJECUTIVO CON GARANTIA REAL",
        PROCESO_ESTADO=wch([("ACTIVO", 80), ("SUSPENDIDO", 8), ("TERMINADO POR PAGO", 7), ("TERMINADO POR DESISTIMIENTO", 5)]),
        PROCESO_FECHA_DE_CREACION=creado, PROCESO_JUZGADO=juz, PROCESO_JUZGADO_CIUDAD=p["ciudad"].upper(), PROCESO_NUMERO_DE_RADICADO=radicado,
        PROCESO_INSTANCIA=random.choice(["PRIMERA INSTANCIA", "PRIMERA INSTANCIA", "SEGUNDA INSTANCIA"]), PROCESO_FECHA_ULTIMA_ACTUALIZACION=ult,
        CANTIDAD_ACCIONES_JURIDICAS_ACTIVAS=act, CANTIDAD_ACCIONES_JURIDICAS_INACTIVAS=ina, CANTIDAD_ACCIONES_JURIDICAS=act + ina,
        ULTIMA_ETAPA=etapa[0], ULTIMA_ETAPA_DESCRIPCION=etapa[1], ULTIMA_ETAPA_ESTADO=random.choice(["EN TRAMITE", "EN TRAMITE", "PENDIENTE", "FINALIZADA"]),
        ULTIMA_ETAPA_OBSERVACION=etapa[2], ULTIMA_SUB_ETAPA=sub[0], ULTIMA_SUB_ETAPA_DESCRIPCION=sub[1], FECHA_INSER=creado.date(),
        FECHA_PROCESO=PROCESO, FECHA_CIERRE=None, USUARIO_CREA=usr[0], USUARIOACTUAL=usr[0])

# ---------------------------------------------------------------- escritura
for t, rows in TABLES.items():
    with open(os.path.join(OUT, f"{t}.csv"), "w", newline="", encoding="utf-8") as fh:
        w = csv.writer(fh)
        w.writerow(SCHEMA[t])
        w.writerows(rows)
    print(f"{t:35s} {len(rows):6d} filas, {len(SCHEMA[t])} columnas")
print("clientes:", N, "| deudores en cartera:", len(deudores), "| juridicos:", sum(1 for p in deudores if p["juridico"]), "| promesas:", promesas_n)
