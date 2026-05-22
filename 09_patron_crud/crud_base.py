# ============================================================
# MÓDULO 09 — PATRÓN CRUD COMPLETO
# ============================================================
# CRUD = Create (crear), Read (leer), Update (actualizar), Delete (eliminar)
# Es el patrón que se repite en TODOS los exámenes de interfaces.
#
# Este archivo es la PLANTILLA BASE que puedes adaptar para cualquier
# sistema: biblioteca, estudiantes, empleados, productos, etc.
#
# Estructura:
#  - Formulario (campos de texto)
#  - Tabla (Treeview) para mostrar los registros
#  - Botones: Agregar, Editar, Eliminar, Limpiar
#  - Búsqueda/filtro
#  - Persistencia con JSON
#
# Para ejecutar: python3 crud_base.py
# ============================================================

import tkinter as tk
from tkinter import ttk, messagebox
import json
import os

ARCHIVO = "crud_registros.json"


def cargar():
    if os.path.exists(ARCHIVO):
        with open(ARCHIVO, "r", encoding="utf-8") as f:
            return json.load(f)
    return []

def guardar(lista):
    with open(ARCHIVO, "w", encoding="utf-8") as f:
        json.dump(lista, f, indent=4, ensure_ascii=False)


# ============================================================
# APLICACIÓN CRUD
# ============================================================

class AppCRUD(tk.Tk):

    def __init__(self):
        super().__init__()
        self.title("Módulo 09 — Patrón CRUD Base")
        self.geometry("700x520")
        self.configure(bg="white")

        self.registros = cargar()
        self.indice_editando = None   # None = no estamos editando ningún registro

        self._crear_widgets()
        self._actualizar_tabla()

    # ──────────────────────────────────────────────────────
    # WIDGETS
    # ──────────────────────────────────────────────────────
    def _crear_widgets(self):
        # ── Título ─────────────────────────────────────────
        tk.Label(self, text="Gestión de Registros — CRUD",
                 font=("Arial", 15, "bold"), bg="white").pack(pady=10)

        # ── Sección: Formulario ────────────────────────────
        frame_form = tk.LabelFrame(self, text=" Datos del registro ",
                                    font=("Arial", 10), bg="white")
        frame_form.pack(padx=15, fill="x", pady=5)

        # Campos (puedes cambiar los nombres para tu examen)
        tk.Label(frame_form, text="Código:", bg="white").grid(row=0, column=0, padx=8, pady=6, sticky="w")
        self.entrada_codigo = tk.Entry(frame_form, width=15, font=("Arial", 11))
        self.entrada_codigo.grid(row=0, column=1, padx=5, pady=6)

        tk.Label(frame_form, text="Nombre:", bg="white").grid(row=0, column=2, padx=8, pady=6, sticky="w")
        self.entrada_nombre = tk.Entry(frame_form, width=20, font=("Arial", 11))
        self.entrada_nombre.grid(row=0, column=3, padx=5, pady=6)

        tk.Label(frame_form, text="Categoría:", bg="white").grid(row=1, column=0, padx=8, pady=6, sticky="w")
        self.combo_categoria = ttk.Combobox(frame_form,
                                             values=["Categoría A", "Categoría B", "Categoría C"],
                                             width=13, state="readonly")
        self.combo_categoria.set("Categoría A")
        self.combo_categoria.grid(row=1, column=1, padx=5, pady=6)

        tk.Label(frame_form, text="Valor:", bg="white").grid(row=1, column=2, padx=8, pady=6, sticky="w")
        self.entrada_valor = tk.Entry(frame_form, width=20, font=("Arial", 11))
        self.entrada_valor.grid(row=1, column=3, padx=5, pady=6)

        # ── Sección: Botones ────────────────────────────────
        frame_btn = tk.Frame(self, bg="white")
        frame_btn.pack(pady=6)

        self.btn_agregar = tk.Button(frame_btn, text="➕ Agregar",
                                      command=self._agregar, bg="lightgreen", width=12, font=("Arial", 10))
        self.btn_agregar.pack(side="left", padx=4)

        self.btn_editar = tk.Button(frame_btn, text="✏ Guardar edición",
                                     command=self._guardar_edicion, bg="lightyellow",
                                     width=15, font=("Arial", 10), state="disabled")
        self.btn_editar.pack(side="left", padx=4)

        tk.Button(frame_btn, text="🗑 Eliminar",
                  command=self._eliminar, bg="#ffcccc", width=12, font=("Arial", 10)).pack(side="left", padx=4)

        tk.Button(frame_btn, text="🔄 Limpiar",
                  command=self._limpiar_form, bg="lightgray", width=10, font=("Arial", 10)).pack(side="left", padx=4)

        # ── Sección: Búsqueda ──────────────────────────────
        frame_busqueda = tk.Frame(self, bg="white")
        frame_busqueda.pack(fill="x", padx=15, pady=3)

        tk.Label(frame_busqueda, text="Buscar:", bg="white", font=("Arial", 10)).pack(side="left")
        self.entrada_busqueda = tk.Entry(frame_busqueda, width=25, font=("Arial", 11))
        self.entrada_busqueda.pack(side="left", padx=5)
        self.entrada_busqueda.bind("<KeyRelease>", lambda e: self._buscar())

        tk.Button(frame_busqueda, text="Mostrar todos", command=self._actualizar_tabla,
                  bg="white", font=("Arial", 9)).pack(side="left", padx=5)

        # ── Sección: Tabla (Treeview) ──────────────────────
        # Treeview es la "tabla" de Tkinter — ideal para mostrar registros
        frame_tabla = tk.Frame(self, bg="white")
        frame_tabla.pack(padx=15, fill="both", expand=True, pady=5)

        columnas = ("codigo", "nombre", "categoria", "valor")
        self.tabla = ttk.Treeview(frame_tabla, columns=columnas, show="headings", height=10)

        # Definir encabezados y anchos de columna
        self.tabla.heading("codigo",    text="Código")
        self.tabla.heading("nombre",    text="Nombre")
        self.tabla.heading("categoria", text="Categoría")
        self.tabla.heading("valor",     text="Valor")

        self.tabla.column("codigo",    width=80,  anchor="center")
        self.tabla.column("nombre",    width=200)
        self.tabla.column("categoria", width=110, anchor="center")
        self.tabla.column("valor",     width=150)

        self.tabla.pack(side="left", fill="both", expand=True)
        sb = ttk.Scrollbar(frame_tabla, orient="vertical", command=self.tabla.yview)
        sb.pack(side="right", fill="y")
        self.tabla.config(yscrollcommand=sb.set)

        # Al hacer doble clic en una fila, cargar los datos para editar
        self.tabla.bind("<Double-1>", self._cargar_para_editar)

        # Etiqueta de estado
        self.etiqueta_estado = tk.Label(self, text="", bg="white",
                                         font=("Arial", 10), fg="green")
        self.etiqueta_estado.pack(pady=4)

    # ──────────────────────────────────────────────────────
    # LÓGICA CRUD
    # ──────────────────────────────────────────────────────

    def _agregar(self):
        datos = self._leer_formulario()
        if not datos:
            return

        # Verificar que el código no esté duplicado
        for r in self.registros:
            if r["codigo"] == datos["codigo"]:
                messagebox.showerror("Duplicado", f"El código '{datos['codigo']}' ya existe.")
                return

        self.registros.append(datos)
        guardar(self.registros)
        self._actualizar_tabla()
        self._limpiar_form()
        self.etiqueta_estado.config(text=f"✓ '{datos['nombre']}' agregado.", fg="green")

    def _cargar_para_editar(self, event):
        """Doble clic en tabla → carga los datos en el formulario para editar."""
        seleccion = self.tabla.selection()
        if not seleccion:
            return

        item = self.tabla.item(seleccion[0])
        valores = item["values"]

        # Encontrar el índice en la lista original
        for i, r in enumerate(self.registros):
            if str(r["codigo"]) == str(valores[0]):
                self.indice_editando = i
                break

        # Llenar el formulario con los datos actuales
        self.entrada_codigo.delete(0, tk.END)
        self.entrada_codigo.insert(0, valores[0])
        self.entrada_codigo.config(state="disabled")   # no se puede cambiar el código al editar

        self.entrada_nombre.delete(0, tk.END)
        self.entrada_nombre.insert(0, valores[1])

        self.combo_categoria.set(valores[2])

        self.entrada_valor.delete(0, tk.END)
        self.entrada_valor.insert(0, valores[3])

        # Activar botón de guardar edición y desactivar agregar
        self.btn_agregar.config(state="disabled")
        self.btn_editar.config(state="normal")
        self.etiqueta_estado.config(text="✏ Modo edición — modifica y presiona 'Guardar edición'.", fg="orange")

    def _guardar_edicion(self):
        """Guarda los cambios del registro que se está editando."""
        if self.indice_editando is None:
            return

        nombre    = self.entrada_nombre.get().strip()
        categoria = self.combo_categoria.get()
        valor     = self.entrada_valor.get().strip()

        if not nombre or not valor:
            messagebox.showwarning("Campos vacíos", "Nombre y Valor no pueden estar vacíos.")
            return

        self.registros[self.indice_editando]["nombre"]    = nombre
        self.registros[self.indice_editando]["categoria"] = categoria
        self.registros[self.indice_editando]["valor"]     = valor

        guardar(self.registros)
        self._actualizar_tabla()
        self._limpiar_form()
        self.etiqueta_estado.config(text=f"✓ Registro actualizado.", fg="green")

    def _eliminar(self):
        seleccion = self.tabla.selection()
        if not seleccion:
            messagebox.showwarning("Sin selección", "Haz clic en una fila de la tabla primero.")
            return

        item     = self.tabla.item(seleccion[0])
        codigo   = item["values"][0]
        nombre   = item["values"][1]

        if not messagebox.askyesno("Confirmar", f"¿Eliminar '{nombre}' (código: {codigo})?"):
            return

        self.registros = [r for r in self.registros if str(r["codigo"]) != str(codigo)]
        guardar(self.registros)
        self._actualizar_tabla()
        self._limpiar_form()
        self.etiqueta_estado.config(text=f"✓ '{nombre}' eliminado.", fg="green")

    def _buscar(self):
        """Filtra la tabla según el texto del campo de búsqueda."""
        texto = self.entrada_busqueda.get().strip().lower()
        self.tabla.delete(*self.tabla.get_children())

        for r in self.registros:
            # Buscar en todos los campos del registro
            if any(texto in str(v).lower() for v in r.values()):
                self.tabla.insert("", tk.END, values=(
                    r["codigo"], r["nombre"], r["categoria"], r["valor"]
                ))

    def _leer_formulario(self):
        """Lee y valida los campos del formulario. Retorna dict o None si hay error."""
        codigo = self.entrada_codigo.get().strip()
        nombre = self.entrada_nombre.get().strip()
        categoria = self.combo_categoria.get()
        valor  = self.entrada_valor.get().strip()

        if not codigo or not nombre or not valor:
            messagebox.showwarning("Campos vacíos", "Código, Nombre y Valor son obligatorios.")
            return None

        return {"codigo": codigo, "nombre": nombre, "categoria": categoria, "valor": valor}

    def _limpiar_form(self):
        """Limpia el formulario y desactiva el modo edición."""
        self.entrada_codigo.config(state="normal")
        for entrada in [self.entrada_codigo, self.entrada_nombre, self.entrada_valor]:
            entrada.delete(0, tk.END)
        self.combo_categoria.set("Categoría A")
        self.indice_editando = None
        self.btn_agregar.config(state="normal")
        self.btn_editar.config(state="disabled")

    def _actualizar_tabla(self):
        """Recarga todos los registros en el Treeview."""
        self.tabla.delete(*self.tabla.get_children())   # limpiar tabla
        for r in self.registros:
            self.tabla.insert("", tk.END, values=(
                r["codigo"], r["nombre"], r["categoria"], r["valor"]
            ))


if __name__ == "__main__":
    app = AppCRUD()
    app.mainloop()
