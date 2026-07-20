from __future__ import annotations

from pathlib import Path
from typing import Any

from configuracion_actos import nombres_actos, obtener_configuracion_acto
from generador_word import GeneradorWord
from utilidades import (
    construir_antecedente_propiedad,
    construir_cierre_apendice,
    construir_clausulas_acto,
    construir_datos_personales,
    construir_datos_registro,
    construir_declaracion_predial,
    construir_descripcion_inmueble,
    construir_firmas,
    construir_introduccion_acto,
    construir_otorgamiento,
    construir_texto_colindancias,
    contexto_legacy_persona,
    fecha_notarial,
    parsear_fecha,
    personas_por_calidad,
    preparar_persona,
)


BASE = Path(__file__).resolve().parent


def personas_ejemplo(config: dict[str, Any]) -> list[dict[str, Any]]:
    fecha = parsear_fecha("27/03/2026")
    crudas = [
        {
            "nombre": "José Estefes Pérez",
            "sexo": "MASCULINO",
            "calidad": config["calidad_transmitente"],
            "originario": "Zacualpan, Estado de Veracruz",
            "vecino": "Tulancingo de Bravo, Estado de Hidalgo",
            "mismo_origen_vecindad": False,
            "domicilio": "calle Teponaxtle número 7, colonia Guadalupe",
            "codigo_postal": "43650",
            "fecha_nacimiento": "25/08/1964",
            "estado_civil": "SOLTERO",
            "ocupacion": "campesino",
            "rfc": "EEPJ640825AB1",
            "curp": "EEPJ640825HVZSRS00",
            "numero_ine": "1512028359884",
            "nacionalidad": "MEXICANA",
            "sabe_firmar": True,
        },
        {
            "nombre": "María Elena López Zavala",
            "sexo": "FEMENINO",
            "calidad": config["calidad_adquirente"],
            "originario": "Zacualpan, Estado de Veracruz",
            "vecino": "Zacualpan, Estado de Veracruz",
            "mismo_origen_vecindad": True,
            "domicilio": "localidad El Guayabal, sin número",
            "codigo_postal": "92650",
            "fecha_nacimiento": "22/05/1998",
            "estado_civil": "SOLTERA",
            "ocupacion": "comerciante",
            "rfc": "LOZM980522EF3",
            "curp": "LOZM980522MVZPVN00",
            "numero_ine": "4551118945120",
            "nacionalidad": "MEXICANA",
            "sabe_firmar": True,
        },
    ]
    return [preparar_persona(persona, fecha) for persona in crudas]


def grupos_ejemplo() -> list[dict[str, Any]]:
    return [
        {
            "punto": "NORTE",
            "tipo_colindante": "PROPIEDAD DE",
            "colindante": "FRANCISCO ESTEFES HINOJOSA",
            "tramos": [
                {
                    "medida": "9.773",
                    "medida_letra": "nueve metros con setecientos setenta y tres centímetros",
                },
                {
                    "medida": "34.795",
                    "medida_letra": "treinta y cuatro metros con setecientos noventa y cinco centímetros",
                },
            ],
        },
        {
            "punto": "SUR",
            "tipo_colindante": "CAMINO",
            "colindante": "REAL A EL GUAYABAL",
            "tramos": [
                {
                    "medida": "55.614",
                    "medida_letra": "cincuenta y cinco metros con seiscientos catorce centímetros",
                }
            ],
        },
        {
            "punto": "ESTE",
            "tipo_colindante": "ARROYO",
            "colindante": "",
            "tramos": [
                {
                    "medida": "132.935",
                    "medida_letra": "ciento treinta y dos metros con novecientos treinta y cinco centímetros",
                }
            ],
        },
        {
            "punto": "OESTE",
            "tipo_colindante": "PROPIEDAD DE",
            "colindante": "DOMINGO LÓPEZ HINOJOSA",
            "tramos": [
                {
                    "medida": "81.332",
                    "medida_letra": "ochenta y un metros con trescientos treinta y dos centímetros",
                }
            ],
        },
    ]


def campos_por_acto(acto: str) -> tuple[dict[str, str], dict[str, str]]:
    if acto == "DONACIÓN":
        return (
            {
                "tipo_donacion": "PURA",
                "reserva_usufructo": "SIN RESERVA DE USUFRUCTO",
            },
            {"importe": "", "importe_letra": "", "precio": "", "precio_letra": ""},
        )
    if acto == "CESIÓN DE DERECHOS":
        return (
            {
                "tipo_derecho": "DERECHOS DE PROPIEDAD",
                "origen_derecho": "el contrato privado relacionado en el antecedente",
            },
            {
                "importe": "75,000.00",
                "importe_letra": "SETENTA Y CINCO MIL",
                "precio": "75,000.00",
                "precio_letra": "SETENTA Y CINCO MIL",
            },
        )
    return (
        {"forma_pago": "TRANSFERENCIA BANCARIA", "entrega_posesion": "EN ESTE ACTO"},
        {
            "importe": "850,000.00",
            "importe_letra": "OCHOCIENTOS CINCUENTA MIL",
            "precio": "850,000.00",
            "precio_letra": "OCHOCIENTOS CINCUENTA MIL",
        },
    )


def datos_ejemplo(acto: str) -> dict[str, Any]:
    config = obtener_configuracion_acto(acto)
    fecha = parsear_fecha("27/03/2026")
    personas = personas_ejemplo(config)
    transmitentes = personas_por_calidad(personas, config["calidad_transmitente"])
    adquirentes = personas_por_calidad(personas, config["calidad_adquirente"])

    descripcion = construir_descripcion_inmueble(
        "PREDIO RÚSTICO",
        "LLANO REDONDO",
        "LA COMUNIDAD DE EL GUAYABAL",
        "ZACUALPAN",
        "VERACRUZ",
        "EL PAREJO",
    )
    antecedente = construir_antecedente_propiedad(
        {
            "texto_libre": (
                "Declara la parte transmitente, de manera expresa y bajo protesta de "
                "decir verdad, que adquirió legítimamente el inmueble de referencia "
                "mediante el documento relacionado en el apéndice"
            )
        },
        transmitentes,
    )
    registro = construir_datos_registro(
        {
            "oficina": (
                "el Registro Público de la Propiedad y del Comercio de "
                "Huayacocotla, Estado de Veracruz"
            ),
            "tipo_asiento": "Partida",
            "numero": "88",
            "numero_letra": "OCHENTA Y OCHO",
            "libro": "I",
            "libro_letra": "PRIMERO",
            "seccion": "I",
            "seccion_letra": "PRIMERA",
            "fecha_texto": "23 veintitrés de noviembre de 2024 dos mil veinticuatro",
        }
    )
    predial = construir_declaracion_predial(
        {
            "municipio": "Zacualpan",
            "estado": "Veracruz",
            "cuenta": "R-02-205-050-00-000-375-00-000-1",
            "clave_catastral": "30-198-001-0001",
        },
        denominacion_parte=config["parte_transmitente"],
    )
    inmueble = {
        "tipo": "PREDIO RÚSTICO",
        "denominacion": "LLANO REDONDO",
        "ubicacion": "LA COMUNIDAD DE EL GUAYABAL",
        "municipio": "ZACUALPAN",
        "estado": "VERACRUZ",
        "nombre_referencia": "EL PAREJO",
        "descripcion": descripcion,
        "antecedente_propiedad": antecedente,
        "datos_registro": registro,
        "declaracion_predial": predial,
        "medidas_colindancias": construir_texto_colindancias(grupos_ejemplo()),
        "superficie": "04-62-12.00",
        "unidad_superficie": "Ha",
        "superficie_letra": "CUATRO HECTÁREAS, SESENTA Y DOS ÁREAS Y DOCE CENTIÁREAS",
        "avaluo_valor": "620,000.00",
        "avaluo_valor_letra": "SEISCIENTOS VEINTE MIL",
    }
    campos, operacion = campos_por_acto(acto)
    escritura = {
        "acto": acto,
        "acto_titulo": config["titulo"],
        "libro_numero": "376",
        "libro_letra": "TRESCIENTOS SETENTA Y SEIS",
        "numero": "PENDIENTE",
        "numero_letra": "PENDIENTE DE ASIGNACIÓN",
        "fecha_texto": fecha_notarial(fecha),
        "ciudad": "Tezontepec de Aldama",
        "estado": "Hidalgo",
    }
    notario = {
        "nombre": "EDÉN KHADAFFY CORNEJO GÓMEZ",
        "numero": "16",
        "numero_letra": "DIECISÉIS",
        "distrito": "Tula de Allende, Hidalgo",
        "residencia": "Tezontepec de Aldama, Hidalgo",
    }

    return {
        "escritura": escritura,
        "notario": notario,
        "acto": config,
        "introduccion_acto": construir_introduccion_acto(acto, descripcion),
        "comparecientes": personas,
        "comparecientes_otorgamiento": construir_otorgamiento(personas),
        "comparecientes_datos_personales": construir_datos_personales(personas),
        "comparecientes_firmas": construir_firmas(personas),
        "transmitente": contexto_legacy_persona(transmitentes[0]),
        "adquirente": contexto_legacy_persona(adquirentes[0]),
        "vendedor": contexto_legacy_persona(transmitentes[0]),
        "comprador": contexto_legacy_persona(adquirentes[0]),
        "inmueble": inmueble,
        "operacion": operacion,
        "campos_especificos": campos,
        "clausulas_acto": construir_clausulas_acto(
            acto, config, personas, inmueble, operacion, campos
        ),
        "cierre_apendice": construir_cierre_apendice(acto, escritura, notario),
    }


def main() -> None:
    generador = GeneradorWord(BASE / "plantillas")
    (BASE / "salidas").mkdir(exist_ok=True)
    for acto in nombres_actos():
        config = obtener_configuracion_acto(acto)
        nombre = acto.lower().replace(" ", "_").replace("ó", "o").replace("í", "i")
        salida = generador.generar(
            datos_ejemplo(acto),
            BASE / "salidas" / f"prueba_paso7_{nombre}.docx",
            nombre_plantilla=config["plantilla"],
        )
        print(f"Documento generado: {salida}")


if __name__ == "__main__":
    main()
