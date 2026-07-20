# Sistema de Escrituras — Paso 7

En este paso se aplica el formato de guiones notariales a todo el documento Word. El sistema conserva los tres actos configurables del Paso 6 y transforma los guiones escritos manualmente en un formato dinámico.

## Qué hace el formato global de guiones

- separa los bloques grandes de la plantilla en párrafos reales;
- agrega una franja breve de guiones al inicio de cada párrafo;
- completa con guiones el espacio disponible al final;
- evita que una línea de guiones se vaya sola al siguiente renglón;
- centra títulos como `ANTECEDENTE`, `DATOS PERSONALES` y `DOCUMENTOS DEL APÉNDICE` entre guiones;
- conserva las firmas sin guiones y alineadas de dos en dos;
- adapta automáticamente el número de guiones a la longitud del texto;
- funciona en compraventa, donación y cesión de derechos.

Los guiones compactos son líderes de tabulación de Word. No se calculan contando caracteres y se ajustan al ancho real de la hoja. Cuando la última línea está casi llena, el programa agrega únicamente los guiones que caben para evitar que bajen a un renglón nuevo.

## Actos incluidos

- COMPRAVENTA
- DONACIÓN
- CESIÓN DE DERECHOS

## Archivos principales

```text
sistema_escrituras_paso7/
├── main.py
├── interfaz.py
├── formularios.py
├── configuracion_actos.py
├── utilidades.py
├── generador_word.py
├── prueba_generacion.py
├── crear_plantillas_paso6.py
├── requirements.txt
├── plantillas/
│   ├── plantilla_compraventa.docx
│   ├── plantilla_donacion.docx
│   ├── plantilla_cesion_derechos.docx
│   └── plantilla_base_paso5.docx
└── salidas/
```

## Cómo instalar

Desde PowerShell, dentro de la carpeta del proyecto:

```powershell
py -m venv entorno
```

```powershell
.\entorno\Scripts\activate
```

```powershell
python -m pip install -r requirements.txt
```

## Cómo ejecutar

```powershell
python main.py
```

## Cómo probar la generación sin llenar el formulario

```powershell
python prueba_generacion.py
```

Se crearán tres documentos de ejemplo dentro de `salidas`.

## Dónde está la lógica nueva

La aplicación global de guiones se encuentra en `generador_word.py`, principalmente en estas funciones:

- `_separar_bloques_manual_guiones`;
- `_aplicar_parrafo_con_guiones`;
- `_aplicar_titulo_con_guiones`;
- `_aplicar_encabezado_escritura`;
- `_es_parrafo_firma`;
- `_espacio_ultima_linea`.

## Advertencia jurídica

Las cláusulas de donación y cesión de derechos son prototipos técnicos. Deben revisarse y adecuarse a la legislación aplicable, al criterio del notario y a las particularidades del acto antes de utilizarse en un instrumento definitivo.
