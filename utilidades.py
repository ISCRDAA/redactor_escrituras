from __future__ import annotations

from collections import OrderedDict
from collections.abc import Iterable
from datetime import date, datetime
from typing import Any
import re
import unicodedata


PUNTOS_CARDINALES = (
    "NORTE",
    "SUR",
    "ESTE",
    "OESTE",
    "ORIENTE",
    "PONIENTE",
    "NORESTE",
    "NOROESTE",
    "SURESTE",
    "SUROESTE",
)

TIPOS_COLINDANTE = (
    "PROPIEDAD DE",
    "CALLE",
    "CAMINO",
    "CARRETERA",
    "ARROYO",
    "RÍO",
    "BARRANCA",
    "PARCELA",
    "EJIDO",
    "OTRO",
)

SEXOS = ("MASCULINO", "FEMENINO")

CALIDADES = (
    "VENDEDOR",
    "COMPRADOR",
    "DONANTE",
    "DONATARIO",
    "CEDENTE",
    "CESIONARIO",
    "PODERDANTE",
    "APODERADO",
    "TESTADOR",
    "ALBACEA",
    "HEREDERO",
    "TESTIGO",
)

ESTADOS_CIVILES = (
    "SOLTERO",
    "CASADO",
    "DIVORCIADO",
    "VIUDO",
    "CONCUBINATO",
    "SOCIEDAD DE CONVIVENCIA",
    "OTRO",
)

MESES = (
    "enero",
    "febrero",
    "marzo",
    "abril",
    "mayo",
    "junio",
    "julio",
    "agosto",
    "septiembre",
    "octubre",
    "noviembre",
    "diciembre",
)

ORDINALES_FEMENINOS = (
    "primera",
    "segunda",
    "tercera",
    "cuarta",
    "quinta",
    "sexta",
    "séptima",
    "octava",
    "novena",
    "décima",
    "décima primera",
    "décima segunda",
    "décima tercera",
    "décima cuarta",
    "décima quinta",
    "décima sexta",
    "décima séptima",
    "décima octava",
    "décima novena",
    "vigésima",
)

UNIDADES = {
    0: "cero",
    1: "uno",
    2: "dos",
    3: "tres",
    4: "cuatro",
    5: "cinco",
    6: "seis",
    7: "siete",
    8: "ocho",
    9: "nueve",
    10: "diez",
    11: "once",
    12: "doce",
    13: "trece",
    14: "catorce",
    15: "quince",
    16: "dieciséis",
    17: "diecisiete",
    18: "dieciocho",
    19: "diecinueve",
    20: "veinte",
    21: "veintiuno",
    22: "veintidós",
    23: "veintitrés",
    24: "veinticuatro",
    25: "veinticinco",
    26: "veintiséis",
    27: "veintisiete",
    28: "veintiocho",
    29: "veintinueve",
}

DECENAS = {
    30: "treinta",
    40: "cuarenta",
    50: "cincuenta",
    60: "sesenta",
    70: "setenta",
    80: "ochenta",
    90: "noventa",
}

CENTENAS = {
    100: "ciento",
    200: "doscientos",
    300: "trescientos",
    400: "cuatrocientos",
    500: "quinientos",
    600: "seiscientos",
    700: "setecientos",
    800: "ochocientos",
    900: "novecientos",
}

CALIDAD_FEMENINA = {
    "VENDEDOR": "VENDEDORA",
    "COMPRADOR": "COMPRADORA",
    "DONANTE": "DONANTE",
    "DONATARIO": "DONATARIA",
    "CEDENTE": "CEDENTE",
    "CESIONARIO": "CESIONARIA",
    "PODERDANTE": "PODERDANTE",
    "APODERADO": "APODERADA",
    "TESTADOR": "TESTADORA",
    "ALBACEA": "ALBACEA",
    "HEREDERO": "HEREDERA",
    "TESTIGO": "TESTIGO",
}

CALIDAD_PLURAL_MASCULINA = {
    "VENDEDOR": "VENDEDORES",
    "COMPRADOR": "COMPRADORES",
    "DONANTE": "DONANTES",
    "DONATARIO": "DONATARIOS",
    "CEDENTE": "CEDENTES",
    "CESIONARIO": "CESIONARIOS",
    "PODERDANTE": "PODERDANTES",
    "APODERADO": "APODERADOS",
    "TESTADOR": "TESTADORES",
    "ALBACEA": "ALBACEAS",
    "HEREDERO": "HEREDEROS",
    "TESTIGO": "TESTIGOS",
}

CALIDAD_PLURAL_FEMENINA = {
    **CALIDAD_PLURAL_MASCULINA,
    "VENDEDOR": "VENDEDORAS",
    "COMPRADOR": "COMPRADORAS",
    "DONATARIO": "DONATARIAS",
    "CESIONARIO": "CESIONARIAS",
    "APODERADO": "APODERADAS",
    "TESTADOR": "TESTADORAS",
    "HEREDERO": "HEREDERAS",
}


def parsear_fecha(valor: str) -> date:
    """Acepta DD/MM/AAAA, DD-MM-AAAA o AAAA-MM-DD."""
    texto = valor.strip()
    formatos = ("%d/%m/%Y", "%d-%m-%Y", "%Y-%m-%d")
    for formato in formatos:
        try:
            return datetime.strptime(texto, formato).date()
        except ValueError:
            continue
    raise ValueError("La fecha debe escribirse como DD/MM/AAAA.")


def calcular_edad(fecha_nacimiento: date, fecha_referencia: date) -> int:
    if fecha_nacimiento > fecha_referencia:
        raise ValueError("La fecha de nacimiento no puede ser posterior a la escritura.")

    return fecha_referencia.year - fecha_nacimiento.year - (
        (fecha_referencia.month, fecha_referencia.day)
        < (fecha_nacimiento.month, fecha_nacimiento.day)
    )


def normalizar_lugar(valor: str) -> str:
    """Normaliza una localidad para compararla sin acentos, mayúsculas ni puntuación."""
    texto = unicodedata.normalize("NFD", str(valor).strip().casefold())
    texto = "".join(caracter for caracter in texto if unicodedata.category(caracter) != "Mn")
    texto = re.sub(r"[^a-z0-9]+", " ", texto)
    return " ".join(texto.split())


def son_lugares_iguales(origen: str, vecindad: str) -> bool:
    origen_normalizado = normalizar_lugar(origen)
    vecindad_normalizada = normalizar_lugar(vecindad)
    return bool(origen_normalizado) and origen_normalizado == vecindad_normalizada


def _menor_mil(numero: int) -> str:
    if numero < 30:
        return UNIDADES[numero]

    if numero < 100:
        decena = (numero // 10) * 10
        unidad = numero % 10
        return DECENAS[decena] if unidad == 0 else f"{DECENAS[decena]} y {UNIDADES[unidad]}"

    if numero == 100:
        return "cien"

    centena = (numero // 100) * 100
    resto = numero % 100
    return CENTENAS[centena] if resto == 0 else f"{CENTENAS[centena]} {_menor_mil(resto)}"


def numero_a_letras(numero: int) -> str:
    """Convierte enteros de 0 a 999,999,999 a palabras en español."""
    if not 0 <= numero <= 999_999_999:
        raise ValueError("El número debe estar entre 0 y 999,999,999.")

    if numero < 1000:
        return _menor_mil(numero)

    if numero < 1_000_000:
        miles = numero // 1000
        resto = numero % 1000
        prefijo = "mil" if miles == 1 else f"{_menor_mil(miles)} mil"
        return prefijo if resto == 0 else f"{prefijo} {_menor_mil(resto)}"

    millones = numero // 1_000_000
    resto = numero % 1_000_000
    prefijo = "un millón" if millones == 1 else f"{numero_a_letras(millones)} millones"
    return prefijo if resto == 0 else f"{prefijo} {numero_a_letras(resto)}"


def convertir_numero_texto(valor: str) -> str:
    limpio = valor.replace(",", "").replace(" ", "").strip()
    if not limpio:
        return ""
    if not limpio.isdigit():
        raise ValueError(f"No se puede convertir a letra: {valor}")
    return numero_a_letras(int(limpio))


def fecha_notarial(fecha: date, incluir_dias: bool = True) -> str:
    dia = fecha.day
    palabra_dias = "día" if dia == 1 else "días"
    inicio = f"{dia} {numero_a_letras(dia)} {palabra_dias}" if incluir_dias else f"{dia} {numero_a_letras(dia)}"
    return (
        f"{inicio} del mes de {MESES[fecha.month - 1]} de "
        f"{fecha.year} {numero_a_letras(fecha.year)}"
    )


def fecha_nacimiento_notarial(fecha: date) -> str:
    return (
        f"{fecha.day} {numero_a_letras(fecha.day)} de {MESES[fecha.month - 1]} "
        f"de {fecha.year} {numero_a_letras(fecha.year)}"
    )


def ordinal_femenino(numero: int) -> str:
    if numero < 1:
        raise ValueError("El número de línea debe ser mayor que cero.")
    if numero <= len(ORDINALES_FEMENINOS):
        return ORDINALES_FEMENINOS[numero - 1]
    return f"número {numero}"


def describir_colindante(tipo: str, nombre: str) -> str:
    tipo_limpio = tipo.strip().upper()
    nombre_limpio = nombre.strip()

    if tipo_limpio == "PROPIEDAD DE":
        return f"propiedad de {nombre_limpio}"
    if tipo_limpio == "CALLE":
        return f"la calle {nombre_limpio}".strip()
    if tipo_limpio == "CAMINO":
        return f"el camino {nombre_limpio}".strip()
    if tipo_limpio == "CARRETERA":
        return f"la carretera {nombre_limpio}".strip()
    if tipo_limpio == "ARROYO":
        return f"el arroyo {nombre_limpio}".strip() if nombre_limpio else "ARROYO"
    if tipo_limpio == "RÍO":
        return f"el río {nombre_limpio}".strip() if nombre_limpio else "RÍO"
    if tipo_limpio == "BARRANCA":
        return f"la barranca {nombre_limpio}".strip() if nombre_limpio else "BARRANCA"
    if tipo_limpio == "PARCELA":
        return f"la parcela {nombre_limpio}".strip()
    if tipo_limpio == "EJIDO":
        return f"el ejido {nombre_limpio}".strip()
    return nombre_limpio


def _texto_tramos(tramos: Iterable[dict[str, str]]) -> tuple[str, int]:
    tramos_lista = list(tramos)
    cantidad = len(tramos_lista)
    if cantidad == 0:
        raise ValueError("Cada grupo de colindancia debe tener por lo menos un tramo.")

    partes: list[str] = []
    for indice, tramo in enumerate(tramos_lista, start=1):
        medida = tramo["medida"].strip()
        medida_letra = tramo["medida_letra"].strip()
        expresion_medida = f"({medida}) {medida_letra}"

        if cantidad == 1:
            partes.append(f"una línea de {expresion_medida}")
        elif indice == 1:
            partes.append(f"una {ordinal_femenino(indice)} línea de {expresion_medida}")
        else:
            partes.append(f"la {ordinal_femenino(indice)} línea de {expresion_medida}")

    if cantidad == 1:
        return partes[0], cantidad
    if cantidad == 2:
        return " y ".join(partes), cantidad
    return ", ".join(partes[:-1]) + ", y " + partes[-1], cantidad


def construir_texto_colindancias(
    grupos: Iterable[dict[str, Any]],
    usar_guiones_automaticos: bool = True,
) -> str:
    grupos_por_cardinal: OrderedDict[str, list[dict[str, Any]]] = OrderedDict()
    for grupo in grupos:
        cardinal = str(grupo["punto"]).strip().upper()
        grupos_por_cardinal.setdefault(cardinal, []).append(grupo)

    parrafos: list[str] = []
    for cardinal, grupos_cardinal in grupos_por_cardinal.items():
        fragmentos: list[str] = []
        for indice_grupo, grupo in enumerate(grupos_cardinal):
            texto_tramos, cantidad = _texto_tramos(grupo["tramos"])
            colindante = describir_colindante(
                str(grupo["tipo_colindante"]),
                str(grupo["colindante"]),
            )
            verbo = "linda" if cantidad == 1 else "lindan"
            inicio = "Colinda en" if indice_grupo == 0 else "y en"
            fragmentos.append(f"{inicio} {texto_tramos}, {verbo} con {colindante}")

        texto_cardinal = f"AL {cardinal}: " + ", ".join(fragmentos) + "."
        if usar_guiones_automaticos:
            texto_cardinal += "\t"
        parrafos.append(texto_cardinal)

    return "\a" + "\a".join(parrafos) + "\a"


def resumen_grupo(grupo: dict[str, Any]) -> str:
    cantidad = len(grupo.get("tramos", []))
    palabra = "tramo" if cantidad == 1 else "tramos"
    return f"{cantidad} {palabra}"


def articulo_persona(sexo: str, plural: bool = False) -> str:
    femenino = sexo.strip().upper() == "FEMENINO"
    if plural:
        return "las señoras" if femenino else "los señores"
    return "la señora" if femenino else "el señor"


def calidad_mostrada(calidad: str, sexo: str, plural: bool = False) -> str:
    base = calidad.strip().upper()
    femenino = sexo.strip().upper() == "FEMENINO"
    if plural:
        return (
            CALIDAD_PLURAL_FEMENINA.get(base, f"{base}S")
            if femenino
            else CALIDAD_PLURAL_MASCULINA.get(base, f"{base}S")
        )
    return CALIDAD_FEMENINA.get(base, base) if femenino else base


def unir_nombres(nombres: list[str]) -> str:
    if not nombres:
        return ""
    if len(nombres) == 1:
        return nombres[0]
    if len(nombres) == 2:
        return f"{nombres[0]} y {nombres[1]}"
    return ", ".join(nombres[:-1]) + f" y {nombres[-1]}"


def construir_otorgamiento(comparecientes: Iterable[dict[str, Any]]) -> str:
    grupos: OrderedDict[str, list[dict[str, Any]]] = OrderedDict()
    for persona in comparecientes:
        calidad = str(persona["calidad"]).strip().upper()
        grupos.setdefault(calidad, []).append(persona)

    fragmentos: list[str] = []
    for calidad, personas in grupos.items():
        nombres = [str(p["nombre"]).strip().upper() for p in personas]
        todos_femeninos = all(str(p["sexo"]).upper() == "FEMENINO" for p in personas)
        sexo_referencia = "FEMENINO" if todos_femeninos else "MASCULINO"
        articulo = articulo_persona(sexo_referencia, plural=len(personas) > 1)
        calidad_texto = calidad_mostrada(
            calidad,
            sexo_referencia,
            plural=len(personas) > 1,
        )
        fragmentos.append(
            f"{articulo} {unir_nombres(nombres)}, como “{calidad_texto}”"
        )

    if not fragmentos:
        return "Que comparecen"
    if len(fragmentos) == 1:
        detalle = fragmentos[0]
    elif len(fragmentos) == 2:
        detalle = f"{fragmentos[0]} y de la otra parte {fragmentos[1]}"
    else:
        detalle = "; ".join(fragmentos[:-1]) + f"; y finalmente {fragmentos[-1]}"

    return f"Que otorgan manifestando su voluntad de una parte {detalle}"


def letra_inciso(indice: int) -> str:
    if indice < 1:
        raise ValueError("El índice debe iniciar en uno.")
    # Para esta etapa son suficientes 26 comparecientes.
    if indice <= 26:
        return chr(96 + indice)
    return str(indice)


def construir_datos_personales(comparecientes: Iterable[dict[str, Any]]) -> str:
    parrafos: list[str] = []
    for indice, persona in enumerate(comparecientes, start=1):
        sexo = str(persona["sexo"]).upper()
        articulo = articulo_persona(sexo).capitalize()
        sabe_firmar = bool(persona.get("sabe_firmar", True))
        firma = "declara saber firmar" if sabe_firmar else "declara no saber firmar"
        nacionalidad = str(persona.get("nacionalidad", "MEXICANA")).strip().lower()
        estado_civil = str(persona.get("estado_civil", "")).strip().lower()
        ocupacion = str(persona.get("ocupacion", "")).strip().lower()
        originario = "originaria" if sexo == "FEMENINO" else "originario"
        vecino = "vecina" if sexo == "FEMENINO" else "vecino"

        mismo_origen_vecindad = bool(persona.get("mismo_origen_vecindad", False)) or son_lugares_iguales(
            str(persona.get("originario", "")),
            str(persona.get("vecino", "")),
        )
        if mismo_origen_vecindad:
            origen_vecindad = f"{originario} y {vecino} de {persona['originario']}"
        else:
            origen_vecindad = (
                f"{originario} de {persona['originario']} y "
                f"{vecino} de {persona['vecino']}"
            )

        texto = (
            f"{letra_inciso(indice)}).- {articulo} {persona['nombre']}, {origen_vecindad}, "
            f"con domicilio en {persona['domicilio']}, Código Postal {persona['codigo_postal']}, con fecha "
            f"de nacimiento el día {persona['fecha_nacimiento_texto']}, de "
            f"{persona['edad_numero']} {persona['edad_letra']} años de edad, {estado_civil}, "
            f"de ocupación {ocupacion}, con Registro Federal de Contribuyentes número "
            f"“{persona['rfc']}”, con Clave Única de Registro de Población número "
            f"“{persona['curp']}”, de nacionalidad {nacionalidad}, misma que conserva y "
            f"{firma}; quien se identifica con Credencial para Votar con Fotografía con "
            f"número “{persona['numero_ine']}”, expedida por el Instituto Nacional "
            f"Electoral, de paso por esta ciudad.\t"
        )
        parrafos.append(texto)

    return "\a" + "\a".join(parrafos) + "\a"


def construir_firmas(comparecientes: Iterable[dict[str, Any]]) -> str:
    nombres = [str(p["nombre"]).strip().upper() for p in comparecientes]
    filas: list[str] = []
    for indice in range(0, len(nombres), 2):
        pareja = nombres[indice : indice + 2]
        filas.append(pareja[0] if len(pareja) == 1 else f"{pareja[0]}\t{pareja[1]}")
    return "\a" + "\a".join(filas) + "\a"


def preparar_persona(persona: dict[str, Any], fecha_escritura: date) -> dict[str, Any]:
    resultado = dict(persona)
    nacimiento = parsear_fecha(str(persona["fecha_nacimiento"]))
    edad = calcular_edad(nacimiento, fecha_escritura)
    resultado["nombre"] = str(persona["nombre"]).strip().upper()
    resultado["rfc"] = str(persona.get("rfc", "")).strip().upper()
    resultado["curp"] = str(persona.get("curp", "")).strip().upper()
    resultado["edad_numero"] = edad
    resultado["edad_letra"] = numero_a_letras(edad)
    resultado["fecha_nacimiento_texto"] = fecha_nacimiento_notarial(nacimiento)
    resultado["anio_nacimiento_letra"] = numero_a_letras(nacimiento.year)
    return resultado


def contexto_legacy_persona(persona: dict[str, Any]) -> dict[str, Any]:
    """Adapta un compareciente a los marcadores heredados de la plantilla."""
    return {
        "nombre": persona["nombre"],
        "originario": persona["originario"],
        "vecino": persona["vecino"],
        "domicilio": persona["domicilio"],
        "codigo_postal": persona["codigo_postal"],
        "fecha_nacimiento": persona["fecha_nacimiento_texto"],
        "anio_nacimiento_letra": persona["anio_nacimiento_letra"],
        "edad_numero": persona["edad_numero"],
        "edad_letra": persona["edad_letra"],
        "estado_civil": str(persona["estado_civil"]).lower(),
        "ocupacion": str(persona["ocupacion"]).lower(),
        "rfc": persona["rfc"],
        "curp": persona["curp"],
        "numero_ine": persona["numero_ine"],
    }


def construir_descripcion_inmueble(
    tipo_inmueble: str,
    denominacion: str,
    ubicacion: str,
    municipio: str,
    estado: str,
    nombre_referencia: str = "",
) -> str:
    """Construye una descripción breve y editable del inmueble."""
    tipo = tipo_inmueble.strip().upper() or "INMUEBLE"
    partes = [f"DEL {tipo}"]

    if denominacion.strip():
        partes.append(f'DENOMINADO “{denominacion.strip().upper()}”')

    if ubicacion.strip():
        partes.append(f"UBICADO EN {ubicacion.strip().upper()}")

    if municipio.strip():
        partes.append(f"MUNICIPIO DE {municipio.strip().upper()}")

    if estado.strip():
        partes.append(f"ESTADO DE {estado.strip().upper()}")

    texto = ", ".join(partes)
    if nombre_referencia.strip():
        texto += (
            f', QUE EN LO SUCESIVO SE DENOMINARÁ '
            f'“{nombre_referencia.strip().upper()}”'
        )
    return texto


def _articulo_personas(personas: list[dict[str, Any]]) -> str:
    if not personas:
        return "la parte transmitente"

    nombres = [str(persona.get("nombre", "")).strip().upper() for persona in personas]
    nombres = [nombre for nombre in nombres if nombre]
    if not nombres:
        return "la parte transmitente"

    if len(nombres) == 1:
        sexo = str(personas[0].get("sexo", "MASCULINO")).upper()
        articulo = "la señora" if sexo == "FEMENINO" else "el señor"
        return f"{articulo} {nombres[0]}"

    solo_mujeres = all(
        str(persona.get("sexo", "MASCULINO")).upper() == "FEMENINO"
        for persona in personas
    )
    articulo = "las señoras" if solo_mujeres else "los señores"
    if len(nombres) == 2:
        nombres_texto = f"{nombres[0]} y {nombres[1]}"
    else:
        nombres_texto = ", ".join(nombres[:-1]) + f" y {nombres[-1]}"
    return f"{articulo} {nombres_texto}"


def construir_antecedente_propiedad(
    antecedente: dict[str, Any],
    vendedores: Iterable[dict[str, Any]],
) -> str:
    """Redacta el antecedente de propiedad o usa una redacción libre."""
    libre = str(antecedente.get("texto_libre", "")).strip()
    if libre:
        return libre.rstrip(". ") + "."

    vendedores_lista = list(vendedores)
    sujeto = _articulo_personas(vendedores_lista)
    plural = len(vendedores_lista) != 1
    declara = "Declaran" if plural else "Declara"
    adquirio = "adquirieron" if plural else "adquirió"

    documento = str(antecedente.get("documento", "")).strip()
    if not documento:
        documento = "Primer Testimonio de la Escritura"

    fragmentos = [f"{declara} {sujeto}, de manera expresa y bajo protesta de decir verdad que por {documento}"]

    numero = str(antecedente.get("numero", "")).strip()
    numero_letra = str(antecedente.get("numero_letra", "")).strip()
    if numero:
        numero_texto = f"Número {numero}"
        if numero_letra:
            numero_texto += f" {numero_letra.lower()}"
        fragmentos.append(numero_texto)

    volumen = str(antecedente.get("volumen", "")).strip()
    volumen_letra = str(antecedente.get("volumen_letra", "")).strip()
    if volumen:
        volumen_texto = f"volumen número {volumen}"
        if volumen_letra:
            volumen_texto += f" {volumen_letra.lower()}"
        fragmentos.append(volumen_texto)

    fecha_texto = str(antecedente.get("fecha_texto", "")).strip()
    if fecha_texto:
        fragmentos.append(f"de fecha {fecha_texto}")

    autoridad = str(antecedente.get("autoridad", "")).strip()
    if autoridad:
        fragmentos.append(f"pasada ante la fe de {autoridad}")

    ubicacion_autoridad = str(antecedente.get("ubicacion_autoridad", "")).strip()
    if ubicacion_autoridad:
        fragmentos.append(f"con ejercicio en {ubicacion_autoridad}")

    acto = str(antecedente.get("acto_adquisicion", "")).strip()
    if acto:
        fragmentos.append(f"que contiene {acto}")

    texto = ", ".join(fragmentos)
    texto += f", mediante el cual {adquirio} en legítima propiedad el predio de referencia."
    return texto


def construir_datos_registro(registro: dict[str, Any]) -> str:
    oficina = str(registro.get("oficina", "")).strip()
    tipo_asiento = str(registro.get("tipo_asiento", "Partida")).strip()
    numero = str(registro.get("numero", "")).strip()
    numero_letra = str(registro.get("numero_letra", "")).strip()
    libro = str(registro.get("libro", "")).strip()
    libro_letra = str(registro.get("libro_letra", "")).strip()
    seccion = str(registro.get("seccion", "")).strip()
    seccion_letra = str(registro.get("seccion_letra", "")).strip()
    fecha_texto = str(registro.get("fecha_texto", "")).strip()

    if not oficina or not numero:
        raise ValueError("Los datos registrales requieren oficina y número de asiento.")

    texto = f"Dicha propiedad se encuentra inscrita ante {oficina}, bajo {tipo_asiento} número {numero}"
    if numero_letra:
        texto += f" {numero_letra.lower()}"
    if libro:
        texto += f", Libro {libro}"
        if libro_letra:
            texto += f" {libro_letra.lower()}"
    if seccion:
        texto += f", Sección {seccion}"
        if seccion_letra:
            texto += f" {seccion_letra.lower()}"
    if fecha_texto:
        texto += f", de fecha {fecha_texto}"
    return texto.rstrip(". ") + "."


def construir_declaracion_predial(
    predial: dict[str, Any],
    denominacion_parte: str = "parte vendedora",
) -> str:
    municipio = str(predial.get("municipio", "")).strip()
    estado = str(predial.get("estado", "")).strip()
    cuenta = str(predial.get("cuenta", "")).strip()
    clave = str(predial.get("clave_catastral", "")).strip()

    if not municipio or not estado:
        raise ValueError("La declaración predial requiere municipio y estado.")
    if not cuenta and not clave:
        raise ValueError("Captura la cuenta predial o la clave catastral.")

    identificadores: list[str] = []
    if cuenta:
        identificadores.append(f"número de cuenta predial {cuenta}")
    if clave:
        identificadores.append(f"clave catastral {clave}")

    if len(identificadores) == 2:
        identificacion = f"{identificadores[0]} y {identificadores[1]}"
    else:
        identificacion = identificadores[0]

    return (
        f"Finalmente declara la {denominacion_parte.strip()} que el inmueble de su propiedad "
        "materia del presente contrato se encuentra debidamente inscrito a su nombre "
        f"en el padrón de la propiedad raíz de la Tesorería Municipal de {municipio}, "
        f"Estado de {estado}, y que a la fecha no reporta adeudo alguno por concepto "
        f"de impuesto predial, según lo justifica con la tarjeta con {identificacion} "
        "y que en este acto exhibe."
    )



def personas_por_calidad(
    comparecientes: Iterable[dict[str, Any]],
    calidad: str,
) -> list[dict[str, Any]]:
    buscada = calidad.strip().upper()
    return [
        persona
        for persona in comparecientes
        if str(persona.get("calidad", "")).strip().upper() == buscada
    ]


def describir_parte(personas: Iterable[dict[str, Any]], fallback: str) -> str:
    lista = list(personas)
    if not lista:
        return fallback
    return _articulo_personas(lista)


def _verbo_por_cantidad(cantidad: int, singular: str, plural: str) -> str:
    return singular if cantidad == 1 else plural


def construir_introduccion_acto(
    acto: str,
    descripcion_inmueble: str,
) -> str:
    clave = acto.strip().upper()
    descripcion = descripcion_inmueble.strip()
    if clave == "DONACIÓN":
        return (
            f"Respecto de “LA TOTALIDAD” {descripcion}, inmueble materia de la "
            "donación que vienen a formalizar hoy a solicitud de los otorgantes, "
            "de conformidad con la declaración, antecedentes y cláusulas siguientes."
        )
    if clave == "CESIÓN DE DERECHOS":
        return (
            f"Respecto de los derechos que corresponden sobre “LA TOTALIDAD” {descripcion}, "
            "cuya cesión vienen a formalizar hoy a solicitud de los otorgantes, de "
            "conformidad con la declaración, antecedentes y cláusulas siguientes."
        )
    return (
        f"Respecto de “LA TOTALIDAD” {descripcion}, y cuyo contrato vienen a formalizar "
        "hoy a solicitud de los contratantes, de conformidad con la declaración, "
        "antecedentes y cláusulas siguientes."
    )


def _importe_texto(operacion: dict[str, Any], etiqueta: str) -> str:
    importe = str(operacion.get("importe", "")).strip()
    importe_letra = str(operacion.get("importe_letra", "")).strip()
    if not importe:
        return ""
    texto = f"{etiqueta} ${importe}"
    if importe_letra:
        texto += f" ({importe_letra.lower()} pesos 00/100 moneda nacional)"
    return texto


def construir_clausulas_acto(
    acto: str,
    configuracion: dict[str, Any],
    comparecientes: Iterable[dict[str, Any]],
    inmueble: dict[str, Any],
    operacion: dict[str, Any],
    campos_especificos: dict[str, str],
) -> str:
    """Construye un cuerpo prototipo según el acto seleccionado.

    Las cláusulas son una base automatizable y deben revisarse jurídicamente antes
    de utilizarse como instrumento definitivo.
    """
    personas = list(comparecientes)
    transmitentes = personas_por_calidad(
        personas, str(configuracion["calidad_transmitente"])
    )
    adquirentes = personas_por_calidad(
        personas, str(configuracion["calidad_adquirente"])
    )
    parte_t = describir_parte(transmitentes, str(configuracion["parte_transmitente"]))
    parte_a = describir_parte(adquirentes, str(configuracion["parte_adquirente"]))
    descripcion = str(inmueble.get("descripcion", "")).strip()
    n_t = len(transmitentes)
    n_a = len(adquirentes)

    declara_t = _verbo_por_cantidad(n_t, "declara", "declaran")
    transmite = _verbo_por_cantidad(n_t, "transmite", "transmiten")
    cede = _verbo_por_cantidad(n_t, "cede", "ceden")
    acepta = _verbo_por_cantidad(n_a, "acepta", "aceptan")
    adquiere = _verbo_por_cantidad(n_a, "adquiere", "adquieren")

    clave = acto.strip().upper()
    parrafos: list[str] = []

    if clave == "DONACIÓN":
        tipo = campos_especificos.get("tipo_donacion", "PURA").strip().lower()
        reserva = campos_especificos.get(
            "reserva_usufructo", "SIN RESERVA DE USUFRUCTO"
        ).strip().lower()
        valor = _importe_texto(operacion, "El valor declarado para efectos de esta operación es de")
        parrafos.extend(
            [
                "Que atentos a los antecedentes expuestos, los otorgantes formalizan la presente donación bajo las siguientes cláusulas.\t",
                (
                    f"PRIMERA.- {parte_t} {transmite} gratuitamente y de manera definitiva "
                    f"a favor de {parte_a}, quien {acepta}, “LA TOTALIDAD” {descripcion}, "
                    "con todo cuanto de hecho y por derecho le corresponda.\t"
                ),
                (
                    f"SEGUNDA.- Las partes manifiestan que la donación es {tipo}. En cuanto "
                    f"al usufructo, convienen lo siguiente: {reserva}.\t"
                ),
                (
                    "TERCERA.- La parte donataria manifiesta que acepta expresamente la "
                    "donación y se da por recibida jurídica y materialmente del inmueble, "
                    "salvo la modalidad que expresamente se haya pactado.\t"
                ),
                (
                    f"CUARTA.- {parte_t} {declara_t} que el inmueble se transmite con las "
                    "medidas, colindancias, superficie y antecedentes descritos en este "
                    "instrumento, obligándose al saneamiento en los términos aplicables.\t"
                ),
            ]
        )
        if valor:
            parrafos.append(f"QUINTA.- {valor}.\t")
            numero_gastos = "SEXTA"
            numero_aceptacion = "SÉPTIMA"
        else:
            numero_gastos = "QUINTA"
            numero_aceptacion = "SEXTA"
        parrafos.extend(
            [
                (
                    f"{numero_gastos}.- Los gastos, derechos e impuestos que se causen "
                    "con motivo de este instrumento serán cubiertos conforme a la ley y al "
                    "acuerdo de las partes.\t"
                ),
                (
                    f"{numero_aceptacion}.- Los otorgantes declaran que su consentimiento "
                    "se encuentra libre de error, dolo, violencia o cualquier otro vicio y "
                    "aceptan el contenido íntegro de la presente escritura.\t"
                ),
            ]
        )

    elif clave == "CESIÓN DE DERECHOS":
        tipo_derecho = campos_especificos.get("tipo_derecho", "DERECHOS").strip().lower()
        origen = campos_especificos.get("origen_derecho", "").strip()
        contraprestacion = _importe_texto(
            operacion, "La contraprestación pactada por la cesión es de"
        )
        parrafos.extend(
            [
                "Que atentos a los antecedentes expuestos, los otorgantes formalizan la presente cesión de derechos bajo las siguientes cláusulas.\t",
                (
                    f"PRIMERA.- {parte_t} {cede} a favor de {parte_a}, quien {acepta}, los "
                    f"{tipo_derecho} relacionados con “LA TOTALIDAD” {descripcion}, en los "
                    "términos y con los alcances descritos en este instrumento.\t"
                ),
                (
                    f"SEGUNDA.- El origen de los derechos materia de la cesión es el siguiente: "
                    f"{origen or 'el que resulta del antecedente de propiedad relacionado'}.\t"
                ),
                (
                    f"TERCERA.- {contraprestacion or 'La cesión se celebra en los términos económicos convenidos por las partes'}. "
                    "La parte cedente reconoce haber recibido o recibir la contraprestación "
                    "en la forma pactada.\t"
                ),
                (
                    "CUARTA.- La parte cedente entrega a la parte cesionaria los documentos "
                    "que acreditan los derechos cedidos y se obliga a realizar los actos "
                    "necesarios para su reconocimiento e inscripción, cuando proceda.\t"
                ),
                (
                    f"QUINTA.- {parte_t} {declara_t} que no ha transmitido previamente los "
                    "mismos derechos a persona distinta y responderá por la existencia y "
                    "legitimidad de los derechos cedidos en los términos de ley.\t"
                ),
                (
                    "SEXTA.- Los gastos, derechos e impuestos derivados de esta escritura se "
                    "cubrirán conforme a la legislación aplicable y al acuerdo de las partes.\t"
                ),
                (
                    "SÉPTIMA.- La parte cesionaria acepta la cesión en todos sus términos y "
                    "los otorgantes ratifican su voluntad libre y expresa.\t"
                ),
            ]
        )

    else:
        forma_pago = campos_especificos.get("forma_pago", "EFECTIVO").strip().lower()
        entrega = campos_especificos.get("entrega_posesion", "EN ESTE ACTO").strip().lower()
        precio = _importe_texto(operacion, "El precio cierto y convenido es la cantidad de")
        parrafos.extend(
            [
                "Que atentos a los antecedentes expuestos, los contratantes formalizan la presente compraventa bajo las siguientes cláusulas.\t",
                (
                    f"PRIMERA.- {parte_t} {transmite} real y jurídicamente a favor de {parte_a}, "
                    f"quien {adquiere}, “LA TOTALIDAD” {descripcion}, con todo cuanto de "
                    "hecho y por derecho le corresponda.\t"
                ),
                (
                    f"SEGUNDA.- {precio}. La forma de pago pactada es {forma_pago}; la parte "
                    "vendedora otorga el recibo más eficaz que en derecho proceda, sujeto a "
                    "la comprobación correspondiente.\t"
                ),
                (
                    f"TERCERA.- La entrega de la posesión se realiza {entrega}. La parte "
                    "compradora declara conocer el estado físico y jurídico del inmueble.\t"
                ),
                (
                    "CUARTA.- La parte vendedora transmite el inmueble al corriente en sus "
                    "contribuciones y sin otras limitaciones que las expresamente relacionadas "
                    "en este instrumento.\t"
                ),
                (
                    "QUINTA.- La parte vendedora responderá por el saneamiento para el caso "
                    "de evicción y por las responsabilidades anteriores al otorgamiento, en "
                    "los términos de la legislación aplicable.\t"
                ),
                (
                    "SEXTA.- Los impuestos, derechos, gastos y honorarios serán cubiertos "
                    "conforme a la ley y al acuerdo de las partes.\t"
                ),
                (
                    "SÉPTIMA.- Las partes manifiestan que no existe error, dolo, violencia o "
                    "cualquier otro vicio del consentimiento y aceptan el contenido íntegro "
                    "de esta escritura.\t"
                ),
                (
                    f"OCTAVA.- {parte_a} {acepta} la presente compraventa y se da por "
                    "recibida de los derechos y de la posesión en los términos pactados.\t"
                ),
            ]
        )

    return "\a" + "\a".join(parrafos) + "\a"


def construir_cierre_apendice(
    acto: str,
    escritura: dict[str, Any],
    notario: dict[str, Any],
) -> str:
    clave = acto.strip().upper()
    documentos = [
        "Certificado de libertad de gravamen.",
        "Avalúo catastral.",
    ]
    if clave == "DONACIÓN":
        documentos.append(
            "Documentación relativa a la donación y parentesco, cuando proceda."
        )
    elif clave == "CESIÓN DE DERECHOS":
        documentos.append("Documentos que acreditan los derechos cedidos.")
    documentos.extend(
        [
            "Documentación fiscal y traslado de dominio, cuando proceda.",
            "Identificaciones de los comparecientes.",
        ]
    )

    ciudad = str(escritura.get("ciudad", "")).strip()
    estado = str(escritura.get("estado", "")).strip()
    notario_nombre = str(notario.get("nombre", "")).strip()
    titulo = clave.title()
    parrafos = [
        (
            f"AUTORIZO.- La escritura de {titulo} que antecede en la Ciudad de {ciudad}, "
            f"Estado de {estado}, en la fecha legalmente correspondiente.- Doy fe.- Una "
            f"firma ilegible del Licenciado {notario_nombre}.- El sello de autorizar de la notaría.\t"
        ),
        "DOCUMENTOS DEL APÉNDICE\t",
        (
            "De conformidad con la legislación notarial aplicable, agrego al apéndice del "
            "presente instrumento los documentos relacionados con esta escritura.\t"
        ),
    ]
    for indice, documento in enumerate(documentos):
        letra = chr(ord("A") + indice)
        parrafos.append(f"Anexo “{letra}”.- {documento}\t")
    parrafos.append(
        "Primer testimonio compulsado de su matriz que obra en esta notaría y que se expide a favor de la parte interesada.\t"
    )
    return "\a" + "\a".join(parrafos) + "\a"
