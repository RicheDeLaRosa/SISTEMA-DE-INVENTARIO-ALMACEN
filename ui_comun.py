import tkinter as tk

# Paleta y tipografía compartidas para mantener una apariencia uniforme.
COLOR_FONDO = "#E6EEF2"
COLOR_SUPERFICIE = "#FFFFFF"
COLOR_TINTA = "#263E49"
COLOR_SECUNDARIO = "#718A94"
COLOR_VERDE = "#19766F"
COLOR_VERDE_HOVER = "#125F59"
COLOR_AMBAR = "#A9682B"
COLOR_AMBAR_HOVER = "#875321"
COLOR_ROJO = "#A8443F"
COLOR_LINEA = "#C9D7DD"
COLOR_MARCA = "#1679A5"
FUENTE = "Segoe UI"


def configurar_ventana(ventana, parent, titulo, geometria):
    """Aplica las opciones comunes a una ventana principal o secundaria."""
    ventana.title(titulo)
    ventana.geometry(geometria)
    ventana.configure(bg=COLOR_FONDO)
    if parent is not None:
        ventana.transient(parent)


def crear_boton(parent, texto, comando, fondo, texto_color=COLOR_SUPERFICIE, fondo_activo=None):
    """Crea un botón plano con colores y espaciado consistentes en toda la app."""
    return tk.Button(
        parent,
        command=comando,
        text=texto,
        font=(FUENTE, 10, "bold"),
        bg=fondo,
        fg=texto_color,
        activebackground=fondo_activo or fondo,
        activeforeground=texto_color,
        relief="flat",
        borderwidth=0,
        highlightthickness=0,
        cursor="hand2",
        padx=14,
        pady=12,
        height=1
    )