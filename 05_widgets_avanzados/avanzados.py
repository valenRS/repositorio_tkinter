# ============================================================
# MÓDULO 05 — WIDGETS AVANZADOS
# ============================================================
# Checkbutton, Radiobutton, Listbox, Combobox y Frame.
# Estos widgets se usan mucho para formularios y selecciones.
#
# Para ejecutar: python3 avanzados.py
# ============================================================

import tkinter as tk
from tkinter import ttk   # ttk tiene widgets más modernos como Combobox

ventana = tk.Tk()
ventana.title("Módulo 05 — Widgets Avanzados")
ventana.geometry("500x580")
ventana.configure(bg="white")


# ============================================================
# 1. CHECKBUTTON — Casilla de verificación (sí/no)
# ============================================================
# Usa IntVar: vale 1 si está marcado, 0 si no.
# Usa BooleanVar: vale True si está marcado, False si no.

tk.Label(ventana, text="── 1. CHECKBUTTON ──", font=("Arial", 12, "bold"),
         bg="white").pack(pady=(15, 5))

var_acepta = tk.BooleanVar()   # variable que guarda True/False
var_suscrito = tk.BooleanVar()

tk.Checkbutton(ventana, text="Acepto los términos y condiciones",
               variable=var_acepta, bg="white", font=("Arial", 11)).pack(anchor="w", padx=30)

tk.Checkbutton(ventana, text="Quiero recibir notificaciones",
               variable=var_suscrito, bg="white", font=("Arial", 11)).pack(anchor="w", padx=30)

def ver_checks():
    msg = f"Acepta términos: {var_acepta.get()}\nSuscrito: {var_suscrito.get()}"
    etiqueta_check.config(text=msg)

etiqueta_check = tk.Label(ventana, text="", bg="white", fg="navy", font=("Arial", 10))
etiqueta_check.pack(pady=3)
tk.Button(ventana, text="Ver selección", command=ver_checks, bg="lightblue").pack()


# ============================================================
# 2. RADIOBUTTON — Selección de una sola opción
# ============================================================
# Todos los Radiobutton del mismo grupo comparten la MISMA variable.
# Solo uno puede estar seleccionado a la vez.

tk.Label(ventana, text="── 2. RADIOBUTTON ──", font=("Arial", 12, "bold"),
         bg="white").pack(pady=(15, 5))

var_genero = tk.StringVar(value="No especificado")  # valor por defecto

opciones_genero = ["Masculino", "Femenino", "No especificado"]
for opcion in opciones_genero:
    tk.Radiobutton(
        ventana,
        text=opcion,
        variable=var_genero,   # todos comparten la misma variable
        value=opcion,          # valor que toma la variable cuando este botón está seleccionado
        bg="white",
        font=("Arial", 11)
    ).pack(anchor="w", padx=30)

def ver_radio():
    etiqueta_radio.config(text=f"Seleccionado: {var_genero.get()}")

etiqueta_radio = tk.Label(ventana, text="", bg="white", fg="navy", font=("Arial", 10))
etiqueta_radio.pack(pady=3)
tk.Button(ventana, text="Ver selección", command=ver_radio, bg="lightyellow").pack()


# ============================================================
# 3. COMBOBOX — Lista desplegable (menú select)
# ============================================================
# ttk.Combobox es un campo con lista de opciones predefinidas.

tk.Label(ventana, text="── 3. COMBOBOX ──", font=("Arial", 12, "bold"),
         bg="white").pack(pady=(15, 5))

tk.Label(ventana, text="Selecciona tu carrera:", bg="white").pack()

combo_carrera = ttk.Combobox(
    ventana,
    values=["Ingeniería de Sistemas", "Ingeniería Electrónica",
            "Ingeniería Civil", "Medicina", "Derecho"],
    width=30,
    state="readonly"   # readonly = solo se puede seleccionar, no escribir
)
combo_carrera.set("Selecciona una opción")  # texto por defecto
combo_carrera.pack(pady=5)

def ver_combo():
    etiqueta_combo.config(text=f"Carrera: {combo_carrera.get()}")

etiqueta_combo = tk.Label(ventana, text="", bg="white", fg="navy", font=("Arial", 10))
etiqueta_combo.pack(pady=3)
tk.Button(ventana, text="Ver selección", command=ver_combo, bg="lightgreen").pack()


# ============================================================
# 4. LISTBOX — Lista de elementos seleccionables
# ============================================================
# Muestra una lista. El usuario puede seleccionar uno o varios elementos.

tk.Label(ventana, text="── 4. LISTBOX ──", font=("Arial", 12, "bold"),
         bg="white").pack(pady=(15, 5))

frame_lista = tk.Frame(ventana, bg="white")
frame_lista.pack()

listbox = tk.Listbox(frame_lista, width=30, height=4, font=("Arial", 11),
                     selectmode="single")  # selectmode="multiple" para seleccionar varios

# Agregar elementos a la lista
frutas = ["Manzana", "Pera", "Naranja", "Uva", "Mango"]
for fruta in frutas:
    listbox.insert(tk.END, fruta)   # tk.END = al final de la lista

listbox.pack(side="left")

# Scrollbar (barra de desplazamiento) vinculada al Listbox
scrollbar = tk.Scrollbar(frame_lista)
scrollbar.pack(side="right", fill="y")
listbox.config(yscrollcommand=scrollbar.set)
scrollbar.config(command=listbox.yview)

def ver_listbox():
    seleccion = listbox.curselection()   # retorna tupla con índices seleccionados
    if seleccion:
        indice = seleccion[0]            # primer índice seleccionado
        valor = listbox.get(indice)      # obtener el texto en ese índice
        etiqueta_lista.config(text=f"Seleccionaste: {valor}")
    else:
        etiqueta_lista.config(text="No seleccionaste nada.")

etiqueta_lista = tk.Label(ventana, text="", bg="white", fg="navy", font=("Arial", 10))
etiqueta_lista.pack(pady=3)
tk.Button(ventana, text="Ver selección", command=ver_listbox, bg="orange").pack(pady=3)


ventana.mainloop()
