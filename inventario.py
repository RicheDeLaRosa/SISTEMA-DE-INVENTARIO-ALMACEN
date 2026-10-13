import tkinter as tk
from tkinter import ttk

from ui_comun import (
    COLOR_FONDO,
    COLOR_LINEA,
    COLOR_ROJO,
    COLOR_SECUNDARIO,
    COLOR_SUPERFICIE,
    COLOR_TINTA,
    COLOR_VERDE,
    FUENTE,
    configurar_ventana,
    crear_boton,
)


def abrir(parent, productos, productos_filtrados=None, titulo="Inventario"):
    ventana = tk.Toplevel(parent)
    configurar_ventana(ventana, parent, titulo, "1040x620")
    ventana.minsize(760, 500)

    contenedor = tk.Frame(ventana, bg=COLOR_FONDO, padx=24, pady=20)
    contenedor.pack(fill="both", expand=True)

    cabecera = tk.Frame(contenedor, bg=COLOR_FONDO)
    cabecera.pack(fill="x", pady=(0, 18))
    bloque_titulo = tk.Frame(cabecera, bg=COLOR_FONDO)
    bloque_titulo.pack(side="left", anchor="w")
    tk.Label(
        bloque_titulo,
        text=titulo,
        bg=COLOR_FONDO,
        fg=COLOR_TINTA,
        font=(FUENTE, 20, "bold")
    ).pack(anchor="w")
    tk.Label(
        bloque_titulo,
        text="Consulta y organiza las existencias del almacén",
        bg=COLOR_FONDO,
        fg=COLOR_SECUNDARIO,
        font=(FUENTE, 10)
    ).pack(anchor="w", pady=(3, 0))

    resumen = tk.Frame(cabecera, bg=COLOR_FONDO)
    resumen.pack(side="right", anchor="e")
    indicador_productos = tk.Frame(resumen, bg=COLOR_SUPERFICIE, padx=14, pady=8)
    indicador_productos.pack(side="left", padx=(0, 8))
    tk.Label(indicador_productos, text="PRODUCTOS", bg=COLOR_SUPERFICIE, fg=COLOR_SECUNDARIO, font=(FUENTE, 8, "bold")).pack(anchor="e")
    valor_productos = tk.Label(indicador_productos, bg=COLOR_SUPERFICIE, fg=COLOR_TINTA, font=(FUENTE, 16, "bold"))
    valor_productos.pack(anchor="e")
    indicador_unidades = tk.Frame(resumen, bg=COLOR_SUPERFICIE, padx=14, pady=8)
    indicador_unidades.pack(side="left")
    tk.Label(indicador_unidades, text="UNIDADES", bg=COLOR_SUPERFICIE, fg=COLOR_SECUNDARIO, font=(FUENTE, 8, "bold")).pack(anchor="e")
    valor_unidades = tk.Label(indicador_unidades, bg=COLOR_SUPERFICIE, fg=COLOR_TINTA, font=(FUENTE, 16, "bold"))
    valor_unidades.pack(anchor="e")

    barra_herramientas = tk.Frame(contenedor, bg=COLOR_FONDO)
    barra_herramientas.pack(fill="x", pady=(0, 12))
    tk.Label(
        barra_herramientas,
        text="FILTRAR",
        bg=COLOR_FONDO,
        fg=COLOR_TINTA,
        font=(FUENTE, 9, "bold")
    ).pack(side="left", padx=(0, 10))
    entrada_filtro = tk.Entry(barra_herramientas, font=(FUENTE, 10), width=38)
    entrada_filtro.pack(side="left", ipady=6)
    entrada_filtro.insert(0, "ID, nombre, categoría o ubicación")
    entrada_filtro.config(fg=COLOR_SECUNDARIO)

    estilo = ttk.Style(ventana)
    estilo.configure("Inventario.Treeview", rowheight=34, font=(FUENTE, 10), background=COLOR_SUPERFICIE, fieldbackground=COLOR_SUPERFICIE)
    estilo.configure("Inventario.Treeview.Heading", font=(FUENTE, 9, "bold"), padding=(8, 9))
    estilo.map("Inventario.Treeview", background=[("selected", COLOR_VERDE)], foreground=[("selected", COLOR_SUPERFICIE)])

    columnas = ("id", "nombre", "categoria", "precio", "stock", "ubicacion")
    encabezados = {
        "id": "ID",
        "nombre": "Nombre",
        "categoria": "Categoría",
        "precio": "Precio",
        "stock": "Existencias",
        "ubicacion": "Ubicación"
    }
    alineaciones = {columna: "w" for columna in columnas}
    marco_tabla = tk.Frame(contenedor, bg=COLOR_SUPERFICIE, highlightbackground=COLOR_LINEA, highlightthickness=1)
    marco_tabla.pack(fill="both", expand=True)
    tabla = ttk.Treeview(marco_tabla, columns=columnas, show="headings", style="Inventario.Treeview")
    anchos = {"id": 90, "nombre": 190, "categoria": 150, "precio": 100, "stock": 105, "ubicacion": 150}
    orden = {columna: False for columna in columnas}

    def ordenar(columna):
        items = [(tabla.set(item, columna), item) for item in tabla.get_children("")]
        try:
            items.sort(key=lambda elemento: float(elemento[0]), reverse=orden[columna])
        except ValueError:
            items.sort(key=lambda elemento: elemento[0].casefold(), reverse=orden[columna])
        for posicion, (_, item) in enumerate(items):
            tabla.move(item, "", posicion)
        orden[columna] = not orden[columna]

    for columna in columnas:
        tabla.heading(
            columna,
            text=encabezados[columna],
            anchor=alineaciones[columna],
            command=lambda clave=columna: ordenar(clave)
        )
        tabla.column(
            columna,
            width=anchos[columna],
            minwidth=70,
            anchor=alineaciones[columna],
            stretch=True
        )
    tabla.tag_configure("sin_stock", foreground=COLOR_ROJO)
    tabla.tag_configure("fila_par", background="#F4F8FA")

    estado_vacio = tk.Label(
        contenedor,
        text="",
        bg=COLOR_SUPERFICIE,
        fg=COLOR_SECUNDARIO,
        font=(FUENTE, 11),
        pady=18
    )
    tabla.pack(side="left", fill="both", expand=True)
    barra_vertical = ttk.Scrollbar(marco_tabla, orient="vertical", command=tabla.yview)
    barra_vertical.pack(side="right", fill="y")
    barra_horizontal = ttk.Scrollbar(contenedor, orient="horizontal", command=tabla.xview)
    barra_horizontal.pack(fill="x")
    tabla.configure(yscrollcommand=barra_vertical.set, xscrollcommand=barra_horizontal.set)

    estado = tk.Label(contenedor, bg=COLOR_FONDO, fg=COLOR_SECUNDARIO, font=(FUENTE, 9))
    estado.pack(anchor="w", pady=(9, 0))

    def refrescar_tabla(*args):
        lista_productos = list(productos if productos_filtrados is None else productos_filtrados)
        consulta = entrada_filtro.get().strip().casefold()
        if consulta == "id, nombre, categoría o ubicación":
            consulta = ""
        filas = [
            producto for producto in lista_productos
            if not consulta or any(consulta in str(producto[columna]).casefold() for columna in columnas)
        ]
        tabla.delete(*tabla.get_children())
        for indice, producto in enumerate(filas):
            etiquetas = []
            if producto["stock"] == 0:
                etiquetas.append("sin_stock")
            if indice % 2:
                etiquetas.append("fila_par")
            tabla.insert("", "end", values=tuple(producto[columna] for columna in columnas), tags=etiquetas)

        valor_productos.config(text=str(len(lista_productos)))
        valor_unidades.config(text=str(sum(producto["stock"] for producto in lista_productos)))
        if not filas:
            estado_vacio.config(text="El inventario está vacío." if not lista_productos else "No hay coincidencias con ese filtro.")
            estado_vacio.pack(fill="x", before=marco_tabla)
        else:
            estado_vacio.pack_forget()
        estado.config(text=f"Mostrando {len(filas)} de {len(lista_productos)} productos  ·  En rojo: sin existencias")

    def limpiar_filtro():
        entrada_filtro.delete(0, tk.END)
        entrada_filtro.config(fg=COLOR_TINTA)
        refrescar_tabla()
        entrada_filtro.focus_set()

    entrada_filtro.bind("<FocusIn>", lambda event: entrada_filtro.delete(0, tk.END) if entrada_filtro.get() == "ID, nombre, categoría o ubicación" else None)
    entrada_filtro.bind("<FocusIn>", lambda event: entrada_filtro.config(fg=COLOR_TINTA), add="+")
    entrada_filtro.bind("<FocusOut>", lambda event: entrada_filtro.insert(0, "ID, nombre, categoría o ubicación") if not entrada_filtro.get().strip() else None)
    entrada_filtro.bind("<FocusOut>", lambda event: entrada_filtro.config(fg=COLOR_SECUNDARIO) if entrada_filtro.get() == "ID, nombre, categoría o ubicación" else None, add="+")
    entrada_filtro.bind("<KeyRelease>", refrescar_tabla)
    entrada_filtro.bind("<Return>", refrescar_tabla)
    entrada_filtro.bind("<Escape>", lambda event: limpiar_filtro())

    boton_limpiar = tk.Button(
        barra_herramientas,
        text="Limpiar",
        command=limpiar_filtro,
        font=(FUENTE, 9, "bold"),
        bg=COLOR_FONDO,
        fg=COLOR_VERDE,
        relief="flat",
        cursor="hand2"
    )
    boton_limpiar.pack(side="left", padx=8)
    crear_boton(barra_herramientas, "Actualizar", refrescar_tabla, COLOR_VERDE).pack(side="right")
    ventana.bind("<FocusIn>", lambda event: refrescar_tabla() if event.widget is ventana else None)
    refrescar_tabla()