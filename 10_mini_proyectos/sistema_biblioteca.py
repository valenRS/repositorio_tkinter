# ============================================================
# MINI PROYECTO — SISTEMA DE BIBLIOTECA
# ============================================================
# Este proyecto replica casi exactamente el Parcial 3 real de
# Programación II (UTP — Ingeniería Electrónica).
#
# Funcionalidades:
#  ✓ Agregar libros (código, título, autor, género, copias, físico/digital)
#  ✓ Todos los campos obligatorios antes de guardar
#  ✓ Persistencia en JSON (datos no se pierden al cerrar)
#  ✓ Buscar por género
#  ✓ Registrar préstamo y devolución
#  ✓ Ver consolidado de préstamos por género
#  ✓ Editar y eliminar libros
#  ✓ Estructura OOP obligatoria
#
# Para ejecutar: python3 sistema_biblioteca.py
# ============================================================

import tkinter as tk
from tkinter import ttk, messagebox
import json
import os

ARCHIVO_LIBROS    = "biblioteca_libros.json"
ARCHIVO_PRESTAMOS = "biblioteca_prestamos.json"


# ── Funciones de persistencia ─────────────────────────────

def cargar_json(archivo):
    if os.path.exists(archivo):
        with open(archivo, "r", encoding="utf-8") as f:
            return json.load(f)
    return []

def guardar_json(archivo, datos):
    with open(archivo, "w", encoding="utf-8") as f:
        json.dump(datos, f, indent=4, ensure_ascii=False)


# ============================================================
# APLICACIÓN PRINCIPAL
# ============================================================

class SistemaBiblioteca(tk.Tk):

    def __init__(self):
        super().__init__()
        self.title("Sistema de Gestión Biblioteca")
        self.geometry("800x600")
        self.configure(bg="#f0f4f8")
        self.resizable(True, True)

        self.libros    = cargar_json(ARCHIVO_LIBROS)
        self.prestamos = cargar_json(ARCHIVO_PRESTAMOS)
        self.indice_editando = None

        self._crear_pestanas()

    # ──────────────────────────────────────────────────────
    # PESTAÑAS (Notebook)
    # ──────────────────────────────────────────────────────
    def _crear_pestanas(self):
        notebook = ttk.Notebook(self)
        notebook.pack(fill="both", expand=True, padx=10, pady=10)

        # Pestaña 1 — Gestión de libros (agregar, editar, eliminar)
        self.frame_libros = tk.Frame(notebook, bg="#f0f4f8")
        notebook.add(self.frame_libros, text="  📚 Gestión de Libros  ")

        # Pestaña 2 — Préstamos
        self.frame_prestamos = tk.Frame(notebook, bg="#f0f4f8")
        notebook.add(self.frame_prestamos, text="  📋 Préstamos  ")

        # Pestaña 3 — Consolidado
        self.frame_consolidado = tk.Frame(notebook, bg="#f0f4f8")
        notebook.add(self.frame_consolidado, text="  📊 Consolidado  ")

        self._crear_tab_libros()
        self._crear_tab_prestamos()
        self._crear_tab_consolidado()

    # ══════════════════════════════════════════════════════
    # PESTAÑA 1 — GESTIÓN DE LIBROS
    # ══════════════════════════════════════════════════════
    def _crear_tab_libros(self):
        parent = self.frame_libros

        tk.Label(parent, text="Registro de Libros", font=("Arial", 13, "bold"),
                 bg="#f0f4f8").pack(pady=8)

        # ── Formulario ─────────────────────────────────────
        frame_form = tk.LabelFrame(parent, text=" Datos del libro ",
                                    font=("Arial", 9), bg="#f0f4f8")
        frame_form.pack(padx=12, fill="x", pady=4)

        # Fila 0: Código | Título
        tk.Label(frame_form, text="Código:", bg="#f0f4f8").grid(row=0, column=0, padx=6, pady=5, sticky="w")
        self.e_codigo = tk.Entry(frame_form, width=12, font=("Arial", 11))
        self.e_codigo.grid(row=0, column=1, padx=5, pady=5)

        tk.Label(frame_form, text="Título:", bg="#f0f4f8").grid(row=0, column=2, padx=6, pady=5, sticky="w")
        self.e_titulo = tk.Entry(frame_form, width=25, font=("Arial", 11))
        self.e_titulo.grid(row=0, column=3, padx=5, pady=5)

        # Fila 1: Autor | Género
        tk.Label(frame_form, text="Autor:", bg="#f0f4f8").grid(row=1, column=0, padx=6, pady=5, sticky="w")
        self.e_autor = tk.Entry(frame_form, width=12, font=("Arial", 11))
        self.e_autor.grid(row=1, column=1, padx=5, pady=5)

        tk.Label(frame_form, text="Género:", bg="#f0f4f8").grid(row=1, column=2, padx=6, pady=5, sticky="w")
        self.combo_genero = ttk.Combobox(
            frame_form,
            values=["Novela", "Ciencia Ficción", "Historia", "Tecnología",
                    "Matemáticas", "Filosofía", "Biografía", "Otro"],
            width=22, state="readonly"
        )
        self.combo_genero.set("Novela")
        self.combo_genero.grid(row=1, column=3, padx=5, pady=5)

        # Fila 2: Copias | Formato
        tk.Label(frame_form, text="Copias:", bg="#f0f4f8").grid(row=2, column=0, padx=6, pady=5, sticky="w")
        self.e_copias = tk.Entry(frame_form, width=12, font=("Arial", 11))
        self.e_copias.grid(row=2, column=1, padx=5, pady=5)

        tk.Label(frame_form, text="Formato:", bg="#f0f4f8").grid(row=2, column=2, padx=6, pady=5, sticky="w")
        self.var_formato = tk.StringVar(value="Físico")
        frame_radio = tk.Frame(frame_form, bg="#f0f4f8")
        frame_radio.grid(row=2, column=3, padx=5, pady=5, sticky="w")
        tk.Radiobutton(frame_radio, text="Físico",  variable=self.var_formato,
                       value="Físico",  bg="#f0f4f8").pack(side="left")
        tk.Radiobutton(frame_radio, text="Digital", variable=self.var_formato,
                       value="Digital", bg="#f0f4f8").pack(side="left", padx=10)

        # ── Botones ─────────────────────────────────────────
        frame_btn = tk.Frame(parent, bg="#f0f4f8")
        frame_btn.pack(pady=5)

        self.btn_agregar_libro = tk.Button(frame_btn, text="➕ Agregar libro",
                                            command=self._agregar_libro,
                                            bg="#4CAF50", fg="white", width=14, font=("Arial", 10))
        self.btn_agregar_libro.pack(side="left", padx=5)

        self.btn_guardar_edicion = tk.Button(frame_btn, text="💾 Guardar edición",
                                              command=self._guardar_edicion_libro,
                                              bg="#FF9800", fg="white", width=15,
                                              font=("Arial", 10), state="disabled")
        self.btn_guardar_edicion.pack(side="left", padx=5)

        tk.Button(frame_btn, text="🗑 Eliminar", command=self._eliminar_libro,
                  bg="#f44336", fg="white", width=10, font=("Arial", 10)).pack(side="left", padx=5)

        tk.Button(frame_btn, text="🔄 Limpiar", command=self._limpiar_form_libro,
                  bg="#9E9E9E", fg="white", width=10, font=("Arial", 10)).pack(side="left", padx=5)

        # ── Tabla de libros ─────────────────────────────────
        frame_tabla = tk.Frame(parent, bg="#f0f4f8")
        frame_tabla.pack(padx=12, fill="both", expand=True, pady=4)

        cols = ("codigo", "titulo", "autor", "genero", "copias", "formato")
        self.tabla_libros = ttk.Treeview(frame_tabla, columns=cols, show="headings", height=8)

        encabezados = {"codigo": "Código", "titulo": "Título", "autor": "Autor",
                       "genero": "Género", "copias": "Copias", "formato": "Formato"}
        anchos = {"codigo": 70, "titulo": 180, "autor": 130,
                  "genero": 110, "copias": 60, "formato": 70}

        for col in cols:
            self.tabla_libros.heading(col, text=encabezados[col])
            self.tabla_libros.column(col, width=anchos[col], anchor="center" if col != "titulo" and col != "autor" else "w")

        self.tabla_libros.pack(side="left", fill="both", expand=True)
        sb = ttk.Scrollbar(frame_tabla, orient="vertical", command=self.tabla_libros.yview)
        sb.pack(side="right", fill="y")
        self.tabla_libros.config(yscrollcommand=sb.set)
        self.tabla_libros.bind("<Double-1>", self._cargar_libro_para_editar)

        self.lbl_estado_libros = tk.Label(parent, text="", bg="#f0f4f8", fg="green", font=("Arial", 10))
        self.lbl_estado_libros.pack(pady=3)

        self._refrescar_tabla_libros()

    # ══════════════════════════════════════════════════════
    # PESTAÑA 2 — PRÉSTAMOS
    # ══════════════════════════════════════════════════════
    def _crear_tab_prestamos(self):
        parent = self.frame_prestamos

        tk.Label(parent, text="Gestión de Préstamos", font=("Arial", 13, "bold"),
                 bg="#f0f4f8").pack(pady=8)

        # Filtro por género
        frame_filtro = tk.LabelFrame(parent, text=" Buscar libros por género ",
                                      font=("Arial", 9), bg="#f0f4f8")
        frame_filtro.pack(padx=12, fill="x", pady=5)

        tk.Label(frame_filtro, text="Género:", bg="#f0f4f8").grid(row=0, column=0, padx=8, pady=8)
        self.combo_genero_buscar = ttk.Combobox(
            frame_filtro,
            values=["Todos", "Novela", "Ciencia Ficción", "Historia", "Tecnología",
                    "Matemáticas", "Filosofía", "Biografía", "Otro"],
            width=20, state="readonly"
        )
        self.combo_genero_buscar.set("Todos")
        self.combo_genero_buscar.grid(row=0, column=1, padx=5, pady=8)

        tk.Button(frame_filtro, text="🔍 Buscar", command=self._buscar_por_genero,
                  bg="#2196F3", fg="white", width=10).grid(row=0, column=2, padx=10)

        # Tabla de resultados de búsqueda
        tk.Label(parent, text="Resultados:", bg="#f0f4f8", font=("Arial", 10)).pack(anchor="w", padx=14)

        frame_tabla_p = tk.Frame(parent, bg="#f0f4f8")
        frame_tabla_p.pack(padx=12, fill="both", expand=True)

        cols_p = ("codigo", "titulo", "autor", "genero", "copias_disp")
        self.tabla_prestamos = ttk.Treeview(frame_tabla_p, columns=cols_p, show="headings", height=7)
        enc_p = {"codigo": "Código", "titulo": "Título", "autor": "Autor",
                 "genero": "Género", "copias_disp": "Copias disp."}
        anc_p = {"codigo": 70, "titulo": 200, "autor": 150, "genero": 110, "copias_disp": 90}
        for col in cols_p:
            self.tabla_prestamos.heading(col, text=enc_p[col])
            self.tabla_prestamos.column(col, width=anc_p[col], anchor="center" if col not in ("titulo","autor") else "w")

        self.tabla_prestamos.pack(side="left", fill="both", expand=True)
        sb2 = ttk.Scrollbar(frame_tabla_p, orient="vertical", command=self.tabla_prestamos.yview)
        sb2.pack(side="right", fill="y")
        self.tabla_prestamos.config(yscrollcommand=sb2.set)

        # Botones de préstamo
        frame_btn_p = tk.Frame(parent, bg="#f0f4f8")
        frame_btn_p.pack(pady=8)

        tk.Button(frame_btn_p, text="📤 Registrar préstamo",
                  command=self._registrar_prestamo,
                  bg="#4CAF50", fg="white", width=18, font=("Arial", 10)).pack(side="left", padx=5)

        tk.Button(frame_btn_p, text="📥 Registrar devolución",
                  command=self._registrar_devolucion,
                  bg="#2196F3", fg="white", width=18, font=("Arial", 10)).pack(side="left", padx=5)

        self.lbl_estado_prestamo = tk.Label(parent, text="", bg="#f0f4f8", fg="green", font=("Arial", 10))
        self.lbl_estado_prestamo.pack(pady=3)

    # ══════════════════════════════════════════════════════
    # PESTAÑA 3 — CONSOLIDADO
    # ══════════════════════════════════════════════════════
    def _crear_tab_consolidado(self):
        parent = self.frame_consolidado

        tk.Label(parent, text="Consolidado de Préstamos por Género",
                 font=("Arial", 13, "bold"), bg="#f0f4f8").pack(pady=10)

        tk.Button(parent, text="🔄 Actualizar consolidado",
                  command=self._actualizar_consolidado,
                  bg="#9C27B0", fg="white", width=22, font=("Arial", 11)).pack(pady=5)

        frame_tabla_c = tk.Frame(parent, bg="#f0f4f8")
        frame_tabla_c.pack(padx=15, fill="both", expand=True, pady=5)

        cols_c = ("genero", "total_prestamos", "activos", "devueltos")
        self.tabla_consolidado = ttk.Treeview(frame_tabla_c, columns=cols_c, show="headings", height=10)

        enc_c = {"genero": "Género", "total_prestamos": "Total Préstamos",
                 "activos": "Activos", "devueltos": "Devueltos"}
        for col in cols_c:
            self.tabla_consolidado.heading(col, text=enc_c[col])
            self.tabla_consolidado.column(col, width=160, anchor="center")

        self.tabla_consolidado.pack(side="left", fill="both", expand=True)
        sb3 = ttk.Scrollbar(frame_tabla_c, orient="vertical", command=self.tabla_consolidado.yview)
        sb3.pack(side="right", fill="y")
        self.tabla_consolidado.config(yscrollcommand=sb3.set)

        self.lbl_total_consolidado = tk.Label(parent, text="", bg="#f0f4f8",
                                               font=("Arial", 11, "bold"), fg="navy")
        self.lbl_total_consolidado.pack(pady=8)

    # ──────────────────────────────────────────────────────
    # LÓGICA — LIBROS
    # ──────────────────────────────────────────────────────

    def _agregar_libro(self):
        datos = self._leer_form_libro()
        if datos is None:
            return

        # Verificar código duplicado
        if any(l["codigo"] == datos["codigo"] for l in self.libros):
            messagebox.showerror("Código duplicado",
                                  f"Ya existe un libro con el código '{datos['codigo']}'.")
            return

        self.libros.append(datos)
        guardar_json(ARCHIVO_LIBROS, self.libros)
        self._refrescar_tabla_libros()
        self._limpiar_form_libro()
        self.lbl_estado_libros.config(text=f"✓ '{datos['titulo']}' agregado.", fg="green")

    def _cargar_libro_para_editar(self, event):
        sel = self.tabla_libros.selection()
        if not sel:
            return
        vals = self.tabla_libros.item(sel[0])["values"]
        codigo = str(vals[0])

        for i, l in enumerate(self.libros):
            if str(l["codigo"]) == codigo:
                self.indice_editando = i
                break

        self.e_codigo.config(state="normal")
        self.e_codigo.delete(0, tk.END);   self.e_codigo.insert(0, vals[0])
        self.e_codigo.config(state="disabled")
        self.e_titulo.delete(0, tk.END);   self.e_titulo.insert(0, vals[1])
        self.e_autor.delete(0, tk.END);    self.e_autor.insert(0, vals[2])
        self.combo_genero.set(vals[3])
        self.e_copias.delete(0, tk.END);   self.e_copias.insert(0, vals[4])
        self.var_formato.set(vals[5])

        self.btn_agregar_libro.config(state="disabled")
        self.btn_guardar_edicion.config(state="normal")
        self.lbl_estado_libros.config(text="✏ Modo edición — modifica y presiona 'Guardar edición'.", fg="orange")

    def _guardar_edicion_libro(self):
        if self.indice_editando is None:
            return
        titulo = self.e_titulo.get().strip()
        autor  = self.e_autor.get().strip()
        copias = self.e_copias.get().strip()

        if not titulo or not autor or not copias:
            messagebox.showwarning("Campos vacíos", "Título, Autor y Copias son obligatorios.")
            return

        l = self.libros[self.indice_editando]
        l["titulo"]  = titulo
        l["autor"]   = autor
        l["genero"]  = self.combo_genero.get()
        l["copias"]  = copias
        l["formato"] = self.var_formato.get()

        guardar_json(ARCHIVO_LIBROS, self.libros)
        self._refrescar_tabla_libros()
        self._limpiar_form_libro()
        self.lbl_estado_libros.config(text="✓ Libro actualizado.", fg="green")

    def _eliminar_libro(self):
        sel = self.tabla_libros.selection()
        if not sel:
            messagebox.showwarning("Sin selección", "Selecciona un libro de la tabla.")
            return
        vals = self.tabla_libros.item(sel[0])["values"]
        codigo, titulo = str(vals[0]), vals[1]

        if not messagebox.askyesno("Confirmar", f"¿Eliminar '{titulo}'?"):
            return

        self.libros = [l for l in self.libros if str(l["codigo"]) != codigo]
        guardar_json(ARCHIVO_LIBROS, self.libros)
        self._refrescar_tabla_libros()
        self._limpiar_form_libro()
        self.lbl_estado_libros.config(text=f"✓ '{titulo}' eliminado.", fg="green")

    def _leer_form_libro(self):
        codigo  = self.e_codigo.get().strip()
        titulo  = self.e_titulo.get().strip()
        autor   = self.e_autor.get().strip()
        genero  = self.combo_genero.get()
        copias  = self.e_copias.get().strip()
        formato = self.var_formato.get()

        if not all([codigo, titulo, autor, copias]):
            messagebox.showwarning("Campos vacíos",
                                    "Todos los campos son obligatorios antes de guardar.")
            return None

        if not copias.isdigit() or int(copias) < 0:
            messagebox.showerror("Valor inválido", "El número de copias debe ser un entero positivo.")
            return None

        return {"codigo": codigo, "titulo": titulo, "autor": autor,
                "genero": genero, "copias": int(copias), "formato": formato}

    def _limpiar_form_libro(self):
        self.e_codigo.config(state="normal")
        for e in [self.e_codigo, self.e_titulo, self.e_autor, self.e_copias]:
            e.delete(0, tk.END)
        self.combo_genero.set("Novela")
        self.var_formato.set("Físico")
        self.indice_editando = None
        self.btn_agregar_libro.config(state="normal")
        self.btn_guardar_edicion.config(state="disabled")

    def _refrescar_tabla_libros(self):
        self.tabla_libros.delete(*self.tabla_libros.get_children())
        for l in self.libros:
            self.tabla_libros.insert("", tk.END, values=(
                l["codigo"], l["titulo"], l["autor"],
                l["genero"], l["copias"], l["formato"]
            ))

    # ──────────────────────────────────────────────────────
    # LÓGICA — PRÉSTAMOS
    # ──────────────────────────────────────────────────────

    def _buscar_por_genero(self):
        genero = self.combo_genero_buscar.get()
        self.tabla_prestamos.delete(*self.tabla_prestamos.get_children())

        for l in self.libros:
            if genero == "Todos" or l["genero"] == genero:
                # Calcular copias disponibles (copias totales - préstamos activos)
                prestamos_activos = sum(
                    1 for p in self.prestamos
                    if p["codigo_libro"] == l["codigo"] and p["estado"] == "activo"
                )
                copias_disp = int(l["copias"]) - prestamos_activos
                self.tabla_prestamos.insert("", tk.END, values=(
                    l["codigo"], l["titulo"], l["autor"], l["genero"], copias_disp
                ))

    def _registrar_prestamo(self):
        sel = self.tabla_prestamos.selection()
        if not sel:
            messagebox.showwarning("Sin selección", "Selecciona un libro de la lista.")
            return

        vals = self.tabla_prestamos.item(sel[0])["values"]
        codigo_libro = str(vals[0])
        titulo       = vals[1]
        copias_disp  = int(vals[4])

        if copias_disp <= 0:
            messagebox.showerror("Sin copias", f"No hay copias disponibles de '{titulo}'.")
            return

        self.prestamos.append({"codigo_libro": codigo_libro,
                                "titulo": titulo, "estado": "activo"})
        guardar_json(ARCHIVO_PRESTAMOS, self.prestamos)
        self._buscar_por_genero()
        self.lbl_estado_prestamo.config(
            text=f"✓ Préstamo registrado: '{titulo}'.", fg="green")

    def _registrar_devolucion(self):
        sel = self.tabla_prestamos.selection()
        if not sel:
            messagebox.showwarning("Sin selección", "Selecciona un libro de la lista.")
            return

        vals         = self.tabla_prestamos.item(sel[0])["values"]
        codigo_libro = str(vals[0])
        titulo       = vals[1]

        # Buscar un préstamo activo de ese libro
        prestamo_activo = next(
            (p for p in self.prestamos
             if p["codigo_libro"] == codigo_libro and p["estado"] == "activo"),
            None
        )

        if not prestamo_activo:
            messagebox.showinfo("Sin préstamos activos",
                                 f"No hay préstamos activos de '{titulo}'.")
            return

        prestamo_activo["estado"] = "devuelto"
        guardar_json(ARCHIVO_PRESTAMOS, self.prestamos)
        self._buscar_por_genero()
        self.lbl_estado_prestamo.config(
            text=f"✓ Devolución registrada: '{titulo}'.", fg="blue")

    # ──────────────────────────────────────────────────────
    # LÓGICA — CONSOLIDADO
    # ──────────────────────────────────────────────────────

    def _actualizar_consolidado(self):
        self.tabla_consolidado.delete(*self.tabla_consolidado.get_children())

        # Obtener géneros únicos de los libros
        generos = sorted(set(l["genero"] for l in self.libros))

        total_general = 0
        for genero in generos:
            codigos_genero = {l["codigo"] for l in self.libros if l["genero"] == genero}
            prestamos_genero = [p for p in self.prestamos if p["codigo_libro"] in codigos_genero]

            total    = len(prestamos_genero)
            activos  = sum(1 for p in prestamos_genero if p["estado"] == "activo")
            devueltos = sum(1 for p in prestamos_genero if p["estado"] == "devuelto")
            total_general += total

            self.tabla_consolidado.insert("", tk.END,
                                           values=(genero, total, activos, devueltos))

        self.lbl_total_consolidado.config(
            text=f"Total general de préstamos: {total_general}")


if __name__ == "__main__":
    app = SistemaBiblioteca()
    app.mainloop()
