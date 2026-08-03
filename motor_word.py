from __future__ import annotations

from pathlib import Path
from typing import Any

from redaccion import construir_datos_motor


def generar_escritura(
    formulario: dict[str, Any],
    ruta_salida: str | Path,
    *,
    ruta_matriz: str | Path | None = None,
) -> Path:
    """Genera la escritura usando Microsoft Word como motor de formato."""
    import generador_base_v12 as base

    proyecto = Path(__file__).resolve().parent
    matriz = Path(ruta_matriz) if ruta_matriz else proyecto / "plantillas" / "MATRIZ_COMPRAVENTA.docx"
    salida = Path(ruta_salida).resolve()
    salida.parent.mkdir(parents=True, exist_ok=True)
    registro = salida.with_name(salida.stem + "_registro.txt")

    datos_motor = construir_datos_motor(formulario)

    base.MATRIZ = matriz.resolve()
    base.SALIDA = salida
    base.REGISTRO = registro
    base.DATOS = datos_motor
    base.main()
    return salida
