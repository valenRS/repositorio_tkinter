# Módulo 01 — La Ventana Básica

## ¿Qué es Tkinter?
Tkinter es la librería que viene incluida con Python para crear ventanas y botones.
No necesitas instalar nada extra.

## Los 3 pasos mínimos para crear una ventana

```python
import tkinter as tk          # 1. Importar la librería

ventana = tk.Tk()             # 2. Crear la ventana principal

ventana.mainloop()            # 3. Mantenerla abierta (siempre va al final)
```

## Métodos útiles de la ventana

| Método | ¿Para qué sirve? | Ejemplo |
|---|---|---|
| `.title("texto")` | Poner título en la barra | `ventana.title("Mi App")` |
| `.geometry("AnchoxAlto")` | Definir tamaño en píxeles | `ventana.geometry("400x300")` |
| `.configure(bg="color")` | Color de fondo | `ventana.configure(bg="lightblue")` |
| `.resizable(False, False)` | Evitar que se redimensione | `ventana.resizable(False, False)` |
| `.minsize(200, 200)` | Tamaño mínimo | `ventana.minsize(200, 200)` |

## Colores en Tkinter
Puedes usar nombres en inglés: `"white"`, `"black"`, `"red"`, `"blue"`, `"green"`, `"yellow"`, `"gray"`, `"lightblue"`, `"lightgreen"`, `"orange"`, etc.
O usar código hexadecimal: `"#FF5733"`, `"#2C3E50"`, etc.

---
Ejecuta el archivo `ventana.py` para ver todos estos conceptos en práctica.
