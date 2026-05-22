# ============================================================
# MÓDULO DE PERSISTENCIA — Lectura y escritura de datos en JSON
# ============================================================
# Este módulo está completamente desacoplado de la interfaz gráfica.
# Solo depende de la librería estándar (json, os) y expone:
#   - Las constantes con los nombres de los archivos de datos.
#   - Las dos funciones reutilizables para leer/escribir JSON.
# ============================================================

import json
import os

# Nombres de los archivos donde se guardan los datos persistentes.
# Se definen aquí para que cualquier módulo que importe persistencia
# use siempre la misma ruta sin repetir el string.
ARCHIVO_LIBROS    = "biblioteca_libros.json"
ARCHIVO_PRESTAMOS = "biblioteca_prestamos.json"


# ── Funciones de persistencia ─────────────────────────────
# Estas dos funciones son las encargadas de leer y escribir datos en archivos
# JSON, de modo que la información NO se pierde al cerrar el programa.

def cargar_json(archivo):
    """
    Lee y devuelve el contenido de un archivo JSON como lista de Python.
    - Si el archivo existe lo abre, lo decodifica y retorna la lista de objetos.
    - Si el archivo NO existe (primera ejecución) retorna una lista vacía []
      para que el resto del programa no explote con un error de fichero.
    """
    if os.path.exists(archivo):
        with open(archivo, "r", encoding="utf-8") as f:
            return json.load(f)
    return []

def guardar_json(archivo, datos):
    """
    Sobreescribe el archivo JSON con la lista `datos` actualizada.
    - indent=4  → escribe el JSON con sangría de 4 espacios (legible).
    - ensure_ascii=False → permite guardar tildes y caracteres especiales.
    Se llama cada vez que se agrega, edita, elimina un libro o se registra
    un préstamo/devolución para mantener el archivo siempre sincronizado.
    """
    with open(archivo, "w", encoding="utf-8") as f:
        json.dump(datos, f, indent=4, ensure_ascii=False)
