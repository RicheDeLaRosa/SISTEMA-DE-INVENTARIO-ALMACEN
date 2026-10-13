import tkinter as tk
from tkinter import ttk

from ui_comun import (
    COLOR_FONDO,
    COLOR_LINEA,
    COLOR_MARCA,
    COLOR_ROJO,
    COLOR_SECUNDARIO,
    COLOR_SUPERFICIE,
    COLOR_TINTA,
    COLOR_VERDE,
    FUENTE,
    configurar_ventana,
    crear_boton,
)


def abrir(parent, productos):
    ventana = tk.Toplevel(parent)
    configurar_ventana(ventana, parent, "Buscar producto", "960x600")
    ventana.minsize(740, 460)

    contenido = tk.Frame(ventana, bg=COLOR_FONDO, padx=24, pady=20)
    contenido.pack(fill="both", expand=True)
    tk.Label(
        contenido,
        text="Buscar producto",
        bg=COLOR_FONDO,
        fg=COLOR_TINTA,
        font=(FUENTE, 20, "bold")
    ).pack(anchor="w")
    tk.Label(
        contenido,
        text="Encuentra artículos por ID o nombre",
        bg=COLOR_FONDO,
        fg=COLOR_SECUNDARIO,
        font=(FUENTE, 10)
    ).pack(anchor="w", pady=(3, 16))

    barra_busqueda = tk.Frame(contenido, bg=COLOR_FONDO)
    barra_busqueda.pack(fill="x", pady=(0, 14))
    entrada = tk.Entry(barra_busqueda, font=(FUENTE, 11), width=42)
    entrada.pack(side="left", ipady=7)
    entrada.insert(0, "ID o nombre del producto")
    entrada.config(fg=COLOR_SECUNDARIO)

    estado_vacio = tk.Label(
        contenido,
        text="",
        bg=COLOR_SUPERFICIE,
        fg=COLOR_SECUNDARIO,
        font=(FUENTE, 11),
        pady=18
    )
    estilo = ttk.Style(ventana)
    estilo.configure(
        "Busqueda.Treeview",
        rowheight=34,
        font=(FUENTE, 10),
        background=COLOR_SUPERFICIE,
        fieldbackground=COLOR_SUPERFICIE
    )
    estilo.configure("Busqueda.Treeview.Heading", font=(FUENTE, 9, "bold"), padding=(8, 9))
    estilo.map(
        "Busqueda.Treeview",
        background=[("selected", COLOR_VERDE)],
        foreground=[("selected", COLOR_SUPERFICIE)]
    )

    columnas = ("id", "nombre", "categoria", "precio", "stock", "ubicacion")
    encabezados = {
        "id": "ID",
        "nombre": "Nombre",
        "categoria": "Categoría",
        "precio": "Precio",
        "stock": "Existencias",
        "ubicacion": "Ubicación"
    }
    marco_tabla = tk.Frame(contenido, bg=COLOR_SUPERFICIE, highlightbackground=COLOR_LINEA, highlightthickness=1)
    marco_tabla.pack(fill="both", expand=True)
    tabla = ttk.Treeview(marco_tabla, columns=columnas, show="headings", style="Busqueda.Treeview")
    anchos = {"id": 90, "nombre": 190, "categoria": 150, "precio": 100, "stock": 105, "ubicacion": 150}
    for columna in columnas:
        tabla.heading(columna, text=encabezados[columna], anchor="w")
        tabla.column(columna, width=anchos[columna], minwidth=70, anchor="w", stretch=True)
    tabla.tag_configure("sin_stock", foreground=COLOR_ROJO)
    tabla.tag_configure("fila_par", background="#F4F8FA")

    tabla.pack(side="left", fill="both", expand=True)
    barra_vertical = ttk.Scrollbar(marco_tabla, orient="vertical", command=tabla.yview)
    barra_vertical.pack(side="right", fill="y")
    barra_horizontal = ttk.Scrollbar(contenido, orient="horizontal", command=tabla.xview)
    barra_horizontal.pack(fill="x")
    tabla.configure(yscrollcommand=barra_vertical.set, xscrollcommand=barra_horizontal.set)

    estado = tk.Label(contenido, bg=COLOR_FONDO, fg=COLOR_SECUNDARIO, font=(FUENTE, 9))
    estado.pack(anchor="w", pady=(9, 0))

    def buscar():
        consulta = entrada.get().strip()
        if consulta == "ID o nombre del producto":
            consulta = ""
        consulta = consulta.casefold()
        coincidencias = [
            producto for producto in productos
            if not consulta or consulta in producto["id"].casefold() or consulta in producto["nombre"].casefold()
        ]
        tabla.delete(*tabla.get_children())
        for indice, producto in enumerate(coincidencias):
            etiquetas = []
            if producto["stock"] == 0:
                etiquetas.append("sin_stock")
            if indice % 2:
                etiquetas.append("fila_par")
            tabla.insert("", "end", values=tuple(producto[columna] for columna in columnas), tags=etiquetas)

        if not coincidencias:
            estado_vacio.config(text="No se encontraron productos." if productos else "Aún no hay productos registrados.")
            estado_vacio.pack(fill="x", before=marco_tabla)
        else:
            estado_vacio.pack_forget()
        estado.config(text=f"{len(coincidencias)} productos encontrados")

    def limpiar_busqueda():
        entrada.delete(0, tk.END)
        entrada.config(fg=COLOR_TINTA)
        buscar()
        entrada.focus_set()

    entrada.bind(
        "<FocusIn>",
        lambda event: (entrada.delete(0, tk.END), entrada.config(fg=COLOR_TINTA))
        if entrada.get() == "ID o nombre del producto" else None
    )
    entrada.bind("<KeyRelease>", lambda event: buscar())
    entrada.bind("<Return>", lambda event: buscar())
    entrada.bind("<Escape>", lambda event: limpiar_busqueda())
    crear_boton(barra_busqueda, "Buscar", buscar, COLOR_MARCA).pack(side="left", padx=(8, 0))
    crear_boton(
        barra_busqueda,
        "Limpiar",
        limpiar_busqueda,
        COLOR_SUPERFICIE,
        texto_color=COLOR_SECUNDARIO
    ).pack(side="left", padx=(6, 0))

    entrada.bind("<FocusOut>", lambda event: entrada.insert(0, "ID o nombre del producto") if not entrada.get().strip() else None)
    buscar()
    entrada.focus_set()