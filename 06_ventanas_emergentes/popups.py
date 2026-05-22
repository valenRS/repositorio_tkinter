# ============================================================
# MÓDULO 06 — VENTANAS EMERGENTES (messagebox)
# ============================================================
# messagebox permite mostrar cuadros de diálogo: mensajes
# de información, errores, advertencias, confirmaciones, etc.
#
# Para ejecutar: python3 popups.py
# ============================================================

import tkinter as tk
from tkinter import messagebox   # hay que importarlo aparte

ventana = tk.Tk()
ventana.title("Módulo 06 — Ventanas Emergentes")
ventana.geometry("400x420")
ventana.configure(bg="white")

tk.Label(ventana, text="Tipos de messagebox", font=("Arial", 14, "bold"),
         bg="white").pack(pady=15)


# ============================================================
# 1. showinfo — Mensaje informativo (ícono azul ℹ)
# ============================================================
def mostrar_info():
    messagebox.showinfo(
        title="Información",              # título del cuadro
        message="¡Operación exitosa!\nEl registro fue guardado."   # mensaje
    )

tk.Button(ventana, text="showinfo  (ℹ Información)", command=mostrar_info,
          bg="lightblue", width=30, font=("Arial", 11)).pack(pady=6)


# ============================================================
# 2. showwarning — Advertencia (ícono amarillo ⚠)
# ============================================================
def mostrar_advertencia():
    messagebox.showwarning(
        title="Advertencia",
        message="¡Atención!\nAlgunos campos están incompletos."
    )

tk.Button(ventana, text="showwarning  (⚠ Advertencia)", command=mostrar_advertencia,
          bg="lightyellow", width=30, font=("Arial", 11)).pack(pady=6)


# ============================================================
# 3. showerror — Error (ícono rojo ✖)
# ============================================================
def mostrar_error():
    messagebox.showerror(
        title="Error",
        message="Ocurrió un error.\nPor favor intenta de nuevo."
    )

tk.Button(ventana, text="showerror  (✖ Error)", command=mostrar_error,
          bg="#ffcccc", width=30, font=("Arial", 11)).pack(pady=6)


# ============================================================
# 4. askyesno — Pregunta Sí/No (retorna True o False)
# ============================================================
# MUY ÚTIL: sirve para confirmar antes de eliminar algo.

etiqueta_respuesta = tk.Label(ventana, text="", bg="white", fg="navy",
                               font=("Arial", 11))

def preguntar_si_no():
    # retorna True si el usuario hace clic en "Sí"
    # retorna False si hace clic en "No"
    respuesta = messagebox.askyesno(
        title="Confirmar",
        message="¿Estás seguro de que quieres eliminar este registro?"
    )
    if respuesta:
        etiqueta_respuesta.config(text="Dijiste: SÍ → eliminado.", fg="red")
    else:
        etiqueta_respuesta.config(text="Dijiste: NO → no se eliminó.", fg="green")

tk.Button(ventana, text="askyesno  (¿Sí o No?)", command=preguntar_si_no,
          bg="lightgreen", width=30, font=("Arial", 11)).pack(pady=6)

etiqueta_respuesta.pack(pady=5)


# ============================================================
# 5. askokcancel — Pregunta OK/Cancelar (retorna True o False)
# ============================================================
def preguntar_ok_cancelar():
    respuesta = messagebox.askokcancel(
        title="Confirmar acción",
        message="¿Deseas continuar con esta operación?"
    )
    if respuesta:
        etiqueta_respuesta.config(text="Hiciste clic en: OK", fg="blue")
    else:
        etiqueta_respuesta.config(text="Hiciste clic en: Cancelar", fg="gray")

tk.Button(ventana, text="askokcancel  (OK / Cancelar)", command=preguntar_ok_cancelar,
          bg="lavender", width=30, font=("Arial", 11)).pack(pady=6)


# ── Resumen de retornos ─────────────────────────────────────
tk.Label(
    ventana,
    text="showinfo/warning/error → no retorna nada\naskyesno / askokcancel → True (sí/ok) o False (no/cancelar)",
    bg="white", fg="gray", font=("Arial", 9), justify="center"
).pack(pady=10)

ventana.mainloop()
