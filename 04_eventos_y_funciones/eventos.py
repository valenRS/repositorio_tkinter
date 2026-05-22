# ============================================================
# MÓDULO 04 — EVENTOS Y FUNCIONES
# ============================================================
# Un "evento" es cualquier acción del usuario: hacer clic,
# presionar una tecla, mover el mouse, etc.
# Aquí aprenderás a reaccionar a esas acciones.
#
# Para ejecutar: python3 eventos.py
# ============================================================

import tkinter as tk
from tkinter import messagebox

ventana = tk.Tk()
ventana.title("Módulo 04 — Eventos y Funciones")
ventana.geometry("480x550")
ventana.configure(bg="white")


# ============================================================
# 1. command= en botón (el más común)
# ============================================================
# La forma más simple de reaccionar al usuario.
# Solo funciona con botones.

tk.Label(ventana, text="── 1. command= en botón ──", font=("Arial", 12, "bold"),
         bg="white").pack(pady=(15, 5))

contador = [0]  # usamos lista para poder modificarlo dentro de la función

def incrementar():
    contador[0] += 1
    etiqueta_contador.config(text=f"Clics: {contador[0]}")

etiqueta_contador = tk.Label(ventana, text="Clics: 0", font=("Arial", 13), bg="white")
etiqueta_contador.pack(pady=3)

tk.Button(ventana, text="Hacer clic", command=incrementar,
          bg="lightblue", font=("Arial", 11), width=15).pack(pady=5)


# ============================================================
# 2. Leer Entry y actualizar Label
# ============================================================
# Patrón MUY común en exámenes: el usuario escribe → presiona botón → se muestra resultado.

tk.Label(ventana, text="── 2. Leer Entry + actualizar Label ──",
         font=("Arial", 12, "bold"), bg="white").pack(pady=(15, 5))

tk.Label(ventana, text="Escribe tu nombre:", bg="white").pack()
campo_nombre = tk.Entry(ventana, width=30, font=("Arial", 11))
campo_nombre.pack(pady=3)

etiqueta_saludo = tk.Label(ventana, text="", bg="white", fg="darkblue", font=("Arial", 12))
etiqueta_saludo.pack(pady=3)

def saludar():
    nombre = campo_nombre.get().strip()  # .strip() elimina espacios al inicio y final
    if nombre == "":
        etiqueta_saludo.config(text="⚠ Escribe tu nombre primero.", fg="red")
    else:
        etiqueta_saludo.config(text=f"¡Hola, {nombre}!", fg="green")

tk.Button(ventana, text="Saludar", command=saludar, bg="lightgreen", width=12).pack(pady=5)


# ============================================================
# 3. bind() — Reaccionar a teclas del teclado
# ============================================================
# bind() conecta un evento de teclado/mouse a una función.
# Formato: widget.bind("evento", función)
# El evento viene entre < > : <Return>, <KeyPress>, <Button-1>, etc.

tk.Label(ventana, text="── 3. bind() — eventos de teclado ──",
         font=("Arial", 12, "bold"), bg="white").pack(pady=(15, 5))

tk.Label(ventana, text="Presiona Enter después de escribir:", bg="white").pack()
campo_enter = tk.Entry(ventana, width=30, font=("Arial", 11))
campo_enter.pack(pady=3)

etiqueta_enter = tk.Label(ventana, text="", bg="white", font=("Arial", 11))
etiqueta_enter.pack(pady=3)

# event es un parámetro que recibe automáticamente bind()
# aunque no lo uses, debes declararlo en la función
def al_presionar_enter(event):
    texto = campo_enter.get().strip()
    etiqueta_enter.config(text=f"Escribiste: {texto}")

# <Return> es la tecla Enter
campo_enter.bind("<Return>", al_presionar_enter)


# ============================================================
# 4. StringVar — Variable ligada a un widget
# ============================================================
# StringVar es una variable especial de Tkinter.
# Cuando cambia su valor, automáticamente actualiza el widget ligado.
# También sirve para leer/escribir el contenido de un Entry.

tk.Label(ventana, text="── 4. StringVar ──", font=("Arial", 12, "bold"),
         bg="white").pack(pady=(15, 5))

# Crear la variable
variable_texto = tk.StringVar()
variable_texto.set("Valor inicial")  # asignar un valor

# Entry ligado a la variable — cuando se escribe, variable_texto cambia automáticamente
tk.Entry(ventana, textvariable=variable_texto, width=30, font=("Arial", 11)).pack(pady=3)

# Label ligado a la variable — cuando variable_texto cambia, el label se actualiza SOLO
tk.Label(ventana, textvariable=variable_texto, bg="lightyellow",
         font=("Arial", 11), width=30).pack(pady=3)

tk.Label(ventana, text="(El label de arriba refleja lo que escribas en el Entry)",
         bg="white", fg="gray", font=("Arial", 9)).pack()

# ── Truco: StringVar para limpiar todos los campos de una vez ──
def limpiar_todo():
    campo_nombre.delete(0, tk.END)
    campo_enter.delete(0, tk.END)
    variable_texto.set("")
    etiqueta_saludo.config(text="")
    etiqueta_enter.config(text="")

tk.Button(ventana, text="Limpiar todo", command=limpiar_todo,
          bg="gray", fg="white", width=15).pack(pady=15)


ventana.mainloop()
