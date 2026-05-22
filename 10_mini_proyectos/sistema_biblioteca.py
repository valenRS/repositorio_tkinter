# ============================================================
# SISTEMA DE BIBLIOTECA — Clase principal (Vista + Lógica)
# ============================================================
# Importa las funciones de persistencia y las constantes de
# archivos desde el módulo separado `persistencia`.
# Para ejecutar la aplicación usa: python3 main.py
# ============================================================

import tkinter as tk
from tkinter import ttk, messagebox
from persistencia import cargar_json, guardar_json, ARCHIVO_LIBROS, ARCHIVO_PRESTAMOS


# ============================================================
# CLASE PRINCIPAL — SistemaBiblioteca
# ============================================================
# Hereda directamente de tk.Tk, lo que la convierte en la ventana
# raíz de la aplicación (patrón OOP obligatorio en el parcial).
# Al heredar de tk.Tk no necesitamos crear una ventana aparte:
# la propia instancia de la clase ES la ventana principal.
class SistemaBiblioteca(tk.Tk):
    def __init__(self):
        """
        Constructor de la clase — se ejecuta automáticamente al hacer
        app = SistemaBiblioteca().

        Responsabilidades:
        1. super().__init__()  → inicializa la ventana raíz de Tkinter
           (SIEMPRE debe ser la primera línea al heredar de tk.Tk).
        2. Configura título, tamaño y color de fondo de la ventana.
        3. Carga los datos persistidos desde los archivos JSON:
           - self.libros    → lista de diccionarios con los libros.
           - self.prestamos → lista de diccionarios con los préstamos.
        4. self.indice_editando → guarda la posición en self.libros del
           libro que está siendo editado (None = no hay edición activa).
        5. Llama a _crear_pestanas() para construir toda la interfaz.
        """
        super().__init__()
        self.title("Sistema de Gestión Biblioteca")
        self.geometry("800x600")
        self.configure(bg="#f0f4f8")
        self.resizable(True, True)

        # Cargar datos desde JSON al iniciar (persistencia)
        self.libros    = cargar_json(ARCHIVO_LIBROS)
        self.prestamos = cargar_json(ARCHIVO_PRESTAMOS)
        # Índice del libro en edición (None = modo creación)
        self.indice_editando = None

        self._crear_pestanas()

    # ──────────────────────────────────────────────────────
    # PESTAÑAS (Notebook)
    # ──────────────────────────────────────────────────────
    def _crear_pestanas(self):
        """
        Crea el widget ttk.Notebook (contenedor de pestañas) y agrega
        los tres frames principales, uno por pestaña:
          - frame_libros      → CRUD de libros
          - frame_prestamos   → búsqueda y gestión de préstamos
          - frame_consolidado → estadísticas por género
        Después delega la construcción interna de cada pestaña a sus
        propios métodos (_crear_tab_*).
        """
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
        """
        Construye visualmente la pestaña de Gestión de Libros.
        Crea y posiciona:
          - Un LabelFrame con el formulario de entrada (código, título,
            autor, género, copias, formato físico/digital).
          - Los botones: Agregar, Guardar edición, Eliminar y Limpiar.
          - Un Treeview (tabla) que muestra todos los libros guardados,
            con scrollbar vertical.
          - Una etiqueta de estado para mostrar mensajes de feedback.
        Los widgets de entrada se guardan como atributos (self.e_codigo,
        self.e_titulo, etc.) para poder leerlos desde otros métodos.
        El evento <Double-1> en la tabla llama a _cargar_libro_para_editar.
        """

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
        """
        Construye visualmente la pestaña de Gestión de Préstamos.
        Crea y posiciona:
          - Un LabelFrame con un Combobox para filtrar libros por género
            y un botón "Buscar".
          - Un Treeview que muestra los resultados de la búsqueda,
            incluyendo las copias disponibles (totales - préstamos activos).
          - Botones "Registrar préstamo" y "Registrar devolución" que
            operan sobre el libro seleccionado en la tabla.
          - Etiqueta de estado para mensajes de feedback.
        """

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
        """
        Construye visualmente la pestaña de Consolidado.
        Crea y posiciona:
          - Un botón "Actualizar consolidado" que recalcula las estadísticas.
          - Un Treeview con 4 columnas: Género, Total Préstamos, Activos,
            Devueltos.
          - Una etiqueta que muestra el total general de préstamos.
        La tabla se llena solo cuando el usuario presiona el botón,
        mediante el método _actualizar_consolidado.
        """

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
        """
        Valida y agrega un nuevo libro a la lista self.libros.
        Pasos:
          1. Llama a _leer_form_libro() para obtener y validar los datos
             del formulario. Si hay un error retorna None y se detiene.
          2. Verifica que el código no esté duplicado (búsqueda con any()).
          3. Agrega el diccionario del libro a self.libros.
          4. Persiste la lista actualizada en el JSON.
          5. Refresca la tabla y limpia el formulario.
        """

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
        """
        Se ejecuta al hacer doble clic en una fila del Treeview de libros.
        Responsabilidades:
          1. Obtiene la fila seleccionada y extrae sus valores.
          2. Busca el índice del libro en self.libros por código y lo
             guarda en self.indice_editando para usarlo al guardar.
          3. Carga los valores de la fila en los campos del formulario.
          4. Deshabilita el campo Código (no se puede cambiar la PK).
          5. Cambia el estado de los botones: desactiva "Agregar" y
             activa "Guardar edición", poniendo la UI en modo edición.
        Parámetro `event`: objeto de evento de Tkinter (requerido por
        bind, pero no se usa directamente).
        """
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
        """
        Guarda los cambios realizados sobre el libro que está en edición.
        Pasos:
          1. Verifica que self.indice_editando no sea None (protección).
          2. Lee y valida los campos editables (título, autor, copias).
             El código NO se toca porque está deshabilitado.
          3. Actualiza directamente el diccionario en self.libros usando
             el índice guardado.
          4. Persiste, refresca tabla y limpia el formulario.
        """
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
        """
        Elimina el libro seleccionado en la tabla de libros.
        Pasos:
          1. Verifica que haya una fila seleccionada.
          2. Pide confirmación con messagebox.askyesno (buena práctica
             para operaciones destructivas).
          3. Filtra self.libros con list comprehension descartando el
             libro cuyo código coincida con el seleccionado.
          4. Persiste la lista sin ese libro y refresca la tabla.
        """
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
        """
        Lee y valida todos los campos del formulario de libros.
        - Usa .get().strip() para eliminar espacios accidentales.
        - Verifica que ningún campo obligatorio esté vacío (all([...])).
        - Verifica que el campo Copias sea un número entero no negativo.
        Retorna:
          - Un diccionario con los datos del libro si todo es válido.
          - None si hay algún error (el llamador debe revisar esto).
        Este patrón de retornar None en caso de error evita tener que
        lanzar excepciones y simplifica el flujo en _agregar_libro.
        """
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
        """
        Resetea el formulario de libros a su estado inicial vacío.
        - Reactiva el campo Código (que se deshabilita en modo edición).
        - Borra el contenido de todos los Entry.
        - Restaura el Combobox y el Radiobutton a sus valores por defecto.
        - Limpia self.indice_editando (sale del modo edición).
        - Reactiva el botón "Agregar" y desactiva "Guardar edición".
        Se llama después de agregar, guardar edición o eliminar un libro.
        """
        self.e_codigo.config(state="normal")
        for e in [self.e_codigo, self.e_titulo, self.e_autor, self.e_copias]:
            e.delete(0, tk.END)
        self.combo_genero.set("Novela")
        self.var_formato.set("Físico")
        self.indice_editando = None
        self.btn_agregar_libro.config(state="normal")
        self.btn_guardar_edicion.config(state="disabled")

    def _refrescar_tabla_libros(self):
        """
        Vuelve a pintar el Treeview de libros desde cero.
        - Borra todas las filas existentes con delete(*get_children()).
        - Itera self.libros e inserta cada libro como una nueva fila.
        Se debe llamar siempre que self.libros cambie (agregar, editar,
        eliminar) para mantener la vista sincronizada con los datos.
        """
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
        """
        Filtra y muestra en la tabla de préstamos los libros que
        corresponden al género seleccionado en el Combobox.
        - Si se selecciona "Todos" no filtra y muestra todos los libros.
        - Para cada libro calcula las copias disponibles en tiempo real:
            copias_disponibles = copias_totales - préstamos_activos
          donde préstamos_activos = registros en self.prestamos con
          estado=='activo' y el mismo código de libro.
        Esto permite ver cuántas copias quedan disponibles para prestar.
        """

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
        """
        Registra un nuevo préstamo del libro seleccionado en la tabla.
        Pasos:
          1. Verifica que haya una fila seleccionada.
          2. Lee las copias disponibles de la tabla (columna índice 4).
          3. Si copias_disp <= 0 muestra error (no se puede prestar).
          4. Agrega un nuevo diccionario a self.prestamos con estado
             'activo' para ese libro.
          5. Persiste y actualiza la tabla para reflejar la nueva
             disponibilidad.
        """
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
        """
        Registra la devolución de una copia del libro seleccionado.
        Pasos:
          1. Verifica que haya una fila seleccionada.
          2. Usa next() con una expresión generadora para encontrar el
             PRIMER préstamo activo de ese libro en self.prestamos.
             (next devuelve None si no encuentra ninguno.)
          3. Si no hay préstamo activo muestra un aviso informativo.
          4. Cambia el estado del préstamo encontrado a 'devuelto'
             (modificación in-place del diccionario dentro de la lista).
          5. Persiste y actualiza la tabla.
        """
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
        """
        Recalcula y muestra el resumen de préstamos agrupado por género.
        Pasos:
          1. Borra las filas actuales de la tabla consolidado.
          2. Obtiene la lista de géneros únicos presentes en self.libros
             usando set() y los ordena alfabéticamente con sorted().
          3. Por cada género:
             a. Obtiene el conjunto de códigos de libros de ese género.
             b. Filtra self.prestamos para quedarse solo con los que
                pertenecen a esos códigos.
             c. Cuenta total, activos y devueltos con sum() y expresiones
                generadoras (patrón eficiente en Python).
          4. Inserta una fila por género en la tabla.
          5. Actualiza la etiqueta con el total general acumulado.
        """
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
