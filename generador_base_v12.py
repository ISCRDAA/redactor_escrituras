from __future__ import annotations

import sys
from datetime import datetime
from pathlib import Path

try:
    import win32com.client  # type: ignore
except ImportError as exc:
    raise SystemExit(
        "Falta pywin32. Ejecuta: python -m pip install -r requirements.txt"
    ) from exc

BASE_DIR = Path(__file__).resolve().parent
MATRIZ = BASE_DIR / "MATRIZ_ORIGINAL.docx"
SALIDA = BASE_DIR / "PRUEBA_GENERADA_WORD_V12.docx"
REGISTRO = BASE_DIR / "registro_v12.txt"

WD_FIND_STOP = 0
WD_SAVE_CHANGES = -1
WD_DO_NOT_SAVE_CHANGES = 0
WD_FORMAT_DOCUMENT_DEFAULT = 16
WD_STATISTIC_PAGES = 2
WD_PAGE_BREAK = 7

DATOS = {
    "LIBRO_NUMERO": "500",
    "LIBRO_LETRA": "QUINIENTOS",
    "ESCRITURA_NUMERO": "19,900",
    "ESCRITURA_LETRA": "DIECINUEVE MIL NOVECIENTOS",
    "VENDEDOR_NOMBRE": "ÁNGEL ALONSO RODRÍGUEZ DOMÍNGUEZ",
    "COMPRADOR_NOMBRE": "MARIAN GARCÍA CANALES",
    "COMPRADOR_TRATAMIENTO": "la señora",
    "COMPRADOR_CALIDAD": "COMPRADORA",
    "DESCRIPCION_INMUEBLE": (
        "DEL PREDIO RÚSTICO DENOMINADO “ACOCUL”, UBICADO EN MIRADOR, "
        "MUNICIPIO DE AGUA BLANCA DE ITURBIDE, ESTADO DE HIDALGO, "
        "QUE EN LO SUCESIVO SE DENOMINARÁ “SAN MATEO”"
    ),
    "ANTECEDENTE_PROPIEDAD": (
        "Declara el señor ÁNGEL ALONSO RODRÍGUEZ DOMÍNGUEZ, de manera "
        "expresa y bajo protesta de decir verdad, que por instrumento notarial "
        "número 8,071 ocho mil setenta y uno, libro 154 ciento cincuenta y "
        "cuatro, de fecha 03 tres de enero de 2022 dos mil veintidós, pasado "
        "ante la fe del Licenciado ALDO AMAURY VILLEGAS GARCÍA, Notario "
        "Titular de la Notaría Número 10 diez del Distrito Judicial de "
        "Tulancingo de Bravo, Hidalgo, adquirió en legítima propiedad el "
        "predio de referencia, mismo que contiene las siguientes. "
    ),
    "MEDIDAS_COLINDANCIAS": (
        "- - - AL NORTE: Colinda en una primera línea de (20.00) veinte metros "
        "con cero centímetros y la segunda línea de (12.10) doce metros con "
        "diez centímetros, lindan con propiedad de HUGO SÁNCHEZ BORBOJA. "
        "- - - - - - - - - AL SUR: Colinda en una línea de (11.12) once "
        "metros con doce centímetros, linda con propiedad de LUIS DE LA "
        "MADRID TORRES. - - - - - - - - - AL OESTE: Colinda en una línea "
        "de (20.00) veinte metros con cero centímetros, linda con propiedad "
        "de LUCA MENDIOLA LAGOS. - - - - - - - - - AL NOROESTE: Colinda "
        "en una primera línea de (9.80) nueve metros con ochenta centímetros "
        "y la segunda línea de (11.12) once metros con doce centímetros, "
        "lindan con propiedad de LUIS ALBERTO DE LA CRUZ GÓMEZ. "
        "- - - - - - - - - - - - - - - - - - - - - - - "
    ),
    "SUPERFICIE_TEXTO": (
        "Con una superficie aproximada de: 10,000 M2. "
        "(DIEZ MIL METROS CUADRADOS). "
        "- - - - - - - - - - - - - - - - - - - - - - - "
    ),
    "DATOS_REGISTRO": (
        "Dicha propiedad se encuentra inscrita ante el Registro Público de la "
        "Propiedad y del Comercio de Tulancingo de Bravo, Estado de Hidalgo, "
        "bajo Folio Real número 135627 ciento treinta y cinco mil seiscientos "
        "veintisiete, de fecha 29 veintinueve de marzo de 2022 dos mil veintidós. "
        "- - - - - - - - - - - - - - - - - - "
    ),
    "AVALUO_TEXTO": (
        "$50,000.00 (cincuenta mil pesos 00/100 moneda nacional). "
        "- - - - - - - - - - - - "
    ),
    "DECLARACION_PREDIAL": (
        "Finalmente declara la parte vendedora que el inmueble materia del "
        "presente contrato se encuentra inscrito a su nombre en el padrón de la "
        "propiedad raíz del Municipio de Agua Blanca de Iturbide, Estado de "
        "Hidalgo, y que a la fecha no reporta adeudo por concepto de impuesto "
        "predial, lo que acreditará con la documentación correspondiente. "
        "- - - - - - - - - - - - - - - - - - - - - - - "
    ),
    "PRECIO_TEXTO": (
        "$25,000.00 (veinticinco mil pesos 00/100 moneda nacional)"
    ),
    "DATOS_PERSONALES_VENDEDOR": (
        "a).-\u00A0El señor ÁNGEL ALONSO RODRÍGUEZ DOMÍNGUEZ, originario y "
        "vecino de Tulancingo de Bravo, Estado de Hidalgo, con domicilio en "
        "Doria Oriente 105, Código Postal 43600, con fecha de nacimiento el "
        "día 23 veintitrés de diciembre de 1998 mil novecientos noventa y ocho, "
        "de 27 veintisiete años de edad, soltero, de ocupación estudiante, con "
        "Registro Federal de Contribuyentes número “ASDECVFRT123”, con Clave "
        "Única de Registro de Población número “ASDCVFRMONO1234567”, de "
        "nacionalidad mexicana, misma que conserva y declara saber firmar; quien "
        "se identifica con Credencial para Votar con Fotografía con número "
        "“123456789000”, expedida por el Instituto Nacional Electoral, de paso "
        "por esta ciudad. - - - - - - - - - - - "
    ),
    "DATOS_PERSONALES_COMPRADORA": (
        "b).-\u00A0La señora MARIAN GARCÍA CANALES, originaria y vecina de "
        "Tulancingo de Bravo, Estado de Hidalgo, con domicilio en Corregidora "
        "205, Código Postal 43560, con fecha de nacimiento el día 24 veinticuatro "
        "de enero de 1996 mil novecientos noventa y seis, de 30 treinta años de "
        "edad, soltera, de ocupación estudiante, con Registro Federal de "
        "Contribuyentes número “QWERTYUIOP12”, con Clave Única de Registro "
        "de Población número “ASWDERFGTBN1234ER5”, de nacionalidad mexicana, "
        "misma que conserva y declara saber firmar; quien se identifica con "
        "Credencial para Votar con Fotografía con número “1234567890999”, "
        "expedida por el Instituto Nacional Electoral, de paso por esta ciudad. "
        "- - - - - - - - - - - "
    ),
    "FECHA_AUTORIZACION": "27 veintisiete días del mes de marzo del año 2026 dos mil veintiséis",
    "FECHA_TESTIMONIO": "27 veintisiete días del mes de marzo del año 2026 dos mil veintiséis",
    "BENEFICIARIO_TESTIMONIO": "MARIAN GARCÍA CANALES",
}


def log(mensaje: str) -> None:
    linea = f"[{datetime.now():%H:%M:%S}] {mensaje}"
    print(linea)
    with REGISTRO.open("a", encoding="utf-8") as archivo:
        archivo.write(linea + "\n")


def configurar_find(
    rango,
    texto: str,
    *,
    distinguir_mayusculas: bool = False,
    palabra_completa: bool = False,
) -> None:
    finder = rango.Find
    finder.ClearFormatting()
    finder.Replacement.ClearFormatting()
    finder.Text = texto
    finder.Forward = True
    finder.Wrap = WD_FIND_STOP
    finder.MatchCase = distinguir_mayusculas
    finder.MatchWholeWord = palabra_completa
    finder.MatchWildcards = False
    finder.Format = False


def buscar_rango(
    documento,
    texto: str,
    inicio: int = 0,
    fin: int | None = None,
    *,
    distinguir_mayusculas: bool = False,
    palabra_completa: bool = False,
):
    limite = documento.Content.End if fin is None else min(fin, documento.Content.End)
    if inicio >= limite:
        raise RuntimeError(f"Rango inválido al buscar: {texto!r}")
    rango = documento.Range(Start=inicio, End=limite)
    configurar_find(
        rango,
        texto,
        distinguir_mayusculas=distinguir_mayusculas,
        palabra_completa=palabra_completa,
    )
    if not rango.Find.Execute():
        raise RuntimeError(f"No se encontró el texto de anclaje: {texto!r}")
    return rango.Duplicate


def buscar_cualquiera(
    documento,
    textos: tuple[str, ...],
    inicio: int = 0,
    fin: int | None = None,
):
    for texto in textos:
        try:
            return buscar_rango(documento, texto, inicio, fin)
        except RuntimeError:
            continue
    raise RuntimeError(f"No se encontró ningún anclaje alternativo: {list(textos)}")


def reemplazar_primera(
    documento,
    anterior: str,
    nuevo: str,
    inicio: int = 0,
    fin: int | None = None,
    *,
    requerido: bool = True,
    distinguir_mayusculas: bool = False,
    palabra_completa: bool = False,
) -> bool:
    try:
        rango = buscar_rango(
            documento,
            anterior,
            inicio,
            fin,
            distinguir_mayusculas=distinguir_mayusculas,
            palabra_completa=palabra_completa,
        )
    except RuntimeError:
        if requerido:
            raise
        log(f"OMITIDO (no existe): {anterior!r}")
        return False
    rango.Text = nuevo
    log(f"OK primera: {anterior!r} -> {nuevo!r}")
    return True


def reemplazar_todas(
    documento,
    anterior: str,
    nuevo: str,
    *,
    requerido: bool = True,
    distinguir_mayusculas: bool = False,
    palabra_completa: bool = False,
) -> int:
    cantidad = 0
    posicion = 0
    while posicion < documento.Content.End:
        try:
            rango = buscar_rango(
                documento,
                anterior,
                posicion,
                distinguir_mayusculas=distinguir_mayusculas,
                palabra_completa=palabra_completa,
            )
        except RuntimeError:
            break
        inicio = rango.Start
        rango.Text = nuevo
        cantidad += 1
        posicion = inicio + len(nuevo)
    if cantidad == 0 and requerido:
        raise RuntimeError(f"No se encontró ninguna aparición de: {anterior!r}")
    if cantidad:
        log(f"OK todas: {cantidad} reemplazos de {anterior!r}")
    else:
        log(f"OMITIDO (no existe): {anterior!r}")
    return cantidad


def aplicar_formato_titulo(documento, texto_titulo: str, inicio: int = 0) -> None:
    rango = buscar_rango(documento, texto_titulo, inicio)
    rango.Font.Bold = True
    rango.Font.Italic = True
    rango.Font.Spacing = 1.2
    log(f"OK formato de título: {texto_titulo!r}")


def comprobar(documento, texto: str) -> None:
    buscar_rango(documento, texto)
    log(f"VERIFICADO: {texto[:70]!r}")


def convertir_paginas_a_letra(numero: int) -> str:
    letras = {
        1: "una", 2: "dos", 3: "tres", 4: "cuatro", 5: "cinco",
        6: "seis", 7: "siete", 8: "ocho", 9: "nueve", 10: "diez",
        11: "once", 12: "doce", 13: "trece", 14: "catorce",
        15: "quince", 16: "dieciséis", 17: "diecisiete",
        18: "dieciocho", 19: "diecinueve", 20: "veinte",
    }
    return letras.get(numero, str(numero))


def proteger_titulo(documento, texto: str) -> None:
    """
    Conserva el texto original del título y solo reafirma su formato.

    Las versiones anteriores reemplazaban los espacios por espacios de no
    separación. Eso ensanchaba algunos títulos y podía dejar expresiones como
    CERTIFICACIÓN o AUTORIZO partidas o pegadas a los guiones. En V11 no se
    reescribe el título: se mantiene exactamente como viene en la matriz.
    """
    try:
        rango = buscar_rango(
            documento,
            texto,
            distinguir_mayusculas=True,
        )
    except RuntimeError:
        log(f"OMITIDO título no localizado: {texto!r}")
        return

    rango.Font.Bold = True
    rango.Font.Italic = True
    log(f"OK título conservado sin reescritura: {texto!r}")

def corregir_ortografia_basica(documento) -> None:
    # MatchWholeWord evita convertir "notarial" en "notaríal" o
    # "Notariado" en "Notaríado".
    cambios = (
        ("Notaria", "Notaría", True),
        ("notaria", "notaría", True),
        ("articulo", "artículo", True),
        ("Articulo", "Artículo", True),
        ("numero", "número", True),
        ("avaluó", "avalúo", True),
        ("AVALUÓ", "AVALÚO", True),
        ("licito", "lícito", True),
        ("Trasparencia", "Transparencia", True),
        ("evitara", "evitará", True),
        ("Rubrica", "Rúbrica", True),
    )
    for anterior, nuevo, palabra_completa in cambios:
        reemplazar_todas(
            documento,
            anterior,
            nuevo,
            requerido=False,
            distinguir_mayusculas=True,
            palabra_completa=palabra_completa,
        )

    # Limpieza defensiva por si el archivo fue generado previamente con V7.
    for anterior, nuevo in (
        ("notaríal", "notarial"),
        ("Notaríal", "Notarial"),
        ("Notaríado", "Notariado"),
        ("notaríado", "notariado"),
    ):
        reemplazar_todas(
            documento,
            anterior,
            nuevo,
            requerido=False,
            distinguir_mayusculas=True,
        )



def insertar_firmas_comparecientes(documento) -> None:
    """Inserta los nombres en el último espacio vacío anterior a "Ante mí"."""
    ante = buscar_cualquiera(documento, ("Ante mi.-", "Ante mí.-"))
    parrafo_ante = ante.Paragraphs(1).Range
    posicion = parrafo_ante.Start

    texto_firmas = (
        DATOS["VENDEDOR_NOMBRE"]
        + "\t"
        + DATOS["COMPRADOR_NOMBRE"]
        + "\r"
    )
    insercion = documento.Range(Start=posicion, End=posicion)
    insercion.Text = texto_firmas

    rango_firma = documento.Range(
        Start=posicion,
        End=posicion + len(texto_firmas) - 1,
    )
    rango_firma.Font.Name = "Arial"
    rango_firma.Font.Size = 10
    rango_firma.Font.Bold = True
    rango_firma.ParagraphFormat.Alignment = 0  # wdAlignParagraphLeft
    rango_firma.ParagraphFormat.SpaceBefore = 0
    rango_firma.ParagraphFormat.SpaceAfter = 0
    rango_firma.ParagraphFormat.TabStops.ClearAll()
    # Ancho útil aproximado de la hoja notarial: 390 puntos.
    rango_firma.ParagraphFormat.TabStops.Add(390, 2, 0)
    log("OK bloque: firmas de vendedor y compradora")

def posicionar_bloque_ante_mi(documento) -> None:
    """
    Reproduce la zona de firmas del formato oficial:

    1. El bloque ``- - - Ante mí`` comienza en una página nueva.
    2. Se insertan 28 renglones vacíos antes del bloque para reservar el
       espacio material de firmas y rúbricas.
    3. El primer testimonio ya no recibe un salto forzado; fluye después
       de los anexos, como en la matriz de la notaría.
    """
    ante = buscar_cualquiera(documento, ("Ante mi.-", "Ante mí.-"))
    inicio_busqueda = max(0, ante.Start - 80)
    previo = documento.Range(Start=inicio_busqueda, End=ante.Start)
    texto_previo = previo.Text
    desplazamiento = texto_previo.rfind("- - -")
    posicion = (
        inicio_busqueda + desplazamiento
        if desplazamiento >= 0
        else ante.Paragraphs(1).Range.Start
    )

    punto = documento.Range(Start=posicion, End=posicion)
    punto.InsertBreak(WD_PAGE_BREAK)

    # Las 28 líneas vacías son deliberadas: la matriz oficial utiliza esa
    # reserva vertical para firmas. Se insertan DESPUÉS del salto de página
    # y ANTES del texto ``- - - Ante mí``.
    ante = buscar_cualquiera(documento, ("Ante mi.-", "Ante mí.-"))
    espacio = documento.Range(Start=ante.Start, End=ante.Start)
    espacio.Text = "\r" * 28
    log("OK distribución: página de firmas y bloque - - - Ante mí")

def preparar_salida() -> None:
    if not MATRIZ.exists():
        raise RuntimeError(f"No existe la matriz: {MATRIZ}")
    if SALIDA.exists():
        try:
            SALIDA.unlink()
        except PermissionError as exc:
            raise RuntimeError(
                "No se puede reemplazar PRUEBA_GENERADA_WORD_V12.docx. "
                "Ciérralo en Microsoft Word y vuelve a ejecutar."
            ) from exc


def main() -> None:
    REGISTRO.write_text("", encoding="utf-8")
    preparar_salida()

    word = win32com.client.DispatchEx("Word.Application")
    word.Visible = True
    word.DisplayAlerts = 0
    documento = None
    exito = False

    try:
        log("Abriendo matriz original en modo solo lectura.")
        documento = word.Documents.Open(
            str(MATRIZ),
            ReadOnly=True,
            AddToRecentFiles=False,
        )
        log("Creando copia de trabajo V12.")
        documento.SaveAs2(
            str(SALIDA),
            FileFormat=WD_FORMAT_DOCUMENT_DEFAULT,
            AddToRecentFiles=False,
        )

        limite_encabezado = min(documento.Content.End, 2500)
        reemplazar_primera(documento, "376", DATOS["LIBRO_NUMERO"], 0, limite_encabezado)
        reemplazar_primera(
            documento,
            "TRESCIENTOS SETENTA Y SEIS",
            DATOS["LIBRO_LETRA"],
            0,
            limite_encabezado,
        )
        reemplazar_primera(documento, "19,726", DATOS["ESCRITURA_NUMERO"], 0, limite_encabezado)
        reemplazar_primera(
            documento,
            "DIECINUEVE MIL SETECIENTOS VEINTISEIS",
            DATOS["ESCRITURA_LETRA"],
            0,
            limite_encabezado,
        )
        reemplazar_primera(
            documento,
            "27 veintisiete días del mes de marzo de 2026 dos mil veintiséis",
            DATOS["FECHA_INSTRUMENTO"],
            0,
            limite_encabezado,
            requerido=False,
        )

        reemplazar_todas(documento, "JOSE ESTEFES PEREZ", DATOS["VENDEDOR_NOMBRE"])
        reemplazar_todas(documento, "JUAN CARLOS LOPEZ ZAVALA", DATOS["COMPRADOR_NOMBRE"])

        reemplazar_todas(
            documento,
            f"el señor {DATOS['VENDEDOR_NOMBRE']}",
            f"{DATOS['VENDEDOR_TRATAMIENTO']} {DATOS['VENDEDOR_NOMBRE']}",
            requerido=False,
        )
        reemplazar_primera(
            documento,
            "como “VENDEDOR”",
            f"como “{DATOS['VENDEDOR_CALIDAD']}”",
            0,
            limite_encabezado,
            requerido=False,
        )

        # MatchCase=False ya cubre "el señor" y "El Señor" en una sola pasada.
        reemplazar_todas(
            documento,
            f"el señor {DATOS['COMPRADOR_NOMBRE']}",
            f"{DATOS['COMPRADOR_TRATAMIENTO']} {DATOS['COMPRADOR_NOMBRE']}",
            requerido=False,
        )
        reemplazar_primera(
            documento,
            "como “COMPRADOR”",
            f"como “{DATOS['COMPRADOR_CALIDAD']}”",
            0,
            limite_encabezado,
        )

        descripcion_inicio = buscar_rango(documento, "DEL PREDIO RÚSTICO DENOMINADO")
        descripcion_fin = buscar_rango(
            documento,
            ", y cuyo contrato vienen a formalizar",
            descripcion_inicio.End,
        )
        documento.Range(
            Start=descripcion_inicio.Start,
            End=descripcion_fin.Start,
        ).Text = DATOS["DESCRIPCION_INMUEBLE"]
        log("OK bloque: descripción inicial del inmueble")

        antecedente_inicio = buscar_cualquiera(
            documento,
            ("Declara el señor", "Declara la señora", "Declara el ciudadano"),
        )
        medidas_intro = buscar_rango(
            documento,
            "El predio antes mencionado",
            antecedente_inicio.End,
        )
        nuevo_antecedente = (
            DATOS["ANTECEDENTE_PROPIEDAD"]
            + "- - - - - - - - - - - - - - - - - - - - - - - "
            + "M E D I D A S Y C O L I N D A N C I A S . - "
        )
        documento.Range(
            Start=antecedente_inicio.Start,
            End=medidas_intro.Start,
        ).Text = nuevo_antecedente
        aplicar_formato_titulo(
            documento,
            "M E D I D A S Y C O L I N D A N C I A S",
            antecedente_inicio.Start,
        )
        log("OK bloque: antecedente de propiedad")

        medidas_intro = buscar_rango(
            documento,
            "El predio antes mencionado",
            antecedente_inicio.Start,
        )
        inicio_medidas = buscar_rango(documento, "AL NORTE:", medidas_intro.End)
        fin_medidas = buscar_rango(
            documento,
            "Con una superficie aproximada de:",
            inicio_medidas.End,
        )
        documento.Range(
            Start=inicio_medidas.Start,
            End=fin_medidas.Start,
        ).Text = DATOS["MEDIDAS_COLINDANCIAS"]
        log("OK bloque: medidas y colindancias")

        # Superficie: se reemplaza el bloque completo hasta el título de registro.
        superficie_inicio = buscar_rango(
            documento,
            "Con una superficie aproximada de:",
            medidas_intro.End,
        )
        titulo_registro = buscar_rango(
            documento,
            "DATOS DE REGISTRO",
            superficie_inicio.End,
        )
        documento.Range(
            Start=superficie_inicio.Start,
            End=titulo_registro.Start,
        ).Text = DATOS["SUPERFICIE_TEXTO"]
        log("OK bloque: superficie")

        # Datos registrales: el título se conserva y solo se sustituye el cuerpo.
        cuerpo_registro = buscar_rango(
            documento,
            "Dicha propiedad se encuentra inscrita",
            titulo_registro.End,
        )
        certificado_inicio = buscar_rango(
            documento,
            "CERTIFICADO DE LIBERTAD DE GRAVAMEN",
            cuerpo_registro.End,
        )
        try:
            numeral_certificado = buscar_rango(
                documento,
                "II.-",
                cuerpo_registro.End,
                certificado_inicio.Start,
                distinguir_mayusculas=True,
            )
            fin_registro = numeral_certificado.Start
        except RuntimeError:
            fin_registro = certificado_inicio.Start
            DATOS["DATOS_REGISTRO"] += "II.- "
        documento.Range(
            Start=cuerpo_registro.Start,
            End=fin_registro,
        ).Text = DATOS["DATOS_REGISTRO"]
        log("OK bloque: datos registrales y conservación de II.-")

        # Avalúo: solo se sustituye la cantidad y su expresión en letra.
        ancla_avaluo = buscar_rango(
            documento,
            "mediante el cual se le asignó un valor de",
        )
        agrega_avaluo = buscar_rango(
            documento,
            "Agrego al apéndice del presente instrumento marcado con la letra “B”",
            ancla_avaluo.End,
        )
        documento.Range(
            Start=ancla_avaluo.End,
            End=agrega_avaluo.Start,
        ).Text = " " + DATOS["AVALUO_TEXTO"]
        log("OK bloque: valor del avalúo")

        # Declaración predial completa.
        predial_inicio = buscar_rango(documento, "c.- Impuesto predial")
        adquisicion_inicio = buscar_rango(
            documento,
            "d.- Impuesto sobre adquisición de inmuebles",
            predial_inicio.End,
        )
        encabezado_predial_fin = buscar_rango(
            documento,
            "Finalmente declara la parte vendedora",
            predial_inicio.End,
            adquisicion_inicio.Start,
        )
        documento.Range(
            Start=encabezado_predial_fin.Start,
            End=adquisicion_inicio.Start,
        ).Text = DATOS["DECLARACION_PREDIAL"]
        log("OK bloque: declaración predial")

        # En el XML de la matriz el título está guardado como "PRIMERA"
        # aunque visualmente Word lo muestre con espaciado entre letras.
        # Usamos la frase anterior como ancla estable y buscamos la segunda
        # descripción del inmueble después de iniciar las cláusulas.
        inicio_clausulas = buscar_cualquiera(
            documento,
            ("las siguientes cláusulas.", "las siguientes clausulas."),
        )
        descripcion_clausula = buscar_rango(
            documento,
            "DEL PREDIO RÚSTICO DENOMINADO",
            inicio_clausulas.End,
        )
        fin_descripcion_clausula = buscar_cualquiera(
            documento,
            (", escrito y deslindado", ", escrito y delimitado"),
            descripcion_clausula.End,
        )
        documento.Range(
            Start=descripcion_clausula.Start,
            End=fin_descripcion_clausula.Start,
        ).Text = DATOS["DESCRIPCION_INMUEBLE"]
        log("OK bloque: descripción repetida en PRIMERA")

        declaracion_adquisicion = buscar_rango(
            documento,
            "no ha adquirido en un periodo de 24",
        )
        comienzo_frase = buscar_cualquiera(
            documento,
            ("Declara el Señor", "Declara el señor", "Declara la señora"),
            max(0, declaracion_adquisicion.Start - 300),
            declaracion_adquisicion.Start,
        )
        documento.Range(
            Start=comienzo_frase.Start,
            End=declaracion_adquisicion.Start,
        ).Text = (
            f"Declara {DATOS['COMPRADOR_TRATAMIENTO']} "
            f"{DATOS['COMPRADOR_NOMBRE']}, que "
        )
        log("OK bloque: adquirente en declaración fiscal")

        # Precio de la operación dentro de la cláusula SEGUNDA.
        precio_ancla = buscar_rango(documento, "es la cantidad de $")
        precio_fin = buscar_rango(
            documento,
            ", misma que la parte compradora",
            precio_ancla.End,
        )
        documento.Range(
            Start=precio_ancla.End - 1,
            End=precio_fin.Start,
        ).Text = DATOS["PRECIO_TEXTO"]
        log("OK bloque: precio de la operación")

        # Numeración correcta del apartado fiscal.
        reemplazar_primera(
            documento,
            "V- DECLARACIONES PARA EFECTOS FISCALES",
            "IV.- DECLARACIONES PARA EFECTOS FISCALES",
            requerido=False,
            distinguir_mayusculas=True,
        )
        reemplazar_primera(
            documento,
            "V.- DECLARACIONES PARA EFECTOS FISCALES",
            "IV.- DECLARACIONES PARA EFECTOS FISCALES",
            requerido=False,
            distinguir_mayusculas=True,
        )

        # Mayúscula inicial en cláusulas que comienzan con la adquirente.
        for ancla in ("TERCERA", "DECIMA", "DÉCIMA"):
            try:
                titulo = buscar_rango(documento, ancla)
                reemplazar_primera(
                    documento,
                    f"la señora {DATOS['COMPRADOR_NOMBRE']}",
                    f"La señora {DATOS['COMPRADOR_NOMBRE']}",
                    inicio=titulo.End,
                    requerido=False,
                    distinguir_mayusculas=True,
                )
            except RuntimeError:
                pass

        # Concordancia femenina en la cláusula DÉCIMA.
        reemplazar_primera(
            documento,
            "dándose por recibido la totalidad",
            "dándose por recibida de la totalidad",
            requerido=False,
        )

        # Correcciones quirúrgicas de V9.
        for variante in (
            "IIV.- DECLARACIONES PARA EFECTOS FISCALES",
            "IIV.-DECLARACIONES PARA EFECTOS FISCALES",
            "IVV.- DECLARACIONES PARA EFECTOS FISCALES",
        ):
            reemplazar_todas(
                documento,
                variante,
                "IV.- DECLARACIONES PARA EFECTOS FISCALES",
                requerido=False,
                distinguir_mayusculas=True,
            )

        reemplazar_todas(
            documento,
            f"y La señora {DATOS['COMPRADOR_NOMBRE']}",
            f"y la señora {DATOS['COMPRADOR_NOMBRE']}",
            requerido=False,
            distinguir_mayusculas=True,
        )
        reemplazar_todas(
            documento,
            f"la señora {DATOS['COMPRADOR_NOMBRE']}, manifiesta y garantiza",
            f"La señora {DATOS['COMPRADOR_NOMBRE']}, manifiesta y garantiza",
            requerido=False,
            distinguir_mayusculas=True,
        )
        reemplazar_todas(
            documento,
            f"la señora {DATOS['COMPRADOR_NOMBRE']}, que acepta",
            f"La señora {DATOS['COMPRADOR_NOMBRE']}, que acepta",
            requerido=False,
            distinguir_mayusculas=True,
        )

        # Datos personales completos de ambas partes.
        datos_vendedor_inicio = buscar_rango(documento, "a).-")
        datos_compradora_inicio = buscar_rango(
            documento,
            "b).-",
            datos_vendedor_inicio.End,
        )
        garantia_inicio = buscar_rango(
            documento,
            "GARANTÍA DE SECRECÍA",
            datos_compradora_inicio.End,
        )
        documento.Range(
            Start=datos_vendedor_inicio.Start,
            End=datos_compradora_inicio.Start,
        ).Text = DATOS["DATOS_PERSONALES_VENDEDOR"]
        # Volvemos a localizar el inicio de b).- porque el primer reemplazo movió posiciones.
        datos_compradora_inicio = buscar_rango(
            documento,
            "b).-",
            datos_vendedor_inicio.Start,
        )
        garantia_inicio = buscar_rango(
            documento,
            "GARANTÍA DE SECRECÍA",
            datos_compradora_inicio.End,
        )
        documento.Range(
            Start=datos_compradora_inicio.Start,
            End=garantia_inicio.Start,
        ).Text = DATOS["DATOS_PERSONALES_COMPRADORA"]
        log("OK bloques: datos personales")

        # Beneficiario del primer testimonio.
        testimonio_inicio = buscar_rango(
            documento,
            "se expide a favor de:",
        )
        ciudad_testimonio = buscar_rango(
            documento,
            "En la Ciudad de Tezontepec de Aldama",
            testimonio_inicio.End,
        )
        documento.Range(
            Start=testimonio_inicio.End,
            End=ciudad_testimonio.Start,
        ).Text = (
            " - - - - - - - - - - - - - - - - - - - - - - - "
            + DATOS["BENEFICIARIO_TESTIMONIO"]
            + " - - - - - - - - - - - - - - - "
        )
        log("OK bloque: beneficiario del primer testimonio")

        insertar_firmas_comparecientes(documento)
        posicionar_bloque_ante_mi(documento)

        # Fechas finales consistentes con el instrumento.
        autorizo_inicio = buscar_cualquiera(documento, ("A u t o r i z o.-", "Autorizo.-"))
        documentos_apendice = buscar_rango(documento, "DOCUMENTOS DEL APÉNDICE", autorizo_inicio.End)
        fecha_autorizo_inicio = buscar_rango(
            documento,
            "a los 12 doce días del mes de septiembre del año 2024 dos mil veinticuatro",
            autorizo_inicio.End,
            documentos_apendice.Start,
        )
        fecha_autorizo_inicio.Text = f"a los {DATOS['FECHA_AUTORIZACION']}"
        log("OK bloque: fecha de autorización")

        testimonio_inicio_fecha = buscar_rango(
            documento,
            "a los 12 doce días del mes de Septiembre del año 2024 dos mil veinticuatro",
            documentos_apendice.End,
        )
        testimonio_inicio_fecha.Text = f"a los {DATOS['FECHA_TESTIMONIO']}"
        log("OK bloque: fecha del primer testimonio")

        corregir_ortografia_basica(documento)

        # La matriz almacena los títulos sin espacios entre cada letra;
        # el espaciado visual pertenece al formato de fuente.
        for titulo_texto in (
            "ANTECEDENTE",
            "MEDIDAS Y COLINDANCIAS",
            "DATOS DE REGISTRO",
            "PRIMERA", "SEGUNDA", "TERCERA",
            "CUARTA", "QUINTA", "SEXTA",
            "SEPTIMA", "SÉPTIMA", "OCTAVA", "NOVENA",
            "DECIMA", "DÉCIMA", "DATOS PERSONALES",
            "GARANTÍA DE SECRECÍA",
            "CERTIFICACIÓN",
            "DOCUMENTOS DEL APÉNDICE",
        ):
            proteger_titulo(documento, titulo_texto)

        for texto in (
            "8,071 ocho mil setenta y uno",
            "HUGO SÁNCHEZ BORBOJA",
            "LUIS ALBERTO DE LA CRUZ GÓMEZ",
            "SAN MATEO",
            f"{DATOS['COMPRADOR_TRATAMIENTO']} {DATOS['COMPRADOR_NOMBRE']}",
            "IV.- DECLARACIONES PARA EFECTOS FISCALES",
        ):
            comprobar(documento, texto)

        log("Actualizando paginación y campos de Word.")
        documento.Repaginate()
        documento.Fields.Update()

        paginas = int(documento.ComputeStatistics(WD_STATISTIC_PAGES))
        texto_paginas = convertir_paginas_a_letra(paginas)
        reemplazar_primera(
            documento,
            "va en 7 siete hojas útiles",
            f"va en {paginas} {texto_paginas} hojas útiles",
            requerido=False,
            distinguir_mayusculas=False,
        )
        documento.Repaginate()
        paginas_finales = int(documento.ComputeStatistics(WD_STATISTIC_PAGES))
        if paginas_finales != paginas:
            reemplazar_primera(
                documento,
                f"va en {paginas} {texto_paginas} hojas útiles",
                f"va en {paginas_finales} {convertir_paginas_a_letra(paginas_finales)} hojas útiles",
                requerido=False,
            )
            documento.Repaginate()
        documento.Fields.Update()
        documento.Save()
        exito = True
        log(f"Documento generado correctamente: {SALIDA}")
    except Exception as exc:
        log(f"ERROR: {type(exc).__name__}: {exc}")
        raise
    finally:
        if documento is not None:
            documento.Close(
                SaveChanges=WD_SAVE_CHANGES if exito else WD_DO_NOT_SAVE_CHANGES
            )
        word.Quit()
        if not exito and SALIDA.exists():
            try:
                SALIDA.unlink()
            except PermissionError:
                log(
                    "AVISO: Word mantuvo bloqueada la copia fallida. "
                    "Ciérralo y elimina PRUEBA_GENERADA_WORD_V12.docx manualmente."
                )


if __name__ == "__main__":
    try:
        main()
    except Exception as exc:
        print(f"\nERROR FINAL: {exc}", file=sys.stderr)
        print(
            "No se guardó ningún documento parcial. "
            "Revisa registro_v12.txt para conocer el paso exacto.",
            file=sys.stderr,
        )
        sys.exit(1)
