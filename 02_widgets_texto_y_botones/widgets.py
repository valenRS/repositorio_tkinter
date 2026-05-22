# ============================================================
# MÓDULO 02 — WIDGETS: TEXTO Y BOTONES
# ============================================================
# Un "widget" es cualquier elemento visual: etiqueta, botón,
# campo de texto, etc. En este módulo verás los más usados.
#
# Para ejecutar: python3 widgets.py
# ============================================================

import tkinter as tk

ventana = tk.Tk()
ventana.title("Módulo 02 — Widgets básicos")
ventana.geometry("500x600")
ventana.configure(bg="white")


# ============================================================
# 1. LABEL — Muestra texto (no se puede editar)
# ============================================================
# Es solo para mostrar información al usuario.

tk.Label(ventana, text="── 1. LABEL ──", font=("Arial", 12, "bold"), bg="white").pack(pady=(15, 5))

# Label simple
tk.Label(ventana, text="Soy un Label simple", bg="white").pack()

# Label con fuente personalizada
tk.Label(
    ventana,
    text="Texto grande en negrita",
    font=("Arial", 16, "bold"),  # (fuente, tamaño, estilo)
    fg="darkblue",               # color del texto
    bg="white"
).pack()

# Label con fondo de color (útil para resaltar información)
tk.Label(
    ventana,
    text="  Label con fondo amarillo  ",
    bg="yellow",
    fg="black",
    font=("Arial", 11)
).pack(pady=5)


# ============================================================
# 2. BUTTON — Botón que ejecuta una acción al hacer clic
# ============================================================
# command= indica qué función se ejecuta cuando se hace clic.

tk.Label(ventana, text="── 2. BUTTON ──", font=("Arial", 12, "bold"), bg="white").pack(pady=(15, 5))

# Función que se ejecuta cuando se hace clic
def al_hacer_clic():
    print("¡Me hicieron clic!")  # imprime en la consola

def cambiar_texto():
    # Cambia el texto del label dinámicamente
    etiqueta_dinamica.config(text="¡El texto cambió!")

tk.Button(
    ventana,
    text="Clic aquí",
    command=al_hacer_clic,       # ← sin paréntesis! solo el nombre de la función
    bg="lightgreen",
    fg="black",
    font=("Arial", 11),
    width=15,                    # ancho en caracteres
    height=1                     # alto en líneas
).pack(pady=3)

etiqueta_dinamica = tk.Label(ventana, text="El texto original", bg="white", font=("Arial", 11))
etiqueta_dinamica.pack(pady=3)

tk.Button(ventana, text="Cambiar texto del Label", command=cambiar_texto, bg="orange").pack(pady=3)


# ============================================================
# 3. ENTRY — Campo de texto de una sola línea
# ============================================================
# Sirve para que el usuario escriba datos: nombre, número, etc.

tk.Label(ventana, text="── 3. ENTRY ──", font=("Arial", 12, "bold"), bg="white").pack(pady=(15, 5))

tk.Label(ventana, text="Escribe tu nombre:", bg="white").pack()

campo_nombre = tk.Entry(
    ventana,
    width=30,                    # ancho en caracteres
    font=("Arial", 12),
    bg="lightyellow"             # color del campo
)
campo_nombre.pack(pady=3)

# Entry con placeholder simulado (texto por defecto que desaparece)
campo_placeholder = tk.Entry(ventana, width=30, font=("Arial", 12), fg="gray")
campo_placeholder.insert(0, "Escribe aquí...")  # insert(posición, texto)
campo_placeholder.pack(pady=3)

# Entry para contraseñas (oculta el texto con asteriscos)
tk.Label(ventana, text="Contraseña:", bg="white").pack()
campo_password = tk.Entry(ventana, width=30, font=("Arial", 12), show="*")  # show="*" oculta el texto
campo_password.pack(pady=3)

def mostrar_nombre():
    # .get() lee lo que el usuario escribió
    nombre = campo_nombre.get()
    etiqueta_resultado.config(text=f"Hola, {nombre}!")

tk.Button(ventana, text="Saludar", command=mostrar_nombre, bg="lightblue").pack(pady=5)
etiqueta_resultado = tk.Label(ventana, text="", bg="white", font=("Arial", 12))
etiqueta_resultado.pack()


# ============================================================
# 4. TEXT — Área de texto de múltiples líneas
# ============================================================
# Sirve para textos largos (como un cuadro de notas).

tk.Label(ventana, text="── 4. TEXT (multilínea) ──", font=("Arial", 12, "bold"), bg="white").pack(pady=(15, 5))

area_texto = tk.Text(
    ventana,
    width=40,     # ancho en caracteres
    height=4,     # alto en líneas
    font=("Arial", 11)
)
area_texto.pack(pady=3)
area_texto.insert("1.0", "Aquí puedes escribir\nvarias líneas de texto.")

def leer_texto():
    # "1.0" = desde la línea 1, carácter 0
    # "end" = hasta el final
    contenido = area_texto.get("1.0", "end")
    print("Contenido del Text:", contenido)

tk.Button(ventana, text="Leer Text (ver consola)", command=leer_texto, bg="lightyellow").pack(pady=3)


ventana.mainloop()
