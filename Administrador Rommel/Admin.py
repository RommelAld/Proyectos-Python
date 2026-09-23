import os
import csv
from datetime import datetime


# Historial de busqueda o acciones

def registrar_historial(accion):
    hora = datetime.now().strftime("%H:%M:%S")
    with open("historial.txt", "a") as archivo:
        archivo.write(f"[{hora}] {accion}\n")


#  Opción 1 Organizador de los archivos 

TIPOS = {
    "Imagenes": [".jpg", ".jpeg", ".png", ".gif"],
    "Documentos": [".pdf", ".docx", ".txt", ".xlsx"],
    "Comprimidos": [".zip", ".rar"],
    "Musica": [".mp3", ".wav"],
    "Videos": [".mp4", ".mov", ".avi"]
}


def organizar_carpeta():
    ruta = input("Ingresa la ruta de la carpeta a organizar: ")
    archivos = os.listdir(ruta)

    for archivo in archivos:
        ruta_completa = os.path.join(ruta, archivo)

        if not os.path.isfile(ruta_completa):
            continue

        extension = os.path.splitext(archivo)[1].lower()
        movido = False

        for categoria, extensiones in TIPOS.items():
            if extension in extensiones:
                carpeta_destino = os.path.join(ruta, categoria)
                if not os.path.exists(carpeta_destino):
                    os.makedirs(carpeta_destino)
                os.rename(ruta_completa, os.path.join(carpeta_destino, archivo))
                print(f"El archivo: {archivo} Fue movido a -> {categoria}")
                movido = True
                break

        if not movido:
            print(f"Sin categoría (se dejó igual): {archivo}")

    print("\nYa esta listo, nos vemos en otra ocación.")
    registrar_historial(f"se Organizó la carpeta '{ruta}'")


# Buscar un texto con palabra 

def analizar_log(ruta_archivo, palabra):
    contador = 0
    with open(ruta_archivo, "r") as archivo:
        for numero_linea, linea in enumerate(archivo, start=1):
            if palabra.lower() in linea.lower():
                print(f"Línea {numero_linea}: {linea.strip()}")
                contador += 1
    print(f"\nSe encontraron {contador} coincidencias de la palabra:'{palabra}'.\n")


def buscar_en_log():
    ruta_archivo = input("Ingrese el nombre del archivo de texto (que termine en txt) a analizar: ")

    while True:
        palabra = input("¿En el archivo, Qué palabra quieres buscar? (si no quieres escribir nada escribe 'volver'): ")

        if palabra.lower() == "volver":
            break

        try:
            analizar_log(ruta_archivo, palabra)
            registrar_historial(f" el Usuario Buscó '{palabra}' en '{ruta_archivo}'")
        except FileNotFoundError:
            print(f"No pude encontrar el archivo '{ruta_archivo}'.")
            break


# Buscar algo en un Catalogo, ahora CVS

def cargar_productos(ruta_archivo):
    productos = []
    with open(ruta_archivo, "r") as archivo:
        lector = csv.DictReader(archivo)
        for fila in lector:
            fila["precio"] = int(fila["precio"])
            fila["stock"] = int(fila["stock"])
            productos.append(fila)
    return productos


def buscar_por_nombre(productos, texto):
    encontrados = []
    for p in productos:
        if texto.lower() in p["nombre"].lower():
            encontrados.append(p)
    return encontrados


def filtrar_por_precio(productos, minimo, maximo):
    encontrados = []
    for p in productos:
        if minimo <= p["precio"] <= maximo:
            encontrados.append(p)
    return encontrados


def sin_stock(productos):
    return [p for p in productos if p["stock"] == 0]


def mostrar(productos):
    if not productos:
        print("No se encontraron productos en el catálogo.\n")
        return
    for p in productos:
        print(f"- {p['nombre']} | ${p['precio']} | Stock: {p['stock']}")
    print()


def buscar_en_catalogo():
    ruta = input(" Ingrese el nombre del archivo CSV del catálogo: ")

    try:
        productos = cargar_productos(ruta)
    except FileNotFoundError:
        print(f"Uy, no encontré el archivo '{ruta}'.")
        return

    while True:
        print("\n--- Catálogo ---")
        print("1. Buscar por nombre")
        print("2. Filtrar por rango de precio")
        print("3. Ver productos sin stock")
        print("4. Volver al menú principal")
        opcion = input("Elige una opción: ")

        if opcion == "1":
            texto = input("¿Qué producto buscas? ")
            mostrar(buscar_por_nombre(productos, texto))
            registrar_historial(f"Buscó '{texto}' en el catálogo")
        elif opcion == "2":
            minimo = int(input("Precio mínimo del producto: "))
            maximo = int(input("Precio máximo del producto: "))
            mostrar(filtrar_por_precio(productos, minimo, maximo))
            registrar_historial(f"Filtró catálogo entre ${minimo} y ${maximo}")
        elif opcion == "3":
            mostrar(sin_stock(productos))
            registrar_historial("Consultó productos sin stock")
        elif opcion == "4":
            break
        else:
            print("Opción no válida.\n")


# MENU

def main():
    while True:
        print("\n=== SUITE DE AUTOMATIZACIÓN ===")
        print("1. Organizar archivos de una carpeta")
        print("2. Buscar texto en un archivo (log)")
        print("3. Buscar producto en catálogo (CSV)")
        print("4. Salir")
        opcion = input("¿Qué quieres hacer? ")

        if opcion == "1":
            organizar_carpeta()
        elif opcion == "2":
            buscar_en_log()
        elif opcion == "3":
            buscar_en_catalogo()
        elif opcion == "4":
            print("¡Listo, hasta la próxima!")
            break
        else:
            print("Opción no válida, intenta de nuevo.")


if __name__ == "__main__":
    main()
