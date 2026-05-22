# CHEATSHEET — Tkinter para el Examen
## Hoja de referencia rápida

---

## 1. ESTRUCTURA BASE (OOP — OBLIGATORIA EN EXAMEN)

```python
import tkinter as tk
from tkinter import ttk, messagebox
import json, os

class MiApp(tk.Tk):
    def __init__(self):
        super().__init__()
        self.title("Mi App")
        self.geometry("700x500")
        self.configure(bg="white")
        self.datos = cargar_json("archivo.json")
        self._crear_widgets()

    def _crear_widgets(self):
        pass   # aquí van todos los widgets

if __name__ == "__main__":
    app = MiApp()
    app.mainloop()
```

---

## 2. PERSISTENCIA JSON (datos no se pierden)

```python
import json, os

def cargar_json(archivo):
    if os.path.exists(archivo):
        with open(archivo, "r", encoding="utf-8") as f:
            return json.load(f)
    return []

def guardar_json(archivo, datos):
    with open(archivo, "w", encoding="utf-8") as f:
        json.dump(datos, f, indent=4, ensure_ascii=False)
```

---

## 3. WIDGETS MÁS USADOS

```python
# Label — mostrar texto
tk.Label(self, text="Hola", font=("Arial", 12), bg="white", fg="navy")

# Entry — campo de una línea
self.e_nombre = tk.Entry(self, width=25, font=("Arial", 11))
nombre = self.e_nombre.get().strip()          # leer
self.e_nombre.delete(0, tk.END)               # limpiar
self.e_nombre.insert(0, "texto")              # insertar texto

# Button
tk.Button(self, text="Guardar", command=self._guardar, bg="lightgreen", width=12)

# Combobox (lista desplegable)
self.combo = ttk.Combobox(self, values=["A","B","C"], state="readonly", width=15)
self.combo.set("A")                           # valor por defecto
valor = self.combo.get()                      # leer

# Checkbutton
self.var = tk.BooleanVar(value=True)
tk.Checkbutton(self, text="Activo", variable=self.var)
estado = self.var.get()                       # True o False

# Radiobutton
self.var_rb = tk.StringVar(value="Físico")
tk.Radiobutton(self, text="Físico",  variable=self.var_rb, value="Físico")
tk.Radiobutton(self, text="Digital", variable=self.var_rb, value="Digital")
formato = self.var_rb.get()                   # leer
```

---

## 4. GRID() — EL MÁS IMPORTANTE

```python
# Columna 0 = etiquetas, columna 1 = campos
tk.Label(frame, text="Nombre:").grid(row=0, column=0, padx=8, pady=5, sticky="w")
self.e_nombre = tk.Entry(frame, width=25).grid(row=0, column=1, padx=5, pady=5)

# sticky="w"  → alinea a la izquierda
# sticky="ew" → se estira de lado a lado
# columnspan=2 → ocupa 2 columnas
# padx/pady   → espacio exterior
```

---

## 5. TREEVIEW (tabla para mostrar registros)

```python
# Crear tabla
cols = ("codigo", "nombre", "categoria")
self.tabla = ttk.Treeview(frame, columns=cols, show="headings", height=8)

# Encabezados y anchos
self.tabla.heading("codigo",    text="Código")
self.tabla.heading("nombre",    text="Nombre")
self.tabla.heading("categoria", text="Categoría")
self.tabla.column("codigo",    width=80,  anchor="center")
self.tabla.column("nombre",    width=200, anchor="w")
self.tabla.column("categoria", width=120, anchor="center")
self.tabla.pack(side="left", fill="both", expand=True)

# Scrollbar
sb = ttk.Scrollbar(frame, orient="vertical", command=self.tabla.yview)
sb.pack(side="right", fill="y")
self.tabla.config(yscrollcommand=sb.set)

# Insertar fila
self.tabla.insert("", tk.END, values=("C001", "Python", "Tecnología"))

# Limpiar tabla
self.tabla.delete(*self.tabla.get_children())

# Leer fila seleccionada (doble clic)
self.tabla.bind("<Double-1>", self._cargar_para_editar)

def _cargar_para_editar(self, event):
    sel = self.tabla.selection()
    if not sel: return
    vals = self.tabla.item(sel[0])["values"]
    # vals[0] = primer columna, vals[1] = segunda, etc.
```

---

## 6. MESSAGEBOX

```python
messagebox.showinfo("Título", "Mensaje informativo")
messagebox.showwarning("Título", "Advertencia")
messagebox.showerror("Título", "Error")
respuesta = messagebox.askyesno("Confirmar", "¿Estás seguro?")  # True / False
```

---

## 7. VALIDACIÓN OBLIGATORIA

```python
def _leer_form(self):
    codigo = self.e_codigo.get().strip()
    nombre = self.e_nombre.get().strip()

    # Verificar que TODOS los campos estén llenos
    if not codigo or not nombre:
        messagebox.showwarning("Campos vacíos", "Todos los campos son obligatorios.")
        return None

    # Verificar número entero
    if not cantidad.isdigit():
        messagebox.showerror("Error", "La cantidad debe ser un número.")
        return None

    return {"codigo": codigo, "nombre": nombre}
```

---

## 8. PATRÓN CRUD COMPLETO (esqueleto para el examen)

```python
def _agregar(self):
    d = self._leer_form()
    if not d: return
    # Verificar duplicado
    if any(x["codigo"] == d["codigo"] for x in self.datos):
        messagebox.showerror("Duplicado", "El código ya existe."); return
    self.datos.append(d)
    guardar_json("archivo.json", self.datos)
    self._refrescar_tabla()
    self._limpiar()

def _eliminar(self):
    sel = self.tabla.selection()
    if not sel:
        messagebox.showwarning("Sin selección", "Selecciona una fila."); return
    vals = self.tabla.item(sel[0])["values"]
    if not messagebox.askyesno("Confirmar", f"¿Eliminar '{vals[1]}'?"): return
    self.datos = [x for x in self.datos if str(x["codigo"]) != str(vals[0])]
    guardar_json("archivo.json", self.datos)
    self._refrescar_tabla()

def _refrescar_tabla(self):
    self.tabla.delete(*self.tabla.get_children())
    for d in self.datos:
        self.tabla.insert("", tk.END, values=(d["codigo"], d["nombre"]))
```

---

## 9. NOTEBOOK (pestañas)

```python
notebook = ttk.Notebook(self)
notebook.pack(fill="both", expand=True, padx=10, pady=10)

frame1 = tk.Frame(notebook, bg="white")
frame2 = tk.Frame(notebook, bg="white")

notebook.add(frame1, text="  Pestaña 1  ")
notebook.add(frame2, text="  Pestaña 2  ")
```

---

## 10. FRAME (contenedor para organizar)

```python
# LabelFrame — frame con título visible
frame_form = tk.LabelFrame(self, text=" Formulario ", bg="white", font=("Arial", 9))
frame_form.pack(padx=14, fill="x", pady=5)

# Frame simple — para agrupar botones horizontalmente
frame_btn = tk.Frame(self, bg="white")
frame_btn.pack(pady=8)
tk.Button(frame_btn, text="Btn1").pack(side="left", padx=5)
tk.Button(frame_btn, text="Btn2").pack(side="left", padx=5)
```

---

## 11. COLORES ÚTILES

| Nombre | Color |
|--------|-------|
| `"white"` | Blanco |
| `"lightblue"` | Azul claro |
| `"lightgreen"` | Verde claro |
| `"lightyellow"` | Amarillo claro |
| `"#f0f4f8"` | Gris azulado suave |
| `"#4CAF50"` | Verde Material Design |
| `"#f44336"` | Rojo Material Design |
| `"#2196F3"` | Azul Material Design |
| `"#FF9800"` | Naranja Material Design |
| `"navy"` | Azul oscuro |

---

## 12. CHECKLIST ANTES DE ENTREGAR EL EXAMEN

- [ ] La clase hereda de `tk.Tk` y usa `super().__init__()`
- [ ] El programa corre desde `if __name__ == "__main__":`
- [ ] Los datos se guardan en JSON (no desaparecen al cerrar)
- [ ] Todos los campos se validan antes de guardar
- [ ] No hay duplicados de código/ID
- [ ] La tabla (Treeview) se actualiza después de cada operación
- [ ] Los botones de editar/eliminar confirman antes de actuar (`askyesno`)
- [ ] Se puede buscar/filtrar por la categoría/género/departamento pedido
