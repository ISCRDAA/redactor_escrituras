from pathlib import Path
from datetime import datetime
from tkinter import (
    Tk,
    Label,
    Button,
    Entry,
    Text,
    Frame,
    messagebox,
    Spinbox,
    Canvas,
    Scrollbar,
)
from tkinter import ttk
from docxtpl import DocxTemplate, Listing


# ==============================
# RUTAS DEL PROYECTO
# ==============================

BASE_DIR = Path(__file__).resolve().parent

RUTA_PLANTILLA = BASE_DIR / "plantilla.docx"
CARPETA_GENERADAS = BASE_DIR / "generadas"

# ==============================
# ESTILO VISUAL
# ==============================

COLOR_FONDO = "#f3f4f6"
COLOR_TARJETA = "#ffffff"
COLOR_TEXTO = "#111827"
COLOR_TEXTO_SECUNDARIO = "#6b7280"
COLOR_PRIMARIO = "#1f4e79"
COLOR_PRIMARIO_OSCURO = "#15395a"
COLOR_BORDE = "#d1d5db"

FUENTE_TITULO = ("Segoe UI", 22, "bold")
FUENTE_SUBTITULO = ("Segoe UI", 11)
FUENTE_PREGUNTA = ("Segoe UI", 16, "bold")
FUENTE_NORMAL = ("Segoe UI", 12)
FUENTE_INPUT = ("Segoe UI", 16)
FUENTE_BOTON = ("Segoe UI", 12, "bold")


# ==============================
# CAMPOS DEL FORMULARIO
# ==============================

CAMPOS = [
    
    
    # ==============================
    # VENDEDOR
    # ==============================

    {
        "ruta": "vendedor.nombre",
        "pregunta": "Nombre completo del vendedor:",
        "tipo": "entry",
        "mayusculas": True,
    },
    {
        "ruta": "vendedor.originario",
        "pregunta": "¿De donde es Originario el vendedor?:",
        "tipo": "entry",
        "mayusculas": True,
    },

     {
        "ruta": "vendedor.vecino",
        "pregunta": "¿De donde es Vecino el vendedor?:",
        "tipo": "entry",
        "mayusculas": True,
    },

     {
        "ruta": "vendedor.domicilio",
        "pregunta": "Ingrese su Domicilio del vendedor:",
        "tipo": "text",
        "mayusculas": True,
    },

    {
        "ruta": "vendedor.codigo_postal",
        "pregunta": "Código postal del vendedor:",
        "tipo": "entry",
        "mayusculas": False,
        "ayuda": "Ejemplo: 43600",
    },
    {
        "ruta": "vendedor.fecha_nacimiento",
        "pregunta": "Fecha completa de nacimiento del vendedor:",
        "tipo": "entry",
        "mayusculas": False,
        "ayuda": "Ejemplo: 27 veintisiete días del mes de marzo de 1998",
    },
    {
        "ruta": "vendedor.anio_nacimiento_letra",
        "pregunta": "Año de nacimiento con letra del vendedor:",
        "tipo": "entry",
        "mayusculas": False,
        "ayuda": "Ejemplo: mil novecientos noventa y ocho",
    },
    {
        "ruta": "vendedor.edad_numero",
        "pregunta": "Edad del vendedor:",
        "tipo": "entry",
        "mayusculas": False,
        "ayuda": "Ejemplo: 28",
    },
    {
        "ruta": "vendedor.edad_letra",
        "pregunta": "Edad en letra del vendedor:",
        "tipo": "entry",
        "mayusculas": False,
        "ayuda": "Ejemplo: veintiocho",
    },
    {
        "ruta": "vendedor.estado_civil",
        "pregunta": "Estado civil del vendedor:",
        "tipo": "combo",
        "opciones": [
            "soltero",
            "soltera",
            "casado",
            "casada",
            "divorciado",
            "divorciada",
            "viudo",
            "viuda",
        ],
        "mayusculas": False,
    },
    {
        "ruta": "vendedor.ocupacion",
        "pregunta": "Ocupación del vendedor:",
        "tipo": "combo",
        "opciones": [
            "campesino",
            "campesina",
            "estudiante",
            "ama de casa",
            "abogado",
            "pensionado",
            "pensionada",
            "comerciante",
            "empleado",
            "empleada",
        ],
        "mayusculas": False,
    },
    {
        "ruta": "vendedor.rfc",
        "pregunta": "Ingrese el RFC:",
        "tipo": "entry",
        "mayusculas": True,
    },
    {
        "ruta": "vendedor.curp",
        "pregunta": "Ingrese el CURP:",
        "tipo": "entry",
        "mayusculas": True,
    },

    {
        "ruta": "vendedor.numero_ine",
        "pregunta": "Ingrese el Numero de el INE:",
        "tipo": "entry",
        "mayusculas": False,
    },
    

    # ==============================
    # COMPRADOR
    # ==============================

    {
        "ruta": "comprador.nombre",
        "pregunta": "Nombre completo del comprador:",
        "tipo": "entry",
        "mayusculas": True,
    },
    {
        "ruta": "comprador.originario",
        "pregunta": "¿De donde es Originario el comprador? :",
        "tipo": "entry",
        "mayusculas": True,
    },

     {
        "ruta": "comprador.vecino",
        "pregunta": "¿De donde es Vecino el comprador?:",
        "tipo": "entry",
        "mayusculas": True,
    },

     {
        "ruta": "comprador.domicilio",
        "pregunta": "Ingrese su Domicilio del comprador:",
        "tipo": "text",
        "mayusculas": True,
    },

    {
        "ruta": "comprador.codigo_postal",
        "pregunta": "Código postal del comprador:",
        "tipo": "entry",
        "mayusculas": False,
        "ayuda": "Ejemplo: 43600",
    },
    {
        "ruta": "comprador.fecha_nacimiento",
        "pregunta": "Fecha completa de nacimiento del comprador:",
        "tipo": "entry",
        "mayusculas": False,
        "ayuda": "Ejemplo: 27 veintisiete días del mes de marzo de 1998",
    },
    {
        "ruta": "comprador.anio_nacimiento_letra",
        "pregunta": "Año de nacimiento con letra del comprador:",
        "tipo": "entry",
        "mayusculas": False,
        "ayuda": "Ejemplo: mil novecientos noventa y ocho",
    },
    {
        "ruta": "comprador.edad_numero",
        "pregunta": "Edad del comprador:",
        "tipo": "entry",
        "mayusculas": False,
        "ayuda": "Ejemplo: 28",
    },
    {
        "ruta": "comprador.edad_letra",
        "pregunta": "Edad en letra del comprador:",
        "tipo": "entry",
        "mayusculas": False,
        "ayuda": "Ejemplo: veintiocho",
    },
    {
        "ruta": "comprador.estado_civil",
        "pregunta": "Estado civil del comprador:",
        "tipo": "combo",
        "opciones": [
            "soltero",
            "soltera",
            "casado",
            "casada",
            "divorciado",
            "divorciada",
            "viudo",
            "viuda",
        ],
        "mayusculas": False,
    },
    {
        "ruta": "comprador.ocupacion",
        "pregunta": "Ocupación del comprador:",
        "tipo": "combo",
        "opciones": [
            "campesino",
            "campesina",
            "estudiante",
            "ama de casa",
            "abogado",
            "pensionado",
            "pensionada",
            "comerciante",
            "empleado",
            "empleada",
        ],
        "mayusculas": False,
    },
    {
        "ruta": "comprador.rfc",
        "pregunta": "Ingrese el RFC del comprador:",
        "tipo": "entry",
        "mayusculas": True,
    },
    {
        "ruta": "comprador.curp",
        "pregunta": "Ingrese el CURP del comprador:",
        "tipo": "entry",
        "mayusculas": True,
    },

    {
        "ruta": "comprador.numero_ine",
        "pregunta": "Ingrese el Numero de el INE del comprador:",
        "tipo": "entry",
        "mayusculas": False,
    },

    # ==============================
    # INMUEBLE
    # ==============================

    {
        "ruta": "inmueble.descripcion",
        "pregunta": "Descripción completa del inmueble:",
        "tipo": "text",
        "mayusculas": True,
        "ayuda": "Ejemplo: DEL PREDIO URBANO IDENTIFICADO COMO LOTE 10 DIEZ...",
    },
    {
        "ruta": "inmueble.medidas_colindancias",
        "pregunta": "Medidas y colindancias del inmueble:",
        "tipo": "colindancias",
        "mayusculas": False,
    },
    {
        "ruta": "inmueble.superficie",
        "pregunta": "Superficie total del inmueble:",
        "tipo": "entry",
        "mayusculas": False,
        "ayuda": "Ejemplo: 197.80",
    },
    {
        "ruta": "inmueble.superficie_letra",
        "pregunta": "Superficie en letra:",
        "tipo": "entry",
        "mayusculas": False,
        "ayuda": "Ejemplo: ciento noventa y siete metros con ochenta centímetros",
    },

    # ==============================
    # OPERACIÓN
    # ==============================

    {
        "ruta": "operacion.precio",
        "pregunta": "Precio de la operación:",
        "tipo": "entry",
        "mayusculas": False,
        "ayuda": "Ejemplo: 1,600,000.00",
    },
    {
        "ruta": "operacion.precio_letra",
        "pregunta": "Precio con letra:",
        "tipo": "entry",
        "mayusculas": False,
        "ayuda": "Ejemplo: un millón seiscientos mil pesos 00/100 moneda nacional",
    },
]


# ==============================
# VARIABLES GLOBALES
# ==============================

datos = {}
indice_actual = 0
entrada_actual = None
campo_actual_tipo = None
colindancias_widgets = []


# ==============================
# FUNCIONES PARA DATOS
# ==============================

def guardar_en_diccionario(ruta, valor):
    """
    Guarda un dato usando rutas como:
    vendedor.nombre
    comprador.estado_civil
    inmueble.medidas_colindancias

    Ejemplo:
    ruta = vendedor.nombre
    valor = JUAN PÉREZ

    Se guarda como:
    datos["vendedor"]["nombre"] = "JUAN PÉREZ"
    """

    partes = ruta.split(".")
    actual = datos

    for parte in partes[:-1]:
        if parte not in actual:
            actual[parte] = {}

        actual = actual[parte]

    actual[partes[-1]] = valor


def obtener_de_diccionario(ruta):
    """
    Recupera un dato previamente capturado.
    Sirve para que al presionar REGRESAR no se pierda lo escrito.
    """

    partes = ruta.split(".")
    actual = datos

    for parte in partes:
        if not isinstance(actual, dict) or parte not in actual:
            return ""

        actual = actual[parte]

    if isinstance(actual, Listing):
        return ""

    return actual


def limpiar_area_captura():
    """
    Limpia la parte central de la ventana para mostrar el siguiente campo.
    """

    for widget in frame_captura.winfo_children():
        widget.destroy()

def centrar_ventana(ventana, ancho, alto):
    """
    Centra la ventana en la pantalla.
    """

    pantalla_ancho = ventana.winfo_screenwidth()
    pantalla_alto = ventana.winfo_screenheight()

    x = int((pantalla_ancho / 2) - (ancho / 2))
    y = int((pantalla_alto / 2) - (alto / 2))

    ventana.geometry(f"{ancho}x{alto}+{x}+{y}")

# ==============================
# FUNCIÓN ESPECIAL DE COLINDANCIAS
# ==============================

def mostrar_captura_colindancias(campo):
    """
    Captura dinámica de medidas y colindancias con scroll interno.
    El botón queda arriba y solo la tabla tiene desplazamiento.
    """

    global colindancias_widgets

    colindancias_widgets = []

    Label(
        frame_captura,
        text=campo["pregunta"],
        font=FUENTE_PREGUNTA,
        bg=COLOR_TARJETA,
        fg=COLOR_TEXTO,
        wraplength=1100,
        justify="left"
    ).pack(pady=(5, 8), anchor="w")

    Label(
        frame_captura,
        text="Primero indica cuántas colindancias tiene el inmueble.",
        font=FUENTE_NORMAL,
        bg=COLOR_TARJETA,
        fg=COLOR_TEXTO,
    ).pack(pady=(0, 5))

    spin_cantidad = Spinbox(
        frame_captura,
        from_=1,
        to=20,
        width=8,
        font=("Segoe UI", 13)
    )
    spin_cantidad.pack(pady=(0, 8))

    # Botón fijo arriba
    boton_crear = Button(
        frame_captura,
        text="Crear campos de colindancias",
        font=FUENTE_BOTON,
        bg=COLOR_PRIMARIO,
        fg="#ffffff",
        activebackground=COLOR_PRIMARIO_OSCURO,
        activeforeground="#ffffff",
        relief="flat",
        cursor="hand2"
    )
    boton_crear.pack(pady=(0, 10))

    # Contenedor general de la tabla
    frame_tabla = Frame(
        frame_captura,
        bg="#f1f1f1"
    )
    frame_tabla.pack(fill="x", pady=(0, 5))

    # Encabezados fijos
    frame_encabezados = Frame(
        frame_tabla,
        bg="#f1f1f1"
    )
    frame_encabezados.pack(fill="x")

    Label(
        frame_encabezados,
        text="Punto cardinal",
        font=("Segoe UI", 10, "bold"),
        bg="#f1f1f1",
        fg=COLOR_TEXTO,
        width=24
    ).grid(row=0, column=0, padx=8, pady=6)

    Label(
        frame_encabezados,
        text="Medida",
        font=("Segoe UI", 10, "bold"),
        bg="#f1f1f1",
        fg=COLOR_TEXTO,
        width=50
    ).grid(row=0, column=1, padx=8, pady=6)

    Label(
        frame_encabezados,
        text="Linda con",
        font=("Segoe UI", 10, "bold"),
        bg="#f1f1f1",
        fg=COLOR_TEXTO,
        width=58
    ).grid(row=0, column=2, padx=8, pady=6)

    # Área con scroll
    frame_scroll = Frame(
        frame_tabla,
        bg="#f1f1f1"
    )
    frame_scroll.pack(fill="x")

    canvas = Canvas(
        frame_scroll,
        height=270,
        bg="#f1f1f1",
        highlightthickness=0
    )
    canvas.pack(side="left", fill="x", expand=True)

    scrollbar = Scrollbar(
        frame_scroll,
        orient="vertical",
        command=canvas.yview
    )
    scrollbar.pack(side="right", fill="y")

    canvas.configure(yscrollcommand=scrollbar.set)

    frame_filas = Frame(
        canvas,
        bg="#f1f1f1"
    )

    ventana_filas = canvas.create_window(
        (0, 0),
        window=frame_filas,
        anchor="nw"
    )

    def actualizar_scroll(event=None):
        canvas.configure(scrollregion=canvas.bbox("all"))
        canvas.itemconfig(ventana_filas, width=canvas.winfo_width())

    frame_filas.bind("<Configure>", actualizar_scroll)
    canvas.bind("<Configure>", actualizar_scroll)

    def mover_rueda(event):
        canvas.yview_scroll(int(-1 * (event.delta / 120)), "units")

    def activar_scroll(event):
        canvas.bind_all("<MouseWheel>", mover_rueda)

    def desactivar_scroll(event):
        canvas.unbind_all("<MouseWheel>")

    canvas.bind("<Enter>", activar_scroll)
    canvas.bind("<Leave>", desactivar_scroll)

    opciones_cardinales = [
        "NORTE",
        "SUR",
        "ORIENTE",
        "PONIENTE",
        "ESTE",
        "OESTE",
        "NORESTE",
        "NOROESTE",
        "SURESTE",
        "SUROESTE",
    ]

    def crear_renglones():
        for widget in frame_filas.winfo_children():
            widget.destroy()

        colindancias_widgets.clear()

        try:
            cantidad = int(spin_cantidad.get())
        except ValueError:
            messagebox.showerror(
                "Error",
                "Captura una cantidad válida de colindancias."
            )
            return

        for i in range(cantidad):
            combo_punto = ttk.Combobox(
                frame_filas,
                values=opciones_cardinales,
                state="readonly",
                width=20,
                font=("Segoe UI", 12),
                height=8
            )
            combo_punto.grid(row=i, column=0, padx=8, pady=5, ipady=5)

            entrada_medida = Entry(
                frame_filas,
                width=48,
                font=("Segoe UI", 12),
                bg="#ffffff",
                fg=COLOR_TEXTO,
                relief="solid",
                bd=1
            )
            entrada_medida.grid(row=i, column=1, padx=8, pady=5, ipady=6)

            entrada_colinda = Entry(
                frame_filas,
                width=58,
                font=("Segoe UI", 12),
                bg="#ffffff",
                fg=COLOR_TEXTO,
                relief="solid",
                bd=1
            )
            entrada_colinda.grid(row=i, column=2, padx=8, pady=5, ipady=6)

            colindancias_widgets.append({
                "punto": combo_punto,
                "medida": entrada_medida,
                "colinda": entrada_colinda
            })

        actualizar_scroll()

    boton_crear.config(command=crear_renglones)

    Label(
        frame_captura,
        text="Ejemplo de medida: (20.00) veinte metros con cero centímetros",
        font=("Segoe UI", 10),
        bg=COLOR_TARJETA,
        fg=COLOR_TEXTO_SECUNDARIO
    ).pack(pady=(5, 0))

def medir_ancho_visual(texto):
    """
    Calcula un ancho aproximado del texto.
    Sirve mejor que len(), porque algunas letras ocupan más espacio que otras.
    """

    angostas = "ilI.,;:'|! "
    anchas = "MWÁÉÍÓÚÑÜ@#%&"

    ancho = 0

    for caracter in texto:
        if caracter in angostas:
            ancho += 0.45
        elif caracter in anchas:
            ancho += 1.35
        else:
            ancho += 1.0

    return ancho


def medir_ancho_visual(texto):
    """
    Calcula un ancho aproximado del texto.
    Sirve mejor que len(), porque algunas letras ocupan más espacio que otras.
    """

    angostas = "ilI.,;:'|! "
    anchas = "MWÁÉÍÓÚÑÜ@#%&"

    ancho = 0

    for caracter in texto:
        if caracter in angostas:
            ancho += 0.45
        elif caracter in anchas:
            ancho += 1.35
        else:
            ancho += 1.0

    return ancho


def rellenar_con_guiones(texto, ancho_linea=155):
    """
    Rellena el espacio sobrante con guiones notariales.
    Ajusta ancho_linea si se pasa o queda corto.
    """

    texto = texto.strip()
    ancho_texto = medir_ancho_visual(texto)

    if ancho_texto >= ancho_linea:
        return texto

    faltante = int(ancho_linea - ancho_texto)

    relleno = " " + ("- " * max(1, faltante // 2))

    return texto + relleno


def obtener_colindancias():
    """
    Toma todos los renglones de colindancias y arma el texto jurídico.
    Si queda espacio en blanco, lo rellena con guiones.
    """

    if not colindancias_widgets:
        return ""

    lineas = []

    for item in colindancias_widgets:
        punto = item["punto"].get().strip()
        medida = item["medida"].get().strip()
        colinda = item["colinda"].get().strip()

        if not punto or not medida or not colinda:
            return ""

        texto_base = f"AL {punto}: En {medida}, linda con {colinda}."

        linea = rellenar_con_guiones(texto_base, ancho_linea=170)

        lineas.append(linea)

    texto_final = "\n".join(lineas)

    return Listing(texto_final)


# ==============================
# FUNCIONES PARA MOSTRAR CAMPOS
# ==============================

def mostrar_campo():
    """
    Muestra el campo actual según su tipo:
    entry, text, combo o colindancias.
    """

    global entrada_actual
    global campo_actual_tipo

    limpiar_area_captura()

    campo = CAMPOS[indice_actual]
    campo_actual_tipo = campo["tipo"]
    valor_guardado = obtener_de_diccionario(campo["ruta"])

    total = len(CAMPOS)
    progreso = int(((indice_actual + 1) / total) * 100)

    label_contador.config(
        text=f"Campo {indice_actual + 1} de {total}"
    )

    barra_progreso["value"] = progreso

    label_ruta.config(
        text=f"Variable: {{{{ {campo['ruta']} }}}}"
    )

    if indice_actual == len(CAMPOS) - 1:
        boton_siguiente.config(text="Generar escritura")
    else:
        boton_siguiente.config(text="Siguiente")

    if campo["tipo"] == "colindancias":
        mostrar_captura_colindancias(campo)
        return

    Label(
        frame_captura,
        text=campo["pregunta"],
        font=FUENTE_PREGUNTA,
        bg=COLOR_TARJETA,
        fg=COLOR_TEXTO,
        wraplength=1100,
        justify="left"
    ).pack(pady=(10, 10), anchor="w")

    if "ayuda" in campo:
        Label(
            frame_captura,
            text=campo["ayuda"],
            font=("Segoe UI", 10),
            bg=COLOR_TARJETA,
            fg=COLOR_TEXTO_SECUNDARIO,
            wraplength=1100,
            justify="left"
        ).pack(pady=(0, 12), anchor="w")

    if campo["tipo"] == "text":
        entrada_actual = Text(
            frame_captura,
            width=100,
            height=10,
            font=FUENTE_INPUT,
            wrap="word",
            bg="#ffffff",
            fg=COLOR_TEXTO,
            insertbackground=COLOR_TEXTO,
            relief="solid",
            bd=1,
            padx=12,
            pady=12
        )
        entrada_actual.pack(pady=10, fill="x")
        entrada_actual.insert("1.0", valor_guardado)

    elif campo["tipo"] == "combo":
        entrada_actual = ttk.Combobox(
            frame_captura,
            values=campo["opciones"],
            state="readonly",
            width=95,
            font=FUENTE_INPUT,
            height=8
        )
        entrada_actual.pack(pady=10, ipady=8, fill="x")

        if valor_guardado:
            entrada_actual.set(valor_guardado)
        else:
            entrada_actual.set("Selecciona una opción")

    else:
        entrada_actual = Entry(
            frame_captura,
            width=100,
            font=FUENTE_INPUT,
            bg="#ffffff",
            fg=COLOR_TEXTO,
            insertbackground=COLOR_TEXTO,
            relief="solid",
            bd=1
        )
        entrada_actual.pack(pady=10, ipady=10, fill="x")
        entrada_actual.insert(0, valor_guardado)

    entrada_actual.focus()


def obtener_valor_input():
    """
    Lee el dato capturado según el tipo de campo actual.
    """

    if campo_actual_tipo == "colindancias":
        return obtener_colindancias()

    if isinstance(entrada_actual, Text):
        return entrada_actual.get("1.0", "end").strip()

    return entrada_actual.get().strip()


# ==============================
# BOTONES
# ==============================

def siguiente():
    """
    Valida el campo actual.
    Guarda el dato.
    Avanza al siguiente campo.
    Al final genera la escritura.
    """

    global indice_actual

    campo = CAMPOS[indice_actual]
    valor = obtener_valor_input()

    if not valor:
        messagebox.showerror(
            "Dato obligatorio",
            "Este campo no puede quedar vacío."
        )
        return

    if campo.get("mayusculas") and isinstance(valor, str):
        valor = valor.upper()

    guardar_en_diccionario(campo["ruta"], valor)

    indice_actual += 1

    if indice_actual < len(CAMPOS):
        mostrar_campo()
    else:
        generar_escritura()


def regresar():
    """
    Regresa al campo anterior.
    Guarda el dato actual si existe.
    """

    global indice_actual

    if indice_actual <= 0:
        return

    campo = CAMPOS[indice_actual]
    valor = obtener_valor_input()

    if valor:
        if campo.get("mayusculas") and isinstance(valor, str):
            valor = valor.upper()

        guardar_en_diccionario(campo["ruta"], valor)

    indice_actual -= 1
    mostrar_campo()


# ==============================
# GENERAR WORD
# ==============================

def limpiar_nombre_archivo(texto):
    """
    Limpia el nombre para evitar caracteres inválidos en Windows.
    """

    caracteres_invalidos = ['\\', '/', ':', '*', '?', '"', '<', '>', '|']

    for caracter in caracteres_invalidos:
        texto = texto.replace(caracter, "")

    return texto.strip().replace(" ", "_").lower()


def generar_escritura():
    """
    Abre la plantilla, inserta datos y guarda la escritura generada.
    """

    if not RUTA_PLANTILLA.exists():
        messagebox.showerror(
            "Plantilla no encontrada",
            "No se encontró el archivo plantilla.docx."
        )
        return

    try:
        CARPETA_GENERADAS.mkdir(exist_ok=True)

        vendedor = datos.get("vendedor", {}).get("nombre", "vendedor")
        comprador = datos.get("comprador", {}).get("nombre", "comprador")

        nombre_base = f"proyecto_compraventa_{vendedor}_a_{comprador}"
        nombre_base = limpiar_nombre_archivo(nombre_base)

        fecha_archivo = datetime.now().strftime("%Y%m%d_%H%M%S")
        ruta_salida = CARPETA_GENERADAS / f"{nombre_base}_{fecha_archivo}.docx"

        doc = DocxTemplate(RUTA_PLANTILLA)
        doc.render(datos)
        doc.save(ruta_salida)

        messagebox.showinfo(
            "Escritura generada",
            f"La escritura fue generada correctamente:\n\n{ruta_salida}"
        )

        ventana.destroy()

    except Exception as error:
        messagebox.showerror(
            "Error al generar escritura",
            f"Ocurrió un error:\n\n{error}"
        )



def configurar_estilos():
    """
    Configura estilos visuales para ttk.
    """

    estilo = ttk.Style()

    try:
        estilo.theme_use("clam")
    except Exception:
        pass

    estilo.configure(
        "TCombobox",
        fieldbackground="#ffffff",
        background="#ffffff",
        foreground=COLOR_TEXTO,
        arrowcolor=COLOR_PRIMARIO,
        bordercolor=COLOR_BORDE,
        lightcolor=COLOR_BORDE,
        darkcolor=COLOR_BORDE,
        padding=8,
        font=FUENTE_INPUT,
    )

    estilo.map(
        "TCombobox",
        fieldbackground=[("readonly", "#ffffff")],
        background=[("readonly", "#ffffff")],
        foreground=[("readonly", COLOR_TEXTO)],
        bordercolor=[("focus", COLOR_PRIMARIO)],
    )

    estilo.configure(
        "Horizontal.TProgressbar",
        troughcolor="#e5e7eb",
        background=COLOR_PRIMARIO,
        bordercolor="#e5e7eb",
        lightcolor=COLOR_PRIMARIO,
        darkcolor=COLOR_PRIMARIO,
    )
# ==============================
# VENTANA PRINCIPAL
# ==============================

ventana = Tk()
ventana.title("Redactor de Escrituras")
ventana.configure(bg=COLOR_FONDO)
ventana.resizable(False, False)

centrar_ventana(ventana, 1250, 760)
configurar_estilos()

ventana.option_add("*TCombobox*Listbox.font", ("Segoe UI", 17))
ventana.option_add("*TCombobox*Listbox.selectBackground", COLOR_PRIMARIO)
ventana.option_add("*TCombobox*Listbox.selectForeground", "white")

# CONTENEDOR GENERAL
frame_principal = Frame(
    ventana,
    bg=COLOR_FONDO
)
frame_principal.pack(fill="both", expand=True, padx=25, pady=20)

# ENCABEZADO FIJO
frame_header = Frame(
    frame_principal,
    bg=COLOR_FONDO
)
frame_header.pack(side="top", fill="x")

Label(
    frame_header,
    text="Sistema Redactor de Escrituras",
    font=FUENTE_TITULO,
    bg=COLOR_FONDO,
    fg=COLOR_TEXTO
).pack(anchor="w")

Label(
    frame_header,
    text="Captura guiada de datos para escritura pública",
    font=FUENTE_SUBTITULO,
    bg=COLOR_FONDO,
    fg=COLOR_TEXTO_SECUNDARIO
).pack(anchor="w", pady=(3, 14))

# PROGRESO FIJO
frame_progreso = Frame(
    frame_principal,
    bg=COLOR_FONDO
)
frame_progreso.pack(side="top", fill="x", pady=(0, 14))

label_contador = Label(
    frame_progreso,
    text="",
    font=("Segoe UI", 11, "bold"),
    bg=COLOR_FONDO,
    fg=COLOR_PRIMARIO
)
label_contador.pack(anchor="w")

barra_progreso = ttk.Progressbar(
    frame_progreso,
    orient="horizontal",
    mode="determinate",
    maximum=100,
    style="Horizontal.TProgressbar"
)
barra_progreso.pack(fill="x", pady=(5, 0))

# BOTONES FIJOS ABAJO
frame_botones = Frame(
    frame_principal,
    bg=COLOR_FONDO,
    height=60
)
frame_botones.pack(side="bottom", fill="x", pady=(15, 0))
frame_botones.pack_propagate(False)

boton_regresar = Button(
    frame_botones,
    text="← Regresar",
    font=FUENTE_BOTON,
    width=18,
    bg="#e5e7eb",
    fg=COLOR_TEXTO,
    activebackground="#d1d5db",
    activeforeground=COLOR_TEXTO,
    relief="flat",
    cursor="hand2",
    command=regresar
)
boton_regresar.pack(side="left", pady=8)

boton_siguiente = Button(
    frame_botones,
    text="Siguiente →",
    font=FUENTE_BOTON,
    width=20,
    bg=COLOR_PRIMARIO,
    fg="#ffffff",
    activebackground=COLOR_PRIMARIO_OSCURO,
    activeforeground="#ffffff",
    relief="flat",
    cursor="hand2",
    command=siguiente
)
boton_siguiente.pack(side="right", pady=8)

# TARJETA DE CAPTURA CON ALTURA FIJA
frame_tarjeta = Frame(
    frame_principal,
    bg=COLOR_TARJETA,
    highlightbackground=COLOR_BORDE,
    highlightthickness=1,
    height=520
)
frame_tarjeta.pack(side="top", fill="x")
frame_tarjeta.pack_propagate(False)

frame_captura = Frame(
    frame_tarjeta,
    bg=COLOR_TARJETA
)
frame_captura.pack(fill="both", expand=True, padx=35, pady=(25, 5))

label_ruta = Label(
    frame_tarjeta,
    text="",
    font=("Segoe UI", 9),
    bg=COLOR_TARJETA,
    fg=COLOR_TEXTO_SECUNDARIO
)
label_ruta.pack(anchor="w", padx=35, pady=(0, 10))

mostrar_campo()

ventana.mainloop()