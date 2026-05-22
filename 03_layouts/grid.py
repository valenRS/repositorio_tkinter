# ============================================================
# MÓDULO 03 — LAYOUT: grid()
# ============================================================
# grid() organiza los widgets en una tabla de filas y columnas.
# Es el layout MÁS USADO en exámenes porque da control total.
#
# Para ejecutar: python3 grid.py
# ============================================================

import tkinter as tk

ventana = tk.Tk()
ventana.title("Módulo 03 — Layout: grid()")
ventana.geometry("450x400")
ventana.configure(bg="white")

# ── Conceptos clave de grid() ──────────────────────────────
#
#   row=    → en qué fila va el widget (empieza en 0)
#   column= → en qué columna va el widget (empieza en 0)
#   columnspan= → cuántas columnas ocupa
#   rowspan=    → cuántas filas ocupa
#   sticky= → a qué lado se "pega" dentro de su celda
#             "w" = izquierda, "e" = derecha, "n" = arriba, "s" = abajo
#             "ew" = se estira de lado a lado
#   padx=   → espacio horizontal fuera del widget
#   pady=   → espacio vertical fuera del widget
#   ipadx=  → espacio horizontal DENTRO del widget
#   ipady=  → espacio vertical DENTRO del widget
# ──────────────────────────────────────────────────────────

# Título
tk.Label(ventana, text="Formulario de Registro", font=("Arial", 14, "bold"),
         bg="white").grid(row=0, column=0, columnspan=2, pady=15)

# --- Fila 1: Nombre ---
tk.Label(ventana, text="Nombre:", bg="white", anchor="w").grid(
    row=1, column=0, padx=20, pady=8, sticky="w"
)
entrada_nombre = tk.Entry(ventana, width=25, font=("Arial", 11))
entrada_nombre.grid(row=1, column=1, padx=10, pady=8, sticky="ew")

# --- Fila 2: Apellido ---
tk.Label(ventana, text="Apellido:", bg="white", anchor="w").grid(
    row=2, column=0, padx=20, pady=8, sticky="w"
)
entrada_apellido = tk.Entry(ventana, width=25, font=("Arial", 11))
entrada_apellido.grid(row=2, column=1, padx=10, pady=8, sticky="ew")

# --- Fila 3: Edad ---
tk.Label(ventana, text="Edad:", bg="white", anchor="w").grid(
    row=3, column=0, padx=20, pady=8, sticky="w"
)
entrada_edad = tk.Entry(ventana, width=25, font=("Arial", 11))
entrada_edad.grid(row=3, column=1, padx=10, pady=8, sticky="ew")

# --- Fila 4: Email ---
tk.Label(ventana, text="Email:", bg="white", anchor="w").grid(
    row=4, column=0, padx=20, pady=8, sticky="w"
)
entrada_email = tk.Entry(ventana, width=25, font=("Arial", 11))
entrada_email.grid(row=4, column=1, padx=10, pady=8, sticky="ew")

# --- Fila 5: Resultado ---
etiqueta_resultado = tk.Label(ventana, text="", bg="white", fg="green",
                               font=("Arial", 11), wraplength=380)
etiqueta_resultado.grid(row=5, column=0, columnspan=2, pady=10)

# --- Fila 6: Botones ---
def registrar():
    nombre   = entrada_nombre.get().strip()
    apellido = entrada_apellido.get().strip()
    edad     = entrada_edad.get().strip()
    email    = entrada_email.get().strip()

    if not nombre or not apellido or not edad or not email:
        etiqueta_resultado.config(text="⚠ Por favor llena todos los campos.", fg="red")
        return

    etiqueta_resultado.config(
        text=f"✓ Registrado: {nombre} {apellido}, {edad} años — {email}",
        fg="green"
    )

def limpiar():
    entrada_nombre.delete(0, tk.END)     # borra desde posición 0 hasta el final
    entrada_apellido.delete(0, tk.END)
    entrada_edad.delete(0, tk.END)
    entrada_email.delete(0, tk.END)
    etiqueta_resultado.config(text="")

tk.Button(ventana, text="Registrar", command=registrar,
          bg="green", fg="white", width=12).grid(row=6, column=0, pady=15, padx=20)

tk.Button(ventana, text="Limpiar", command=limpiar,
          bg="gray", fg="white", width=12).grid(row=6, column=1, pady=15, padx=10)

# Importante: columnconfigure() hace que la columna 1 se expanda si se cambia el tamaño
ventana.columnconfigure(1, weight=1)

ventana.mainloop()
