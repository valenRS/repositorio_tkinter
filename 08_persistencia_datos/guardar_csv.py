# ============================================================
# MÓDULO 08 — PERSISTENCIA DE DATOS CON CSV
# ============================================================
# CSV = Comma Separated Values (valores separados por comas).
# Es como una hoja de Excel guardada como texto:
#
#   nombre,edad,ciudad
#   Ana,20,Bogotá
#   Luis,22,Medellín
#
# Python tiene el módulo 'csv' incluido — no se instala nada.
# Usa JSON si necesitas datos complejos (listas, anidados).
# Usa CSV si los datos son simples (filas y columnas planas).
#
# Para ejecutar: python3 guardar_csv.py
# ============================================================

import tkinter as tk
from tkinter import messagebox
import csv
import os

ARCHIVO_CSV = "registro_productos.csv"
# Las columnas del CSV — el orden importa
COLUMNAS = ["codigo", "nombre", "precio", "stock"]


# ============================================================
# FUNCIONES DE PERSISTENCIA CSV
# ============================================================

def cargar_csv():
    """Lee el CSV y retorna una lista de diccionarios."""
    if not os.path.exists(ARCHIVO_CSV):
        return []
    productos = []
    with open(ARCHIVO_CSV, "r", encoding="utf-8", newline="") as f:
        reader = csv.DictReader(f)   # DictReader convierte cada fila en diccionario
        for fila in reader:
            productos.append(dict(fila))
    return productos

def guardar_csv(lista):
    """Escribe la lista completa en el CSV (sobreescribe el archivo)."""
    with open(ARCHIVO_CSV, "w", encoding="utf-8", newline="") as f:
        writer = csv.DictWriter(f, fieldnames=COLUMNAS)
        writer.writeheader()         # escribe la fila de encabezados
        writer.writerows(lista)      # escribe todas las filas


# ============================================================
# APLICACIÓN
# ============================================================

class AppProductos(tk.Tk):

    def __init__(self):
        super().__init__()
        self.title("Módulo 08 — Persistencia con CSV")
        self.geometry("520x430")
        self.configure(bg="white")

        self.productos = cargar_csv()
        self._crear_widgets()
        self._actualizar_lista()

    def _crear_widgets(self):
        tk.Label(self, text="Inventario — Guardado en CSV",
                 font=("Arial", 14, "bold"), bg="white").pack(pady=10)

        frame = tk.Frame(self, bg="white")
        frame.pack(padx=20)

        campos = [("Código:", "entrada_codigo"), ("Nombre:", "entrada_nombre"),
                  ("Precio $:", "entrada_precio"), ("Stock:", "entrada_stock")]

        for i, (label, attr) in enumerate(campos):
            tk.Label(frame, text=label, bg="white").grid(row=i, column=0, sticky="w", pady=3)
            entrada = tk.Entry(frame, width=22, font=("Arial", 11))
            entrada.grid(row=i, column=1, padx=10, pady=3)
            setattr(self, attr, entrada)   # equivale a: self.entrada_codigo = entrada

        frame_btn = tk.Frame(self, bg="white")
        frame_btn.pack(pady=8)

        tk.Button(frame_btn, text="Guardar en CSV",
                  command=self._guardar, bg="lightgreen", width=14).pack(side="left", padx=5)
        tk.Button(frame_btn, text="Eliminar",
                  command=self._eliminar, bg="#ffcccc", width=10).pack(side="left", padx=5)

        tk.Label(self, text="Productos (guardados en CSV):", bg="white",
                 font=("Arial", 10)).pack(anchor="w", padx=20)

        frame_lista = tk.Frame(self, bg="white")
        frame_lista.pack(padx=20, fill="both", expand=True)

        self.listbox = tk.Listbox(frame_lista, font=("Arial", 10), height=8)
        self.listbox.pack(side="left", fill="both", expand=True)
        sb = tk.Scrollbar(frame_lista, command=self.listbox.yview)
        sb.pack(side="right", fill="y")
        self.listbox.config(yscrollcommand=sb.set)

        tk.Label(self, text=f"Archivo: {os.path.abspath(ARCHIVO_CSV)}",
                 bg="white", fg="gray", font=("Arial", 8), wraplength=480).pack(pady=4)

    def _guardar(self):
        codigo = self.entrada_codigo.get().strip()
        nombre = self.entrada_nombre.get().strip()
        precio = self.entrada_precio.get().strip()
        stock  = self.entrada_stock.get().strip()

        if not all([codigo, nombre, precio, stock]):
            messagebox.showwarning("Campos vacíos", "Completa todos los campos.")
            return

        self.productos.append({"codigo": codigo, "nombre": nombre,
                                "precio": precio,  "stock": stock})
        guardar_csv(self.productos)

        for entrada in [self.entrada_codigo, self.entrada_nombre,
                        self.entrada_precio, self.entrada_stock]:
            entrada.delete(0, tk.END)

        self._actualizar_lista()
        messagebox.showinfo("Guardado", f"'{nombre}' guardado en el CSV.")

    def _eliminar(self):
        sel = self.listbox.curselection()
        if not sel:
            messagebox.showwarning("Sin selección", "Selecciona un producto.")
            return
        idx = sel[0]
        nombre = self.productos[idx]["nombre"]
        if messagebox.askyesno("Confirmar", f"¿Eliminar '{nombre}'?"):
            self.productos.pop(idx)
            guardar_csv(self.productos)
            self._actualizar_lista()

    def _actualizar_lista(self):
        self.listbox.delete(0, tk.END)
        for p in self.productos:
            self.listbox.insert(
                tk.END, f"[{p['codigo']}]  {p['nombre']}  —  ${p['precio']}  —  Stock: {p['stock']}"
            )


if __name__ == "__main__":
    app = AppProductos()
    app.mainloop()
