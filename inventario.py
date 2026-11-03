import tkinter as tk
from tkinter import ttk

from base_datos import filtrar_productos, producto_requiere_reposicion
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
    """Muestra existencias, indicadores y herramientas de filtro y ordenamiento."""
    productos_disponibles = productos if productos_filtrados is None else productos_filtrados
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
    fila_busqueda = tk.Frame(barra_herramientas, bg=COLOR_FONDO)
    fila_busqueda.pack(fill="x", pady=(0, 8))
    tk.Label(
        fila_busqueda,
        text="BUSCAR",
        bg=COLOR_FONDO,
        fg=COLOR_TINTA,
        font=(FUENTE, 9, "bold")
    ).pack(side="left", padx=(0, 10))
    entrada_filtro = tk.Entry(fila_busqueda, font=(FUENTE, 10))
    entrada_filtro.pack(side="left", fill="x", expand=True, ipady=6)
    entrada_filtro.insert(0, "ID, nombre, categoría, ubicación o stock")
    entrada_filtro.config(fg=COLOR_SECUNDARIO)

    fila_filtros = tk.Frame(barra_herramientas, bg=COLOR_FONDO)
    fila_filtros.pack(fill="x")
    categorias = sorted(
        {producto["categoria"] for producto in productos_disponibles if producto["categoria"]},
        key=str.casefold,
    )
    ubicaciones = sorted(
        {producto["ubicacion"] for producto in productos_disponibles if producto["ubicacion"]},
        key=str.casefold,
    )

    def crear_filtro(etiqueta, valores, ancho):
        tk.Label(
            fila_filtros,
            text=etiqueta,
            bg=COLOR_FONDO,
            fg=COLOR_TINTA,
            font=(FUENTE, 8, "bold"),
        ).pack(side="left", padx=(0, 5))
        selector = ttk.Combobox(
            fila_filtros,
            state="readonly",
            values=valores,
            width=ancho,
            font=(FUENTE, 9),
        )
        selector.current(0)
        selector.pack(side="left", padx=(0, 12), ipady=3)
        return selector

    filtro_categoria = crear_filtro("CATEGORÍA", ["Todas"] + categorias, 16)
    filtro_ubicacion = crear_filtro("UBICACIÓN", ["Todas"] + ubicaciones, 14)
    filtro_stock = crear_filtro(
        "STOCK",
        ["Todos", "Agotado", "Por reponer", "Existencias suficientes"],
        23,
    )

    estilo = ttk.Style(ventana)
    estilo.configure("Inventario.Treeview", rowheight=34, font=(FUENTE, 10), background=COLOR_SUPERFICIE, fieldbackground=COLOR_SUPERFICIE)
    estilo.configure("Inventario.Treeview.Heading", font=(FUENTE, 9, "bold"), padding=(8, 9))
    estilo.map("Inventario.Treeview", background=[("selected", COLOR_VERDE)], foreground=[("selected", COLOR_SUPERFICIE)])

    columnas = ("id", "nombre", "categoria", "precio", "stock", "stock_minimo", "ubicacion")
    encabezados = {
        "id": "ID",
        "nombre": "Nombre",
        "categoria": "Categoría",
        "precio": "Precio",
        "stock": "Existencias",
        "stock_minimo": "Mínimo",
        "ubicacion": "Ubicación"
    }
    alineaciones = {columna: "w" for columna in columnas}
    marco_tabla = tk.Frame(contenedor, bg=COLOR_SUPERFICIE, highlightbackground=COLOR_LINEA, highlightthickness=1)
    marco_tabla.pack(fill="both", expand=True)
    tabla = ttk.Treeview(marco_tabla, columns=columnas, show="headings", style="Inventario.Treeview")
    anchos = {
        "id": 90,
        "nombre": 190,
        "categoria": 150,
        "precio": 100,
        "stock": 105,
        "stock_minimo": 90,
        "ubicacion": 150,
    }
    orden = {columna: False for columna in columnas}

    def ordenar(columna):
        # Alterna ascendente/descendente y trata los valores numéricos como números.
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
    tabla.tag_configure("stock_bajo", foreground="#A9682B")
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
        # Vuelve a calcular filas e indicadores usando el filtro activo.
        lista_productos = list(productos_disponibles)
        consulta = entrada_filtro.get().strip()
        if consulta == "ID, nombre, categoría, ubicación o stock":
            consulta = ""
        categoria = filtro_categoria.get()
        ubicacion = filtro_ubicacion.get()
        filas = filtrar_productos(
            lista_productos,
            consulta=consulta,
            categoria="" if categoria == "Todas" else categoria,
            ubicacion="" if ubicacion == "Todas" else ubicacion,
            nivel_stock=filtro_stock.get(),
        )
        tabla.delete(*tabla.get_children())
        for indice, producto in enumerate(filas):
            etiquetas = []
            if producto["stock"] <= 0:
                etiquetas.append("sin_stock")
            elif producto_requiere_reposicion(producto):
                etiquetas.append("stock_bajo")
            if indice % 2:
                etiquetas.append("fila_par")
            tabla.insert("", "end", values=tuple(producto[columna] for columna in columnas), tags=etiquetas)

        valor_productos.config(text=str(len(lista_productos)))
        valor_unidades.config(text=str(sum(producto["stock"] for producto in lista_productos)))
        if not filas:
            if titulo == "Productos por reponer":
                mensaje_vacio = (
                    "No hay productos por reponer."
                    if not lista_productos
                    else "No hay coincidencias con ese filtro."
                )
            else:
                mensaje_vacio = (
                    "El inventario está vacío."
                    if not lista_productos
                    else "No hay coincidencias con ese filtro."
                )
            estado_vacio.config(text=mensaje_vacio)
            estado_vacio.pack(fill="x", before=marco_tabla)
        else:
            estado_vacio.pack_forget()
        estado.config(
            text=(
                f"Mostrando {len(filas)} de {len(lista_productos)} productos  ·  "
                "En rojo: sin existencias  ·  En ámbar: stock bajo el mínimo"
            )
        )

    def limpiar_filtro():
        # Quita el texto de búsqueda y reconstruye la vista sin restricciones.
        entrada_filtro.delete(0, tk.END)
        entrada_filtro.insert(0, "ID, nombre, categoría, ubicación o stock")
        entrada_filtro.config(fg=COLOR_SECUNDARIO)
        filtro_categoria.current(0)
        filtro_ubicacion.current(0)
        filtro_stock.current(0)
        refrescar_tabla()
        entrada_filtro.focus_set()

    entrada_filtro.bind("<FocusIn>", lambda event: entrada_filtro.delete(0, tk.END) if entrada_filtro.get() == "ID, nombre, categoría, ubicación o stock" else None)
    entrada_filtro.bind("<FocusIn>", lambda event: entrada_filtro.config(fg=COLOR_TINTA), add="+")
    entrada_filtro.bind("<FocusOut>", lambda event: entrada_filtro.insert(0, "ID, nombre, categoría, ubicación o stock") if not entrada_filtro.get().strip() else None)
    entrada_filtro.bind("<FocusOut>", lambda event: entrada_filtro.config(fg=COLOR_SECUNDARIO) if entrada_filtro.get() == "ID, nombre, categoría, ubicación o stock" else None, add="+")
    entrada_filtro.bind("<KeyRelease>", refrescar_tabla)
    entrada_filtro.bind("<Return>", refrescar_tabla)
    entrada_filtro.bind("<Escape>", lambda event: limpiar_filtro())
    filtro_categoria.bind("<<ComboboxSelected>>", refrescar_tabla)
    filtro_ubicacion.bind("<<ComboboxSelected>>", refrescar_tabla)
    filtro_stock.bind("<<ComboboxSelected>>", refrescar_tabla)

    boton_limpiar = tk.Button(
        barra_herramientas,
        text="Limpiar filtros",
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