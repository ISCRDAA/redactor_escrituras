from __future__ import annotations

import tkinter as tk
from copy import deepcopy
from tkinter import messagebox, ttk
from typing import Any, Callable

from utilidades import (
    CALIDADES,
    ESTADOS_CIVILES,
    PUNTOS_CARDINALES,
    SEXOS,
    TIPOS_COLINDANTE,
    calcular_edad,
    numero_a_letras,
    parsear_fecha,
    son_lugares_iguales,
)


class VentanaCompareciente(tk.Toplevel):
    """Formulario desplazable para agregar o editar una persona."""

    def __init__(
        self,
        padre: tk.Misc,
        fecha_referencia: Callable[[], Any],
        al_guardar: Callable[[dict[str, Any]], None],
        persona_existente: dict[str, Any] | None = None,
        calidades_permitidas: tuple[str, ...] | None = None,
    ) -> None:
        super().__init__(padre)
        self.title("Compareciente")
        self.geometry("760x690")
        self.minsize(680, 560)
        self.transient(padre)
        self.grab_set()

        self.fecha_referencia = fecha_referencia
        self.al_guardar = al_guardar
        self.calidades_permitidas = calidades_permitidas or CALIDADES

        self.variables: dict[str, tk.Variable] = {
            "nombre": tk.StringVar(),
            "sexo": tk.StringVar(value=SEXOS[0]),
            "calidad": tk.StringVar(value=self.calidades_permitidas[0]),
            "originario": tk.StringVar(),
            "vecino": tk.StringVar(),
            "mismo_origen_vecindad": tk.BooleanVar(value=False),
            "domicilio": tk.StringVar(),
            "codigo_postal": tk.StringVar(),
            "fecha_nacimiento": tk.StringVar(),
            "edad_numero": tk.StringVar(),
            "edad_letra": tk.StringVar(),
            "estado_civil": tk.StringVar(value=ESTADOS_CIVILES[0]),
            "ocupacion": tk.StringVar(),
            "rfc": tk.StringVar(),
            "curp": tk.StringVar(),
            "numero_ine": tk.StringVar(),
            "nacionalidad": tk.StringVar(value="MEXICANA"),
            "sabe_firmar": tk.BooleanVar(value=True),
        }

        self._crear_interfaz()
        if persona_existente:
            self._cargar_persona(persona_existente)

        self.protocol("WM_DELETE_WINDOW", self.destroy)

    def _crear_interfaz(self) -> None:
        exterior = ttk.Frame(self, padding=(12, 12, 4, 12))
        exterior.pack(fill="both", expand=True)
        exterior.columnconfigure(0, weight=1)
        exterior.rowconfigure(0, weight=1)

        canvas = tk.Canvas(exterior, highlightthickness=0)
        barra = ttk.Scrollbar(exterior, orient="vertical", command=canvas.yview)
        canvas.configure(yscrollcommand=barra.set)
        canvas.grid(row=0, column=0, sticky="nsew")
        barra.grid(row=0, column=1, sticky="ns")

        contenido = ttk.Frame(canvas, padding=8)
        ventana = canvas.create_window((0, 0), window=contenido, anchor="nw")

        contenido.bind(
            "<Configure>",
            lambda _evento: canvas.configure(scrollregion=canvas.bbox("all")),
        )
        canvas.bind(
            "<Configure>",
            lambda evento: canvas.itemconfigure(ventana, width=evento.width),
        )
        canvas.bind_all(
            "<MouseWheel>",
            lambda evento: canvas.yview_scroll(int(-1 * (evento.delta / 120)), "units"),
        )

        contenido.columnconfigure(1, weight=1)

        ttk.Label(
            contenido,
            text="Datos del compareciente",
            font=("Arial", 15, "bold"),
        ).grid(row=0, column=0, columnspan=2, sticky="w", pady=(0, 14))

        fila = 1
        fila = self._campo(contenido, fila, "Nombre completo:", "nombre")
        fila = self._combo(contenido, fila, "Sexo:", "sexo", SEXOS)
        fila = self._combo(
            contenido,
            fila,
            "Calidad jurídica:",
            "calidad",
            self.calidades_permitidas,
        )
        fila = self._campo(
            contenido,
            fila,
            "Originario de:",
            "originario",
            "Ejemplo: Zacualpan, Estado de Veracruz",
        )

        ttk.Checkbutton(
            contenido,
            text="El lugar de origen y vecindad es el mismo",
            variable=self.variables["mismo_origen_vecindad"],
            command=self._actualizar_origen_vecindad,
        ).grid(row=fila, column=1, sticky="w", pady=(2, 7))
        fila += 1

        ttk.Label(contenido, text="Vecino de:").grid(
            row=fila, column=0, sticky="w", padx=(0, 12), pady=5
        )
        self.entrada_vecino = ttk.Entry(
            contenido,
            textvariable=self.variables["vecino"],
        )
        self.entrada_vecino.grid(row=fila, column=1, sticky="ew", pady=5)
        ttk.Label(
            contenido,
            text="Ejemplo: Tulancingo de Bravo, Estado de Hidalgo",
            foreground="#555555",
        ).grid(row=fila + 1, column=1, sticky="w", pady=(0, 5))
        fila += 2

        self.variables["originario"].trace_add(
            "write", lambda *_args: self._copiar_origen_a_vecindad()
        )
        fila = self._campo(contenido, fila, "Domicilio:", "domicilio")
        fila = self._campo(contenido, fila, "Código postal:", "codigo_postal")

        ttk.Label(contenido, text="Fecha de nacimiento:").grid(
            row=fila, column=0, sticky="w", padx=(0, 12), pady=5
        )
        marco_fecha = ttk.Frame(contenido)
        marco_fecha.grid(row=fila, column=1, sticky="ew", pady=5)
        marco_fecha.columnconfigure(0, weight=1)
        ttk.Entry(
            marco_fecha,
            textvariable=self.variables["fecha_nacimiento"],
        ).grid(row=0, column=0, sticky="ew")
        ttk.Button(
            marco_fecha,
            text="Calcular edad",
            command=self._calcular_edad,
        ).grid(row=0, column=1, padx=(8, 0))
        ttk.Label(
            contenido,
            text="Formato DD/MM/AAAA; la edad se calcula a la fecha de la escritura.",
            foreground="#555555",
        ).grid(row=fila + 1, column=1, sticky="w", pady=(0, 5))
        fila += 2

        fila = self._campo(
            contenido,
            fila,
            "Edad:",
            "edad_numero",
            solo_lectura=True,
        )
        fila = self._campo(
            contenido,
            fila,
            "Edad en letra:",
            "edad_letra",
            solo_lectura=True,
        )
        fila = self._combo(
            contenido,
            fila,
            "Estado civil:",
            "estado_civil",
            ESTADOS_CIVILES,
            editable=True,
        )
        fila = self._campo(contenido, fila, "Ocupación:", "ocupacion")
        fila = self._campo(contenido, fila, "RFC:", "rfc")
        fila = self._campo(contenido, fila, "CURP:", "curp")
        fila = self._campo(contenido, fila, "Número de INE:", "numero_ine")
        fila = self._campo(contenido, fila, "Nacionalidad:", "nacionalidad")

        ttk.Checkbutton(
            contenido,
            text="La persona sabe firmar",
            variable=self.variables["sabe_firmar"],
        ).grid(row=fila, column=1, sticky="w", pady=(8, 16))

        botones = ttk.Frame(self, padding=(12, 0, 12, 12))
        botones.pack(fill="x")
        botones.columnconfigure(0, weight=1)
        ttk.Button(botones, text="Cancelar", command=self.destroy).grid(
            row=0, column=1, padx=(0, 8)
        )
        ttk.Button(botones, text="Guardar compareciente", command=self._guardar).grid(
            row=0, column=2
        )

    def _campo(
        self,
        padre: ttk.Frame,
        fila: int,
        etiqueta: str,
        clave: str,
        ayuda: str = "",
        solo_lectura: bool = False,
    ) -> int:
        ttk.Label(padre, text=etiqueta).grid(
            row=fila, column=0, sticky="w", padx=(0, 12), pady=5
        )
        ttk.Entry(
            padre,
            textvariable=self.variables[clave],
            state="readonly" if solo_lectura else "normal",
        ).grid(row=fila, column=1, sticky="ew", pady=5)
        if ayuda:
            ttk.Label(padre, text=ayuda, foreground="#555555").grid(
                row=fila + 1, column=1, sticky="w", pady=(0, 5)
            )
            return fila + 2
        return fila + 1

    def _combo(
        self,
        padre: ttk.Frame,
        fila: int,
        etiqueta: str,
        clave: str,
        valores: tuple[str, ...],
        editable: bool = False,
    ) -> int:
        ttk.Label(padre, text=etiqueta).grid(
            row=fila, column=0, sticky="w", padx=(0, 12), pady=5
        )
        ttk.Combobox(
            padre,
            textvariable=self.variables[clave],
            values=valores,
            state="normal" if editable else "readonly",
        ).grid(row=fila, column=1, sticky="ew", pady=5)
        return fila + 1

    def _cargar_persona(self, persona: dict[str, Any]) -> None:
        calidad_existente = str(persona.get("calidad", "")).strip().upper()
        if calidad_existente and calidad_existente not in self.calidades_permitidas:
            self.calidades_permitidas = self.calidades_permitidas + (calidad_existente,)

        for clave, variable in self.variables.items():
            if clave in persona:
                variable.set(persona[clave])

        if "mismo_origen_vecindad" not in persona:
            self.variables["mismo_origen_vecindad"].set(
                son_lugares_iguales(
                    str(persona.get("originario", "")),
                    str(persona.get("vecino", "")),
                )
            )

        self._actualizar_origen_vecindad()
        self._calcular_edad(mostrar_error=False)

    def _copiar_origen_a_vecindad(self) -> None:
        if bool(self.variables["mismo_origen_vecindad"].get()):
            self.variables["vecino"].set(self.variables["originario"].get())

    def _actualizar_origen_vecindad(self) -> None:
        mismo_lugar = bool(self.variables["mismo_origen_vecindad"].get())
        if mismo_lugar:
            self._copiar_origen_a_vecindad()
            self.entrada_vecino.configure(state="disabled")
        else:
            self.entrada_vecino.configure(state="normal")

    def _calcular_edad(self, mostrar_error: bool = True) -> bool:
        try:
            nacimiento = parsear_fecha(str(self.variables["fecha_nacimiento"].get()))
            referencia = self.fecha_referencia()
            edad = calcular_edad(nacimiento, referencia)
        except (ValueError, TypeError) as error:
            self.variables["edad_numero"].set("")
            self.variables["edad_letra"].set("")
            if mostrar_error:
                messagebox.showwarning("Fecha incorrecta", str(error), parent=self)
            return False

        self.variables["edad_numero"].set(str(edad))
        self.variables["edad_letra"].set(numero_a_letras(edad))
        return True

    def _guardar(self) -> None:
        if not self._calcular_edad():
            return

        datos = {clave: variable.get() for clave, variable in self.variables.items()}
        if bool(datos["mismo_origen_vecindad"]):
            datos["vecino"] = datos["originario"]

        datos["nombre"] = str(datos["nombre"]).strip().upper()
        datos["sexo"] = str(datos["sexo"]).strip().upper()
        datos["calidad"] = str(datos["calidad"]).strip().upper()
        datos["rfc"] = str(datos["rfc"]).strip().upper()
        datos["curp"] = str(datos["curp"]).strip().upper()
        datos["nacionalidad"] = str(datos["nacionalidad"]).strip().upper()

        obligatorios = {
            "Nombre completo": datos["nombre"],
            "Originario de": datos["originario"],
            "Vecino de": datos["vecino"],
            "Domicilio": datos["domicilio"],
            "Código postal": datos["codigo_postal"],
            "Fecha de nacimiento": datos["fecha_nacimiento"],
            "Estado civil": datos["estado_civil"],
            "Ocupación": datos["ocupacion"],
            "RFC": datos["rfc"],
            "CURP": datos["curp"],
            "Número de INE": datos["numero_ine"],
        }
        faltantes = [nombre for nombre, valor in obligatorios.items() if not str(valor).strip()]
        if faltantes:
            messagebox.showwarning(
                "Datos incompletos",
                "Faltan los siguientes campos:\n\n- " + "\n- ".join(faltantes),
                parent=self,
            )
            return

        if len(str(datos["curp"])) != 18:
            messagebox.showwarning(
                "CURP incorrecta",
                "La CURP debe contener exactamente 18 caracteres.",
                parent=self,
            )
            return

        if len(str(datos["rfc"])) not in {12, 13}:
            messagebox.showwarning(
                "RFC incorrecto",
                "El RFC debe contener 12 caracteres para persona moral o 13 para persona física.",
                parent=self,
            )
            return

        self.al_guardar(deepcopy(datos))
        self.destroy()


class VentanaGrupoColindancia(tk.Toplevel):
    """Ventana para capturar un colindante y todos sus tramos."""

    def __init__(
        self,
        padre: tk.Misc,
        al_guardar: Callable[[dict[str, Any]], None],
        grupo_existente: dict[str, Any] | None = None,
    ) -> None:
        super().__init__(padre)
        self.title("Grupo de colindancia")
        self.geometry("920x570")
        self.minsize(820, 500)
        self.transient(padre)
        self.grab_set()

        self.al_guardar = al_guardar
        self.tramos: list[dict[str, str]] = []

        self.punto = tk.StringVar(value=PUNTOS_CARDINALES[0])
        self.tipo_colindante = tk.StringVar(value=TIPOS_COLINDANTE[0])
        self.colindante = tk.StringVar()
        self.medida = tk.StringVar()
        self.medida_letra = tk.StringVar()

        self._crear_interfaz()
        if grupo_existente:
            self._cargar_grupo(grupo_existente)
        self.protocol("WM_DELETE_WINDOW", self.destroy)

    def _crear_interfaz(self) -> None:
        contenedor = ttk.Frame(self, padding=16)
        contenedor.pack(fill="both", expand=True)
        contenedor.columnconfigure(0, weight=1)
        contenedor.rowconfigure(2, weight=1)

        datos = ttk.LabelFrame(contenedor, text="1. Punto cardinal y colindante", padding=12)
        datos.grid(row=0, column=0, sticky="ew", pady=(0, 12))
        datos.columnconfigure(1, weight=1)
        datos.columnconfigure(3, weight=1)

        ttk.Label(datos, text="Punto cardinal:").grid(row=0, column=0, sticky="w")
        ttk.Combobox(
            datos,
            textvariable=self.punto,
            values=PUNTOS_CARDINALES,
            state="normal",
            width=20,
        ).grid(row=0, column=1, sticky="ew", padx=(8, 18))

        ttk.Label(datos, text="Tipo:").grid(row=0, column=2, sticky="w")
        ttk.Combobox(
            datos,
            textvariable=self.tipo_colindante,
            values=TIPOS_COLINDANTE,
            state="readonly",
            width=20,
        ).grid(row=0, column=3, sticky="ew", padx=(8, 0))

        ttk.Label(datos, text="Nombre o descripción:").grid(
            row=1, column=0, sticky="w", pady=(10, 0)
        )
        ttk.Entry(datos, textvariable=self.colindante).grid(
            row=1, column=1, columnspan=3, sticky="ew", padx=(8, 0), pady=(10, 0)
        )

        captura = ttk.LabelFrame(contenedor, text="2. Agregar tramo", padding=12)
        captura.grid(row=1, column=0, sticky="ew", pady=(0, 12))
        captura.columnconfigure(1, weight=1)
        captura.columnconfigure(3, weight=2)

        ttk.Label(captura, text="Medida numérica:").grid(row=0, column=0, sticky="w")
        ttk.Entry(captura, textvariable=self.medida, width=18).grid(
            row=0, column=1, sticky="ew", padx=(8, 18)
        )
        ttk.Label(captura, text="Medida en letra:").grid(row=0, column=2, sticky="w")
        ttk.Entry(captura, textvariable=self.medida_letra).grid(
            row=0, column=3, sticky="ew", padx=(8, 18)
        )
        ttk.Button(captura, text="Agregar tramo", command=self._agregar_tramo).grid(
            row=0, column=4, sticky="e"
        )

        lista = ttk.LabelFrame(contenedor, text="3. Tramos del colindante", padding=12)
        lista.grid(row=2, column=0, sticky="nsew", pady=(0, 12))
        lista.columnconfigure(0, weight=1)
        lista.rowconfigure(0, weight=1)

        columnas = ("numero", "medida", "medida_letra")
        self.tabla_tramos = ttk.Treeview(lista, columns=columnas, show="headings")
        self.tabla_tramos.heading("numero", text="Línea")
        self.tabla_tramos.heading("medida", text="Medida numérica")
        self.tabla_tramos.heading("medida_letra", text="Medida en letra")
        self.tabla_tramos.column("numero", width=70, anchor="center", stretch=False)
        self.tabla_tramos.column("medida", width=150, anchor="center", stretch=False)
        self.tabla_tramos.column("medida_letra", width=580, anchor="w")
        self.tabla_tramos.grid(row=0, column=0, sticky="nsew")

        barra = ttk.Scrollbar(lista, orient="vertical", command=self.tabla_tramos.yview)
        barra.grid(row=0, column=1, sticky="ns")
        self.tabla_tramos.configure(yscrollcommand=barra.set)

        ttk.Button(lista, text="Eliminar tramo", command=self._eliminar_tramo).grid(
            row=1, column=0, sticky="w", pady=(8, 0)
        )

        botones = ttk.Frame(contenedor)
        botones.grid(row=3, column=0, sticky="ew")
        botones.columnconfigure(0, weight=1)
        ttk.Button(botones, text="Cancelar", command=self.destroy).grid(
            row=0, column=1, padx=(0, 8)
        )
        ttk.Button(botones, text="Guardar grupo", command=self._guardar).grid(
            row=0, column=2
        )

    def _cargar_grupo(self, grupo: dict[str, Any]) -> None:
        self.punto.set(str(grupo["punto"]))
        self.tipo_colindante.set(str(grupo["tipo_colindante"]))
        self.colindante.set(str(grupo["colindante"]))
        self.tramos = deepcopy(grupo["tramos"])
        self._actualizar_tabla_tramos()

    def _agregar_tramo(self) -> None:
        medida = self.medida.get().strip()
        medida_letra = self.medida_letra.get().strip()
        if not medida or not medida_letra:
            messagebox.showwarning(
                "Datos incompletos",
                "Escribe la medida numérica y la medida en letra.",
                parent=self,
            )
            return
        self.tramos.append({"medida": medida, "medida_letra": medida_letra})
        self._actualizar_tabla_tramos()
        self.medida.set("")
        self.medida_letra.set("")

    def _eliminar_tramo(self) -> None:
        seleccion = self.tabla_tramos.selection()
        if not seleccion:
            messagebox.showinfo(
                "Selecciona un tramo",
                "Selecciona el tramo que deseas eliminar.",
                parent=self,
            )
            return
        indices = sorted(
            (self.tabla_tramos.index(item) for item in seleccion), reverse=True
        )
        for indice in indices:
            del self.tramos[indice]
        self._actualizar_tabla_tramos()

    def _actualizar_tabla_tramos(self) -> None:
        for item in self.tabla_tramos.get_children():
            self.tabla_tramos.delete(item)
        for numero, tramo in enumerate(self.tramos, start=1):
            self.tabla_tramos.insert(
                "", "end", values=(numero, tramo["medida"], tramo["medida_letra"])
            )

    def _guardar(self) -> None:
        punto = self.punto.get().strip().upper()
        tipo = self.tipo_colindante.get().strip().upper()
        colindante = self.colindante.get().strip()
        tipo_permite_vacio = tipo in {"ARROYO", "RÍO", "BARRANCA"}

        if not punto:
            messagebox.showwarning(
                "Punto cardinal faltante",
                "Escribe o selecciona el punto cardinal.",
                parent=self,
            )
            return
        if not colindante and not tipo_permite_vacio:
            messagebox.showwarning(
                "Colindante faltante",
                "Escribe el nombre o la descripción del colindante.",
                parent=self,
            )
            return
        if not self.tramos:
            messagebox.showwarning(
                "Sin tramos", "Agrega por lo menos un tramo.", parent=self
            )
            return

        self.al_guardar(
            {
                "punto": punto,
                "tipo_colindante": tipo,
                "colindante": colindante,
                "tramos": deepcopy(self.tramos),
            }
        )
        self.destroy()
