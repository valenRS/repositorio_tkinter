# ============================================================
# MÓDULO 07 — OOP CON TKINTER (⭐ MUY IMPORTANTE PARA EXAMEN)
# ============================================================
# En muchos exámenes de la universidad piden que la interfaz
# esté implementada con Programación Orientada a Objetos (POO).
#
# La estructura base es:
#   class NombreApp(tk.Tk):    ← hereda de tk.Tk
#       def __init__(self):
#           super().__init__() ← inicializa la ventana
#           # aquí configuras la ventana y creas los widgets
#
# SIN esta estructura, en algunos parciales te califican sobre 3.0/5.0
#
# Para ejecutar: python3 clase_ventana.py
# ============================================================

import tkinter as tk
from tkinter import messagebox


# ============================================================
# LA CLASE PRINCIPAL — Hereda de tk.Tk
# ============================================================
# Al heredar de tk.Tk, tu clase ES la ventana.
# self = la ventana misma.

class AplicacionEjemplo(tk.Tk):

    def __init__(self):
        # super().__init__() inicializa tk.Tk (la ventana)
        # SIEMPRE debe ser la primera línea de __init__
        super().__init__()

        # Configurar la ventana (igual que antes, pero con self en vez de ventana)
        self.title("Módulo 07 — OOP con Tkinter")
        self.geometry("450x380")
        self.configure(bg="white")
        self.resizable(False, False)

        # Lista interna para guardar nombres (estado de la aplicación)
        self.nombres = []

        # Llamar al método que crea todos los widgets
        self._crear_widgets()

    # ──────────────────────────────────────────────────────
    # Es buena práctica crear los widgets en un método aparte.
    # El prefijo _ indica que es un método "privado" (solo para uso interno).
    # ──────────────────────────────────────────────────────
    def _crear_widgets(self):
        # --- Título ---
        tk.Label(self, text="Agenda de Nombres", font=("Arial", 16, "bold"),
                 bg="white", fg="navy").pack(pady=15)

        # --- Frame del formulario ---
        # Frame es un contenedor invisible que ayuda a organizar widgets
        frame_form = tk.Frame(self, bg="white")
        frame_form.pack(padx=20, fill="x")

        tk.Label(frame_form, text="Nombre:", bg="white",
                 font=("Arial", 11)).grid(row=0, column=0, sticky="w", pady=5)

        # self.entrada_nombre → al guardarla en self, podemos usarla en otros métodos
        self.entrada_nombre = tk.Entry(frame_form, width=25, font=("Arial", 11))
        self.entrada_nombre.grid(row=0, column=1, padx=10, pady=5)
        # Vincular la tecla Enter al método agregar
        self.entrada_nombre.bind("<Return>", lambda e: self._agregar_nombre())

        # --- Botones ---
        frame_botones = tk.Frame(self, bg="white")
        frame_botones.pack(pady=10)

        tk.Button(frame_botones, text="Agregar", command=self._agregar_nombre,
                  bg="lightgreen", width=12, font=("Arial", 11)).pack(side="left", padx=5)

        tk.Button(frame_botones, text="Eliminar", command=self._eliminar_nombre,
                  bg="#ffcccc", width=12, font=("Arial", 11)).pack(side="left", padx=5)

        tk.Button(frame_botones, text="Limpiar todo", command=self._limpiar_todo,
                  bg="lightgray", width=12, font=("Arial", 11)).pack(side="left", padx=5)

        # --- Lista ---
        tk.Label(self, text="Nombres registrados:", bg="white",
                 font=("Arial", 11)).pack(anchor="w", padx=20)

        frame_lista = tk.Frame(self, bg="white")
        frame_lista.pack(padx=20, fill="both", expand=True)

        self.listbox = tk.Listbox(frame_lista, font=("Arial", 11), height=8)
        self.listbox.pack(side="left", fill="both", expand=True)

        scrollbar = tk.Scrollbar(frame_lista, command=self.listbox.yview)
        scrollbar.pack(side="right", fill="y")
        self.listbox.config(yscrollcommand=scrollbar.set)

        # --- Etiqueta de estado ---
        self.etiqueta_estado = tk.Label(self, text="", bg="white",
                                         font=("Arial", 10), fg="green")
        self.etiqueta_estado.pack(pady=5)

    # ──────────────────────────────────────────────────────
    # MÉTODOS de la aplicación (la lógica del negocio)
    # ──────────────────────────────────────────────────────

    def _agregar_nombre(self):
        """Agrega el nombre del campo de texto a la lista."""
        nombre = self.entrada_nombre.get().strip()

        if not nombre:
            self.etiqueta_estado.config(text="⚠ Escribe un nombre primero.", fg="red")
            return

        if nombre in self.nombres:
            self.etiqueta_estado.config(text=f"⚠ '{nombre}' ya está en la lista.", fg="orange")
            return

        # Agregar a la lista interna
        self.nombres.append(nombre)

        # Agregar al Listbox
        self.listbox.insert(tk.END, nombre)

        # Limpiar el campo de texto
        self.entrada_nombre.delete(0, tk.END)

        self.etiqueta_estado.config(text=f"✓ '{nombre}' agregado.", fg="green")

    def _eliminar_nombre(self):
        """Elimina el nombre seleccionado en el Listbox."""
        seleccion = self.listbox.curselection()

        if not seleccion:
            self.etiqueta_estado.config(text="⚠ Selecciona un nombre de la lista.", fg="red")
            return

        indice = seleccion[0]
        nombre = self.listbox.get(indice)

        confirmado = messagebox.askyesno("Confirmar", f"¿Eliminar '{nombre}'?")
        if confirmado:
            self.listbox.delete(indice)
            self.nombres.remove(nombre)
            self.etiqueta_estado.config(text=f"✓ '{nombre}' eliminado.", fg="green")

    def _limpiar_todo(self):
        """Limpia toda la lista después de confirmar."""
        if not self.nombres:
            self.etiqueta_estado.config(text="La lista ya está vacía.", fg="gray")
            return

        confirmado = messagebox.askyesno("Confirmar", "¿Limpiar toda la lista?")
        if confirmado:
            self.listbox.delete(0, tk.END)
            self.nombres.clear()
            self.etiqueta_estado.config(text="✓ Lista limpiada.", fg="green")


# ============================================================
# PUNTO DE ENTRADA (la "cabecera" que piden en exámenes)
# ============================================================
# if __name__ == "__main__": significa:
#   "Ejecuta este código solo si estoy corriendo este archivo directamente"
#   (no si alguien me importa como módulo)

if __name__ == "__main__":
    app = AplicacionEjemplo()  # crear la instancia de la app (= crear la ventana)
    app.mainloop()             # mantener la ventana abierta
