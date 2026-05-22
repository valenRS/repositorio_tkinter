# ============================================================
# MINI PROYECTO — LISTA DE TAREAS (To-Do List)
# ============================================================
#  ✓ Agregar tareas con descripción y prioridad
#  ✓ Marcar como completada / pendiente
#  ✓ Eliminar tareas
#  ✓ Filtrar por estado
#  ✓ Persistencia en JSON (tareas no se pierden al cerrar)
#  ✓ Estructura OOP
#
# Para ejecutar: python3 lista_de_tareas.py
# ============================================================

import tkinter as tk
from tkinter import ttk, messagebox
from datetime import date
import json, os

ARCHIVO = "tareas.json"

def cargar():
    return json.load(open(ARCHIVO, "r", encoding="utf-8")) if os.path.exists(ARCHIVO) else []

def guardar(datos):
    with open(ARCHIVO, "w", encoding="utf-8") as f:
        json.dump(datos, f, indent=4, ensure_ascii=False)


class ListaDeTareas(tk.Tk):

    def __init__(self):
        super().__init__()
        self.title("Lista de Tareas")
        self.geometry("650x520")
        self.configure(bg="#f5f5f5")
        self.tareas = cargar()
        self._construir_ui()
        self._refrescar_tabla()

    def _construir_ui(self):
        tk.Label(self, text="📝 Lista de Tareas",
                 font=("Arial", 15, "bold"), bg="#f5f5f5", fg="#1a237e").pack(pady=10)

        # ── Formulario ──────────────────────────────────────
        ff = tk.LabelFrame(self, text=" Nueva tarea ", bg="#f5f5f5", font=("Arial", 9))
        ff.pack(padx=14, fill="x", pady=5)

        tk.Label(ff, text="Descripción:", bg="#f5f5f5").grid(row=0, column=0, padx=8, pady=6, sticky="w")
        self.e_desc = tk.Entry(ff, width=35, font=("Arial", 11))
        self.e_desc.grid(row=0, column=1, padx=5, pady=6, columnspan=2)
        self.e_desc.bind("<Return>", lambda e: self._agregar())

        tk.Label(ff, text="Prioridad:", bg="#f5f5f5").grid(row=1, column=0, padx=8, pady=6, sticky="w")
        self.combo_prioridad = ttk.Combobox(
            ff, values=["Alta", "Media", "Baja"], width=10, state="readonly"
        )
        self.combo_prioridad.set("Media")
        self.combo_prioridad.grid(row=1, column=1, padx=5, pady=6, sticky="w")

        tk.Button(ff, text="➕ Agregar tarea", command=self._agregar,
                  bg="#3F51B5", fg="white", font=("Arial", 10),
                  width=14).grid(row=1, column=2, padx=10, pady=6)

        # ── Filtros ─────────────────────────────────────────
        bf = tk.Frame(self, bg="#f5f5f5")
        bf.pack(padx=14, fill="x", pady=3)
        tk.Label(bf, text="Mostrar:", bg="#f5f5f5").pack(side="left")
        for texto, cmd in [
            ("Todas",      lambda: self._filtrar("Todas")),
            ("Pendientes", lambda: self._filtrar("Pendiente")),
            ("Completadas",lambda: self._filtrar("Completada")),
        ]:
            tk.Button(bf, text=texto, command=cmd,
                      bg="#e8eaf6", font=("Arial", 9), width=10).pack(side="left", padx=3)

        # ── Tabla ───────────────────────────────────────────
        tf = tk.Frame(self, bg="#f5f5f5")
        tf.pack(padx=14, fill="both", expand=True, pady=5)

        cols = ("id", "descripcion", "prioridad", "estado", "fecha")
        self.tabla = ttk.Treeview(tf, columns=cols, show="headings", height=10)

        # Estilos para filas según prioridad y estado
        self.tabla.tag_configure("alta",      background="#ffebee")
        self.tabla.tag_configure("completada", foreground="#9E9E9E",
                                  font=("Arial", 10, "overstrike"))  # tachado

        enc = {"id":"#", "descripcion":"Descripción", "prioridad":"Prioridad",
               "estado":"Estado", "fecha":"Creada"}
        anc = {"id":35, "descripcion":280, "prioridad":80, "estado":90, "fecha":95}
        for c in cols:
            self.tabla.heading(c, text=enc[c])
            self.tabla.column(c, width=anc[c],
                               anchor="center" if c not in ("descripcion",) else "w")
        self.tabla.pack(side="left", fill="both", expand=True)
        sb = ttk.Scrollbar(tf, orient="vertical", command=self.tabla.yview)
        sb.pack(side="right", fill="y")
        self.tabla.config(yscrollcommand=sb.set)

        # ── Botones de acción ───────────────────────────────
        btnf = tk.Frame(self, bg="#f5f5f5")
        btnf.pack(pady=6)
        tk.Button(btnf, text="✓ Marcar completada", command=self._completar,
                  bg="#4CAF50", fg="white", width=18).pack(side="left", padx=5)
        tk.Button(btnf, text="↩ Marcar pendiente", command=self._pendiente,
                  bg="#FF9800", fg="white", width=18).pack(side="left", padx=5)
        tk.Button(btnf, text="🗑 Eliminar", command=self._eliminar,
                  bg="#f44336", fg="white", width=10).pack(side="left", padx=5)

        # ── Contador ────────────────────────────────────────
        self.lbl_contador = tk.Label(self, text="", bg="#f5f5f5", fg="#555", font=("Arial", 10))
        self.lbl_contador.pack(pady=3)

    def _agregar(self):
        desc      = self.e_desc.get().strip()
        prioridad = self.combo_prioridad.get()
        if not desc:
            messagebox.showwarning("Campo vacío", "Escribe una descripción para la tarea."); return

        nuevo_id = (max((t["id"] for t in self.tareas), default=0)) + 1
        self.tareas.append({
            "id": nuevo_id,
            "descripcion": desc,
            "prioridad": prioridad,
            "estado": "Pendiente",
            "fecha": str(date.today())
        })
        guardar(self.tareas)
        self.e_desc.delete(0, tk.END)
        self._refrescar_tabla()

    def _completar(self):
        self._cambiar_estado("Completada")

    def _pendiente(self):
        self._cambiar_estado("Pendiente")

    def _cambiar_estado(self, nuevo_estado):
        sel = self.tabla.selection()
        if not sel:
            messagebox.showwarning("Sin selección", "Selecciona una tarea."); return
        id_tarea = int(self.tabla.item(sel[0])["values"][0])
        for t in self.tareas:
            if t["id"] == id_tarea:
                t["estado"] = nuevo_estado; break
        guardar(self.tareas)
        self._refrescar_tabla()

    def _eliminar(self):
        sel = self.tabla.selection()
        if not sel:
            messagebox.showwarning("Sin selección", "Selecciona una tarea."); return
        id_tarea = int(self.tabla.item(sel[0])["values"][0])
        desc = self.tabla.item(sel[0])["values"][1]
        if not messagebox.askyesno("Confirmar", f"¿Eliminar la tarea '{desc}'?"): return
        self.tareas = [t for t in self.tareas if t["id"] != id_tarea]
        guardar(self.tareas)
        self._refrescar_tabla()

    def _filtrar(self, filtro):
        self.tabla.delete(*self.tabla.get_children())
        for t in self.tareas:
            if filtro == "Todas" or t["estado"] == filtro:
                self._insertar_fila(t)

    def _insertar_fila(self, t):
        if t["estado"] == "Completada":
            tag = "completada"
        elif t["prioridad"] == "Alta":
            tag = "alta"
        else:
            tag = ""
        self.tabla.insert("", tk.END, values=(
            t["id"], t["descripcion"], t["prioridad"], t["estado"], t["fecha"]
        ), tags=(tag,) if tag else ())

    def _refrescar_tabla(self):
        self.tabla.delete(*self.tabla.get_children())
        for t in self.tareas:
            self._insertar_fila(t)
        total      = len(self.tareas)
        pendientes = sum(1 for t in self.tareas if t["estado"] == "Pendiente")
        completadas = total - pendientes
        self.lbl_contador.config(
            text=f"Total: {total}  |  Pendientes: {pendientes}  |  Completadas: {completadas}")


if __name__ == "__main__":
    app = ListaDeTareas()
    app.mainloop()
