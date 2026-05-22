# ============================================================
# MÓDULO 03 — LAYOUT: pack()
# ============================================================
# pack() apila los widgets uno debajo del otro (o al lado).
# Es el más simple pero menos controlable que grid().
#
# Para ejecutar: python3 pack.py
# ============================================================

import tkinter as tk

ventana = tk.Tk()
ventana.title("Módulo 03 — Layout: pack()")
ventana.geometry("350x450")
ventana.configure(bg="white")

# ── Opciones de pack() ─────────────────────────────────────
#
#   side=    → de qué lado apila: "top"(defecto), "bottom", "left", "right"
#   fill=    → si se estira: "x" (horizontal), "y" (vertical), "both"
#   expand=  → si ocupa espacio extra disponible: True / False
#   padx=    → espacio horizontal fuera del widget
#   pady=    → espacio vertical fuera del widget
#   anchor=  → dónde se alinea: "center"(defecto), "w", "e", "n", "s"
# ──────────────────────────────────────────────────────────

tk.Label(ventana, text="Ejemplos de pack()", font=("Arial", 14, "bold"),
         bg="white").pack(pady=10)

# --- pack() básico: apila de arriba hacia abajo ---
tk.Label(ventana, text="Widget 1 (top — defecto)", bg="lightblue",
         font=("Arial", 11)).pack(pady=5)

tk.Label(ventana, text="Widget 2 (también top)", bg="lightgreen",
         font=("Arial", 11)).pack(pady=5)

# --- fill="x": el widget se estira para ocupar todo el ancho ---
tk.Label(ventana, text="fill='x' — ocupa todo el ancho", bg="yellow",
         font=("Arial", 11)).pack(fill="x", pady=5, padx=20)

# --- Widgets uno al lado del otro con side="left" ---
frame_horizontal = tk.Frame(ventana, bg="white")
frame_horizontal.pack(pady=10)

tk.Button(frame_horizontal, text="Izquierda", bg="orange").pack(side="left", padx=5)
tk.Button(frame_horizontal, text="Centro",    bg="orange").pack(side="left", padx=5)
tk.Button(frame_horizontal, text="Derecha",   bg="orange").pack(side="left", padx=5)

# --- anchor: alinear a la izquierda o derecha ---
tk.Label(ventana, text="← anchor='w' (izquierda)", bg="white",
         font=("Arial", 11)).pack(anchor="w", padx=20, pady=3)

tk.Label(ventana, text="anchor='e' (derecha) →", bg="white",
         font=("Arial", 11)).pack(anchor="e", padx=20, pady=3)

tk.Label(ventana, text="anchor='center' (centro)", bg="white",
         font=("Arial", 11)).pack(anchor="center", pady=3)

# --- Un separador visual simple ---
tk.Frame(ventana, height=2, bg="gray").pack(fill="x", padx=20, pady=10)

tk.Label(ventana, text="¡Listo! pack() apila de arriba hacia abajo.",
         bg="white", fg="navy", font=("Arial", 10, "italic"),
         wraplength=300).pack(pady=5)

ventana.mainloop()
