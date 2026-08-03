from __future__ import annotations

import json
import threading
from pathlib import Path
from tkinter import filedialog, messagebox, ttk
from typing import Any, Callable

import customtkinter as ctk

from motor_word import generar_escritura
from redaccion import medida_a_letras, numero_a_letras

ctk.set_appearance_mode("System")
ctk.set_default_color_theme("blue")

BASE_DIR = Path(__file__).resolve().parent


class VentanaColindancia(ctk.CTkToplevel):
    CARDINALES = (
        "NORTE", "SUR", "ESTE", "OESTE", "ORIENTE", "PONIENTE",
        "NORESTE", "NOROESTE", "SURESTE", "SUROESTE",
    )
    TIPOS = (
        "PROPIEDAD DE", "CALLE", "CAMINO", "CARRETERA", "ARROYO",
        "RÍO", "BARRANCA", "PARCELA", "EJIDO", "OTRO",
    )

    def __init__(
        self,
        master: ctk.CTk,
        callback: Callable[[dict[str, Any]], None],
        datos: dict[str, Any] | None = None,
    ) -> None:
        super().__init__(master)
        self.callback = callback
        self.tramos: list[dict[str, str]] = []
        self.title("Grupo de colindancia")
        self.geometry("820x590")
        self.minsize(720, 520)
        self.transient(master)
        self.grab_set()

        self.grid_columnconfigure(0, weight=1)
        self.grid_rowconfigure(1, weight=1)

        cabecera = ctk.CTkFrame(self)
        cabecera.grid(row=0, column=0, sticky="ew", padx=16, pady=(16, 8))
        cabecera.grid_columnconfigure((0, 1, 2), weight=1)

        self.cardinal = ctk.StringVar(value="NORTE")
        self.tipo = ctk.StringVar(value="PROPIEDAD DE")
        self.colindante = ctk.StringVar()

        self._campo_combo(cabecera, "Punto cardinal", self.cardinal, self.CARDINALES, 0)
        self._campo_combo(cabecera, "Tipo de colindante", self.tipo, self.TIPOS, 1)
        self._campo_entry(cabecera, "Nombre o descripción", self.colindante, 2)

        cuerpo = ctk.CTkFrame(self)
        cuerpo.grid(row=1, column=0, sticky="nsew", padx=16, pady=8)
        cuerpo.grid_columnconfigure(0, weight=1)
        cuerpo.grid_rowconfigure(2, weight=1)

        captura = ctk.CTkFrame(cuerpo, fg_color="transparent")
        captura.grid(row=0, column=0, sticky="ew", padx=12, pady=(12, 4))
        captura.grid_columnconfigure(1, weight=1)
        captura.grid_columnconfigure(3, weight=2)

        ctk.CTkLabel(captura, text="Medida numérica").grid(row=0, column=0, padx=6, pady=6)
        self.medida = ctk.StringVar()
        ctk.CTkEntry(captura, textvariable=self.medida, width=140).grid(row=0, column=1, sticky="ew", padx=6, pady=6)

        ctk.CTkLabel(captura, text="Medida en letra").grid(row=0, column=2, padx=6, pady=6)
        self.medida_letra = ctk.StringVar()
        ctk.CTkEntry(captura, textvariable=self.medida_letra).grid(row=0, column=3, sticky="ew", padx=6, pady=6)

        ctk.CTkButton(captura, text="Convertir", width=90, command=self._convertir).grid(row=0, column=4, padx=6, pady=6)
        ctk.CTkButton(captura, text="Agregar tramo", command=self._agregar_tramo).grid(row=0, column=5, padx=6, pady=6)

        ctk.CTkLabel(cuerpo, text="Tramos capturados", font=ctk.CTkFont(size=15, weight="bold")).grid(
            row=1, column=0, sticky="w", padx=14, pady=(8, 4)
        )

        tabla_frame = ctk.CTkFrame(cuerpo)
        tabla_frame.grid(row=2, column=0, sticky="nsew", padx=12, pady=4)
        tabla_frame.grid_columnconfigure(0, weight=1)
        tabla_frame.grid_rowconfigure(0, weight=1)

        self.tabla = ttk.Treeview(tabla_frame, columns=("numero", "medida", "letra"), show="headings")
        self.tabla.heading("numero", text="#")
        self.tabla.heading("medida", text="Medida")
        self.tabla.heading("letra", text="Medida en letra")
        self.tabla.column("numero", width=45, anchor="center")
        self.tabla.column("medida", width=110, anchor="center")
        self.tabla.column("letra", width=520)
        self.tabla.grid(row=0, column=0, sticky="nsew")
        scroll = ttk.Scrollbar(tabla_frame, orient="vertical", command=self.tabla.yview)
        scroll.grid(row=0, column=1, sticky="ns")
        self.tabla.configure(yscrollcommand=scroll.set)

        acciones = ctk.CTkFrame(cuerpo, fg_color="transparent")
        acciones.grid(row=3, column=0, sticky="ew", padx=12, pady=8)
        ctk.CTkButton(acciones, text="Eliminar tramo", fg_color="#a33", hover_color="#822", command=self._eliminar_tramo).pack(side="left")

        pie = ctk.CTkFrame(self, fg_color="transparent")
        pie.grid(row=2, column=0, sticky="ew", padx=16, pady=(8, 16))
        ctk.CTkButton(pie, text="Cancelar", fg_color="gray45", command=self.destroy).pack(side="right", padx=6)
        ctk.CTkButton(pie, text="Guardar grupo", command=self._guardar).pack(side="right", padx=6)

        if datos:
            self.cardinal.set(str(datos.get("cardinal", "NORTE")))
            self.tipo.set(str(datos.get("tipo_colindante", "PROPIEDAD DE")))
            self.colindante.set(str(datos.get("colindante", "")))
            self.tramos = [dict(t) for t in datos.get("tramos", [])]
            self._actualizar_tabla()

    def _campo_combo(self, parent, titulo, variable, valores, columna):
        marco = ctk.CTkFrame(parent, fg_color="transparent")
        marco.grid(row=0, column=columna, sticky="ew", padx=8, pady=8)
        ctk.CTkLabel(marco, text=titulo).pack(anchor="w")
        ctk.CTkComboBox(marco, variable=variable, values=list(valores)).pack(fill="x", pady=(4, 0))

    def _campo_entry(self, parent, titulo, variable, columna):
        marco = ctk.CTkFrame(parent, fg_color="transparent")
        marco.grid(row=0, column=columna, sticky="ew", padx=8, pady=8)
        ctk.CTkLabel(marco, text=titulo).pack(anchor="w")
        ctk.CTkEntry(marco, textvariable=variable).pack(fill="x", pady=(4, 0))

    def _convertir(self) -> None:
        self.medida_letra.set(medida_a_letras(self.medida.get()))

    def _agregar_tramo(self) -> None:
        medida = self.medida.get().strip()
        if not medida:
            messagebox.showwarning("Dato faltante", "Escribe la medida numérica.", parent=self)
            return
        letra = self.medida_letra.get().strip() or medida_a_letras(medida)
        self.tramos.append({"medida": medida, "medida_letra": letra})
        self.medida.set("")
        self.medida_letra.set("")
        self._actualizar_tabla()

    def _eliminar_tramo(self) -> None:
        seleccion = self.tabla.selection()
        if not seleccion:
            return
        indice = int(self.tabla.item(seleccion[0], "values")[0]) - 1
        if 0 <= indice < len(self.tramos):
            self.tramos.pop(indice)
            self._actualizar_tabla()

    def _actualizar_tabla(self) -> None:
        for item in self.tabla.get_children():
            self.tabla.delete(item)
        for indice, tramo in enumerate(self.tramos, start=1):
            self.tabla.insert("", "end", values=(indice, tramo["medida"], tramo["medida_letra"]))

    def _guardar(self) -> None:
        if not self.colindante.get().strip():
            messagebox.showwarning("Dato faltante", "Escribe el colindante o la descripción.", parent=self)
            return
        if not self.tramos:
            messagebox.showwarning("Dato faltante", "Agrega al menos un tramo.", parent=self)
            return
        self.callback({
            "cardinal": self.cardinal.get().strip().upper(),
            "tipo_colindante": self.tipo.get().strip().upper(),
            "colindante": self.colindante.get().strip(),
            "tramos": self.tramos,
        })
        self.destroy()


class AplicacionEscrituras(ctk.CTk):
    def __init__(self) -> None:
        super().__init__()
        self.title("Sistema de Escrituras Notariales — Compraventa")
        self.geometry("1280x820")
        self.minsize(1080, 700)
        self.colindancias: list[dict[str, Any]] = []
        self.campos: dict[str, ctk.StringVar] = {}
        self.booleanos: dict[str, ctk.BooleanVar] = {}

        self.grid_columnconfigure(0, weight=1)
        self.grid_rowconfigure(1, weight=1)

        encabezado = ctk.CTkFrame(self, corner_radius=0)
        encabezado.grid(row=0, column=0, sticky="ew")
        encabezado.grid_columnconfigure(0, weight=1)
        ctk.CTkLabel(
            encabezado,
            text="Generador de Escritura de Compraventa",
            font=ctk.CTkFont(size=22, weight="bold"),
        ).grid(row=0, column=0, sticky="w", padx=22, pady=16)
        ctk.CTkLabel(
            encabezado,
            text="Motor de formato: Microsoft Word",
            text_color="gray65",
        ).grid(row=0, column=1, padx=22, pady=16)

        self.tabs = ctk.CTkTabview(self)
        self.tabs.grid(row=1, column=0, sticky="nsew", padx=14, pady=12)
        for nombre in (
            "Datos generales", "Vendedor", "Comprador", "Inmueble",
            "Antecedente y operación", "Colindancias", "Salida",
        ):
            self.tabs.add(nombre)

        self._crear_generales()
        self._crear_persona("Vendedor", "vendedor")
        self._crear_persona("Comprador", "comprador")
        self._crear_inmueble()
        self._crear_antecedente_operacion()
        self._crear_colindancias()
        self._crear_salida()

        pie = ctk.CTkFrame(self, corner_radius=0)
        pie.grid(row=2, column=0, sticky="ew")
        pie.grid_columnconfigure(0, weight=1)
        self.estado = ctk.StringVar(value="Listo para capturar datos.")
        ctk.CTkLabel(pie, textvariable=self.estado).grid(row=0, column=0, sticky="w", padx=18, pady=14)
        ctk.CTkButton(pie, text="Cargar borrador", fg_color="gray40", command=self.cargar_borrador).grid(row=0, column=1, padx=6, pady=10)
        ctk.CTkButton(pie, text="Guardar borrador", fg_color="gray40", command=self.guardar_borrador).grid(row=0, column=2, padx=6, pady=10)
        self.boton_generar = ctk.CTkButton(pie, text="Generar documento Word", width=210, command=self.generar)
        self.boton_generar.grid(row=0, column=3, padx=(6, 18), pady=10)

        self._cargar_valores_iniciales()

    def _scroll(self, tab: str) -> ctk.CTkScrollableFrame:
        frame = ctk.CTkScrollableFrame(self.tabs.tab(tab))
        frame.pack(fill="both", expand=True, padx=8, pady=8)
        frame.grid_columnconfigure(0, weight=1)
        return frame

    def _seccion(self, parent, titulo: str, fila: int) -> ctk.CTkFrame:
        marco = ctk.CTkFrame(parent)
        marco.grid(row=fila, column=0, sticky="ew", padx=8, pady=8)
        marco.grid_columnconfigure((0, 1), weight=1)
        ctk.CTkLabel(marco, text=titulo, font=ctk.CTkFont(size=16, weight="bold")).grid(
            row=0, column=0, columnspan=2, sticky="w", padx=14, pady=(12, 8)
        )
        return marco

    def _entry(self, parent, etiqueta: str, clave: str, fila: int, columna: int = 0, *, ancho_columnas: int = 1) -> None:
        variable = self.campos.setdefault(clave, ctk.StringVar())
        bloque = ctk.CTkFrame(parent, fg_color="transparent")
        bloque.grid(row=fila, column=columna, columnspan=ancho_columnas, sticky="ew", padx=12, pady=6)
        bloque.grid_columnconfigure(0, weight=1)
        ctk.CTkLabel(bloque, text=etiqueta).grid(row=0, column=0, sticky="w")
        ctk.CTkEntry(bloque, textvariable=variable).grid(row=1, column=0, sticky="ew", pady=(3, 0))

    def _combo(self, parent, etiqueta: str, clave: str, valores: list[str], fila: int, columna: int = 0) -> None:
        variable = self.campos.setdefault(clave, ctk.StringVar())
        bloque = ctk.CTkFrame(parent, fg_color="transparent")
        bloque.grid(row=fila, column=columna, sticky="ew", padx=12, pady=6)
        bloque.grid_columnconfigure(0, weight=1)
        ctk.CTkLabel(bloque, text=etiqueta).grid(row=0, column=0, sticky="w")
        ctk.CTkComboBox(bloque, variable=variable, values=valores).grid(row=1, column=0, sticky="ew", pady=(3, 0))

    def _textbox(self, parent, etiqueta: str, clave: str, fila: int, altura: int = 140) -> ctk.CTkTextbox:
        bloque = ctk.CTkFrame(parent, fg_color="transparent")
        bloque.grid(row=fila, column=0, columnspan=2, sticky="ew", padx=12, pady=8)
        bloque.grid_columnconfigure(0, weight=1)
        ctk.CTkLabel(bloque, text=etiqueta).grid(row=0, column=0, sticky="w")
        caja = ctk.CTkTextbox(bloque, height=altura, wrap="word")
        caja.grid(row=1, column=0, sticky="ew", pady=(4, 0))
        setattr(self, f"textbox_{clave}", caja)
        return caja

    def _crear_generales(self) -> None:
        cont = self._scroll("Datos generales")
        sec = self._seccion(cont, "Identificación del instrumento", 0)
        self._entry(sec, "Número de libro", "libro_numero", 1, 0)
        self._entry(sec, "Libro en letra", "libro_letra", 1, 1)
        self._entry(sec, "Número de escritura", "escritura_numero", 2, 0)
        self._entry(sec, "Escritura en letra", "escritura_letra", 2, 1)
        self._entry(sec, "Fecha del instrumento (DD/MM/AAAA)", "fecha_instrumento", 3, 0)
        ctk.CTkButton(sec, text="Convertir números a letra", command=self._convertir_generales).grid(row=3, column=1, padx=12, pady=(28, 6), sticky="ew")

        aviso = ctk.CTkLabel(
            cont,
            text=(
                "La ciudad, notaría, distrito y residencia permanecen como en la matriz oficial. "
                "Esta primera integración se concentra en los datos variables de la compraventa."
            ),
            wraplength=900,
            justify="left",
            text_color="gray65",
        )
        aviso.grid(row=1, column=0, sticky="w", padx=18, pady=12)

    def _crear_persona(self, tab: str, prefijo: str) -> None:
        cont = self._scroll(tab)
        sec = self._seccion(cont, f"Datos de la parte {tab.lower()}", 0)
        self._entry(sec, "Nombre completo", f"{prefijo}_nombre", 1, 0, ancho_columnas=2)
        self._combo(sec, "Sexo", f"{prefijo}_sexo", ["MASCULINO", "FEMENINO"], 2, 0)
        self._entry(sec, "Fecha de nacimiento (DD/MM/AAAA)", f"{prefijo}_fecha_nacimiento", 2, 1)
        self._entry(sec, "Originario(a) de", f"{prefijo}_origen", 3, 0)
        self._entry(sec, "Vecino(a) de", f"{prefijo}_vecindad", 3, 1)
        self._entry(sec, "Domicilio", f"{prefijo}_domicilio", 4, 0)
        self._entry(sec, "Código Postal", f"{prefijo}_codigo_postal", 4, 1)
        self._entry(sec, "Estado civil", f"{prefijo}_estado_civil", 5, 0)
        self._entry(sec, "Ocupación", f"{prefijo}_ocupacion", 5, 1)
        self._entry(sec, "RFC", f"{prefijo}_rfc", 6, 0)
        self._entry(sec, "CURP", f"{prefijo}_curp", 6, 1)
        self._entry(sec, "Número de INE", f"{prefijo}_ine", 7, 0)
        self._entry(sec, "Nacionalidad", f"{prefijo}_nacionalidad", 7, 1)
        variable = self.booleanos.setdefault(f"{prefijo}_sabe_firmar", ctk.BooleanVar(value=True))
        ctk.CTkCheckBox(sec, text="Declara saber firmar", variable=variable).grid(row=8, column=0, sticky="w", padx=14, pady=12)

    def _crear_inmueble(self) -> None:
        cont = self._scroll("Inmueble")
        sec = self._seccion(cont, "Descripción del inmueble", 0)
        self._entry(sec, "Tipo de inmueble", "tipo_inmueble", 1, 0)
        self._entry(sec, "Denominación", "denominacion", 1, 1)
        self._entry(sec, "Ubicación o localidad", "ubicacion", 2, 0)
        self._entry(sec, "Municipio", "municipio", 2, 1)
        self._entry(sec, "Estado", "estado_inmueble", 3, 0)
        self._entry(sec, "Nombre de referencia", "nombre_referencia", 3, 1)
        self._textbox(sec, "Descripción final (opcional; si queda vacía se construye automáticamente)", "descripcion_inmueble", 4, 100)

        sup = self._seccion(cont, "Superficie y registro", 1)
        self._entry(sup, "Superficie", "superficie", 1, 0)
        self._combo(sup, "Unidad", "unidad_superficie", ["M2", "Ha", "M²", "OTRA"], 1, 1)
        self._entry(sup, "Superficie en letra", "superficie_letra", 2, 0, ancho_columnas=2)
        self._textbox(sup, "Datos de registro (redacción completa)", "datos_registro", 3, 130)

    def _crear_antecedente_operacion(self) -> None:
        cont = self._scroll("Antecedente y operación")
        ant = self._seccion(cont, "Antecedente de propiedad", 0)
        self._textbox(ant, "Redacción libre del antecedente", "antecedente_propiedad", 1, 190)

        op = self._seccion(cont, "Valores y declaraciones", 1)
        self._entry(op, "Valor del avalúo", "avaluo", 1, 0)
        self._entry(op, "Avalúo en letra", "avaluo_letra", 1, 1)
        self._entry(op, "Precio de compraventa", "precio", 2, 0)
        self._entry(op, "Precio en letra", "precio_letra", 2, 1)
        self._textbox(op, "Declaración predial", "declaracion_predial", 3, 150)
        ctk.CTkButton(op, text="Convertir valores a letra", command=self._convertir_valores).grid(row=4, column=0, columnspan=2, padx=12, pady=12, sticky="ew")

    def _crear_colindancias(self) -> None:
        tab = self.tabs.tab("Colindancias")
        tab.grid_columnconfigure(0, weight=1)
        tab.grid_rowconfigure(1, weight=1)
        barra = ctk.CTkFrame(tab)
        barra.grid(row=0, column=0, sticky="ew", padx=10, pady=10)
        ctk.CTkButton(barra, text="Agregar grupo", command=self.agregar_colindancia).pack(side="left", padx=5, pady=8)
        ctk.CTkButton(barra, text="Editar", command=self.editar_colindancia).pack(side="left", padx=5, pady=8)
        ctk.CTkButton(barra, text="Eliminar", fg_color="#a33", hover_color="#822", command=self.eliminar_colindancia).pack(side="left", padx=5, pady=8)
        ctk.CTkLabel(
            barra,
            text="Un mismo punto cardinal puede registrarse en varios grupos cuando cambia el colindante.",
            text_color="gray65",
        ).pack(side="right", padx=10)

        marco = ctk.CTkFrame(tab)
        marco.grid(row=1, column=0, sticky="nsew", padx=10, pady=(0, 10))
        marco.grid_columnconfigure(0, weight=1)
        marco.grid_rowconfigure(0, weight=1)
        self.tabla_colindancias = ttk.Treeview(
            marco,
            columns=("numero", "cardinal", "tipo", "colindante", "tramos"),
            show="headings",
        )
        for col, titulo, ancho in (
            ("numero", "#", 45), ("cardinal", "Cardinal", 100),
            ("tipo", "Tipo", 135), ("colindante", "Colindante", 390),
            ("tramos", "Tramos", 90),
        ):
            self.tabla_colindancias.heading(col, text=titulo)
            self.tabla_colindancias.column(col, width=ancho, anchor="center" if col in {"numero", "cardinal", "tramos"} else "w")
        self.tabla_colindancias.grid(row=0, column=0, sticky="nsew")
        scroll = ttk.Scrollbar(marco, orient="vertical", command=self.tabla_colindancias.yview)
        scroll.grid(row=0, column=1, sticky="ns")
        self.tabla_colindancias.configure(yscrollcommand=scroll.set)
        self.tabla_colindancias.bind("<Double-1>", lambda _e: self.editar_colindancia())

    def _crear_salida(self) -> None:
        cont = self._scroll("Salida")
        sec = self._seccion(cont, "Documento final", 0)
        self._entry(sec, "Beneficiario del primer testimonio", "beneficiario_testimonio", 1, 0, ancho_columnas=2)
        self._entry(sec, "Nombre sugerido del archivo", "nombre_salida", 2, 0, ancho_columnas=2)
        ctk.CTkLabel(
            sec,
            text=(
                "Al generar, Microsoft Word abrirá la matriz oficial, reemplazará los datos, "
                "actualizará la paginación y guardará una copia nueva."
            ),
            wraplength=850,
            justify="left",
            text_color="gray65",
        ).grid(row=3, column=0, columnspan=2, sticky="w", padx=14, pady=14)

    def _cargar_valores_iniciales(self) -> None:
        valores = {
            "libro_numero": "500", "libro_letra": "QUINIENTOS",
            "escritura_numero": "19,900", "escritura_letra": "DIECINUEVE MIL NOVECIENTOS",
            "fecha_instrumento": "27/03/2026",
            "vendedor_nombre": "ÁNGEL ALONSO RODRÍGUEZ DOMÍNGUEZ",
            "vendedor_sexo": "MASCULINO", "vendedor_fecha_nacimiento": "23/12/1998",
            "vendedor_origen": "Tulancingo de Bravo, Estado de Hidalgo",
            "vendedor_vecindad": "Tulancingo de Bravo, Estado de Hidalgo",
            "vendedor_domicilio": "Doria Oriente 105", "vendedor_codigo_postal": "43600",
            "vendedor_estado_civil": "soltero", "vendedor_ocupacion": "estudiante",
            "vendedor_rfc": "ASDECVFRT123", "vendedor_curp": "ASDCVFRMONO1234567",
            "vendedor_ine": "123456789000", "vendedor_nacionalidad": "mexicana",
            "comprador_nombre": "MARIAN GARCÍA CANALES", "comprador_sexo": "FEMENINO",
            "comprador_fecha_nacimiento": "24/01/1996",
            "comprador_origen": "Tulancingo de Bravo, Estado de Hidalgo",
            "comprador_vecindad": "Tulancingo de Bravo, Estado de Hidalgo",
            "comprador_domicilio": "Corregidora 205", "comprador_codigo_postal": "43560",
            "comprador_estado_civil": "soltera", "comprador_ocupacion": "estudiante",
            "comprador_rfc": "QWERTYUIOP12", "comprador_curp": "ASWDERFGTBN1234ER5",
            "comprador_ine": "1234567890999", "comprador_nacionalidad": "mexicana",
            "tipo_inmueble": "PREDIO RÚSTICO", "denominacion": "ACOCUL",
            "ubicacion": "MIRADOR", "municipio": "AGUA BLANCA DE ITURBIDE",
            "estado_inmueble": "HIDALGO", "nombre_referencia": "SAN MATEO",
            "superficie": "10,000", "unidad_superficie": "M2",
            "superficie_letra": "DIEZ MIL METROS CUADRADOS",
            "avaluo": "50,000.00", "avaluo_letra": "cincuenta mil",
            "precio": "25,000.00", "precio_letra": "veinticinco mil",
            "beneficiario_testimonio": "MARIAN GARCÍA CANALES",
            "nombre_salida": "ESCRITURA_COMPRAVENTA.docx",
        }
        for clave, valor in valores.items():
            if clave in self.campos:
                self.campos[clave].set(valor)

        self.textbox_antecedente_propiedad.insert(
            "1.0",
            "Declara el señor ÁNGEL ALONSO RODRÍGUEZ DOMÍNGUEZ, de manera expresa y bajo protesta de decir verdad, que por instrumento notarial número 8,071 ocho mil setenta y uno, libro 154 ciento cincuenta y cuatro, de fecha 03 tres de enero de 2022 dos mil veintidós, pasado ante la fe del Licenciado ALDO AMAURY VILLEGAS GARCÍA, Notario Titular de la Notaría Número 10 diez del Distrito Judicial de Tulancingo de Bravo, Hidalgo, adquirió en legítima propiedad el predio de referencia, mismo que contiene las siguientes."
        )
        self.textbox_datos_registro.insert(
            "1.0",
            "Dicha propiedad se encuentra inscrita ante el Registro Público de la Propiedad y del Comercio de Tulancingo de Bravo, Estado de Hidalgo, bajo Folio Real número 135627 ciento treinta y cinco mil seiscientos veintisiete, de fecha 29 veintinueve de marzo de 2022 dos mil veintidós."
        )
        self.textbox_declaracion_predial.insert(
            "1.0",
            "Finalmente declara la parte vendedora que el inmueble materia del presente contrato se encuentra inscrito a su nombre en el padrón de la propiedad raíz del Municipio de Agua Blanca de Iturbide, Estado de Hidalgo, y que a la fecha no reporta adeudo por concepto de impuesto predial, lo que acreditará con la documentación correspondiente."
        )
        self.colindancias = [
            {
                "cardinal": "NORTE",
                "tipo_colindante": "PROPIEDAD DE",
                "colindante": "HUGO SÁNCHEZ BORBOJA",
                "tramos": [
                    {"medida": "20.00", "medida_letra": "veinte metros con cero centímetros"},
                    {"medida": "12.10", "medida_letra": "doce metros con diez centímetros"},
                ],
            },
            {
                "cardinal": "SUR",
                "tipo_colindante": "PROPIEDAD DE",
                "colindante": "LUIS DE LA MADRID TORRES",
                "tramos": [{"medida": "11.12", "medida_letra": "once metros con doce centímetros"}],
            },
            {
                "cardinal": "OESTE",
                "tipo_colindante": "PROPIEDAD DE",
                "colindante": "LUCA MENDIOLA LAGOS",
                "tramos": [{"medida": "20.00", "medida_letra": "veinte metros con cero centímetros"}],
            },
            {
                "cardinal": "NOROESTE",
                "tipo_colindante": "PROPIEDAD DE",
                "colindante": "LUIS ALBERTO DE LA CRUZ GÓMEZ",
                "tramos": [
                    {"medida": "9.80", "medida_letra": "nueve metros con ochenta centímetros"},
                    {"medida": "11.12", "medida_letra": "once metros con doce centímetros"},
                ],
            },
        ]
        self._actualizar_colindancias()

    def _convertir_generales(self) -> None:
        self.campos["libro_letra"].set(numero_a_letras(self.campos["libro_numero"].get()))
        self.campos["escritura_letra"].set(numero_a_letras(self.campos["escritura_numero"].get()))

    def _convertir_valores(self) -> None:
        from redaccion import cantidad_a_letras
        self.campos["avaluo_letra"].set(cantidad_a_letras(self.campos["avaluo"].get()))
        self.campos["precio_letra"].set(cantidad_a_letras(self.campos["precio"].get()))

    def agregar_colindancia(self) -> None:
        VentanaColindancia(self, self._guardar_nueva_colindancia)

    def _guardar_nueva_colindancia(self, datos: dict[str, Any]) -> None:
        self.colindancias.append(datos)
        self._actualizar_colindancias()

    def _indice_colindancia(self) -> int | None:
        seleccion = self.tabla_colindancias.selection()
        if not seleccion:
            return None
        return int(self.tabla_colindancias.item(seleccion[0], "values")[0]) - 1

    def editar_colindancia(self) -> None:
        indice = self._indice_colindancia()
        if indice is None:
            return
        def guardar(datos: dict[str, Any]) -> None:
            self.colindancias[indice] = datos
            self._actualizar_colindancias()
        VentanaColindancia(self, guardar, self.colindancias[indice])

    def eliminar_colindancia(self) -> None:
        indice = self._indice_colindancia()
        if indice is None:
            return
        if messagebox.askyesno("Eliminar", "¿Eliminar este grupo de colindancia?"):
            self.colindancias.pop(indice)
            self._actualizar_colindancias()

    def _actualizar_colindancias(self) -> None:
        for item in self.tabla_colindancias.get_children():
            self.tabla_colindancias.delete(item)
        for indice, grupo in enumerate(self.colindancias, start=1):
            self.tabla_colindancias.insert(
                "", "end",
                values=(indice, grupo["cardinal"], grupo["tipo_colindante"], grupo["colindante"], len(grupo["tramos"])),
            )

    def _persona(self, prefijo: str) -> dict[str, Any]:
        return {
            "nombre": self.campos[f"{prefijo}_nombre"].get(),
            "sexo": self.campos[f"{prefijo}_sexo"].get(),
            "fecha_nacimiento": self.campos[f"{prefijo}_fecha_nacimiento"].get(),
            "origen": self.campos[f"{prefijo}_origen"].get(),
            "vecindad": self.campos[f"{prefijo}_vecindad"].get(),
            "domicilio": self.campos[f"{prefijo}_domicilio"].get(),
            "codigo_postal": self.campos[f"{prefijo}_codigo_postal"].get(),
            "estado_civil": self.campos[f"{prefijo}_estado_civil"].get(),
            "ocupacion": self.campos[f"{prefijo}_ocupacion"].get(),
            "rfc": self.campos[f"{prefijo}_rfc"].get(),
            "curp": self.campos[f"{prefijo}_curp"].get(),
            "ine": self.campos[f"{prefijo}_ine"].get(),
            "nacionalidad": self.campos[f"{prefijo}_nacionalidad"].get(),
            "sabe_firmar": self.booleanos[f"{prefijo}_sabe_firmar"].get(),
        }

    def recopilar(self) -> dict[str, Any]:
        datos: dict[str, Any] = {clave: variable.get() for clave, variable in self.campos.items()}
        datos["vendedor"] = self._persona("vendedor")
        datos["comprador"] = self._persona("comprador")
        datos["descripcion_inmueble"] = self.textbox_descripcion_inmueble.get("1.0", "end").strip()
        datos["antecedente_propiedad"] = self.textbox_antecedente_propiedad.get("1.0", "end").strip()
        datos["datos_registro"] = self.textbox_datos_registro.get("1.0", "end").strip()
        datos["declaracion_predial"] = self.textbox_declaracion_predial.get("1.0", "end").strip()
        datos["colindancias"] = self.colindancias
        return datos

    def validar(self, datos: dict[str, Any]) -> list[str]:
        faltantes: list[str] = []
        requeridos = {
            "libro_numero": "Número de libro",
            "escritura_numero": "Número de escritura",
            "fecha_instrumento": "Fecha del instrumento",
            "superficie": "Superficie",
            "datos_registro": "Datos registrales",
            "avaluo": "Avalúo",
            "precio": "Precio",
        }
        for clave, etiqueta in requeridos.items():
            if not str(datos.get(clave, "")).strip():
                faltantes.append(etiqueta)
        for parte, etiqueta in (("vendedor", "Vendedor"), ("comprador", "Comprador")):
            persona = datos[parte]
            for clave in ("nombre", "fecha_nacimiento", "domicilio", "rfc", "curp"):
                if not str(persona.get(clave, "")).strip():
                    faltantes.append(f"{etiqueta}: {clave.replace('_', ' ')}")
        if not datos["antecedente_propiedad"]:
            faltantes.append("Antecedente de propiedad")
        if not self.colindancias:
            faltantes.append("Al menos una colindancia")
        return faltantes

    def guardar_borrador(self) -> None:
        datos = self.recopilar()
        ruta = filedialog.asksaveasfilename(
            title="Guardar borrador",
            initialdir=BASE_DIR / "borradores",
            defaultextension=".json",
            filetypes=[("Borrador JSON", "*.json")],
        )
        if not ruta:
            return
        Path(ruta).write_text(json.dumps(datos, ensure_ascii=False, indent=2), encoding="utf-8")
        self.estado.set(f"Borrador guardado: {Path(ruta).name}")

    def cargar_borrador(self) -> None:
        ruta = filedialog.askopenfilename(
            title="Cargar borrador",
            initialdir=BASE_DIR / "borradores",
            filetypes=[("Borrador JSON", "*.json")],
        )
        if not ruta:
            return
        datos = json.loads(Path(ruta).read_text(encoding="utf-8"))
        for clave, variable in self.campos.items():
            if clave in datos:
                variable.set(str(datos[clave]))
        for prefijo in ("vendedor", "comprador"):
            persona = datos.get(prefijo, {})
            for clave, valor in persona.items():
                nombre = f"{prefijo}_{clave}"
                if nombre in self.campos:
                    self.campos[nombre].set(str(valor))
                elif nombre in self.booleanos:
                    self.booleanos[nombre].set(bool(valor))
        for clave in ("descripcion_inmueble", "antecedente_propiedad", "datos_registro", "declaracion_predial"):
            caja = getattr(self, f"textbox_{clave}")
            caja.delete("1.0", "end")
            caja.insert("1.0", datos.get(clave, ""))
        self.colindancias = datos.get("colindancias", [])
        self._actualizar_colindancias()
        self.estado.set(f"Borrador cargado: {Path(ruta).name}")

    def generar(self) -> None:
        datos = self.recopilar()
        faltantes = self.validar(datos)
        if faltantes:
            messagebox.showwarning(
                "Datos faltantes",
                "Completa los siguientes datos:\n\n- " + "\n- ".join(faltantes),
            )
            return

        nombre = self.campos["nombre_salida"].get().strip() or "ESCRITURA_COMPRAVENTA.docx"
        if not nombre.lower().endswith(".docx"):
            nombre += ".docx"
        ruta = filedialog.asksaveasfilename(
            title="Guardar escritura",
            initialdir=BASE_DIR / "salidas",
            initialfile=nombre,
            defaultextension=".docx",
            filetypes=[("Documento Word", "*.docx")],
        )
        if not ruta:
            return

        self.boton_generar.configure(state="disabled", text="Generando...")
        self.estado.set("Microsoft Word está generando el documento. No cierres Word.")

        def trabajo() -> None:
            try:
                import pythoncom
                pythoncom.CoInitialize()
                try:
                    salida = generar_escritura(datos, ruta)
                finally:
                    pythoncom.CoUninitialize()
                self.after(0, lambda: self._generacion_exitosa(salida))
            except Exception as exc:
                self.after(0, lambda error=exc: self._generacion_fallida(error))

        threading.Thread(target=trabajo, daemon=True).start()

    def _generacion_exitosa(self, salida: Path) -> None:
        self.boton_generar.configure(state="normal", text="Generar documento Word")
        self.estado.set(f"Documento generado: {salida.name}")
        messagebox.showinfo("Documento generado", f"La escritura se guardó correctamente en:\n\n{salida}")

    def _generacion_fallida(self, error: Exception) -> None:
        self.boton_generar.configure(state="normal", text="Generar documento Word")
        self.estado.set("No fue posible generar el documento.")
        messagebox.showerror(
            "Error al generar",
            f"No fue posible generar el Word:\n\n{error}\n\n"
            "Cierra los documentos de Word abiertos y revisa el archivo de registro junto a la salida.",
        )
