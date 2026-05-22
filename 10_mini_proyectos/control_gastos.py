# ============================================================
# MINI PROYECTO — CONTROL DE GASTOS
# ============================================================
# Registro personal de gastos con:
#  ✓ Campos: descripción, categoría, monto, fecha
#  ✓ Filtro por categoría
#  ✓ Total acumulado (general y por categoría)
#  ✓ Persistencia en JSON + OOP
#
# Para ejecutar: python3 control_gastos.py
# ============================================================

import tkinter as tk
from tkinter import ttk, messagebox
from datetime import date
import json, os

ARCHIVO = "gastos.json"

def cargar():
    return json.load(open(ARCHIVO, "r", encoding="utf-8")) if os.path.exists(ARCHIVO) else []

def guardar(datos):
    with open(ARCHIVO, "w", encoding="utf-8") as f:
        json.dump(datos, f, indent=4, ensure_ascii=False)

CATEGORIAS = ["Alimentación", "Transporte", "Entretenimiento",
              "Salud", "Educación", "Ropa", "Hogar", "Otro"]


class ControlGastos(tk.Tk):

    def __init__(self):
        super().__init__()
        self.title("Control de Gastos Personales")
        self.geometry("750x560")
        self.configure(bg="#fafafa")
        self.gastos = cargar()
        self._construir_ui()
        self._refrescar_tabla()
        self._actualizar_totales()

    def _construir_ui(self):
        tk.Label(self, text="Control de Gastos Personales",
                 font=("Arial", 14, "bold"), bg="#fafafa", fg="#4a148c").pack(pady=10)

        # ── Formulario ──────────────────────────────────────
        ff = tk.LabelFrame(self, text=" Nuevo gasto ", bg="#fafafa", font=("Arial", 9))
        ff.pack(padx=14, fill="x", pady=5)

        tk.Label(ff, text="Descripción:", bg="#fafafa").grid(row=0, column=0, padx=8, pady=5, sticky="w")
        self.e_desc = tk.Entry(ff, width=28, font=("Arial", 11))
        self.e_desc.grid(row=0, column=1, padx=5, pady=5)

        tk.Label(ff, text="Categoría:", bg="#fafafa").grid(row=0, column=2, padx=8, pady=5, sticky="w")
        self.combo_cat = ttk.Combobox(ff, values=CATEGORIAS, width=15, state="readonly")
        self.combo_cat.set("Alimentación")
        self.combo_cat.grid(row=0, column=3, padx=5, pady=5)

        tk.Label(ff, text="Monto $:", bg="#fafafa").grid(row=1, column=0, padx=8, pady=5, sticky="w")
        self.e_monto = tk.Entry(ff, width=28, font=("Arial", 11))
        self.e_monto.grid(row=1, column=1, padx=5, pady=5)

        tk.Label(ff, text="Fecha:", bg="#fafafa").grid(row=1, column=2, padx=8, pady=5, sticky="w")
        self.e_fecha = tk.Entry(ff, width=15, font=("Arial", 11))
        self.e_fecha.insert(0, str(date.today()))   # fecha de hoy por defecto
        self.e_fecha.grid(row=1, column=3, padx=5, pady=5)

        # ── Filtro ──────────────────────────────────────────
        bf = tk.Frame(self, bg="#fafafa")
        bf.pack(padx=14, fill="x", pady=3)
        tk.Label(bf, text="Filtrar por categoría:", bg="#fafafa").pack(side="left")
        self.combo_filtro = ttk.Combobox(bf, values=["Todas"] + CATEGORIAS, width=15, state="readonly")
        self.combo_filtro.set("Todas")
        self.combo_filtro.pack(side="left", padx=5)
        tk.Button(bf, text="Filtrar", command=self._filtrar, bg="#7B1FA2", fg="white").pack(side="left", padx=5)
        tk.Button(bf, text="Ver todos", command=self._refrescar_tabla, bg="#9E9E9E", fg="white").pack(side="left")

        # ── Botones ─────────────────────────────────────────
        btnf = tk.Frame(self, bg="#fafafa")
        btnf.pack(pady=5)
        tk.Button(btnf, text="➕ Registrar gasto", command=self._agregar,
                  bg="#4CAF50", fg="white", width=16, font=("Arial", 10)).pack(side="left", padx=5)
        tk.Button(btnf, text="🗑 Eliminar seleccionado", command=self._eliminar,
                  bg="#f44336", fg="white", width=20, font=("Arial", 10)).pack(side="left", padx=5)
        tk.Button(btnf, text="🔄 Limpiar form", command=self._limpiar,
                  bg="#9E9E9E", fg="white", width=12, font=("Arial", 10)).pack(side="left", padx=5)

        # ── Tabla ───────────────────────────────────────────
        tf = tk.Frame(self, bg="#fafafa")
        tf.pack(padx=14, fill="both", expand=True)

        cols = ("id", "descripcion", "categoria", "monto", "fecha")
        self.tabla = ttk.Treeview(tf, columns=cols, show="headings", height=9)
        enc = {"id":"#", "descripcion":"Descripción", "categoria":"Categoría",
               "monto":"Monto $", "fecha":"Fecha"}
        anc = {"id":40, "descripcion":240, "categoria":120, "monto":90, "fecha":100}
        for c in cols:
            self.tabla.heading(c, text=enc[c])
            self.tabla.column(c, width=anc[c], anchor="center" if c not in ("descripcion",) else "w")
        self.tabla.pack(side="left", fill="both", expand=True)
        sb = ttk.Scrollbar(tf, orient="vertical", command=self.tabla.yview)
        sb.pack(side="right", fill="y")
        self.tabla.config(yscrollcommand=sb.set)

        # ── Totales ─────────────────────────────────────────
        frame_totales = tk.Frame(self, bg="#4a148c")
        frame_totales.pack(fill="x", padx=14, pady=6)

        self.lbl_total_general = tk.Label(
            frame_totales, text="Total general: $0.00",
            bg="#4a148c", fg="white", font=("Arial", 12, "bold")
        )
        self.lbl_total_general.pack(side="left", padx=15, pady=6)

        self.lbl_total_filtro = tk.Label(
            frame_totales, text="",
            bg="#4a148c", fg="#FFD54F", font=("Arial", 11)
        )
        self.lbl_total_filtro.pack(side="left", padx=15, pady=6)

        self.lbl_estado = tk.Label(self, text="", bg="#fafafa", fg="green", font=("Arial", 10))
        self.lbl_estado.pack(pady=3)

    def _agregar(self):
        desc   = self.e_desc.get().strip()
        monto  = self.e_monto.get().strip()
        fecha  = self.e_fecha.get().strip()
        cat    = self.combo_cat.get()

        if not desc or not monto or not fecha:
            messagebox.showwarning("Campos vacíos", "Todos los campos son obligatorios."); return

        try:
            monto_f = float(monto)
            if monto_f <= 0:
                raise ValueError
        except ValueError:
            messagebox.showerror("Monto inválido", "El monto debe ser un número positivo."); return

        nuevo_id = (max((g["id"] for g in self.gastos), default=0)) + 1
        self.gastos.append({"id": nuevo_id, "descripcion": desc, "categoria": cat,
                             "monto": round(monto_f, 2), "fecha": fecha})
        guardar(self.gastos)
        self._refrescar_tabla()
        self._actualizar_totales()
        self._limpiar()
        self.lbl_estado.config(text=f"✓ Gasto registrado: ${monto_f:.2f}", fg="green")

    def _eliminar(self):
        sel = self.tabla.selection()
        if not sel:
            messagebox.showwarning("Sin selección", "Selecciona un gasto de la tabla."); return
        v = self.tabla.item(sel[0])["values"]
        id_gasto = int(v[0])
        desc     = v[1]
        if not messagebox.askyesno("Confirmar", f"¿Eliminar el gasto '{desc}'?"): return
        self.gastos = [g for g in self.gastos if g["id"] != id_gasto]
        guardar(self.gastos)
        self._refrescar_tabla()
        self._actualizar_totales()
        self.lbl_estado.config(text=f"✓ Gasto eliminado.", fg="green")

    def _filtrar(self):
        filtro = self.combo_filtro.get()
        self.tabla.delete(*self.tabla.get_children())
        total_filtro = 0
        for g in self.gastos:
            if filtro == "Todas" or g["categoria"] == filtro:
                self.tabla.insert("", tk.END,
                                   values=(g["id"], g["descripcion"], g["categoria"],
                                           f"${g['monto']:.2f}", g["fecha"]))
                total_filtro += g["monto"]
        if filtro != "Todas":
            self.lbl_total_filtro.config(text=f"Total {filtro}: ${total_filtro:.2f}")
        else:
            self.lbl_total_filtro.config(text="")

    def _actualizar_totales(self):
        total = sum(g["monto"] for g in self.gastos)
        self.lbl_total_general.config(text=f"Total general: ${total:.2f}")

    def _limpiar(self):
        self.e_desc.delete(0, tk.END)
        self.e_monto.delete(0, tk.END)
        self.e_fecha.delete(0, tk.END)
        self.e_fecha.insert(0, str(date.today()))
        self.combo_cat.set("Alimentación")

    def _refrescar_tabla(self):
        self.tabla.delete(*self.tabla.get_children())
        for g in self.gastos:
            self.tabla.insert("", tk.END,
                               values=(g["id"], g["descripcion"], g["categoria"],
                                       f"${g['monto']:.2f}", g["fecha"]))
        self.lbl_total_filtro.config(text="")


if __name__ == "__main__":
    app = ControlGastos()
    app.mainloop()
