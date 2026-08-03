# Sistema de Escrituras — Formulario V13

Aplicación de escritorio para capturar los datos de una compraventa y generar el documento Word utilizando Microsoft Word como motor de formato.

## Requisitos

- Windows 10 u 11.
- Python 3.11 o superior.
- Microsoft Word de escritorio instalado.
- Word debe estar cerrado antes de generar el documento.

## Primera ejecución

1. Descomprime la carpeta.
2. Haz doble clic en `INSTALAR_Y_EJECUTAR.bat`.
3. El instalador crea el entorno virtual, instala las dependencias y abre el formulario.

En ejecuciones posteriores usa `EJECUTAR.bat`.

## Pestañas del formulario

1. **Datos generales:** libro, escritura y fecha del instrumento.
2. **Vendedor:** datos personales de la parte vendedora.
3. **Comprador:** datos personales, sexo y calidad de la parte adquirente.
4. **Inmueble:** descripción, superficie y datos registrales.
5. **Antecedente y operación:** antecedente libre, avalúo, precio y declaración predial.
6. **Colindancias:** cardinales, distintos colindantes y varios tramos por grupo.
7. **Salida:** beneficiario del primer testimonio y nombre del Word.

## Medidas y colindancias

- Presiona **Agregar grupo**.
- Selecciona el punto cardinal y el tipo de colindante.
- Captura una medida y pulsa **Convertir** para generar la medida en letra.
- Agrega todos los tramos del mismo colindante.
- Guarda el grupo.
- Repite el cardinal en otro grupo cuando cambie el colindante.

## Generar Word

1. Completa los campos obligatorios.
2. Pulsa **Generar documento Word**.
3. Elige el nombre y la ubicación.
4. Microsoft Word abrirá la matriz, sustituirá los datos, actualizará la paginación y guardará una copia.

Junto al Word se crea un archivo `*_registro.txt`. Si ocurre un error, ese archivo indica el paso exacto.

## Borradores

- **Guardar borrador:** conserva la captura en formato JSON.
- **Cargar borrador:** recupera una captura anterior, incluidas las colindancias.

## Estructura

```text
sistema_escrituras_formulario_v13/
├── main.py
├── interfaz.py
├── redaccion.py
├── motor_word.py
├── generador_base_v12.py
├── requirements.txt
├── INSTALAR_Y_EJECUTAR.bat
├── EJECUTAR.bat
├── plantillas/
│   └── MATRIZ_COMPRAVENTA.docx
├── borradores/
└── salidas/
```

## Alcance de esta versión

La V13 integra el formulario con la matriz oficial de **compraventa**. Mantiene la lógica de generación V12. En la siguiente etapa se podrá ampliar a múltiples vendedores/compradores y a otros actos jurídicos con sus propias matrices oficiales.
