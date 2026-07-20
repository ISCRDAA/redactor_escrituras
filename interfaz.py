from __future__ import annotations

import tkinter as tk
from copy import deepcopy
from datetime import date
from pathlib import Path
from tkinter import filedialog, messagebox, ttk
from typing import Any

from configuracion_actos import nombres_actos, obtener_configuracion_acto
from formularios import VentanaCompareciente, VentanaGrupoColindancia
from generador_word import GeneradorWord
from utilidades import (
    construir_antecedente_propiedad,
    construir_datos_personales,
    construir_datos_registro,
    construir_clausulas_acto,
    construir_cierre_apendice,
    construir_declaracion_predial,
    construir_descripcion_inmueble,
    construir_firmas,
    construir_introduccion_acto,
    construir_otorgamiento,
    construir_texto_colindancias,
    contexto_legacy_persona,
    convertir_numero_texto,
    fecha_notarial,
    parsear_fecha,
    personas_por_calidad,
    preparar_persona,
    resumen_grupo,
)


RUTA_BASE = Path(__file__).resolve().parent
RUTA_PLANTILLAS = RUTA_BASE / "plantillas"
RUTA_SALIDAS = RUTA_BASE / "salidas"


class AplicacionEscrituras(tk.Tk):
    def __init__(self) -> None:
        super().__init__()
        self.title("Sistema de generación de escrituras - Paso 6")
        self.geometry("1240x800")
        self.minsize(1050, 680)

        self.comparecientes: list[dict[str, Any]] = []
        self.grupos_colindancias: list[dict[str, Any]] = []
        self.generador = GeneradorWord(RUTA_PLANTILLAS)

        self._crear_variables()
        self._crear_estilos()
        self._crear_interfaz()

    def _crear_variables(self) -> None:
        # Datos generales de la escritura.
        self.acto = tk.StringVar(value="COMPRAVENTA")
        self.libro_numero = tk.StringVar(value="376")
        self.libro_letra = tk.StringVar(value="TRESCIENTOS SETENTA Y SEIS")
        self.escritura_numero = tk.StringVar(value="")
        self.escritura_letra = tk.StringVar(value="")
        self.fecha_escritura = tk.StringVar(value="27/03/2026")
        self.ciudad = tk.StringVar(value="Tezontepec de Aldama")
        self.estado = tk.StringVar(value="Hidalgo")
        self.notario_nombre = tk.StringVar(value="EDÉN KHADAFFY CORNEJO GÓMEZ")
        self.notaria_numero = tk.StringVar(value="16")
        self.notaria_numero_letra = tk.StringVar(value="DIECISÉIS")
        self.distrito_judicial = tk.StringVar(value="Tula de Allende, Hidalgo")
        self.residencia_notaria = tk.StringVar(value="Tezontepec de Aldama, Hidalgo")

        # Inmueble y operación.
        self.tipo_inmueble = tk.StringVar(value="PREDIO RÚSTICO")
        self.denominacion_inmueble = tk.StringVar()
        self.ubicacion_inmueble = tk.StringVar()
        self.municipio_inmueble = tk.StringVar()
        self.estado_inmueble = tk.StringVar(value="Hidalgo")
        self.nombre_referencia_inmueble = tk.StringVar()
        self.descripcion_inmueble = tk.StringVar()
        self.superficie = tk.StringVar()
        self.superficie_letra = tk.StringVar()
        self.unidad_superficie = tk.StringVar(value="M2")
        self.precio = tk.StringVar()
        self.precio_letra = tk.StringVar()

        # Antecedente de propiedad.
        self.antecedente_documento = tk.StringVar(value="Primer Testimonio de la Escritura")
        self.antecedente_numero = tk.StringVar()
        self.antecedente_numero_letra = tk.StringVar()
        self.antecedente_volumen = tk.StringVar()
        self.antecedente_volumen_letra = tk.StringVar()
        self.antecedente_fecha = tk.StringVar()
        self.antecedente_autoridad = tk.StringVar()
        self.antecedente_ubicacion_autoridad = tk.StringVar()
        self.antecedente_acto = tk.StringVar(value="contrato de compraventa")

        # Datos registrales y fiscales del inmueble.
        self.registro_oficina = tk.StringVar(value="el Registro Público de la Propiedad y del Comercio")
        self.registro_tipo_asiento = tk.StringVar(value="Partida")
        self.registro_numero = tk.StringVar()
        self.registro_numero_letra = tk.StringVar()
        self.registro_libro = tk.StringVar()
        self.registro_libro_letra = tk.StringVar()
        self.registro_seccion = tk.StringVar()
        self.registro_seccion_letra = tk.StringVar()
        self.registro_fecha = tk.StringVar()
        self.predial_municipio = tk.StringVar()
        self.predial_estado = tk.StringVar(value="Hidalgo")
        self.cuenta_predial = tk.StringVar()
        self.clave_catastral = tk.StringVar()
        self.avaluo_valor = tk.StringVar()
        self.avaluo_valor_letra = tk.StringVar()

        # Campos que cambian según el acto jurídico.
        self.campo_especifico_1 = tk.StringVar()
        self.campo_especifico_2 = tk.StringVar()
        self.texto_config_acto = tk.StringVar()
        self.texto_requisitos_comparecientes = tk.StringVar()

        self.estado_aplicacion = tk.StringVar(
            value="Paso 6: selecciona el acto jurídico y captura sus campos particulares."
        )

    def _crear_estilos(self) -> None:
        estilo = ttk.Style(self)
        estilo.configure("Titulo.TLabel", font=("Arial", 18, "bold"))
        estilo.configure("Subtitulo.TLabel", font=("Arial", 10))
        estilo.configure("Seccion.TLabelframe.Label", font=("Arial", 11, "bold"))
        estilo.configure("Accion.TButton", font=("Arial", 11, "bold"), padding=9)

    def _crear_interfaz(self) -> None:
        superior = ttk.Frame(self, padding=(18, 14, 18, 8))
        superior.pack(fill="x")
        ttk.Label(
            superior,
            text="Generador de escrituras notariales",
            style="Titulo.TLabel",
        ).pack(anchor="w")
        ttk.Label(
            superior,
            text=(
                "Paso 6 · Actos jurídicos configurables. La aplicación selecciona "
                "calidades, campos y plantilla según el acto."
            ),
            style="Subtitulo.TLabel",
        ).pack(anchor="w", pady=(2, 0))

        self.cuaderno = ttk.Notebook(self)
        self.cuaderno.pack(fill="both", expand=True, padx=18, pady=(0, 10))

        self.tab_generales = ttk.Frame(self.cuaderno, padding=16)
        self.tab_comparecientes = ttk.Frame(self.cuaderno, padding=16)
        self.tab_inmueble = ttk.Frame(self.cuaderno, padding=16)
        self.tab_antecedente = ttk.Frame(self.cuaderno, padding=16)
        self.tab_colindancias = ttk.Frame(self.cuaderno, padding=16)

        self.cuaderno.add(self.tab_generales, text="1. Datos generales")
        self.cuaderno.add(self.tab_comparecientes, text="2. Comparecientes")
        self.cuaderno.add(self.tab_inmueble, text="3. Inmueble y operación")
        self.cuaderno.add(self.tab_antecedente, text="4. Antecedente y registro")
        self.cuaderno.add(self.tab_colindancias, text="5. Medidas y colindancias")

        self._crear_tab_generales()
        self._crear_tab_comparecientes()
        self._crear_tab_inmueble()
        self._crear_tab_antecedente()
        self._crear_tab_colindancias()

        inferior = ttk.Frame(self, padding=(18, 0, 18, 14))
        inferior.pack(fill="x")
        inferior.columnconfigure(0, weight=1)
        ttk.Label(inferior, textvariable=self.estado_aplicacion).grid(
            row=0, column=0, sticky="w"
        )
        ttk.Button(
            inferior,
            text="Generar documento Word",
            command=self._generar_documento,
            style="Accion.TButton",
        ).grid(row=0, column=1, sticky="e")

        self._aplicar_configuracion_acto(inicial=True)

    def _crear_tab_generales(self) -> None:
        tab = self.tab_generales
        tab.columnconfigure(1, weight=1)
        tab.columnconfigure(3, weight=1)

        ttk.Label(
            tab,
            text="Datos generales del instrumento",
            font=("Arial", 14, "bold"),
        ).grid(row=0, column=0, columnspan=4, sticky="w", pady=(0, 12))

        ttk.Label(tab, text="Tipo de acto:").grid(row=1, column=0, sticky="w", pady=5)
        self.combo_acto = ttk.Combobox(
            tab,
            textvariable=self.acto,
            values=nombres_actos(),
            state="readonly",
        )
        self.combo_acto.grid(row=1, column=1, sticky="ew", padx=(8, 18), pady=5)
        self.combo_acto.bind(
            "<<ComboboxSelected>>", lambda _evento: self._aplicar_configuracion_acto()
        )

        ttk.Label(
            tab,
            textvariable=self.texto_config_acto,
            wraplength=520,
            foreground="#34495E",
        ).grid(row=1, column=2, columnspan=2, sticky="w", pady=5)

        self._entrada(tab, 2, 0, "Libro número:", self.libro_numero)
        self._entrada(tab, 2, 2, "Libro en letra:", self.libro_letra)
        self._entrada(tab, 3, 0, "Escritura número:", self.escritura_numero)
        self._entrada(tab, 3, 2, "Escritura en letra:", self.escritura_letra)
        self._entrada(tab, 4, 0, "Fecha de escritura:", self.fecha_escritura)
        ttk.Label(
            tab,
            text="Formato DD/MM/AAAA. El número de escritura puede quedar vacío.",
            foreground="#555555",
        ).grid(row=4, column=2, columnspan=2, sticky="w", pady=5)
        self._entrada(tab, 5, 0, "Ciudad:", self.ciudad)
        self._entrada(tab, 5, 2, "Estado:", self.estado)

        separador = ttk.Separator(tab, orient="horizontal")
        separador.grid(row=6, column=0, columnspan=4, sticky="ew", pady=16)

        ttk.Label(
            tab,
            text="Datos del notario",
            font=("Arial", 13, "bold"),
        ).grid(row=7, column=0, columnspan=4, sticky="w", pady=(0, 8))

        self._entrada(tab, 8, 0, "Nombre del notario:", self.notario_nombre, columnas=3)
        self._entrada(tab, 9, 0, "Notaría número:", self.notaria_numero)
        self._entrada(tab, 9, 2, "Número en letra:", self.notaria_numero_letra)
        self._entrada(tab, 10, 0, "Distrito judicial:", self.distrito_judicial, columnas=3)
        self._entrada(tab, 11, 0, "Residencia:", self.residencia_notaria, columnas=3)

        ttk.Button(
            tab,
            text="Completar números en letra",
            command=self._completar_numeros_en_letra,
        ).grid(row=12, column=3, sticky="e", pady=(18, 0))

    def _entrada(
        self,
        padre: ttk.Frame,
        fila: int,
        columna: int,
        etiqueta: str,
        variable: tk.StringVar,
        columnas: int = 1,
    ) -> None:
        ttk.Label(padre, text=etiqueta).grid(
            row=fila, column=columna, sticky="w", pady=5
        )
        ttk.Entry(padre, textvariable=variable).grid(
            row=fila,
            column=columna + 1,
            columnspan=columnas,
            sticky="ew",
            padx=(8, 18 if columnas == 1 and columna == 0 else 0),
            pady=5,
        )

    def _crear_tab_comparecientes(self) -> None:
        tab = self.tab_comparecientes
        tab.columnconfigure(0, weight=1)
        tab.rowconfigure(2, weight=1)

        ttk.Label(
            tab,
            text="Comparecientes",
            font=("Arial", 14, "bold"),
        ).grid(row=0, column=0, sticky="w")
        ttk.Label(
            tab,
            textvariable=self.texto_requisitos_comparecientes,
            wraplength=1050,
        ).grid(row=1, column=0, sticky="w", pady=(4, 12))

        columnas = ("numero", "nombre", "calidad", "sexo", "edad", "rfc", "curp")
        self.tabla_comparecientes = ttk.Treeview(tab, columns=columnas, show="headings")
        encabezados = {
            "numero": "#",
            "nombre": "Nombre",
            "calidad": "Calidad",
            "sexo": "Sexo",
            "edad": "Edad",
            "rfc": "RFC",
            "curp": "CURP",
        }
        for clave, texto in encabezados.items():
            self.tabla_comparecientes.heading(clave, text=texto)
        self.tabla_comparecientes.column("numero", width=45, anchor="center", stretch=False)
        self.tabla_comparecientes.column("nombre", width=330, anchor="w")
        self.tabla_comparecientes.column("calidad", width=125, anchor="center", stretch=False)
        self.tabla_comparecientes.column("sexo", width=110, anchor="center", stretch=False)
        self.tabla_comparecientes.column("edad", width=65, anchor="center", stretch=False)
        self.tabla_comparecientes.column("rfc", width=125, anchor="center", stretch=False)
        self.tabla_comparecientes.column("curp", width=175, anchor="center", stretch=False)
        self.tabla_comparecientes.grid(row=2, column=0, sticky="nsew")
        self.tabla_comparecientes.bind("<Double-1>", lambda _e: self._editar_compareciente())

        barra = ttk.Scrollbar(tab, orient="vertical", command=self.tabla_comparecientes.yview)
        barra.grid(row=2, column=1, sticky="ns")
        self.tabla_comparecientes.configure(yscrollcommand=barra.set)

        acciones = ttk.Frame(tab)
        acciones.grid(row=3, column=0, sticky="ew", pady=(10, 0))
        ttk.Button(
            acciones,
            text="Agregar compareciente",
            command=self._abrir_nuevo_compareciente,
        ).grid(row=0, column=0, padx=(0, 8))
        ttk.Button(
            acciones,
            text="Editar seleccionado",
            command=self._editar_compareciente,
        ).grid(row=0, column=1, padx=(0, 8))
        ttk.Button(
            acciones,
            text="Eliminar seleccionado",
            command=self._eliminar_compareciente,
        ).grid(row=0, column=2, padx=(0, 8))
        ttk.Button(
            acciones,
            text="Recalcular edades",
            command=self._recalcular_edades,
        ).grid(row=0, column=3)

    def _crear_tab_inmueble(self) -> None:
        tab = self.tab_inmueble
        tab.columnconfigure(1, weight=1)
        tab.columnconfigure(3, weight=1)

        ttk.Label(
            tab,
            text="Identificación del inmueble y datos del acto",
            font=("Arial", 14, "bold"),
        ).grid(row=0, column=0, columnspan=4, sticky="w", pady=(0, 12))

        ttk.Label(tab, text="Tipo de inmueble:").grid(row=1, column=0, sticky="w", pady=5)
        ttk.Combobox(
            tab,
            textvariable=self.tipo_inmueble,
            values=(
                "PREDIO RÚSTICO",
                "PREDIO URBANO",
                "TERRENO",
                "LOTE",
                "CASA HABITACIÓN",
                "PARCELA",
                "FRACCIÓN DE PREDIO",
                "OTRO INMUEBLE",
            ),
        ).grid(row=1, column=1, sticky="ew", padx=(8, 18), pady=5)

        self._entrada(tab, 1, 2, "Denominación:", self.denominacion_inmueble)
        self._entrada(tab, 2, 0, "Ubicación o localidad:", self.ubicacion_inmueble)
        self._entrada(tab, 2, 2, "Municipio:", self.municipio_inmueble)
        self._entrada(tab, 3, 0, "Estado:", self.estado_inmueble)
        self._entrada(tab, 3, 2, "Nombre de referencia:", self.nombre_referencia_inmueble)

        ttk.Button(
            tab,
            text="Construir descripción",
            command=self._construir_descripcion_inmueble,
        ).grid(row=4, column=3, sticky="e", pady=(6, 8))

        self._entrada(
            tab,
            5,
            0,
            "Descripción que irá en Word:",
            self.descripcion_inmueble,
            columnas=3,
        )
        ttk.Label(
            tab,
            text="La descripción generada puede editarse manualmente.",
            foreground="#555555",
        ).grid(row=6, column=1, columnspan=3, sticky="w", pady=(0, 10))

        ttk.Separator(tab, orient="horizontal").grid(
            row=7, column=0, columnspan=4, sticky="ew", pady=12
        )

        self._entrada(tab, 8, 0, "Superficie:", self.superficie)
        ttk.Label(tab, text="Unidad:").grid(row=8, column=2, sticky="w", pady=5)
        ttk.Combobox(
            tab,
            textvariable=self.unidad_superficie,
            values=("M2", "Ha", "HECTÁREAS", "UNIDAD PERSONALIZADA"),
        ).grid(row=8, column=3, sticky="ew", padx=(8, 0), pady=5)
        self._entrada(tab, 9, 0, "Superficie en letra:", self.superficie_letra, columnas=3)

        self.etiqueta_importe = ttk.Label(tab, text="Precio de la operación:")
        self.etiqueta_importe.grid(row=10, column=0, sticky="w", pady=5)
        ttk.Entry(tab, textvariable=self.precio).grid(
            row=10, column=1, sticky="ew", padx=(8, 18), pady=5
        )
        self.etiqueta_importe_letra = ttk.Label(tab, text="Precio en letra:")
        self.etiqueta_importe_letra.grid(row=10, column=2, sticky="w", pady=5)
        ttk.Entry(tab, textvariable=self.precio_letra).grid(
            row=10, column=3, sticky="ew", padx=(8, 0), pady=5
        )

        self.etiqueta_campo_1 = ttk.Label(tab, text="Campo específico 1:")
        self.etiqueta_campo_1.grid(row=11, column=0, sticky="w", pady=5)
        self.combo_campo_1 = ttk.Combobox(tab, textvariable=self.campo_especifico_1)
        self.combo_campo_1.grid(row=11, column=1, sticky="ew", padx=(8, 18), pady=5)

        self.etiqueta_campo_2 = ttk.Label(tab, text="Campo específico 2:")
        self.etiqueta_campo_2.grid(row=11, column=2, sticky="w", pady=5)
        self.combo_campo_2 = ttk.Combobox(tab, textvariable=self.campo_especifico_2)
        self.combo_campo_2.grid(row=11, column=3, sticky="ew", padx=(8, 0), pady=5)

        ttk.Label(
            tab,
            text=(
                "Los dos últimos campos cambian automáticamente al seleccionar "
                "compraventa, donación o cesión de derechos."
            ),
            foreground="#555555",
            wraplength=950,
        ).grid(row=12, column=0, columnspan=4, sticky="w", pady=(8, 0))

    def _construir_descripcion_inmueble(self) -> None:
        descripcion = construir_descripcion_inmueble(
            self.tipo_inmueble.get(),
            self.denominacion_inmueble.get(),
            self.ubicacion_inmueble.get(),
            self.municipio_inmueble.get(),
            self.estado_inmueble.get(),
            self.nombre_referencia_inmueble.get(),
        )
        self.descripcion_inmueble.set(descripcion)
        self.estado_aplicacion.set("Se construyó la descripción editable del inmueble.")

    def _crear_tab_antecedente(self) -> None:
        tab = self.tab_antecedente
        tab.columnconfigure(0, weight=1)
        tab.rowconfigure(1, weight=1)

        ttk.Label(
            tab,
            text="Antecedente de propiedad, registro y situación fiscal",
            font=("Arial", 14, "bold"),
        ).grid(row=0, column=0, sticky="w", pady=(0, 10))

        secciones = ttk.Notebook(tab)
        secciones.grid(row=1, column=0, sticky="nsew")

        titulo = ttk.Frame(secciones, padding=14)
        registro = ttk.Frame(secciones, padding=14)
        fiscal = ttk.Frame(secciones, padding=14)
        secciones.add(titulo, text="Título de propiedad")
        secciones.add(registro, text="Datos registrales")
        secciones.add(fiscal, text="Predial y avalúo")

        for marco in (titulo, registro, fiscal):
            marco.columnconfigure(1, weight=1)
            marco.columnconfigure(3, weight=1)

        self._entrada(titulo, 0, 0, "Documento o título:", self.antecedente_documento, columnas=3)
        self._entrada(titulo, 1, 0, "Número:", self.antecedente_numero)
        self._entrada(titulo, 1, 2, "Número en letra:", self.antecedente_numero_letra)
        self._entrada(titulo, 2, 0, "Volumen:", self.antecedente_volumen)
        self._entrada(titulo, 2, 2, "Volumen en letra:", self.antecedente_volumen_letra)
        self._entrada(titulo, 3, 0, "Fecha del título:", self.antecedente_fecha)
        ttk.Label(titulo, text="Formato DD/MM/AAAA").grid(
            row=3, column=2, columnspan=2, sticky="w", pady=5
        )
        self._entrada(titulo, 4, 0, "Fedatario o autoridad:", self.antecedente_autoridad, columnas=3)
        self._entrada(
            titulo,
            5,
            0,
            "Lugar o jurisdicción:",
            self.antecedente_ubicacion_autoridad,
            columnas=3,
        )
        self._entrada(titulo, 6, 0, "Acto de adquisición:", self.antecedente_acto, columnas=3)

        ttk.Label(
            titulo,
            text="Redacción libre opcional del antecedente:",
        ).grid(row=7, column=0, columnspan=4, sticky="w", pady=(12, 4))
        self.texto_antecedente_libre = tk.Text(
            titulo,
            height=7,
            wrap="word",
            font=("Arial", 10),
        )
        self.texto_antecedente_libre.grid(row=8, column=0, columnspan=4, sticky="nsew")
        titulo.rowconfigure(8, weight=1)
        ttk.Label(
            titulo,
            text=(
                "Cuando este espacio tenga texto, se utilizará en lugar de los campos "
                "estructurados. Es útil para contratos privados, sentencias o títulos atípicos."
            ),
            foreground="#555555",
            wraplength=950,
        ).grid(row=9, column=0, columnspan=4, sticky="w", pady=(5, 0))

        ttk.Label(registro, text="Oficina registral:").grid(row=0, column=0, sticky="w", pady=5)
        ttk.Entry(registro, textvariable=self.registro_oficina).grid(
            row=0, column=1, columnspan=3, sticky="ew", padx=(8, 0), pady=5
        )
        ttk.Label(registro, text="Tipo de asiento:").grid(row=1, column=0, sticky="w", pady=5)
        ttk.Combobox(
            registro,
            textvariable=self.registro_tipo_asiento,
            values=("Partida", "Folio Real", "Inscripción", "Asiento", "Otro"),
        ).grid(row=1, column=1, sticky="ew", padx=(8, 18), pady=5)
        self._entrada(registro, 1, 2, "Número:", self.registro_numero)
        self._entrada(registro, 2, 0, "Número en letra:", self.registro_numero_letra)
        self._entrada(registro, 2, 2, "Libro:", self.registro_libro)
        self._entrada(registro, 3, 0, "Libro en letra:", self.registro_libro_letra)
        self._entrada(registro, 3, 2, "Sección:", self.registro_seccion)
        self._entrada(registro, 4, 0, "Sección en letra:", self.registro_seccion_letra)
        self._entrada(registro, 4, 2, "Fecha de inscripción:", self.registro_fecha)

        self._entrada(fiscal, 0, 0, "Municipio del predial:", self.predial_municipio)
        self._entrada(fiscal, 0, 2, "Estado:", self.predial_estado)
        self._entrada(fiscal, 1, 0, "Cuenta predial:", self.cuenta_predial)
        self._entrada(fiscal, 1, 2, "Clave catastral:", self.clave_catastral)
        self._entrada(fiscal, 2, 0, "Valor de avalúo:", self.avaluo_valor)
        self._entrada(fiscal, 2, 2, "Avalúo en letra:", self.avaluo_valor_letra)
        ttk.Label(
            fiscal,
            text=(
                "El valor de avalúo es independiente del precio pactado en la compraventa. "
                "Puede coincidir, pero el sistema los conserva como datos separados."
            ),
            wraplength=950,
            foreground="#555555",
        ).grid(row=3, column=0, columnspan=4, sticky="w", pady=(12, 0))

    def _crear_tab_colindancias(self) -> None:
        tab = self.tab_colindancias
        tab.columnconfigure(0, weight=1)
        tab.rowconfigure(2, weight=1)

        ttk.Label(
            tab,
            text="Medidas y colindancias por grupos",
            font=("Arial", 14, "bold"),
        ).grid(row=0, column=0, sticky="w")
        ttk.Label(
            tab,
            text=(
                "Cada grupo representa un punto cardinal, un colindante y uno o varios "
                "tramos. Repita el cardinal cuando cambie el colindante."
            ),
            wraplength=1050,
        ).grid(row=1, column=0, sticky="w", pady=(4, 12))

        columnas = ("numero", "punto", "tipo", "colindante", "tramos")
        self.tabla_grupos = ttk.Treeview(tab, columns=columnas, show="headings")
        self.tabla_grupos.heading("numero", text="#")
        self.tabla_grupos.heading("punto", text="Punto cardinal")
        self.tabla_grupos.heading("tipo", text="Tipo")
        self.tabla_grupos.heading("colindante", text="Colindante")
        self.tabla_grupos.heading("tramos", text="Tramos")
        self.tabla_grupos.column("numero", width=45, anchor="center", stretch=False)
        self.tabla_grupos.column("punto", width=130, anchor="center", stretch=False)
        self.tabla_grupos.column("tipo", width=160, anchor="center", stretch=False)
        self.tabla_grupos.column("colindante", width=650, anchor="w")
        self.tabla_grupos.column("tramos", width=110, anchor="center", stretch=False)
        self.tabla_grupos.grid(row=2, column=0, sticky="nsew")
        self.tabla_grupos.bind("<Double-1>", lambda _e: self._editar_grupo())

        barra = ttk.Scrollbar(tab, orient="vertical", command=self.tabla_grupos.yview)
        barra.grid(row=2, column=1, sticky="ns")
        self.tabla_grupos.configure(yscrollcommand=barra.set)

        acciones = ttk.Frame(tab)
        acciones.grid(row=3, column=0, sticky="ew", pady=(10, 0))
        ttk.Button(acciones, text="Agregar grupo", command=self._abrir_nuevo_grupo).grid(
            row=0, column=0, padx=(0, 8)
        )
        ttk.Button(acciones, text="Editar seleccionado", command=self._editar_grupo).grid(
            row=0, column=1, padx=(0, 8)
        )
        ttk.Button(acciones, text="Eliminar seleccionado", command=self._eliminar_grupo).grid(
            row=0, column=2
        )

    def _configuracion_actual(self) -> dict[str, Any]:
        return obtener_configuracion_acto(self.acto.get())

    def _aplicar_configuracion_acto(self, inicial: bool = False) -> None:
        config = self._configuracion_actual()
        self.texto_config_acto.set(config["descripcion"])

        requeridas = config["requeridas"]
        requisitos = ", ".join(
            f"{cantidad} {calidad}" for calidad, cantidad in requeridas.items()
        )
        calidades = ", ".join(config["calidades"])
        self.texto_requisitos_comparecientes.set(
            f"Este acto requiere como mínimo: {requisitos}. Calidades disponibles: {calidades}."
        )

        self.etiqueta_importe.configure(text=config["etiqueta_importe"])
        self.etiqueta_importe_letra.configure(text=config["etiqueta_importe_letra"])

        campo_1 = config["campo_1"]
        campo_2 = config["campo_2"]
        self.etiqueta_campo_1.configure(text=campo_1["etiqueta"])
        self.etiqueta_campo_2.configure(text=campo_2["etiqueta"])
        self.combo_campo_1.configure(values=campo_1["valores"])
        self.combo_campo_2.configure(values=campo_2["valores"])

        if inicial or not self.campo_especifico_1.get().strip():
            self.campo_especifico_1.set(campo_1["valor_inicial"])
        else:
            self.campo_especifico_1.set(campo_1["valor_inicial"])
        if inicial or not self.campo_especifico_2.get().strip():
            self.campo_especifico_2.set(campo_2["valor_inicial"])
        else:
            self.campo_especifico_2.set(campo_2["valor_inicial"])

        incompatibles = [
            p for p in self.comparecientes
            if str(p.get("calidad", "")).upper() not in config["calidades"]
        ]
        mensaje = f"Acto seleccionado: {self.acto.get()}. Plantilla: {config['plantilla']}."
        if incompatibles:
            mensaje += " Revisa las calidades de los comparecientes ya capturados."
        self.estado_aplicacion.set(mensaje)

    def _fecha_referencia(self) -> date:
        return parsear_fecha(self.fecha_escritura.get())

    def _completar_numeros_en_letra(self) -> None:
        try:
            if self.libro_numero.get().strip() and not self.libro_letra.get().strip():
                self.libro_letra.set(convertir_numero_texto(self.libro_numero.get()).upper())
            if self.escritura_numero.get().strip() and not self.escritura_letra.get().strip():
                self.escritura_letra.set(
                    convertir_numero_texto(self.escritura_numero.get()).upper()
                )
            if self.notaria_numero.get().strip() and not self.notaria_numero_letra.get().strip():
                self.notaria_numero_letra.set(
                    convertir_numero_texto(self.notaria_numero.get()).upper()
                )
        except ValueError as error:
            messagebox.showwarning("Número incorrecto", str(error))
            return
        self.estado_aplicacion.set("Los números disponibles se convirtieron a letra.")

    # Comparecientes -----------------------------------------------------
    def _abrir_nuevo_compareciente(self) -> None:
        config = self._configuracion_actual()
        VentanaCompareciente(
            self,
            fecha_referencia=self._fecha_referencia,
            al_guardar=self._agregar_compareciente,
            calidades_permitidas=tuple(config["calidades"]),
        )

    def _agregar_compareciente(self, persona: dict[str, Any]) -> None:
        self.comparecientes.append(persona)
        self._actualizar_tabla_comparecientes()
        self.estado_aplicacion.set(f"Compareciente agregado: {persona['nombre']}")

    def _editar_compareciente(self) -> None:
        seleccion = self.tabla_comparecientes.selection()
        if not seleccion:
            messagebox.showwarning(
                "Sin selección",
                "Selecciona un compareciente para editarlo.",
            )
            return
        indice = int(seleccion[0])
        config = self._configuracion_actual()

        def guardar(persona: dict[str, Any]) -> None:
            self.comparecientes[indice] = persona
            self._actualizar_tabla_comparecientes()
            self.estado_aplicacion.set("Se actualizó el compareciente.")

        VentanaCompareciente(
            self,
            fecha_referencia=self._fecha_referencia,
            al_guardar=guardar,
            persona_existente=deepcopy(self.comparecientes[indice]),
            calidades_permitidas=tuple(config["calidades"]),
        )

    def _eliminar_compareciente(self) -> None:
        seleccion = self.tabla_comparecientes.selection()
        if not seleccion:
            messagebox.showinfo(
                "Selecciona una persona",
                "Selecciona el compareciente que deseas eliminar.",
            )
            return
        indices = sorted(
            (self.tabla_comparecientes.index(item) for item in seleccion), reverse=True
        )
        for indice in indices:
            del self.comparecientes[indice]
        self._actualizar_tabla_comparecientes()

    def _recalcular_edades(self) -> None:
        try:
            referencia = self._fecha_referencia()
            self.comparecientes = [
                preparar_persona(persona, referencia) for persona in self.comparecientes
            ]
        except ValueError as error:
            messagebox.showwarning("No se pudieron recalcular", str(error))
            return
        self._actualizar_tabla_comparecientes()
        self.estado_aplicacion.set("Edades recalculadas a la fecha de la escritura.")

    def _actualizar_tabla_comparecientes(self) -> None:
        for item in self.tabla_comparecientes.get_children():
            self.tabla_comparecientes.delete(item)
        try:
            referencia = self._fecha_referencia()
        except ValueError:
            referencia = date.today()

        for numero, persona in enumerate(self.comparecientes, start=1):
            try:
                preparada = preparar_persona(persona, referencia)
                edad = preparada["edad_numero"]
            except ValueError:
                edad = "?"
            self.tabla_comparecientes.insert(
                "",
                "end",
                values=(
                    numero,
                    persona.get("nombre", ""),
                    persona.get("calidad", ""),
                    persona.get("sexo", ""),
                    edad,
                    persona.get("rfc", ""),
                    persona.get("curp", ""),
                ),
            )

    # Colindancias -------------------------------------------------------
    def _abrir_nuevo_grupo(self) -> None:
        VentanaGrupoColindancia(self, self._agregar_grupo)

    def _agregar_grupo(self, grupo: dict[str, Any]) -> None:
        self.grupos_colindancias.append(grupo)
        self._actualizar_tabla_grupos()

    def _editar_grupo(self) -> None:
        seleccion = self.tabla_grupos.selection()
        if not seleccion:
            messagebox.showinfo(
                "Selecciona un grupo",
                "Selecciona el grupo de colindancia que deseas editar.",
            )
            return
        indice = self.tabla_grupos.index(seleccion[0])

        def guardar(grupo: dict[str, Any]) -> None:
            self.grupos_colindancias[indice] = grupo
            self._actualizar_tabla_grupos()

        VentanaGrupoColindancia(
            self,
            guardar,
            grupo_existente=self.grupos_colindancias[indice],
        )

    def _eliminar_grupo(self) -> None:
        seleccion = self.tabla_grupos.selection()
        if not seleccion:
            messagebox.showinfo(
                "Selecciona un grupo",
                "Selecciona el grupo de colindancia que deseas eliminar.",
            )
            return
        indices = sorted((self.tabla_grupos.index(i) for i in seleccion), reverse=True)
        for indice in indices:
            del self.grupos_colindancias[indice]
        self._actualizar_tabla_grupos()

    def _actualizar_tabla_grupos(self) -> None:
        for item in self.tabla_grupos.get_children():
            self.tabla_grupos.delete(item)
        for numero, grupo in enumerate(self.grupos_colindancias, start=1):
            self.tabla_grupos.insert(
                "",
                "end",
                values=(
                    numero,
                    grupo["punto"],
                    grupo["tipo_colindante"],
                    grupo["colindante"] or grupo["tipo_colindante"],
                    resumen_grupo(grupo),
                ),
            )

    # Generación ---------------------------------------------------------
    def _validar_datos(self) -> bool:
        try:
            self._fecha_referencia()
        except ValueError as error:
            messagebox.showwarning("Fecha de escritura incorrecta", str(error))
            self.cuaderno.select(self.tab_generales)
            return False

        generales = {
            "Libro número": self.libro_numero.get(),
            "Ciudad": self.ciudad.get(),
            "Estado": self.estado.get(),
            "Nombre del notario": self.notario_nombre.get(),
            "Número de notaría": self.notaria_numero.get(),
            "Distrito judicial": self.distrito_judicial.get(),
            "Residencia": self.residencia_notaria.get(),
        }
        faltantes = [nombre for nombre, valor in generales.items() if not valor.strip()]
        if faltantes:
            messagebox.showwarning(
                "Datos generales incompletos",
                "Faltan:\n\n- " + "\n- ".join(faltantes),
            )
            self.cuaderno.select(self.tab_generales)
            return False

        config = self._configuracion_actual()
        if not self.comparecientes:
            messagebox.showwarning(
                "Sin comparecientes",
                "Agrega las partes requeridas para el acto seleccionado.",
            )
            self.cuaderno.select(self.tab_comparecientes)
            return False

        conteo: dict[str, int] = {}
        incompatibles: list[str] = []
        for persona in self.comparecientes:
            calidad = str(persona.get("calidad", "")).strip().upper()
            conteo[calidad] = conteo.get(calidad, 0) + 1
            if calidad not in config["calidades"]:
                incompatibles.append(f"{persona.get('nombre', '')}: {calidad}")

        if incompatibles:
            messagebox.showwarning(
                "Calidades incompatibles",
                "Estas personas tienen calidades que no corresponden al acto:\n\n- "
                + "\n- ".join(incompatibles),
            )
            self.cuaderno.select(self.tab_comparecientes)
            return False

        partes_faltantes = [
            f"{cantidad} {calidad}"
            for calidad, cantidad in config["requeridas"].items()
            if conteo.get(calidad, 0) < cantidad
        ]
        if partes_faltantes:
            messagebox.showwarning(
                "Partes incompletas",
                f"El acto {self.acto.get()} necesita:\n\n- "
                + "\n- ".join(partes_faltantes),
            )
            self.cuaderno.select(self.tab_comparecientes)
            return False

        inmueble = {
            "Descripción del inmueble": self.descripcion_inmueble.get(),
            "Superficie": self.superficie.get(),
            "Superficie en letra": self.superficie_letra.get(),
        }
        if config["importe_requerido"]:
            inmueble[config["etiqueta_importe"].rstrip(":")] = self.precio.get()
            inmueble[config["etiqueta_importe_letra"].rstrip(":")] = self.precio_letra.get()
        for campo in (config["campo_1"], config["campo_2"]):
            if campo["requerido"]:
                valor = (
                    self.campo_especifico_1.get()
                    if campo is config["campo_1"]
                    else self.campo_especifico_2.get()
                )
                inmueble[campo["etiqueta"].rstrip(":")] = valor

        faltantes = [nombre for nombre, valor in inmueble.items() if not str(valor).strip()]
        if faltantes:
            messagebox.showwarning(
                "Datos del inmueble incompletos",
                "Faltan:\n\n- " + "\n- ".join(faltantes),
            )
            self.cuaderno.select(self.tab_inmueble)
            return False

        texto_libre = self.texto_antecedente_libre.get("1.0", "end").strip()
        if not texto_libre:
            titulo_requerido = {
                "Documento o título": self.antecedente_documento.get(),
                "Fecha del título": self.antecedente_fecha.get(),
                "Fedatario o autoridad": self.antecedente_autoridad.get(),
                "Acto de adquisición": self.antecedente_acto.get(),
            }
            faltantes = [
                nombre for nombre, valor in titulo_requerido.items() if not valor.strip()
            ]
            if faltantes:
                messagebox.showwarning(
                    "Antecedente incompleto",
                    "Captura una redacción libre o completa:\n\n- " + "\n- ".join(faltantes),
                )
                self.cuaderno.select(self.tab_antecedente)
                return False
            try:
                parsear_fecha(self.antecedente_fecha.get())
            except ValueError as error:
                messagebox.showwarning("Fecha del título incorrecta", str(error))
                self.cuaderno.select(self.tab_antecedente)
                return False

        registro_requerido = {
            "Oficina registral": self.registro_oficina.get(),
            "Número de asiento": self.registro_numero.get(),
            "Fecha de inscripción": self.registro_fecha.get(),
            "Municipio del predial": self.predial_municipio.get(),
            "Estado del predial": self.predial_estado.get(),
            "Valor de avalúo": self.avaluo_valor.get(),
            "Avalúo en letra": self.avaluo_valor_letra.get(),
        }
        if not self.cuenta_predial.get().strip() and not self.clave_catastral.get().strip():
            registro_requerido["Cuenta predial o clave catastral"] = ""
        faltantes = [nombre for nombre, valor in registro_requerido.items() if not valor.strip()]
        if faltantes:
            messagebox.showwarning(
                "Registro o datos fiscales incompletos",
                "Faltan:\n\n- " + "\n- ".join(faltantes),
            )
            self.cuaderno.select(self.tab_antecedente)
            return False
        try:
            parsear_fecha(self.registro_fecha.get())
        except ValueError as error:
            messagebox.showwarning("Fecha registral incorrecta", str(error))
            self.cuaderno.select(self.tab_antecedente)
            return False

        if not self.grupos_colindancias:
            messagebox.showwarning(
                "Sin colindancias",
                "Agrega por lo menos un grupo de medidas y colindancias.",
            )
            self.cuaderno.select(self.tab_colindancias)
            return False
        return True

    def _crear_contexto(self) -> dict[str, Any]:
        config = self._configuracion_actual()
        fecha = self._fecha_referencia()
        personas = [preparar_persona(p, fecha) for p in self.comparecientes]
        transmitentes = personas_por_calidad(personas, config["calidad_transmitente"])
        adquirentes = personas_por_calidad(personas, config["calidad_adquirente"])
        transmitente = transmitentes[0]
        adquirente = adquirentes[0]

        libro_letra = self.libro_letra.get().strip()
        if not libro_letra:
            libro_letra = convertir_numero_texto(self.libro_numero.get()).upper()

        numero_escritura = self.escritura_numero.get().strip()
        letra_escritura = self.escritura_letra.get().strip()
        if numero_escritura and not letra_escritura:
            letra_escritura = convertir_numero_texto(numero_escritura).upper()
        if not numero_escritura:
            numero_escritura = "PENDIENTE"
            letra_escritura = "PENDIENTE DE ASIGNACIÓN"

        notaria_letra = self.notaria_numero_letra.get().strip()
        if not notaria_letra:
            notaria_letra = convertir_numero_texto(self.notaria_numero.get()).upper()

        texto_libre_antecedente = self.texto_antecedente_libre.get("1.0", "end").strip()
        fecha_titulo_texto = ""
        if self.antecedente_fecha.get().strip():
            fecha_titulo_texto = fecha_notarial(
                parsear_fecha(self.antecedente_fecha.get()), incluir_dias=False
            )
        antecedente_propiedad = construir_antecedente_propiedad(
            {
                "texto_libre": texto_libre_antecedente,
                "documento": self.antecedente_documento.get(),
                "numero": self.antecedente_numero.get(),
                "numero_letra": self.antecedente_numero_letra.get(),
                "volumen": self.antecedente_volumen.get(),
                "volumen_letra": self.antecedente_volumen_letra.get(),
                "fecha_texto": fecha_titulo_texto,
                "autoridad": self.antecedente_autoridad.get(),
                "ubicacion_autoridad": self.antecedente_ubicacion_autoridad.get(),
                "acto_adquisicion": self.antecedente_acto.get(),
            },
            transmitentes,
        )

        fecha_registro_texto = fecha_notarial(
            parsear_fecha(self.registro_fecha.get()), incluir_dias=False
        )
        datos_registro = construir_datos_registro(
            {
                "oficina": self.registro_oficina.get(),
                "tipo_asiento": self.registro_tipo_asiento.get(),
                "numero": self.registro_numero.get(),
                "numero_letra": self.registro_numero_letra.get(),
                "libro": self.registro_libro.get(),
                "libro_letra": self.registro_libro_letra.get(),
                "seccion": self.registro_seccion.get(),
                "seccion_letra": self.registro_seccion_letra.get(),
                "fecha_texto": fecha_registro_texto,
            }
        )
        declaracion_predial = construir_declaracion_predial(
            {
                "municipio": self.predial_municipio.get(),
                "estado": self.predial_estado.get(),
                "cuenta": self.cuenta_predial.get(),
                "clave_catastral": self.clave_catastral.get(),
            },
            denominacion_parte=config["parte_transmitente"],
        )

        escritura = {
            "acto": self.acto.get().strip(),
            "acto_titulo": config["titulo"],
            "libro_numero": self.libro_numero.get().strip(),
            "libro_letra": libro_letra,
            "numero": numero_escritura,
            "numero_letra": letra_escritura,
            "fecha_texto": fecha_notarial(fecha),
            "ciudad": self.ciudad.get().strip(),
            "estado": self.estado.get().strip(),
        }
        notario = {
            "nombre": self.notario_nombre.get().strip().upper(),
            "numero": self.notaria_numero.get().strip(),
            "numero_letra": notaria_letra,
            "distrito": self.distrito_judicial.get().strip(),
            "residencia": self.residencia_notaria.get().strip(),
        }
        inmueble = {
            "tipo": self.tipo_inmueble.get().strip(),
            "denominacion": self.denominacion_inmueble.get().strip(),
            "ubicacion": self.ubicacion_inmueble.get().strip(),
            "municipio": self.municipio_inmueble.get().strip(),
            "estado": self.estado_inmueble.get().strip(),
            "nombre_referencia": self.nombre_referencia_inmueble.get().strip(),
            "descripcion": self.descripcion_inmueble.get().strip(),
            "antecedente_propiedad": antecedente_propiedad,
            "datos_registro": datos_registro,
            "declaracion_predial": declaracion_predial,
            "medidas_colindancias": construir_texto_colindancias(
                self.grupos_colindancias
            ),
            "superficie": self.superficie.get().strip(),
            "unidad_superficie": self.unidad_superficie.get().strip(),
            "superficie_letra": self.superficie_letra.get().strip(),
            "avaluo_valor": self.avaluo_valor.get().strip(),
            "avaluo_valor_letra": self.avaluo_valor_letra.get().strip(),
        }
        operacion = {
            "importe": self.precio.get().strip(),
            "importe_letra": self.precio_letra.get().strip(),
            # Alias conservados para futuras plantillas heredadas.
            "precio": self.precio.get().strip(),
            "precio_letra": self.precio_letra.get().strip(),
        }
        campos = {
            config["campo_1"]["clave"]: self.campo_especifico_1.get().strip(),
            config["campo_2"]["clave"]: self.campo_especifico_2.get().strip(),
        }

        return {
            "escritura": escritura,
            "notario": notario,
            "acto": config,
            "introduccion_acto": construir_introduccion_acto(
                self.acto.get(), inmueble["descripcion"]
            ),
            "comparecientes": personas,
            "comparecientes_otorgamiento": construir_otorgamiento(personas),
            "comparecientes_datos_personales": construir_datos_personales(personas),
            "comparecientes_firmas": construir_firmas(personas),
            "transmitente": contexto_legacy_persona(transmitente),
            "adquirente": contexto_legacy_persona(adquirente),
            "vendedor": contexto_legacy_persona(transmitente),
            "comprador": contexto_legacy_persona(adquirente),
            "inmueble": inmueble,
            "operacion": operacion,
            "campos_especificos": campos,
            "clausulas_acto": construir_clausulas_acto(
                self.acto.get(), config, personas, inmueble, operacion, campos
            ),
            "cierre_apendice": construir_cierre_apendice(
                self.acto.get(), escritura, notario
            ),
        }

    def _generar_documento(self) -> None:
        if not self._validar_datos():
            return

        config = self._configuracion_actual()
        RUTA_SALIDAS.mkdir(parents=True, exist_ok=True)
        nombre_base = self.acto.get().lower().replace(" ", "_").replace("ó", "o")
        ruta = filedialog.asksaveasfilename(
            title="Guardar escritura",
            initialdir=RUTA_SALIDAS,
            initialfile=f"escritura_{nombre_base}_paso6.docx",
            defaultextension=".docx",
            filetypes=[("Documento de Word", "*.docx")],
        )
        if not ruta:
            return

        try:
            contexto = self._crear_contexto()
            archivo = self.generador.generar(
                contexto, ruta, nombre_plantilla=config["plantilla"]
            )
        except Exception as error:
            messagebox.showerror(
                "No se pudo generar",
                f"Ocurrió un error al crear el documento:\n\n{error}",
            )
            return

        self.estado_aplicacion.set(f"Documento generado: {archivo.name}")
        messagebox.showinfo(
            "Documento generado",
            f"La escritura se creó correctamente en:\n\n{archivo}",
        )
