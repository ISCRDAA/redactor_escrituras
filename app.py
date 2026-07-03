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
        "pregunta": "Ingrese su Domicilio:",
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
            "soltero"
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
        "ruta": "vendedor.numero_ine",
        "pregunta": "Ingrese el Numero de el INE:",
        "tipo": "entry",
        "mayusculas": True,
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
        "ruta": "comprador.codigo_postal",
        "pregunta": "Código postal del comprador:",
        "tipo": "entry",
        "mayusculas": False,
        "ayuda": "Ejemplo: 43600",
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


# ==============================
# FUNCIÓN ESPECIAL DE COLINDANCIAS
# ==============================

def mostrar_captura_colindancias(campo):
    """
    Muestra un formulario especial para capturar:
    - cantidad de colindancias
    - punto cardinal
    - medida
    - colindante
    """

    global colindancias_widgets

    colindancias_widgets = []

    Label(
        frame_captura,
        text=campo["pregunta"],
        font=("Arial", 16, "bold"),
        wraplength=850,
        justify="left"
    ).pack(pady=(10, 8))

    Label(
        frame_captura,
        text="Primero indica cuántas colindancias tiene el inmueble.",
        font=("Arial", 11)
    ).pack()

    spin_cantidad = Spinbox(
        frame_captura,
        from_=1,
        to=20,
        width=10,
        font=("Arial", 13)
    )
    spin_cantidad.pack(pady=8)

    frame_lista = Frame(frame_captura)
    frame_lista.pack(pady=10)

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
        for widget in frame_lista.winfo_children():
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

        Label(
            frame_lista,
            text="Punto cardinal",
            font=("Arial", 10, "bold")
        ).grid(row=0, column=0, padx=5, pady=5)

        Label(
            frame_lista,
            text="Medida",
            font=("Arial", 10, "bold")
        ).grid(row=0, column=1, padx=5, pady=5)

        Label(
            frame_lista,
            text="Linda con",
            font=("Arial", 10, "bold")
        ).grid(row=0, column=2, padx=5, pady=5)

        for i in range(cantidad):
            combo_punto = ttk.Combobox(
                frame_lista,
                values=opciones_cardinales,
                state="readonly",
                width=17,
                font=("Arial", 10)
            )
            combo_punto.grid(row=i + 1, column=0, padx=5, pady=4)

            entrada_medida = Entry(
                frame_lista,
                width=38,
                font=("Arial", 10)
            )
            entrada_medida.grid(row=i + 1, column=1, padx=5, pady=4)

            entrada_colinda = Entry(
                frame_lista,
                width=48,
                font=("Arial", 10)
            )
            entrada_colinda.grid(row=i + 1, column=2, padx=5, pady=4)

            colindancias_widgets.append({
                "punto": combo_punto,
                "medida": entrada_medida,
                "colinda": entrada_colinda
            })

    Button(
        frame_captura,
        text="Crear campos de colindancias",
        font=("Arial", 11, "bold"),
        command=crear_renglones
    ).pack(pady=8)

    Label(
        frame_captura,
        text="Ejemplo de medida: (20.00) veinte metros con cero centímetros",
        font=("Arial", 10),
        fg="gray"
    ).pack(pady=(5, 0))


def obtener_colindancias():
    """
    Toma todos los renglones de colindancias y arma el texto jurídico.
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

        linea = f"AL {punto}: En {medida}, linda con {colinda}."
        lineas.append(linea)

    texto_final = "\n".join(lineas)

    # Listing ayuda a que Word respete los saltos de línea.
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

    label_contador.config(
        text=f"Campo {indice_actual + 1} de {len(CAMPOS)}"
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
        font=("Arial", 16, "bold"),
        wraplength=850,
        justify="left"
    ).pack(pady=(10, 10))

    if "ayuda" in campo:
        Label(
            frame_captura,
            text=campo["ayuda"],
            font=("Arial", 10),
            fg="gray",
            wraplength=850,
            justify="left"
        ).pack(pady=(0, 10))

    if campo["tipo"] == "text":
        entrada_actual = Text(
            frame_captura,
            width=85,
            height=9,
            font=("Arial", 13),
            wrap="word"
        )
        entrada_actual.pack(pady=10)
        entrada_actual.insert("1.0", valor_guardado)

    elif campo["tipo"] == "combo":
        entrada_actual = ttk.Combobox(
            frame_captura,
            values=campo["opciones"],
            state="readonly",
            width=82,
            font=("Arial", 14)
        )
        entrada_actual.pack(pady=10, ipady=5)

        if valor_guardado:
            entrada_actual.set(valor_guardado)

    else:
        entrada_actual = Entry(
            frame_captura,
            width=85,
            font=("Arial", 15)
        )
        entrada_actual.pack(pady=10, ipady=8)
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
        numero_escritura = datos.get("escritura", {}).get("numero", "sin_numero")

        nombre_base = f"escritura_{numero_escritura}_{vendedor}_a_{comprador}"
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


# ==============================
# VENTANA PRINCIPAL
# ==============================

ventana = Tk()
ventana.title("Redactor de Escrituras")
ventana.geometry("980x620")
ventana.resizable(False, False)

Label(
    ventana,
    text="Sistema Redactor de Escrituras",
    font=("Arial", 21, "bold")
).pack(pady=(18, 5))

Label(
    ventana,
    text="Captura guiada de datos para escritura",
    font=("Arial", 11)
).pack(pady=(0, 8))

label_contador = Label(
    ventana,
    text="",
    font=("Arial", 12, "bold")
)
label_contador.pack()

frame_captura = Frame(ventana)
frame_captura.pack(pady=10)

frame_botones = Frame(ventana)
frame_botones.pack(pady=18)

Button(
    frame_botones,
    text="Regresar",
    font=("Arial", 13),
    width=18,
    command=regresar
).grid(row=0, column=0, padx=10)

boton_siguiente = Button(
    frame_botones,
    text="Siguiente",
    font=("Arial", 13, "bold"),
    width=18,
    command=siguiente
)
boton_siguiente.grid(row=0, column=1, padx=10)

mostrar_campo()

ventana.mainloop()