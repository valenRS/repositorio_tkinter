# ============================================================
# MINI PROYECTO — REGISTRO DE EMPLEADOS
# ============================================================
# CRUD de empleados con:
#  ✓ Campos: ID, nombre, cargo, departamento, salario, activo/inactivo
#  ✓ Búsqueda por departamento
#  ✓ Total de salarios por departamento
#  ✓ Persistencia en JSON + OOP
#
# Para ejecutar: python3 registro_empleados.py
# ============================================================

import tkinter as tk
from tkinter import ttk, messagebox
import json, os

ARCHIVO = "empleados.json"

def cargar():
    return json.load(open(ARCHIVO, "r", encoding="utf-8")) if os.path.exists(ARCHIVO) else []

def guardar(datos):
    with open(ARCHIVO, "w", encoding="utf-8") as f:
        json.dump(datos, f, indent=4, ensure_ascii=False)

DEPARTAMENTOS = ["Sistemas", "Recursos Humanos", "Contabilidad",
                 "Ventas", "Marketing", "Operaciones", "Gerencia"]


class RegistroEmpleados(tk.Tk):

    def __init__(self):
        super().__init__()
        self.title("Registro de Empleados")
        self.geometry("800x570")
        self.configure(bg="#f0fff4")
        self.empleados = cargar()
        self.indice_editando = None
        self._construir_ui()
        self._refrescar_tabla()

    def _construir_ui(self):
        tk.Label(self, text="Sistema de Registro de Empleados",
                 font=("Arial", 14, "bold"), bg="#f0fff4", fg="#1b5e20").pack(pady=10)

        # ── Formulario ──────────────────────────────────────
        ff = tk.LabelFrame(self, text=" Datos del empleado ", bg="#f0fff4", font=("Arial", 9))
        ff.pack(padx=14, fill="x", pady=5)

        tk.Label(ff, text="ID:", bg="#f0fff4").grid(row=0, column=0, padx=8, pady=5, sticky="w")
        self.e_id = tk.Entry(ff, width=14, font=("Arial", 11))
        self.e_id.grid(row=0, column=1, padx=5)

        tk.Label(ff, text="Nombre completo:", bg="#f0fff4").grid(row=0, column=2, padx=8, pady=5, sticky="w")
        self.e_nombre = tk.Entry(ff, width=22, font=("Arial", 11))
        self.e_nombre.grid(row=0, column=3, padx=5)

        tk.Label(ff, text="Cargo:", bg="#f0fff4").grid(row=1, column=0, padx=8, pady=5, sticky="w")
        self.e_cargo = tk.Entry(ff, width=14, font=("Arial", 11))
        self.e_cargo.grid(row=1, column=1, padx=5)

        tk.Label(ff, text="Departamento:", bg="#f0fff4").grid(row=1, column=2, padx=8, pady=5, sticky="w")
        self.combo_depto = ttk.Combobox(ff, values=DEPARTAMENTOS, width=20, state="readonly")
        self.combo_depto.set("Sistemas")
        self.combo_depto.grid(row=1, column=3, padx=5)

        tk.Label(ff, text="Salario $:", bg="#f0fff4").grid(row=2, column=0, padx=8, pady=5, sticky="w")
        self.e_salario = tk.Entry(ff, width=14, font=("Arial", 11))
        self.e_salario.grid(row=2, column=1, padx=5)

        self.var_activo = tk.BooleanVar(value=True)
        tk.Checkbutton(ff, text="Empleado activo", variable=self.var_activo,
                       bg="#f0fff4", font=("Arial", 10)).grid(row=2, column=2, columnspan=2, padx=8, sticky="w")

        # ── Filtro ──────────────────────────────────────────
        bf = tk.Frame(self, bg="#f0fff4")
        bf.pack(padx=14, fill="x", pady=3)
        tk.Label(bf, text="Filtrar por departamento:", bg="#f0fff4").pack(side="left")
        self.combo_filtro = ttk.Combobox(bf, values=["Todos"] + DEPARTAMENTOS, width=16, state="readonly")
        self.combo_filtro.set("Todos")
        self.combo_filtro.pack(side="left", padx=5)
        tk.Button(bf, text="Filtrar", command=self._filtrar,
                  bg="#388E3C", fg="white").pack(side="left", padx=5)
        tk.Button(bf, text="Ver todos", command=self._refrescar_tabla,
                  bg="#9E9E9E", fg="white").pack(side="left")
        tk.Button(bf, text="💰 Total salarios", command=self._total_salarios,
                  bg="#1565C0", fg="white").pack(side="left", padx=10)

        # ── Botones CRUD ────────────────────────────────────
        btnf = tk.Frame(self, bg="#f0fff4")
        btnf.pack(pady=5)
        self.btn_add = tk.Button(btnf, text="➕ Agregar", command=self._agregar,
                                  bg="#4CAF50", fg="white", width=12)
        self.btn_add.pack(side="left", padx=4)
        self.btn_edit = tk.Button(btnf, text="💾 Guardar edición", command=self._guardar_edicion,
                                   bg="#FF9800", fg="white", width=15, state="disabled")
        self.btn_edit.pack(side="left", padx=4)
        tk.Button(btnf, text="🗑 Eliminar", command=self._eliminar,
                  bg="#f44336", fg="white", width=10).pack(side="left", padx=4)
        tk.Button(btnf, text="🔄 Limpiar", command=self._limpiar,
                  bg="#9E9E9E", fg="white", width=10).pack(side="left", padx=4)

        # ── Tabla ───────────────────────────────────────────
        tf = tk.Frame(self, bg="#f0fff4")
        tf.pack(padx=14, fill="both", expand=True)

        cols = ("id", "nombre", "cargo", "departamento", "salario", "estado")
        self.tabla = ttk.Treeview(tf, columns=cols, show="headings", height=9)
        self.tabla.tag_configure("inactivo", foreground="gray")

        enc = {"id":"ID", "nombre":"Nombre", "cargo":"Cargo",
               "departamento":"Departamento", "salario":"Salario $", "estado":"Estado"}
        anc = {"id":70, "nombre":180, "cargo":120, "departamento":110, "salario":90, "estado":80}
        for c in cols:
            self.tabla.heading(c, text=enc[c])
            self.tabla.column(c, width=anc[c], anchor="center" if c not in ("nombre","cargo") else "w")
        self.tabla.pack(side="left", fill="both", expand=True)
        sb = ttk.Scrollbar(tf, orient="vertical", command=self.tabla.yview)
        sb.pack(side="right", fill="y")
        self.tabla.config(yscrollcommand=sb.set)
        self.tabla.bind("<Double-1>", self._cargar_para_editar)

        self.lbl = tk.Label(self, text="", bg="#f0fff4", fg="green", font=("Arial", 10))
        self.lbl.pack(pady=4)

    def _agregar(self):
        d = self._leer_form()
        if not d: return
        if any(e["id"] == d["id"] for e in self.empleados):
            messagebox.showerror("Duplicado", f"El ID '{d['id']}' ya existe."); return
        self.empleados.append(d)
        guardar(self.empleados)
        self._refrescar_tabla()
        self._limpiar()
        self.lbl.config(text=f"✓ '{d['nombre']}' agregado.", fg="green")

    def _cargar_para_editar(self, event):
        sel = self.tabla.selection()
        if not sel: return
        v = self.tabla.item(sel[0])["values"]
        for i, e in enumerate(self.empleados):
            if str(e["id"]) == str(v[0]):
                self.indice_editando = i; break
        self.e_id.config(state="normal")
        self.e_id.delete(0, tk.END);     self.e_id.insert(0, v[0])
        self.e_id.config(state="disabled")
        self.e_nombre.delete(0, tk.END); self.e_nombre.insert(0, v[1])
        self.e_cargo.delete(0, tk.END);  self.e_cargo.insert(0, v[2])
        self.combo_depto.set(v[3])
        self.e_salario.delete(0, tk.END); self.e_salario.insert(0, v[4])
        self.var_activo.set(v[5] == "Activo")
        self.btn_add.config(state="disabled")
        self.btn_edit.config(state="normal")
        self.lbl.config(text="✏ Modo edición", fg="orange")

    def _guardar_edicion(self):
        if self.indice_editando is None: return
        nombre  = self.e_nombre.get().strip()
        cargo   = self.e_cargo.get().strip()
        salario = self.e_salario.get().strip()
        if not nombre or not cargo or not salario:
            messagebox.showwarning("Campos vacíos", "Completa todos los campos."); return
        e = self.empleados[self.indice_editando]
        e["nombre"]       = nombre
        e["cargo"]        = cargo
        e["departamento"] = self.combo_depto.get()
        e["salario"]      = salario
        e["activo"]       = self.var_activo.get()
        guardar(self.empleados)
        self._refrescar_tabla()
        self._limpiar()
        self.lbl.config(text="✓ Empleado actualizado.", fg="green")

    def _eliminar(self):
        sel = self.tabla.selection()
        if not sel:
            messagebox.showwarning("Sin selección", "Selecciona un empleado."); return
        v = self.tabla.item(sel[0])["values"]
        if not messagebox.askyesno("Confirmar", f"¿Eliminar a '{v[1]}'?"): return
        self.empleados = [e for e in self.empleados if str(e["id"]) != str(v[0])]
        guardar(self.empleados)
        self._refrescar_tabla()
        self._limpiar()
        self.lbl.config(text=f"✓ '{v[1]}' eliminado.", fg="green")

    def _filtrar(self):
        filtro = self.combo_filtro.get()
        self.tabla.delete(*self.tabla.get_children())
        for e in self.empleados:
            if filtro == "Todos" or e["departamento"] == filtro:
                self._insertar_fila(e)

    def _total_salarios(self):
        filtro = self.combo_filtro.get()
        total = 0
        for e in self.empleados:
            if (filtro == "Todos" or e["departamento"] == filtro) and e.get("activo", True):
                try: total += float(e["salario"])
                except ValueError: pass
        depto_txt = "todos los departamentos" if filtro == "Todos" else filtro
        messagebox.showinfo("Total salarios",
                             f"Total de salarios activos ({depto_txt}):\n$ {total:,.2f}")

    def _leer_form(self):
        id_emp  = self.e_id.get().strip()
        nombre  = self.e_nombre.get().strip()
        cargo   = self.e_cargo.get().strip()
        salario = self.e_salario.get().strip()
        if not all([id_emp, nombre, cargo, salario]):
            messagebox.showwarning("Campos vacíos", "Todos los campos son obligatorios."); return None
        return {"id": id_emp, "nombre": nombre, "cargo": cargo,
                "departamento": self.combo_depto.get(), "salario": salario,
                "activo": self.var_activo.get()}

    def _limpiar(self):
        self.e_id.config(state="normal")
        for e in [self.e_id, self.e_nombre, self.e_cargo, self.e_salario]: e.delete(0, tk.END)
        self.combo_depto.set("Sistemas")
        self.var_activo.set(True)
        self.indice_editando = None
        self.btn_add.config(state="normal")
        self.btn_edit.config(state="disabled")

    def _insertar_fila(self, e):
        tag = "" if e.get("activo", True) else "inactivo"
        self.tabla.insert("", tk.END, values=(
            e["id"], e["nombre"], e["cargo"], e["departamento"],
            e["salario"], "Activo" if e.get("activo", True) else "Inactivo"
        ), tags=(tag,) if tag else ())

    def _refrescar_tabla(self):
        self.tabla.delete(*self.tabla.get_children())
        for e in self.empleados:
            self._insertar_fila(e)


if __name__ == "__main__":
    app = RegistroEmpleados()
    app.mainloop()
