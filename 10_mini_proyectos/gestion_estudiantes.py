# ============================================================
# MINI PROYECTO — GESTIÓN DE ESTUDIANTES
# ============================================================
# CRUD completo de estudiantes con:
#  ✓ Campos: nombre, ID, carrera, semestre, promedio, activo
#  ✓ Búsqueda por carrera
#  ✓ Validación de campos
#  ✓ Persistencia en JSON
#  ✓ Estructura OOP
#
# Para ejecutar: python3 gestion_estudiantes.py
# ============================================================

import tkinter as tk
from tkinter import ttk, messagebox
import json, os

ARCHIVO = "estudiantes.json"

def cargar():
    return json.load(open(ARCHIVO, "r", encoding="utf-8")) if os.path.exists(ARCHIVO) else []

def guardar(datos):
    with open(ARCHIVO, "w", encoding="utf-8") as f:
        json.dump(datos, f, indent=4, ensure_ascii=False)


class GestionEstudiantes(tk.Tk):

    def __init__(self):
        super().__init__()
        self.title("Gestión de Estudiantes")
        self.geometry("780x560")
        self.configure(bg="#eef2f7")
        self.estudiantes = cargar()
        self.indice_editando = None
        self._construir_ui()
        self._refrescar_tabla()

    def _construir_ui(self):
        tk.Label(self, text="Sistema de Gestión de Estudiantes",
                 font=("Arial", 14, "bold"), bg="#eef2f7", fg="#2c3e50").pack(pady=10)

        # ── Formulario ─────────────────────────────────────
        fframe = tk.LabelFrame(self, text=" Datos del estudiante ",
                                bg="#eef2f7", font=("Arial", 9))
        fframe.pack(padx=14, fill="x", pady=5)

        labels_entries = [
            ("ID / Código:", "e_id", 0, 0),
            ("Nombre completo:", "e_nombre", 0, 2),
            ("Carrera:", None, 1, 0),
            ("Semestre:", "e_semestre", 1, 2),
            ("Promedio:", "e_promedio", 2, 0),
        ]

        for texto, attr, row, col in labels_entries:
            tk.Label(fframe, text=texto, bg="#eef2f7").grid(row=row, column=col,
                                                             padx=8, pady=5, sticky="w")
            if attr:
                e = tk.Entry(fframe, width=20, font=("Arial", 11))
                e.grid(row=row, column=col+1, padx=5, pady=5)
                setattr(self, attr, e)

        # Combobox para carrera
        self.combo_carrera = ttk.Combobox(
            fframe,
            values=["Ing. de Sistemas", "Ing. Electrónica", "Ing. Civil",
                    "Medicina", "Derecho", "Administración", "Psicología"],
            width=18, state="readonly"
        )
        self.combo_carrera.set("Ing. de Sistemas")
        self.combo_carrera.grid(row=1, column=1, padx=5, pady=5)

        # Checkbutton activo/inactivo
        self.var_activo = tk.BooleanVar(value=True)
        tk.Checkbutton(fframe, text="Estudiante activo", variable=self.var_activo,
                       bg="#eef2f7", font=("Arial", 10)).grid(row=2, column=1, padx=5, pady=5, sticky="w")

        # ── Filtro de búsqueda ──────────────────────────────
        bframe = tk.Frame(self, bg="#eef2f7")
        bframe.pack(padx=14, fill="x", pady=3)

        tk.Label(bframe, text="Filtrar por carrera:", bg="#eef2f7").pack(side="left")
        self.combo_filtro = ttk.Combobox(
            bframe,
            values=["Todos", "Ing. de Sistemas", "Ing. Electrónica", "Ing. Civil",
                    "Medicina", "Derecho", "Administración", "Psicología"],
            width=18, state="readonly"
        )
        self.combo_filtro.set("Todos")
        self.combo_filtro.pack(side="left", padx=5)
        tk.Button(bframe, text="Filtrar", command=self._filtrar,
                  bg="#2196F3", fg="white").pack(side="left", padx=5)
        tk.Button(bframe, text="Ver todos", command=self._refrescar_tabla,
                  bg="#9E9E9E", fg="white").pack(side="left")

        # ── Botones CRUD ────────────────────────────────────
        btnf = tk.Frame(self, bg="#eef2f7")
        btnf.pack(pady=6)
        self.btn_add = tk.Button(btnf, text="➕ Agregar",
                                  command=self._agregar, bg="#4CAF50", fg="white", width=12)
        self.btn_add.pack(side="left", padx=4)
        self.btn_edit = tk.Button(btnf, text="💾 Guardar edición",
                                   command=self._guardar_edicion, bg="#FF9800", fg="white",
                                   width=15, state="disabled")
        self.btn_edit.pack(side="left", padx=4)
        tk.Button(btnf, text="🗑 Eliminar", command=self._eliminar,
                  bg="#f44336", fg="white", width=10).pack(side="left", padx=4)
        tk.Button(btnf, text="🔄 Limpiar", command=self._limpiar,
                  bg="#9E9E9E", fg="white", width=10).pack(side="left", padx=4)

        # ── Tabla ───────────────────────────────────────────
        tf = tk.Frame(self, bg="#eef2f7")
        tf.pack(padx=14, fill="both", expand=True)

        cols = ("id", "nombre", "carrera", "semestre", "promedio", "estado")
        self.tabla = ttk.Treeview(tf, columns=cols, show="headings", height=9)
        enc = {"id":"ID", "nombre":"Nombre", "carrera":"Carrera",
               "semestre":"Semestre", "promedio":"Promedio", "estado":"Estado"}
        anc = {"id":80, "nombre":180, "carrera":150, "semestre":70, "promedio":80, "estado":80}
        for c in cols:
            self.tabla.heading(c, text=enc[c])
            self.tabla.column(c, width=anc[c], anchor="center" if c != "nombre" and c != "carrera" else "w")
        self.tabla.pack(side="left", fill="both", expand=True)
        sb = ttk.Scrollbar(tf, orient="vertical", command=self.tabla.yview)
        sb.pack(side="right", fill="y")
        self.tabla.config(yscrollcommand=sb.set)
        self.tabla.bind("<Double-1>", self._cargar_para_editar)

        self.lbl = tk.Label(self, text="", bg="#eef2f7", fg="green", font=("Arial", 10))
        self.lbl.pack(pady=4)

    def _agregar(self):
        d = self._leer_form()
        if not d: return
        if any(e["id"] == d["id"] for e in self.estudiantes):
            messagebox.showerror("Duplicado", f"El ID '{d['id']}' ya existe.")
            return
        self.estudiantes.append(d)
        guardar(self.estudiantes)
        self._refrescar_tabla()
        self._limpiar()
        self.lbl.config(text=f"✓ '{d['nombre']}' agregado.", fg="green")

    def _cargar_para_editar(self, event):
        sel = self.tabla.selection()
        if not sel: return
        v = self.tabla.item(sel[0])["values"]
        for i, e in enumerate(self.estudiantes):
            if str(e["id"]) == str(v[0]):
                self.indice_editando = i; break

        self.e_id.config(state="normal")
        self.e_id.delete(0, tk.END);        self.e_id.insert(0, v[0])
        self.e_id.config(state="disabled")
        self.e_nombre.delete(0, tk.END);    self.e_nombre.insert(0, v[1])
        self.combo_carrera.set(v[2])
        self.e_semestre.delete(0, tk.END);  self.e_semestre.insert(0, v[3])
        self.e_promedio.delete(0, tk.END);  self.e_promedio.insert(0, v[4])
        self.var_activo.set(v[5] == "Activo")
        self.btn_add.config(state="disabled")
        self.btn_edit.config(state="normal")
        self.lbl.config(text="✏ Modo edición", fg="orange")

    def _guardar_edicion(self):
        if self.indice_editando is None: return
        nombre   = self.e_nombre.get().strip()
        semestre = self.e_semestre.get().strip()
        promedio = self.e_promedio.get().strip()
        if not nombre or not semestre or not promedio:
            messagebox.showwarning("Campos vacíos", "Completa todos los campos."); return
        e = self.estudiantes[self.indice_editando]
        e["nombre"]   = nombre
        e["carrera"]  = self.combo_carrera.get()
        e["semestre"] = semestre
        e["promedio"] = promedio
        e["activo"]   = self.var_activo.get()
        guardar(self.estudiantes)
        self._refrescar_tabla()
        self._limpiar()
        self.lbl.config(text="✓ Estudiante actualizado.", fg="green")

    def _eliminar(self):
        sel = self.tabla.selection()
        if not sel:
            messagebox.showwarning("Sin selección", "Selecciona un estudiante."); return
        v = self.tabla.item(sel[0])["values"]
        if not messagebox.askyesno("Confirmar", f"¿Eliminar a '{v[1]}'?"): return
        self.estudiantes = [e for e in self.estudiantes if str(e["id"]) != str(v[0])]
        guardar(self.estudiantes)
        self._refrescar_tabla()
        self._limpiar()
        self.lbl.config(text=f"✓ '{v[1]}' eliminado.", fg="green")

    def _filtrar(self):
        filtro = self.combo_filtro.get()
        self.tabla.delete(*self.tabla.get_children())
        for e in self.estudiantes:
            if filtro == "Todos" or e["carrera"] == filtro:
                self.tabla.insert("", tk.END, values=(
                    e["id"], e["nombre"], e["carrera"], e["semestre"],
                    e["promedio"], "Activo" if e.get("activo", True) else "Inactivo"
                ))

    def _leer_form(self):
        id_est   = self.e_id.get().strip()
        nombre   = self.e_nombre.get().strip()
        semestre = self.e_semestre.get().strip()
        promedio = self.e_promedio.get().strip()
        if not all([id_est, nombre, semestre, promedio]):
            messagebox.showwarning("Campos vacíos", "Todos los campos son obligatorios."); return None
        return {"id": id_est, "nombre": nombre, "carrera": self.combo_carrera.get(),
                "semestre": semestre, "promedio": promedio, "activo": self.var_activo.get()}

    def _limpiar(self):
        self.e_id.config(state="normal")
        for e in [self.e_id, self.e_nombre, self.e_semestre, self.e_promedio]: e.delete(0, tk.END)
        self.combo_carrera.set("Ing. de Sistemas")
        self.var_activo.set(True)
        self.indice_editando = None
        self.btn_add.config(state="normal")
        self.btn_edit.config(state="disabled")

    def _refrescar_tabla(self):
        self.tabla.delete(*self.tabla.get_children())
        for e in self.estudiantes:
            self.tabla.insert("", tk.END, values=(
                e["id"], e["nombre"], e["carrera"], e["semestre"],
                e["promedio"], "Activo" if e.get("activo", True) else "Inactivo"
            ))


if __name__ == "__main__":
    app = GestionEstudiantes()
    app.mainloop()
