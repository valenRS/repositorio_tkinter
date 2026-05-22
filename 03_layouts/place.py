# ============================================================
# MÓDULO 03 — LAYOUT: place()
# ============================================================
# place() permite posicionar un widget en coordenadas exactas.
# Es el más preciso pero el más difícil de mantener.
# Se usa cuando necesitas posiciones absolutas (x, y en píxeles).
#
# Para ejecutar: python3 place.py
# ============================================================

import tkinter as tk

ventana = tk.Tk()
ventana.title("Módulo 03 — Layout: place()")
ventana.geometry("400x350")
ventana.configure(bg="lightyellow")

# ── Opciones de place() ────────────────────────────────────
#
#   x=      → posición horizontal en píxeles desde la izquierda
#   y=      → posición vertical en píxeles desde arriba
#   width=  → ancho del widget en píxeles
#   height= → alto del widget en píxeles
#   relx=   → posición relativa 0.0 a 1.0 (0.5 = centro horizontal)
#   rely=   → posición relativa 0.0 a 1.0 (0.5 = centro vertical)
#   anchor= → qué punto del widget se posiciona en x,y
#             "nw" (defecto), "center", "ne", "sw", etc.
# ──────────────────────────────────────────────────────────

# Widget en coordenadas absolutas
tk.Label(ventana, text="Estoy en x=10, y=10", bg="lightblue",
         font=("Arial", 11)).place(x=10, y=10)

tk.Label(ventana, text="Estoy en x=200, y=10", bg="lightgreen",
         font=("Arial", 11)).place(x=200, y=10)

tk.Label(ventana, text="Estoy en x=10, y=80", bg="orange",
         font=("Arial", 11)).place(x=10, y=80)

# Widget centrado usando relx y rely (posición relativa)
# relx=0.5 = 50% del ancho → centro horizontal
# rely=0.5 = 50% del alto  → centro vertical
# anchor="center" = el punto central del widget queda en esas coordenadas
tk.Label(
    ventana,
    text="¡Estoy centrado!",
    bg="white",
    fg="darkblue",
    font=("Arial", 13, "bold"),
    width=20,
    height=2,
    relief="ridge"             # borde tipo "ridge"
).place(relx=0.5, rely=0.5, anchor="center")

# Widget en la esquina inferior derecha
tk.Button(
    ventana,
    text="Esquina inferior derecha",
    bg="red",
    fg="white",
    font=("Arial", 10)
).place(relx=1.0, rely=1.0, anchor="se")  # "se" = south-east = abajo a la derecha

# Widget con tamaño explícito
tk.Entry(ventana, font=("Arial", 11)).place(x=50, y=180, width=200, height=30)
tk.Label(ventana, text="↑ Entry en x=50, y=180", bg="lightyellow",
         font=("Arial", 9)).place(x=50, y=215)

ventana.mainloop()
