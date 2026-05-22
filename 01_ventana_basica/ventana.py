# ============================================================
# MÓDULO 01 — LA VENTANA BÁSICA
# ============================================================
# Tkinter viene incluido con Python, no se instala nada extra.
# Este archivo muestra cómo crear y configurar la ventana principal.
#
# Para ejecutar: python3 ventana.py
# ============================================================

import tkinter as tk

# --- Paso 1: Crear la ventana principal ---
# tk.Tk() crea la ventana. Siempre es el primer paso.
ventana = tk.Tk()

# --- Paso 2: Configurar la ventana ---

# Título que aparece en la barra superior de la ventana
ventana.title("Mi primera ventana con Tkinter")

# Tamaño de la ventana: "ancho x alto" en píxeles
# 600 píxeles de ancho, 400 de alto
ventana.geometry("600x400")

# Color de fondo de la ventana
# Puedes usar nombres en inglés o códigos hexadecimales (#RRGGBB)
ventana.configure(bg="lightblue")

# Evitar que el usuario pueda cambiar el tamaño de la ventana
# El primer False = no redimensionar ancho, el segundo = no redimensionar alto
ventana.resizable(False, False)

# Tamaño mínimo permitido (si resizable está en True)
# ventana.minsize(300, 200)

# --- Paso 3: Mostrar algo dentro de la ventana ---
# Un Label es simplemente un texto que se muestra en pantalla
# padx y pady son márgenes internos en píxeles
etiqueta_titulo = tk.Label(
    ventana,                    # ← dentro de qué ventana va
    text="¡Hola! Esta es mi primera ventana",
    font=("Arial", 18, "bold"), # fuente, tamaño, estilo
    bg="lightblue",             # color de fondo del label (igual que la ventana para que se vea bien)
    fg="navy"                   # color del texto (fg = foreground = primer plano)
)
etiqueta_titulo.pack(pady=40)   # pack() coloca el widget en la ventana, pady = espacio vertical

etiqueta_info = tk.Label(
    ventana,
    text="Tamaño: 600 x 400 píxeles\nColor de fondo: lightblue",
    font=("Arial", 12),
    bg="lightblue",
    fg="darkblue"
)
etiqueta_info.pack(pady=10)

# Ejemplo de otro color usando código hexadecimal
etiqueta_hex = tk.Label(
    ventana,
    text="Este texto usa color hexadecimal #2C3E50",
    font=("Courier", 11),
    bg="lightblue",
    fg="#2C3E50"
)
etiqueta_hex.pack(pady=10)

# --- Paso 4 (OBLIGATORIO): Mantener la ventana abierta ---
# mainloop() es un bucle infinito que mantiene la ventana activa.
# Siempre debe ser la ÚLTIMA línea del programa.
ventana.mainloop()
