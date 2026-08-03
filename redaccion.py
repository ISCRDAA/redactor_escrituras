from __future__ import annotations

from collections import OrderedDict
from datetime import datetime
from decimal import Decimal, InvalidOperation
from typing import Any



UNIDADES = {
    0: "cero", 1: "uno", 2: "dos", 3: "tres", 4: "cuatro", 5: "cinco",
    6: "seis", 7: "siete", 8: "ocho", 9: "nueve", 10: "diez",
    11: "once", 12: "doce", 13: "trece", 14: "catorce", 15: "quince",
    16: "dieciséis", 17: "diecisiete", 18: "dieciocho", 19: "diecinueve",
    20: "veinte", 21: "veintiuno", 22: "veintidós", 23: "veintitrés",
    24: "veinticuatro", 25: "veinticinco", 26: "veintiséis",
    27: "veintisiete", 28: "veintiocho", 29: "veintinueve",
}
DECENAS = {30: "treinta", 40: "cuarenta", 50: "cincuenta", 60: "sesenta", 70: "setenta", 80: "ochenta", 90: "noventa"}
CENTENAS = {200: "doscientos", 300: "trescientos", 400: "cuatrocientos", 500: "quinientos", 600: "seiscientos", 700: "setecientos", 800: "ochocientos", 900: "novecientos"}


def entero_a_letras(numero: int) -> str:
    if numero < 0:
        return "menos " + entero_a_letras(abs(numero))
    if numero < 30:
        return UNIDADES[numero]
    if numero < 100:
        decena = (numero // 10) * 10
        resto = numero % 10
        return DECENAS[decena] if resto == 0 else f"{DECENAS[decena]} y {entero_a_letras(resto)}"
    if numero == 100:
        return "cien"
    if numero < 200:
        return "ciento " + entero_a_letras(numero - 100)
    if numero < 1000:
        centena = (numero // 100) * 100
        resto = numero % 100
        return CENTENAS[centena] if resto == 0 else f"{CENTENAS[centena]} {entero_a_letras(resto)}"
    if numero < 1_000_000:
        miles = numero // 1000
        resto = numero % 1000
        prefijo = "mil" if miles == 1 else f"{entero_a_letras(miles)} mil"
        return prefijo if resto == 0 else f"{prefijo} {entero_a_letras(resto)}"
    if numero < 1_000_000_000:
        millones = numero // 1_000_000
        resto = numero % 1_000_000
        prefijo = "un millón" if millones == 1 else f"{entero_a_letras(millones)} millones"
        return prefijo if resto == 0 else f"{prefijo} {entero_a_letras(resto)}"
    raise ValueError("El número es demasiado grande para convertirlo automáticamente.")

MESES = (
    "enero", "febrero", "marzo", "abril", "mayo", "junio",
    "julio", "agosto", "septiembre", "octubre", "noviembre", "diciembre",
)

ORDINALES = (
    "primera", "segunda", "tercera", "cuarta", "quinta", "sexta",
    "séptima", "octava", "novena", "décima", "décima primera",
    "décima segunda", "décima tercera", "décima cuarta", "décima quinta",
)


def limpiar(texto: Any) -> str:
    return " ".join(str(texto or "").strip().split())


def mayusculas(texto: Any) -> str:
    return limpiar(texto).upper()


def numero_a_letras(valor: Any) -> str:
    texto = limpiar(valor).replace(",", "")
    if not texto:
        return ""
    try:
        numero = int(Decimal(texto))
    except (InvalidOperation, ValueError):
        return ""
    return entero_a_letras(numero).upper()


def cantidad_a_letras(valor: Any) -> str:
    texto = limpiar(valor).replace(",", "")
    if not texto:
        return ""
    try:
        numero = Decimal(texto)
    except InvalidOperation:
        return ""
    entero = int(numero)
    return entero_a_letras(entero)


def parsear_fecha(texto: str) -> datetime:
    valor = limpiar(texto)
    for formato in ("%d/%m/%Y", "%Y-%m-%d", "%d-%m-%Y"):
        try:
            return datetime.strptime(valor, formato)
        except ValueError:
            continue
    raise ValueError(f"Fecha inválida: {texto!r}. Usa DD/MM/AAAA.")


def fecha_notarial(texto: str, *, incluir_ano_literal: bool = False) -> str:
    fecha = parsear_fecha(texto)
    dia_letra = entero_a_letras(fecha.day)
    ano_letra = entero_a_letras(fecha.year)
    if incluir_ano_literal:
        return (
            f"{fecha.day:02d} {dia_letra} días del mes de {MESES[fecha.month - 1]} "
            f"del año {fecha.year} {ano_letra}"
        )
    return (
        f"{fecha.day:02d} {dia_letra} días del mes de {MESES[fecha.month - 1]} "
        f"de {fecha.year} {ano_letra}"
    )


def calcular_edad(fecha_nacimiento: str, fecha_instrumento: str) -> int:
    nacimiento = parsear_fecha(fecha_nacimiento)
    referencia = parsear_fecha(fecha_instrumento)
    edad = referencia.year - nacimiento.year
    if (referencia.month, referencia.day) < (nacimiento.month, nacimiento.day):
        edad -= 1
    return edad


def fecha_nacimiento_notarial(texto: str) -> str:
    fecha = parsear_fecha(texto)
    return (
        f"{fecha.day:02d} {entero_a_letras(fecha.day)} de "
        f"{MESES[fecha.month - 1]} de {fecha.year} "
        f"{entero_a_letras(fecha.year)}"
    )


def son_lugares_iguales(origen: str, vecindad: str) -> bool:
    def normalizar(valor: str) -> str:
        tabla = str.maketrans("ÁÉÍÓÚÜÑ", "AEIOUUN")
        return "".join(c for c in mayusculas(valor).translate(tabla) if c.isalnum())
    return bool(normalizar(origen)) and normalizar(origen) == normalizar(vecindad)


def construir_descripcion_inmueble(datos: dict[str, Any]) -> str:
    tipo = mayusculas(datos.get("tipo_inmueble")) or "PREDIO"
    denominacion = mayusculas(datos.get("denominacion"))
    ubicacion = mayusculas(datos.get("ubicacion"))
    municipio = mayusculas(datos.get("municipio"))
    estado = mayusculas(datos.get("estado_inmueble"))
    referencia = mayusculas(datos.get("nombre_referencia"))

    partes = [f"DEL {tipo}"]
    if denominacion:
        partes.append(f"DENOMINADO “{denominacion}”")
    if ubicacion:
        partes.append(f"UBICADO EN {ubicacion}")
    if municipio:
        partes.append(f"MUNICIPIO DE {municipio}")
    if estado:
        partes.append(f"ESTADO DE {estado}")
    descripcion = ", ".join(partes)
    if referencia:
        descripcion += f", QUE EN LO SUCESIVO SE DENOMINARÁ “{referencia}”"
    return descripcion


def medida_a_letras(valor: str) -> str:
    texto = limpiar(valor).replace(",", ".")
    if not texto:
        return ""
    if "." in texto:
        entero_texto, decimal_texto = texto.split(".", 1)
    else:
        entero_texto, decimal_texto = texto, "0"
    try:
        entero = int(entero_texto or "0")
        fraccion = int(decimal_texto or "0")
    except ValueError:
        return ""
    metro = "metro" if entero == 1 else "metros"
    centimetro = "centímetro" if fraccion == 1 else "centímetros"
    return (
        f"{entero_a_letras(entero)} {metro} con "
        f"{entero_a_letras(fraccion)} {centimetro}"
    )


def frase_colindante(tipo: str, nombre: str) -> str:
    tipo_limpio = limpiar(tipo).upper()
    nombre_limpio = mayusculas(nombre)
    if tipo_limpio == "PROPIEDAD DE":
        return f"propiedad de {nombre_limpio}"
    if tipo_limpio in {"ARROYO", "RÍO", "BARRANCA", "CAMINO", "CARRETERA"}:
        return f"{tipo_limpio} {nombre_limpio}".strip()
    if tipo_limpio == "CALLE":
        return f"la calle {nombre_limpio}"
    if tipo_limpio == "OTRO":
        return nombre_limpio
    return f"{tipo_limpio} {nombre_limpio}".strip()


def redactar_tramos(tramos: list[dict[str, str]]) -> str:
    partes: list[str] = []
    for indice, tramo in enumerate(tramos):
        medida = limpiar(tramo.get("medida"))
        medida_letra = limpiar(tramo.get("medida_letra")) or medida_a_letras(medida)
        ordinal = ORDINALES[indice] if indice < len(ORDINALES) else f"número {indice + 1}"
        if len(tramos) == 1:
            partes.append(f"una línea de ({medida}) {medida_letra}")
        elif indice == 0:
            partes.append(f"una {ordinal} línea de ({medida}) {medida_letra}")
        else:
            partes.append(f"la {ordinal} línea de ({medida}) {medida_letra}")
    if not partes:
        return ""
    if len(partes) == 1:
        return partes[0]
    return ", ".join(partes[:-1]) + " y " + partes[-1]


def redactar_colindancias(grupos: list[dict[str, Any]]) -> str:
    por_cardinal: OrderedDict[str, list[dict[str, Any]]] = OrderedDict()
    for grupo in grupos:
        cardinal = mayusculas(grupo.get("cardinal"))
        if not cardinal:
            continue
        por_cardinal.setdefault(cardinal, []).append(grupo)

    bloques: list[str] = []
    for indice_cardinal, (cardinal, grupos_cardinal) in enumerate(por_cardinal.items()):
        prefijo = "- - - " if indice_cardinal == 0 else "- - - - - - - - - "
        frases_grupo: list[str] = []
        for grupo in grupos_cardinal:
            tramos = grupo.get("tramos") or []
            tramos_texto = redactar_tramos(tramos)
            lindero = frase_colindante(
                str(grupo.get("tipo_colindante", "PROPIEDAD DE")),
                str(grupo.get("colindante", "")),
            )
            verbo = "linda" if len(tramos) == 1 else "lindan"
            frases_grupo.append(f"Colinda en {tramos_texto}, {verbo} con {lindero}.")
        bloques.append(prefijo + f"AL {cardinal}: " + " ".join(frases_grupo))

    cierre = " - - - - - - - - - - - - - - - - - - - - - - - "
    return " ".join(bloques) + cierre


def redactar_persona(
    persona: dict[str, Any],
    fecha_instrumento: str,
    inciso: str,
) -> str:
    sexo = limpiar(persona.get("sexo")).upper()
    femenina = sexo == "FEMENINO"
    tratamiento = "La señora" if femenina else "El señor"
    originario = "originaria" if femenina else "originario"
    vecino = "vecina" if femenina else "vecino"
    estado_civil = limpiar(persona.get("estado_civil"))
    ocupacion = limpiar(persona.get("ocupacion"))
    origen = limpiar(persona.get("origen"))
    vecindad = limpiar(persona.get("vecindad"))
    if son_lugares_iguales(origen, vecindad):
        lugar = f"{originario} y {vecino} de {origen}"
    else:
        lugar = f"{originario} de {origen} y {vecino} de {vecindad}"

    nacimiento = limpiar(persona.get("fecha_nacimiento"))
    edad = calcular_edad(nacimiento, fecha_instrumento)
    edad_letra = entero_a_letras(edad)
    nombre = mayusculas(persona.get("nombre"))
    domicilio = limpiar(persona.get("domicilio"))
    cp = limpiar(persona.get("codigo_postal"))
    rfc = mayusculas(persona.get("rfc"))
    curp = mayusculas(persona.get("curp"))
    ine = limpiar(persona.get("ine"))
    nacionalidad = limpiar(persona.get("nacionalidad")) or "mexicana"
    sabe_firmar = bool(persona.get("sabe_firmar", True))
    firma = "declara saber firmar" if sabe_firmar else "declara no saber firmar"

    return (
        f"{inciso}).-\u00A0{tratamiento} {nombre}, {lugar}, con domicilio en {domicilio}, "
        f"Código Postal {cp}, con fecha de nacimiento el día "
        f"{fecha_nacimiento_notarial(nacimiento)}, de {edad} {edad_letra} años de edad, "
        f"{estado_civil}, de ocupación {ocupacion}, con Registro Federal de "
        f"Contribuyentes número “{rfc}”, con Clave Única de Registro de Población "
        f"número “{curp}”, de nacionalidad {nacionalidad}, misma que conserva y "
        f"{firma}; quien se identifica con Credencial para Votar con Fotografía "
        f"con número “{ine}”, expedida por el Instituto Nacional Electoral, de paso "
        f"por esta ciudad. - - - - - - - - - - - "
    )


def construir_datos_motor(formulario: dict[str, Any]) -> dict[str, str]:
    vendedor = formulario["vendedor"]
    comprador = formulario["comprador"]
    fecha_instrumento = formulario["fecha_instrumento"]
    sexo_vendedor = limpiar(vendedor.get("sexo")).upper()
    vendedora = sexo_vendedor == "FEMENINO"
    sexo_comprador = limpiar(comprador.get("sexo")).upper()
    compradora = sexo_comprador == "FEMENINO"
    tratamiento_vendedor = "la señora" if vendedora else "el señor"
    calidad_vendedor = "VENDEDORA" if vendedora else "VENDEDOR"
    tratamiento = "la señora" if compradora else "el señor"
    calidad = "COMPRADORA" if compradora else "COMPRADOR"

    descripcion = limpiar(formulario.get("descripcion_inmueble"))
    if not descripcion:
        descripcion = construir_descripcion_inmueble(formulario)

    antecedente = limpiar(formulario.get("antecedente_propiedad"))
    if not antecedente:
        antecedente = (
            f"Declara el señor {mayusculas(vendedor.get('nombre'))}, de manera expresa "
            "y bajo protesta de decir verdad, que adquirió en legítima propiedad el "
            "predio de referencia, mismo que contiene las siguientes. "
        )

    superficie = limpiar(formulario.get("superficie"))
    unidad = limpiar(formulario.get("unidad_superficie")) or "M2"
    superficie_letra = limpiar(formulario.get("superficie_letra"))
    if not superficie_letra:
        superficie_letra = numero_a_letras(superficie)
        if unidad.upper() in {"M2", "M²"}:
            superficie_letra += " METROS CUADRADOS"

    registro = limpiar(formulario.get("datos_registro"))
    avaluo = limpiar(formulario.get("avaluo"))
    avaluo_letra = limpiar(formulario.get("avaluo_letra")) or cantidad_a_letras(avaluo)
    precio = limpiar(formulario.get("precio"))
    precio_letra = limpiar(formulario.get("precio_letra")) or cantidad_a_letras(precio)

    predial = limpiar(formulario.get("declaracion_predial"))
    if not predial:
        predial = (
            "Finalmente declara la parte vendedora que el inmueble materia del "
            "presente contrato se encuentra inscrito a su nombre en el padrón de la "
            "propiedad raíz y que a la fecha no reporta adeudo por concepto de "
            "impuesto predial, lo que acreditará con la documentación correspondiente. "
        )

    fecha_final = fecha_notarial(fecha_instrumento, incluir_ano_literal=True)
    colindancias = redactar_colindancias(formulario.get("colindancias") or [])

    return {
        "LIBRO_NUMERO": limpiar(formulario.get("libro_numero")),
        "LIBRO_LETRA": mayusculas(formulario.get("libro_letra")),
        "ESCRITURA_NUMERO": limpiar(formulario.get("escritura_numero")),
        "ESCRITURA_LETRA": mayusculas(formulario.get("escritura_letra")),
        "FECHA_INSTRUMENTO": fecha_notarial(fecha_instrumento),
        "VENDEDOR_NOMBRE": mayusculas(vendedor.get("nombre")),
        "VENDEDOR_TRATAMIENTO": tratamiento_vendedor,
        "VENDEDOR_CALIDAD": calidad_vendedor,
        "COMPRADOR_NOMBRE": mayusculas(comprador.get("nombre")),
        "COMPRADOR_TRATAMIENTO": tratamiento,
        "COMPRADOR_CALIDAD": calidad,
        "DESCRIPCION_INMUEBLE": descripcion,
        "ANTECEDENTE_PROPIEDAD": antecedente + (" " if not antecedente.endswith(" ") else ""),
        "MEDIDAS_COLINDANCIAS": colindancias,
        "SUPERFICIE_TEXTO": (
            f"Con una superficie aproximada de: {superficie} {unidad}. "
            f"({superficie_letra}). - - - - - - - - - - - - - - - - - - - - - - - "
        ),
        "DATOS_REGISTRO": registro + " - - - - - - - - - - - - - - - - - - ",
        "AVALUO_TEXTO": (
            f"${avaluo} ({avaluo_letra} pesos 00/100 moneda nacional). "
            "- - - - - - - - - - - - "
        ),
        "DECLARACION_PREDIAL": predial + " - - - - - - - - - - - - - - - - - - - - - - - ",
        "PRECIO_TEXTO": f"${precio} ({precio_letra} pesos 00/100 moneda nacional)",
        "DATOS_PERSONALES_VENDEDOR": redactar_persona(vendedor, fecha_instrumento, "a"),
        "DATOS_PERSONALES_COMPRADORA": redactar_persona(comprador, fecha_instrumento, "b"),
        "FECHA_AUTORIZACION": fecha_final,
        "FECHA_TESTIMONIO": fecha_final,
        "BENEFICIARIO_TESTIMONIO": mayusculas(
            formulario.get("beneficiario_testimonio") or comprador.get("nombre")
        ),
    }
