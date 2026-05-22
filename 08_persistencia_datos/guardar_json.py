# ============================================================
# MÓDULO 08 — PERSISTENCIA DE DATOS CON JSON
# ============================================================
# "Persistencia" = que los datos NO desaparezcan cuando se cierra la app.
# El parcial lo pide explícitamente.
#
# JSON es un formato de archivo como este:
# [
#   {"nombre": "Ana", "edad": 20},
#   {"nombre": "Luis", "edad": 22}
# ]
#
# Python tiene el módulo 'json' incluido — no se instala nada.
#
# Para ejecutar: python3 guardar_json.py
# ============================================================

import tkinter as tk
from tkinter import messagebox
import json
import os

# ─── Nombre del archivo donde se guardan los datos ───────────
ARCHIVO_DATOS = "datos_personas.json"


# ============================================================
# FUNCIONES DE PERSISTENCIA
# (úsalas igual en tus exámenes — solo cambia el nombre del archivo)
# ============================================================

def cargar_datos():
    """Lee el archivo JSON y retorna una lista. Si no existe, retorna lista vacía."""
    if os.path.exists(ARCHIVO_DATOS):
        with open(ARCHIVO_DATOS, "r", encoding="utf-8") as f:
            return json.load(f)
    return []   # si el archivo no existe, empezar con lista vacía

def guardar_datos(lista):
    """Escribe la lista completa en el archivo JSON."""
    with open(ARCHIVO_DATOS, "w", encoding="utf-8") as f:
        # indent=4 hace que el archivo sea legible (sangría de 4 espacios)
        # ensure_ascii=False permite caracteres como ñ, á, é, etc.
        json.dump(lista, f, indent=4, ensure_ascii=False)


# ============================================================
# APLICACIÓN
# ============================================================

class AppPersonas(tk.Tk):

    def __init__(self):
        super().__init__()
        self.title("Módulo 08 — Persistencia con JSON")
        self.geometry("480x420")
        self.configure(bg="white")

        # Cargar datos del archivo al iniciar la app
        # Si el archivo existe, los datos se recuperan automáticamente
        self.personas = cargar_datos()

        self._crear_widgets()
        self._actualizar_lista()

    def _crear_widgets(self):
        tk.Label(self, text="Registro con guardado en JSON",
                 font=("Arial", 14, "bold"), bg="white").pack(pady=10)

        # Formulario
        frame = tk.Frame(self, bg="white")
        frame.pack(padx=20)

        tk.Label(frame, text="Nombre:", bg="white").grid(row=0, column=0, sticky="w", pady=4)
        self.entrada_nombre = tk.Entry(frame, width=22, font=("Arial", 11))
        self.entrada_nombre.grid(row=0, column=1, padx=10, pady=4)

        tk.Label(frame, text="Edad:", bg="white").grid(row=1, column=0, sticky="w", pady=4)
        self.entrada_edad = tk.Entry(frame, width=22, font=("Arial", 11))
        self.entrada_edad.grid(row=1, column=1, padx=10, pady=4)

        tk.Label(frame, text="Ciudad:", bg="white").grid(row=2, column=0, sticky="w", pady=4)
        self.entrada_ciudad = tk.Entry(frame, width=22, font=("Arial", 11))
        self.entrada_ciudad.grid(row=2, column=1, padx=10, pady=4)

        # Botones
        frame_btn = tk.Frame(self, bg="white")
        frame_btn.pack(pady=10)

        tk.Button(frame_btn, text="Guardar",
                  command=self._guardar_persona, bg="lightgreen", width=12).pack(side="left", padx=5)
        tk.Button(frame_btn, text="Eliminar seleccionado",
                  command=self._eliminar_persona, bg="#ffcccc", width=18).pack(side="left", padx=5)

        # Lista
        tk.Label(self, text="Personas guardadas (persisten al cerrar):",
                 bg="white", font=("Arial", 10)).pack(anchor="w", padx=20)

        frame_lista = tk.Frame(self, bg="white")
        frame_lista.pack(padx=20, fill="both", expand=True)

        self.listbox = tk.Listbox(frame_lista, font=("Arial", 10), height=8)
        self.listbox.pack(side="left", fill="both", expand=True)
        scrollbar = tk.Scrollbar(frame_lista, command=self.listbox.yview)
        scrollbar.pack(side="right", fill="y")
        self.listbox.config(yscrollcommand=scrollbar.set)

        # Info del archivo
        self.etiqueta_archivo = tk.Label(
            self, text=f"Archivo: {os.path.abspath(ARCHIVO_DATOS)}",
            bg="white", fg="gray", font=("Arial", 8), wraplength=460
        )
        self.etiqueta_archivo.pack(pady=5)

    def _guardar_persona(self):
        nombre = self.entrada_nombre.get().strip()
        edad   = self.entrada_edad.get().strip()
        ciudad = self.entrada_ciudad.get().strip()

        if not nombre or not edad or not ciudad:
            messagebox.showwarning("Campos vacíos", "Completa todos los campos.")
            return

        # Crear el diccionario con los datos
        persona = {"nombre": nombre, "edad": edad, "ciudad": ciudad}

        # Agregar a la lista en memoria
        self.personas.append(persona)

        # ─── GUARDAR EN ARCHIVO ───────────────────────────────
        guardar_datos(self.personas)
        # ──────────────────────────────────────────────────────

        # Limpiar campos
        self.entrada_nombre.delete(0, tk.END)
        self.entrada_edad.delete(0, tk.END)
        self.entrada_ciudad.delete(0, tk.END)

        self._actualizar_lista()
        messagebox.showinfo("Guardado", f"'{nombre}' guardado en el archivo JSON.")

    def _eliminar_persona(self):
        seleccion = self.listbox.curselection()
        if not seleccion:
            messagebox.showwarning("Nada seleccionado", "Selecciona una persona de la lista.")
            return

        indice = seleccion[0]
        persona = self.personas[indice]

        if messagebox.askyesno("Confirmar", f"¿Eliminar a '{persona['nombre']}'?"):
            self.personas.pop(indice)
            guardar_datos(self.personas)   # guardar el cambio inmediatamente
            self._actualizar_lista()

    def _actualizar_lista(self):
        """Refresca el Listbox con los datos actuales."""
        self.listbox.delete(0, tk.END)
        for p in self.personas:
            self.listbox.insert(tk.END, f"{p['nombre']}  |  {p['edad']} años  |  {p['ciudad']}")


if __name__ == "__main__":
    app = AppPersonas()
    app.mainloop()
