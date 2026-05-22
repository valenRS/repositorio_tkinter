# ============================================================
# MINI PROYECTO — CALCULADORA
# ============================================================
# Calculadora básica con operaciones: + - * /
#  ✓ Layout con grid()
#  ✓ Botones numéricos y de operación
#  ✓ Manejo de errores (división por cero, etc.)
#  ✓ Estructura OOP
#
# Para ejecutar: python3 calculadora.py
# ============================================================

import tkinter as tk
from tkinter import messagebox


class Calculadora(tk.Tk):

    def __init__(self):
        super().__init__()
        self.title("Calculadora")
        self.geometry("320x450")
        self.configure(bg="#1e1e2e")
        self.resizable(False, False)

        # Variable que guarda la expresión actual
        self.expresion = ""
        self.var_display = tk.StringVar(value="0")

        self._construir_ui()

    def _construir_ui(self):
        # ── Display ─────────────────────────────────────────
        display = tk.Entry(
            self,
            textvariable=self.var_display,
            font=("Courier", 24, "bold"),
            justify="right",
            state="readonly",       # el usuario no puede escribir directo, solo con botones
            bg="#2d2d44",
            fg="white",
            relief="flat",
            bd=10
        )
        display.pack(fill="x", padx=10, pady=(15, 5))

        # ── Botones ─────────────────────────────────────────
        # Definir los botones en filas (igual que una calculadora física)
        # (texto_botón, color_fondo, color_texto)
        botones = [
            [("C", "#e74c3c", "white"), ("±", "#555", "white"),
             ("%", "#555", "white"),  ("÷", "#f39c12", "white")],
            [("7", "#2d2d44", "white"), ("8", "#2d2d44", "white"),
             ("9", "#2d2d44", "white"), ("×", "#f39c12", "white")],
            [("4", "#2d2d44", "white"), ("5", "#2d2d44", "white"),
             ("6", "#2d2d44", "white"), ("−", "#f39c12", "white")],
            [("1", "#2d2d44", "white"), ("2", "#2d2d44", "white"),
             ("3", "#2d2d44", "white"), ("+", "#f39c12", "white")],
            [("0", "#2d2d44", "white"), (".", "#2d2d44", "white"),
             ("⌫", "#555", "white"),   ("=", "#4CAF50", "white")],
        ]

        frame_botones = tk.Frame(self, bg="#1e1e2e")
        frame_botones.pack(padx=10, pady=5, fill="both", expand=True)

        for fila_idx, fila in enumerate(botones):
            for col_idx, (texto, bg, fg) in enumerate(fila):
                btn = tk.Button(
                    frame_botones,
                    text=texto,
                    font=("Arial", 16, "bold"),
                    bg=bg, fg=fg,
                    relief="flat",
                    activebackground="#444",
                    activeforeground="white",
                    # lambda con default arg para capturar el valor actual de 'texto'
                    command=lambda t=texto: self._presionar(t)
                )
                btn.grid(
                    row=fila_idx, column=col_idx,
                    padx=4, pady=4,
                    sticky="nsew",    # el botón se estira para llenar su celda
                    ipadx=5, ipady=8
                )

        # Hacer que todas las celdas del grid se expandan igual
        for i in range(4):
            frame_botones.columnconfigure(i, weight=1)
        for i in range(5):
            frame_botones.rowconfigure(i, weight=1)

    def _presionar(self, tecla):
        """Se llama cuando el usuario presiona cualquier botón."""

        if tecla == "C":
            # Limpiar todo
            self.expresion = ""
            self.var_display.set("0")

        elif tecla == "=":
            # Calcular el resultado
            self._calcular()

        elif tecla == "⌫":
            # Borrar el último carácter
            self.expresion = self.expresion[:-1]
            self.var_display.set(self.expresion if self.expresion else "0")

        elif tecla == "±":
            # Cambiar el signo del número actual
            try:
                valor = float(self.expresion)
                self.expresion = str(-valor)
                self.var_display.set(self.expresion)
            except ValueError:
                pass

        elif tecla == "%":
            # Convertir a porcentaje
            try:
                valor = float(self.expresion)
                self.expresion = str(valor / 100)
                self.var_display.set(self.expresion)
            except ValueError:
                pass

        else:
            # Número, punto o operador: agregar a la expresión
            # Reemplazar los símbolos visuales por los de Python
            tecla_python = tecla.replace("÷", "/").replace("×", "*").replace("−", "-")
            self.expresion += tecla_python
            self.var_display.set(self.expresion)

    def _calcular(self):
        """Evalúa la expresión matemática y muestra el resultado."""
        if not self.expresion:
            return
        try:
            # eval() calcula la expresión matemática como texto
            resultado = eval(self.expresion)

            # Si el resultado es entero, no mostrar decimales innecesarios
            if resultado == int(resultado):
                resultado = int(resultado)

            self.expresion = str(resultado)
            self.var_display.set(self.expresion)

        except ZeroDivisionError:
            messagebox.showerror("Error", "No se puede dividir entre cero.")
            self.expresion = ""
            self.var_display.set("0")

        except Exception:
            messagebox.showerror("Error", "Expresión inválida.")
            self.expresion = ""
            self.var_display.set("0")


if __name__ == "__main__":
    app = Calculadora()
    app.mainloop()
