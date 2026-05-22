## Plan: Repositorio de Tkinter para principiantes

El objetivo es crear un repositorio didáctico en español, con código muy comentado, organizado por temas progresivos. Cada tema tiene su propio archivo `.py` listo para ejecutar, con ejemplos que ella puede copiar y adaptar para el examen.

---

**Estructura de archivos propuesta**

```
muchachita_explain/
│
├── README.md                        ← Índice general + cómo ejecutar
│
├── 01_ventana_basica/
│   ├── explicacion.md
│   └── ventana.py                   ← Crear ventana, título, tamaño, color
│
├── 02_widgets_texto_y_botones/
│   ├── explicacion.md
│   └── widgets.py                   ← Label, Button, Entry, Text
│
├── 03_layouts/
│   ├── explicacion.md
│   ├── pack.py                      ← Layout con pack()
│   ├── grid.py                      ← Layout con grid() (el más útil en examen)
│   └── place.py                     ← Layout con place()
│
├── 04_eventos_y_funciones/
│   ├── explicacion.md
│   └── eventos.py                   ← command=, bind(), leer Entry, mostrar en Label
│
├── 05_widgets_avanzados/
│   ├── explicacion.md
│   └── avanzados.py                 ← Checkbutton, Radiobutton, Listbox, Combobox
│
├── 06_ventanas_emergentes/
│   ├── explicacion.md
│   └── popups.py                    ← messagebox (info, error, pregunta)
│
├── 07_oop_con_tkinter/
│   ├── explicacion.md
│   └── clase_ventana.py             ← Estructura base OOP (class App(tk.Tk)) — OBLIGATORIO en examen
│
├── 08_persistencia_datos/
│   ├── explicacion.md
│   ├── guardar_json.py              ← Leer/escribir JSON (datos no se pierden al cerrar)
│   └── guardar_csv.py               ← Leer/escribir CSV
│
├── 09_patron_crud/
│   ├── explicacion.md
│   └── crud_base.py                 ← Agregar, buscar, editar, eliminar + mostrar en Listbox/Treeview
│
├── 10_mini_proyectos/
│   ├── calculadora.py               ← Calculadora completa con grid
│   ├── lista_de_tareas.py           ← To-do list con persistencia JSON
│   ├── sistema_biblioteca.py        ← CRUD libros: código, título, autor, género, copias, físico/digital — IDÉNTICO al parcial
│   ├── gestion_estudiantes.py       ← CRUD estudiantes: nombre, ID, carrera, notas, búsqueda por carrera
│   ├── inventario_tienda.py         ← CRUD productos: nombre, categoría, precio, stock, alertas de mínimo
│   ├── registro_empleados.py        ← CRUD empleados: nombre, cargo, salario, departamento, activo/inactivo
│   └── control_gastos.py            ← Registrar gastos por categoría, filtrar, mostrar total
│
└── CHEATSHEET.md                    ← Hoja de trampa rápida para el examen
```

---

**Pasos de implementación**

1. Crear `README.md` — índice visual con links a cada sección y cómo correr los scripts
2. Crear módulo `01` — ventana básica, `geometry()`, `title()`, `configure(bg=)`
3. Crear módulo `02` — todos los widgets de texto con opciones de estilo (fuente, color, tamaño)
4. Crear módulo `03` — los 3 layouts, énfasis en `grid()` porque es el más pedido en exámenes
5. Crear módulo `04` — eventos: leer input del usuario, conectar botón a función, actualizar label
6. Crear módulo `05` — widgets más complejos con `StringVar`, `IntVar`
7. Crear módulo `06` — `messagebox` para mostrar resultados o errores
8. Crear módulo `07` — estructura OOP base (`class App(tk.Tk)`) ← patrón obligatorio según el parcial real
9. Crear módulo `08` — persistencia con JSON y CSV (los datos no desaparecen al cerrar la app)
10. Crear módulo `09` — patrón CRUD completo con Treeview/Listbox + botones Agregar/Editar/Eliminar
11. Crear los mini proyectos — empezando por `sistema_biblioteca.py` que replica el parcial real
12. Crear `CHEATSHEET.md` — resumen de 1 página con los snippets más importantes

---

**Decisiones de diseño**
- Todo en **español**: comentarios, nombres de variables, explicaciones
- Cada `.py` tiene una sección `# === CÓMO FUNCIONA ===` al inicio antes del código
- Los ejemplos son independientes (no importan otros archivos del repo)
- Sin librerías externas — solo `tkinter` + `json` + `csv` que vienen con Python
- Todos los mini proyectos usan la estructura OOP (`class App(tk.Tk)`) requerida en el parcial real

---

**Contexto del parcial real (Ejemplo_Parcial_3_1.pdf)**
- Materia: Programación II — Universidad Tecnológica de Pereira, Ingeniería Electrónica
- El examen pide un sistema CRUD completo de biblioteca con:
  - Campos: código, título, autor, género, copias disponibles, físico/digital
  - Validación de campos antes de guardar
  - Persistencia de datos (no se pierden al cerrar)
  - Búsqueda por género + gestión de préstamos (prestar / entregar)
  - Reporte de préstamos por género
  - Editar y eliminar libros
  - **OOP obligatorio** — sin OOP se califica sobre 3.0 / 5.0
- Los mini proyectos adicionales (`gestion_estudiantes`, `inventario_tienda`, `registro_empleados`, `control_gastos`) replican el mismo patrón con distintos dominios

---

**Further Considerations**

1. **Mini proyectos**: El parcial real pide OOP + CRUD + persistencia + búsqueda/filtro. Los 5 mini proyectos nuevos cubren exactamente ese patrón con distintos temas.
2. **Nivel de comentarios**: ¿Prefieres comentarios línea por línea (para alguien que nunca ha programado) o comentarios por bloques (más rápido de leer)?
3. **CHEATSHEET**: ¿Lo quieres como `.md` para leer en GitHub, o también como `.py` ejecutable con todos los snippets juntos?
4. **Persistencia**: El parcial dice "la información no debe eliminarse aunque la aplicación se cierre" → se usará JSON como formato por defecto en todos los proyectos.
