import tkinter as tk
from tkinter import ttk

from ui_comun import COLOR_FONDO, COLOR_VERDE, COLOR_SECUNDARIO, COLOR_TINTA, FUENTE, configurar_ventana


def abrir(parent, productos, productos_filtrados=None, titulo="Inventario"):
    lista_productos = productos if productos_filtrados is None else productos_filtrados
    ventana = tk.Toplevel(parent)
    configurar_ventana(ventana, parent, titulo, "820x440")
    ventana.minsize(680, 340)

    contenedor = tk.Frame(ventana, bg=COLOR_FONDO, padx=24, pady=22)
    contenedor.pack(fill="both", expand=True)
    tk.Label(
        contenedor,
        text=titulo,
        bg=COLOR_FONDO,
        fg=COLOR_TINTA,
        font=(FUENTE, 18, "bold")
    ).pack(anchor="w", pady=(0, 14))
    if not lista_productos:
        tk.Label(
            contenedor,
            text="El inventario está vacío." if productos_filtrados is None else "No se encontraron productos.",
            bg=COLOR_FONDO,
            fg=COLOR_SECUNDARIO,
            font=(FUENTE, 10)
        ).pack(anchor="w", pady=(0, 12))

    estilo = ttk.Style(ventana)
    estilo.configure("Inventario.Treeview", rowheight=30, font=(FUENTE, 10))
    estilo.configure("Inventario.Treeview.Heading", font=(FUENTE, 9, "bold"))
    estilo.map("Inventario.Treeview", background=[("selected", COLOR_VERDE)])

    columnas = ("id", "nombre", "categoria", "precio", "stock", "ubicacion")
    tabla = ttk.Treeview(contenedor, columns=columnas, show="headings", style="Inventario.Treeview")
    encabezados = {
        "id": "ID",
        "nombre": "Nombre",
        "categoria": "Categoría",
        "precio": "Precio",
        "stock": "Stock",
        "ubicacion": "Ubicación"
    }
    anchos = {"id": 80, "nombre": 170, "categoria": 130, "precio": 90, "stock": 80, "ubicacion": 130}
    for columna in columnas:
        tabla.heading(columna, text=encabezados[columna])
        tabla.column(columna, width=anchos[columna], minwidth=60, anchor="w")
    tabla.column("precio", anchor="e")
    tabla.column("stock", anchor="center")

    barra = ttk.Scrollbar(contenedor, orient="vertical", command=tabla.yview)
    tabla.configure(yscrollcommand=barra.set)
    tabla.pack(side="left", fill="both", expand=True)
    barra.pack(side="right", fill="y")

    for producto in lista_productos:
        tabla.insert("", "end", values=tuple(producto[columna] for columna in columnas))