# Administrador Automatizado

Programa de consola hecho en Python que contiene tres herramientas/formas de automatización y procesamiento de archivos en un solo lugar, pensado para resolver tareas repetitivas de forma simple.

## Las Funcionalidades

### 1. Organizador de archivos
La principal funcion es que recibe la ruta de una carpeta y ordena automáticamente los archivos que hay dentro en subcarpetas según su tipo (Imágenes, Documentos, Comprimidos, Música, Videos).

### 2. Analizador de Archivos de Registros
Recibe un archivo de texto y pide una palabra a buscar. Recorre el archivo línea por línea e indica en qué líneas aparece la palabra y cuántas coincidencias hay en total.

### 3. Catálogo de productos (CSV)
Carga un catálogo de productos desde un archivo `.csv` y permite:
- Buscar productos por nombre
- Filtrar productos por rango de precio (precio minimo y máximo)
- Ver qué productos están sin stock

### Historial
Cada acción realizada (organizar una carpeta, buscar en un log, buscar en el catálogo) queda registrada con hora en un archivo `historial.txt`, que se genera automáticamente en la misma carpeta del programa, esto con el fin de mantener un orden a las acciones que se realiza.

## Requisitos

- Python 3
- No requiere instalar librerías externas (usa `os`, `csv` y `datetime`, incluidas en Python (éste ultimo solo lo use para darle una interfaz mas organizada y quizas sirva para llevar un resumen de las acciones.))

## Cómo usarlo

1. Clona o descarga este repositorio.
2. Abre una terminal en la carpeta del proyecto.
3. Ejecuta:

   ```bash
   python3 Admin.py
   ```

4. Elige una opción del menú principal:

   ```
   === SUITE DE AUTOMATIZACIÓN ===
   1. Organizar archivos de una carpeta
   2. Buscar texto en un archivo (log)
   3. Buscar producto en catálogo (CSV)
   4. Salir
   ```
- Despues de seleccionar un numero para el 

### Ejemplo  Organizar archivos
```
¿Qué quieres hacer? 1
Ingresa la ruta de la carpeta a organizar: Descargas
```
> Aunque se recomienda NO USAR en una carpeta del computador si se va a usar como prueba
### Ejemplo  Buscar en un Archivo de Registro
```
¿Qué quieres hacer? 2
Nombre del archivo de texto a analizar: log_prueba.txt
¿Qué palabra quieres buscar? (o 'volver'): error
```

### Ejemplo Buscar en el catálogo
```
¿Qué quieres hacer? 3
Nombre del archivo CSV del catálogo: productos.csv

--- Catálogo ---
1. Buscar por nombre
2. Filtrar por rango de precio
3. Ver productos sin stock
4. Volver al menú principal
```

> **Nota:** para probarlo sin usar tus propios archivos, este repositorio incluye `log_prueba.txt` y `productos.csv` como ejemplos.

## Estructura del proyecto

```
├── Admin.py          # Programa principal
├── productos.csv      # Catálogo de ejemplo
├── log_prueba.txt     # Log de ejemplo
└── README.md
```

## Autor

Rommel José Aldana Túa — Estudiante de Técnico Medio en Telecomunicaciones

>**IMPORTANTE:** Este pqueño proyecto fue hecho con ayuda de Claude, para la creacion de los archivos txt. csv y como Herramienta para Optimizar el  Programa y hacer una Interfaz Basica mas llamativa, sin embargo, el Desarrollo de éste fue creación mia. 
