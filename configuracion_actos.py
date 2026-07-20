from __future__ import annotations

from copy import deepcopy
from typing import Any


ACTOS_JURIDICOS: dict[str, dict[str, Any]] = {
    "COMPRAVENTA": {
        "titulo": "COMPRA VENTA",
        "plantilla": "plantilla_compraventa.docx",
        "descripcion": (
            "Transmisión onerosa de la propiedad de un inmueble. Requiere por lo "
            "menos una parte vendedora y una parte compradora."
        ),
        "calidades": ("VENDEDOR", "COMPRADOR", "APODERADO", "TESTIGO"),
        "requeridas": {"VENDEDOR": 1, "COMPRADOR": 1},
        "calidad_transmitente": "VENDEDOR",
        "calidad_adquirente": "COMPRADOR",
        "parte_transmitente": "parte vendedora",
        "parte_adquirente": "parte compradora",
        "etiqueta_importe": "Precio de la operación:",
        "etiqueta_importe_letra": "Precio en letra:",
        "importe_requerido": True,
        "campo_1": {
            "clave": "forma_pago",
            "etiqueta": "Forma de pago:",
            "valores": (
                "EFECTIVO",
                "TRANSFERENCIA BANCARIA",
                "CHEQUE",
                "PAGO MIXTO",
                "OTRA",
            ),
            "valor_inicial": "EFECTIVO",
            "requerido": True,
        },
        "campo_2": {
            "clave": "entrega_posesion",
            "etiqueta": "Entrega de posesión:",
            "valores": (
                "EN ESTE ACTO",
                "CON ANTERIORIDAD",
                "EN FECHA POSTERIOR",
                "OTRA",
            ),
            "valor_inicial": "EN ESTE ACTO",
            "requerido": True,
        },
    },
    "DONACIÓN": {
        "titulo": "DONACIÓN",
        "plantilla": "plantilla_donacion.docx",
        "descripcion": (
            "Transmisión gratuita de un inmueble. Requiere por lo menos una parte "
            "donante y una parte donataria."
        ),
        "calidades": ("DONANTE", "DONATARIO", "APODERADO", "TESTIGO"),
        "requeridas": {"DONANTE": 1, "DONATARIO": 1},
        "calidad_transmitente": "DONANTE",
        "calidad_adquirente": "DONATARIO",
        "parte_transmitente": "parte donante",
        "parte_adquirente": "parte donataria",
        "etiqueta_importe": "Valor declarado (opcional):",
        "etiqueta_importe_letra": "Valor en letra:",
        "importe_requerido": False,
        "campo_1": {
            "clave": "tipo_donacion",
            "etiqueta": "Tipo de donación:",
            "valores": (
                "PURA",
                "CONDICIONAL",
                "ONEROSA",
                "REMUNERATORIA",
                "OTRA",
            ),
            "valor_inicial": "PURA",
            "requerido": True,
        },
        "campo_2": {
            "clave": "reserva_usufructo",
            "etiqueta": "Reserva de usufructo:",
            "valores": (
                "SIN RESERVA DE USUFRUCTO",
                "CON RESERVA DE USUFRUCTO VITALICIO",
                "OTRA MODALIDAD",
            ),
            "valor_inicial": "SIN RESERVA DE USUFRUCTO",
            "requerido": True,
        },
    },
    "CESIÓN DE DERECHOS": {
        "titulo": "CESIÓN DE DERECHOS",
        "plantilla": "plantilla_cesion_derechos.docx",
        "descripcion": (
            "Transmisión de derechos relacionados con un inmueble. Requiere por lo "
            "menos una parte cedente y una parte cesionaria."
        ),
        "calidades": ("CEDENTE", "CESIONARIO", "APODERADO", "TESTIGO"),
        "requeridas": {"CEDENTE": 1, "CESIONARIO": 1},
        "calidad_transmitente": "CEDENTE",
        "calidad_adquirente": "CESIONARIO",
        "parte_transmitente": "parte cedente",
        "parte_adquirente": "parte cesionaria",
        "etiqueta_importe": "Contraprestación de la cesión:",
        "etiqueta_importe_letra": "Contraprestación en letra:",
        "importe_requerido": True,
        "campo_1": {
            "clave": "tipo_derecho",
            "etiqueta": "Derecho que se cede:",
            "valores": (
                "DERECHOS DE PROPIEDAD",
                "DERECHOS HEREDITARIOS",
                "DERECHOS POSESORIOS",
                "DERECHOS PARCELARIOS",
                "OTRO DERECHO",
            ),
            "valor_inicial": "DERECHOS DE PROPIEDAD",
            "requerido": True,
        },
        "campo_2": {
            "clave": "origen_derecho",
            "etiqueta": "Origen del derecho:",
            "valores": (),
            "valor_inicial": "",
            "requerido": True,
        },
    },
}


def nombres_actos() -> tuple[str, ...]:
    return tuple(ACTOS_JURIDICOS.keys())


def obtener_configuracion_acto(nombre: str) -> dict[str, Any]:
    clave = nombre.strip().upper()
    if clave not in ACTOS_JURIDICOS:
        raise ValueError(f"Acto jurídico no configurado: {nombre}")
    return deepcopy(ACTOS_JURIDICOS[clave])
