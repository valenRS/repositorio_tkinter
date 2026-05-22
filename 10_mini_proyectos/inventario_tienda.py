# ============================================================
# MINI PROYECTO — INVENTARIO DE TIENDA
# ============================================================
# CRUD completo de productos con:
#  ✓ Campos: código, nombre, categoría, precio, stock, disponible
#  ✓ Alerta visual cuando el stock está bajo (< 5)
#  ✓ Búsqueda por categoría
#  ✓ Persistencia en JSON
#  ✓ Estructura OOP
#
# Para ejecutar: python3 inventario_tienda.py
# ============================================================

import tkinter as tk
from tkinter import ttk, messagebox
import json, os

ARCHIVO = "inventario.json"

def cargar():
    return json.load(open(ARCHIVO, "r", encoding="utf-8")) if os.path.exists(ARCHIVO) else []

def guardar(datos):
    with open(ARCHIVO, "w", encoding="utf-8") as f:
        json.dump(datos, f, indent=4, ensure_ascii=False)


class InventarioTienda(tk.Tk):

    def __init__(self):
        super().__init__()
        self.title("Inventario de Tienda")
        self.geometry("820x570")
        self.configure(bg="#fff8f0")
        self.productos = cargar()
        self.indice_editando = None
        self._construir_ui()
        self._refrescar_tabla()

    def _construir_ui(self):
        tk.Label(self, text="Inventario de Productos",
                 font=("Arial", 14, "bold"), bg="#fff8f0", fg="#b35900").pack(pady=10)

        # ── Formulario ──────────────────────────────────────
        ff = tk.LabelFrame(self, text=" Datos del producto ",
                            bg="#fff8f0", font=("Arial", 9))
        ff.pack(padx=14, fill="x", pady=5)

        tk.Label(ff, text="Código:", bg="#fff8f0").grid(row=0, column=0, padx=8, pady=5, sticky="w")
        self.e_codigo = tk.Entry(ff, width=14, font=("Arial", 11))
        self.e_codigo.grid(row=0, column=1, padx=5, pady=5)

        tk.Label(ff, text="Nombre:", bg="#fff8f0").grid(row=0, column=2, padx=8, pady=5, sticky="w")
        self.e_nombre = tk.Entry(ff, width=22, font=("Arial", 11))
        self.e_nombre.grid(row=0, column=3, padx=5, pady=5)

        tk.Label(ff, text="Categoría:", bg="#fff8f0").grid(row=1, column=0, padx=8, pady=5, sticky="w")
        self.combo_cat = ttk.Combobox(
            ff,
            values=["Electrónica", "Ropa", "Alimentos", "Hogar", "Deportes",
                    "Juguetes", "Papelería", "Otro"],
            width=12, state="readonly"
        )
        self.combo_cat.set("Electrónica")
        self.combo_cat.grid(row=1, column=1, padx=5, pady=5)

        tk.Label(ff, text="Precio $:", bg="#fff8f0").grid(row=1, column=2, padx=8, pady=5, sticky="w")
        self.e_precio = tk.Entry(ff, width=22, font=("Arial", 11))
        self.e_precio.grid(row=1, column=3, padx=5, pady=5)

        tk.Label(ff, text="Stock:", bg="#fff8f0").grid(row=2, column=0, padx=8, pady=5, sticky="w")
        self.e_stock = tk.Entry(ff, width=14, font=("Arial", 11))
        self.e_stock.grid(row=2, column=1, padx=5, pady=5)

        self.var_disponible = tk.BooleanVar(value=True)
        tk.Checkbutton(ff, text="Disponible para venta",
                       variable=self.var_disponible, bg="#fff8f0").grid(
            row=2, column=2, columnspan=2, padx=8, pady=5, sticky="w")

        # ── Filtro ──────────────────────────────────────────
        bf = tk.Frame(self, bg="#fff8f0")
        bf.pack(padx=14, fill="x", pady=3)
        tk.Label(bf, text="Filtrar por categoría:", bg="#fff8f0").pack(side="left")
        self.combo_filtro = ttk.Combobox(
            bf,
            values=["Todos", "Electrónica", "Ropa", "Alimentos", "Hogar",
                    "Deportes", "Juguetes", "Papelería", "Otro"],
            width=14, state="readonly"
        )
        self.combo_filtro.set("Todos")
        self.combo_filtro.pack(side="left", padx=5)
        tk.Button(bf, text="Filtrar", command=self._filtrar,
                  bg="#FF9800", fg="white").pack(side="left", padx=5)
        tk.Button(bf, text="Ver todos", command=self._refrescar_tabla,
                  bg="#9E9E9E", fg="white").pack(side="left")
        tk.Button(bf, text="⚠ Stock bajo (<5)", command=self._ver_stock_bajo,
                  bg="#f44336", fg="white").pack(side="left", padx=10)

        # ── Botones CRUD ────────────────────────────────────
        btnf = tk.Frame(self, bg="#fff8f0")
        btnf.pack(pady=6)
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
        tf = tk.Frame(self, bg="#fff8f0")
        tf.pack(padx=14, fill="both", expand=True)

        cols = ("codigo", "nombre", "categoria", "precio", "stock", "disponible")
        self.tabla = ttk.Treeview(tf, columns=cols, show="headings", height=9)

        # Estilo para filas con stock bajo
        self.tabla.tag_configure("stock_bajo", background="#ffdddd")

        enc = {"codigo":"Código", "nombre":"Nombre", "categoria":"Categoría",
               "precio":"Precio $", "stock":"Stock", "disponible":"Disponible"}
        anc = {"codigo":80, "nombre":200, "categoria":110, "precio":90, "stock":70, "disponible":90}
        for c in cols:
            self.tabla.heading(c, text=enc[c])
            self.tabla.column(c, width=anc[c], anchor="center" if c not in ("nombre",) else "w")

        self.tabla.pack(side="left", fill="both", expand=True)
        sb = ttk.Scrollbar(tf, orient="vertical", command=self.tabla.yview)
        sb.pack(side="right", fill="y")
        self.tabla.config(yscrollcommand=sb.set)
        self.tabla.bind("<Double-1>", self._cargar_para_editar)

        self.lbl = tk.Label(self, text="", bg="#fff8f0", fg="green", font=("Arial", 10))
        self.lbl.pack(pady=4)

    def _agregar(self):
        d = self._leer_form()
        if not d: return
        if any(p["codigo"] == d["codigo"] for p in self.productos):
            messagebox.showerror("Duplicado", f"El código '{d['codigo']}' ya existe."); return
        self.productos.append(d)
        guardar(self.productos)
        self._refrescar_tabla()
        self._limpiar()
        self.lbl.config(text=f"✓ '{d['nombre']}' agregado.", fg="green")

    def _cargar_para_editar(self, event):
        sel = self.tabla.selection()
        if not sel: return
        v = self.tabla.item(sel[0])["values"]
        for i, p in enumerate(self.productos):
            if str(p["codigo"]) == str(v[0]):
                self.indice_editando = i; break
        self.e_codigo.config(state="normal")
        self.e_codigo.delete(0, tk.END);  self.e_codigo.insert(0, v[0])
        self.e_codigo.config(state="disabled")
        self.e_nombre.delete(0, tk.END);  self.e_nombre.insert(0, v[1])
        self.combo_cat.set(v[2])
        self.e_precio.delete(0, tk.END);  self.e_precio.insert(0, v[3])
        self.e_stock.delete(0, tk.END);   self.e_stock.insert(0, v[4])
        self.var_disponible.set(v[5] == "Sí")
        self.btn_add.config(state="disabled")
        self.btn_edit.config(state="normal")
        self.lbl.config(text="✏ Modo edición — modifica y presiona 'Guardar edición'.", fg="orange")

    def _guardar_edicion(self):
        if self.indice_editando is None: return
        nombre = self.e_nombre.get().strip()
        precio = self.e_precio.get().strip()
        stock  = self.e_stock.get().strip()
        if not nombre or not precio or not stock:
            messagebox.showwarning("Campos vacíos", "Completa todos los campos."); return
        p = self.productos[self.indice_editando]
        p["nombre"]     = nombre
        p["categoria"]  = self.combo_cat.get()
        p["precio"]     = precio
        p["stock"]      = int(stock)
        p["disponible"] = self.var_disponible.get()
        guardar(self.productos)
        self._refrescar_tabla()
        self._limpiar()
        self.lbl.config(text="✓ Producto actualizado.", fg="green")

    def _eliminar(self):
        sel = self.tabla.selection()
        if not sel:
            messagebox.showwarning("Sin selección", "Selecciona un producto."); return
        v = self.tabla.item(sel[0])["values"]
        if not messagebox.askyesno("Confirmar", f"¿Eliminar '{v[1]}'?"): return
        self.productos = [p for p in self.productos if str(p["codigo"]) != str(v[0])]
        guardar(self.productos)
        self._refrescar_tabla()
        self._limpiar()
        self.lbl.config(text=f"✓ '{v[1]}' eliminado.", fg="green")

    def _filtrar(self):
        filtro = self.combo_filtro.get()
        self.tabla.delete(*self.tabla.get_children())
        for p in self.productos:
            if filtro == "Todos" or p["categoria"] == filtro:
                self._insertar_fila(p)

    def _ver_stock_bajo(self):
        self.tabla.delete(*self.tabla.get_children())
        for p in self.productos:
            if int(p["stock"]) < 5:
                self._insertar_fila(p, tag="stock_bajo")
        self.lbl.config(text="Mostrando productos con stock menor a 5.", fg="red")

    def _leer_form(self):
        codigo = self.e_codigo.get().strip()
        nombre = self.e_nombre.get().strip()
        precio = self.e_precio.get().strip()
        stock  = self.e_stock.get().strip()
        if not all([codigo, nombre, precio, stock]):
            messagebox.showwarning("Campos vacíos", "Todos los campos son obligatorios."); return None
        if not stock.isdigit():
            messagebox.showerror("Error", "El stock debe ser un número entero."); return None
        return {"codigo": codigo, "nombre": nombre, "categoria": self.combo_cat.get(),
                "precio": precio, "stock": int(stock), "disponible": self.var_disponible.get()}

    def _limpiar(self):
        self.e_codigo.config(state="normal")
        for e in [self.e_codigo, self.e_nombre, self.e_precio, self.e_stock]: e.delete(0, tk.END)
        self.combo_cat.set("Electrónica")
        self.var_disponible.set(True)
        self.indice_editando = None
        self.btn_add.config(state="normal")
        self.btn_edit.config(state="disabled")

    def _insertar_fila(self, p, tag=""):
        self.tabla.insert("", tk.END, values=(
            p["codigo"], p["nombre"], p["categoria"], p["precio"],
            p["stock"], "Sí" if p.get("disponible", True) else "No"
        ), tags=(tag,) if tag else ())

    def _refrescar_tabla(self):
        self.tabla.delete(*self.tabla.get_children())
        for p in self.productos:
            self._insertar_fila(p, "stock_bajo" if int(p["stock"]) < 5 else "")


if __name__ == "__main__":
    app = InventarioTienda()
    app.mainloop()
