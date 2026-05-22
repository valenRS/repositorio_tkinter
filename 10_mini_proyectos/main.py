# ============================================================
# PUNTO DE ENTRADA — main.py
# ============================================================
# Este es el único archivo que se ejecuta directamente:
#   python3 main.py
#
# Su única responsabilidad es importar la clase principal,
# crear la instancia y arrancar el loop de eventos de Tkinter.
# No contiene lógica de negocio ni de interfaz gráfica.
# ============================================================

from sistema_biblioteca import SistemaBiblioteca

if __name__ == "__main__":
    app = SistemaBiblioteca()
    app.mainloop()
