import tkinter as tk #Lo que hace esta linea es crear la interfaz grafica
from tkinter import messagebox
from tkinter import ttk

ventana = tk.Tk() #Lo que hace esta linea es crear nuestra ventana principal

COLOR_FONDO = "#E6EEF2"
COLOR_SUPERFICIE = "#FFFFFF"
COLOR_TINTA = "#263E49"
COLOR_SECUNDARIO = "#718A94"
COLOR_VERDE = "#19766F"
COLOR_VERDE_HOVER = "#125F59"
COLOR_AMBAR = "#A9682B"
COLOR_AMBAR_HOVER = "#875321"
COLOR_ROJO = "#A8443F"
COLOR_ROJO_SUAVE = "#F8E9E7"
COLOR_LINEA = "#C9D7DD"
COLOR_MARCA = "#1679A5"
FUENTE = "Segoe UI"

ventana.title("ALMACEN RICHIE") #Coloca el titulo en la ventana
ventana.geometry("940x700")
ventana.minsize(760, 620)
ventana.configure(bg=COLOR_FONDO)
ventana.option_add("*Font", f"{{{FUENTE}}} 10")
ventana.option_add("*Label.background", COLOR_FONDO)
ventana.option_add("*Label.foreground", COLOR_TINTA)
ventana.option_add("*Entry.background", COLOR_SUPERFICIE)
ventana.option_add("*Entry.foreground", COLOR_TINTA)
ventana.option_add("*Entry.insertBackground", COLOR_VERDE)
ventana.option_add("*Entry.relief", "flat")
ventana.option_add("*Entry.highlightThickness", 1)
ventana.option_add("*Entry.highlightBackground", COLOR_LINEA)
ventana.option_add("*Entry.highlightColor", COLOR_VERDE)
ventana.option_add("*Button.background", COLOR_SUPERFICIE)
ventana.option_add("*Button.foreground", COLOR_TINTA)
ventana.option_add("*Button.activeBackground", COLOR_FONDO)
ventana.option_add("*Button.activeForeground", COLOR_TINTA)
ventana.option_add("*Button.relief", "flat")
ventana.option_add("*Button.borderWidth", 0)

productos = []
conteo_productos = tk.StringVar(value="0")

def actualizar_conteo_productos():
    conteo_productos.set(str(len(productos)))

def configurar_ventana_secundaria(ventana_secundaria, titulo, geometria):
    ventana_secundaria.title(titulo)
    ventana_secundaria.geometry(geometria)
    ventana_secundaria.configure(bg=COLOR_FONDO)

def crear_boton(parent, texto, comando, fondo, texto_color=COLOR_SUPERFICIE, fondo_activo=None):
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

cabecera = tk.Frame(ventana, bg=COLOR_SUPERFICIE, padx=26, pady=16)
cabecera.pack(fill="x")

fila_marca = tk.Frame(cabecera, bg=COLOR_SUPERFICIE)
fila_marca.pack(fill="x")
marca = tk.Frame(fila_marca, bg=COLOR_MARCA, padx=13, pady=7)
marca.pack(side="left")
tk.Label(marca, text="ALMACÉN", bg=COLOR_MARCA, fg=COLOR_SUPERFICIE, font=(FUENTE, 8, "bold")).pack(anchor="w")
tk.Label(marca, text="RICHIE", bg=COLOR_MARCA, fg=COLOR_SUPERFICIE, font=(FUENTE, 17, "bold")).pack(anchor="w")
tk.Label(
    fila_marca,
    text="CONTROL DE INVENTARIO",
    bg=COLOR_SUPERFICIE,
    fg=COLOR_MARCA,
    font=(FUENTE, 10, "bold")
).pack(side="left", padx=16)

indicador = tk.Frame(fila_marca, bg=COLOR_SUPERFICIE, padx=8, pady=4)
indicador.pack(side="right")
tk.Label(indicador, text="PRODUCTOS", bg=COLOR_SUPERFICIE, fg=COLOR_SECUNDARIO, font=(FUENTE, 8, "bold")).pack(anchor="e")
tk.Label(indicador, textvariable=conteo_productos, bg=COLOR_SUPERFICIE, fg=COLOR_TINTA, font=(FUENTE, 20, "bold")).pack(anchor="e")

barra_busqueda = tk.Frame(ventana, bg=COLOR_SUPERFICIE, padx=26)
barra_busqueda.pack(fill="x", pady=(0, 0))
contenedor_busqueda = tk.Frame(barra_busqueda, bg=COLOR_SUPERFICIE)
contenedor_busqueda.pack(anchor="center", pady=(8, 18))
busqueda_entry = tk.Entry(contenedor_busqueda, width=42, font=(FUENTE, 11))
busqueda_entry.pack(side="left", ipady=7, padx=(0, 6))
busqueda_entry.insert(0, "Buscar por ID o nombre")
busqueda_entry.config(fg=COLOR_SECUNDARIO)

def enfocar_busqueda(event):
    if busqueda_entry.get() == "Buscar por ID o nombre":
        busqueda_entry.delete(0, tk.END)
        busqueda_entry.config(fg=COLOR_TINTA)

def restaurar_busqueda(event):
    if not busqueda_entry.get().strip():
        busqueda_entry.insert(0, "Buscar por ID o nombre")
        busqueda_entry.config(fg=COLOR_SECUNDARIO)

busqueda_entry.bind("<FocusIn>", enfocar_busqueda)
busqueda_entry.bind("<FocusOut>", restaurar_busqueda)
busqueda_entry.bind("<Return>", lambda event: buscar_desde_panel())
crear_boton(contenedor_busqueda, "Buscar", lambda: buscar_desde_panel(), COLOR_MARCA).pack(side="left")

contenido = tk.Frame(ventana, bg=COLOR_FONDO, padx=26, pady=22)
contenido.pack(fill="both", expand=True)
tk.Label(
    contenido,
    text="Módulos de inventario",
    bg=COLOR_FONDO,
    fg=COLOR_TINTA,
    font=(FUENTE, 18, "bold")
).pack(anchor="w", pady=(0, 12))
rejilla_modulos = tk.Frame(contenido, bg=COLOR_FONDO)
rejilla_modulos.pack(fill="both", expand=True)
for columna in range(4):
    rejilla_modulos.columnconfigure(columna, weight=1, uniform="modulos")
for fila in range(2):
    rejilla_modulos.rowconfigure(fila, weight=1, uniform="filas_modulos")

pie = tk.Frame(contenido, bg=COLOR_FONDO)
pie.pack(fill="x")
tk.Frame(pie, bg=COLOR_LINEA, height=1).pack(fill="x", pady=(12, 12))


def registrar(): #Lo que hacemos aqui es crear una funcion para que al momento de precioar el boton nos aparezca el mensaje de registrar
    ventana_registrar = tk.Toplevel() #Esta linea lo que hace es generar otra ventana al darle click en registrar producto
    configurar_ventana_secundaria(ventana_registrar, "Registrar producto", "440x520")
    ventana_registrar.minsize(400, 460)

    label_id = tk.Label(ventana_registrar, text="ID", font=(FUENTE, 11, "bold"))
    label_id.pack()
    label_id1 = tk.Entry(ventana_registrar)
    label_id1.pack()

    nombre = tk.Label(ventana_registrar, text="INGRESA EL NOMBRE", font=(FUENTE, 11, "bold"))
    nombre.pack()
    nombre1 = tk.Entry(ventana_registrar)
    nombre1.pack()

    categoria = tk.Label(ventana_registrar, text="INGRESA LA CATEGORIA", font=(FUENTE, 11, "bold"))
    categoria.pack()
    categoria1 = tk.Entry(ventana_registrar)
    categoria1.pack()

    precio = tk.Label(ventana_registrar, text="INGRESA EL PRECIO", font=(FUENTE, 11, "bold"))
    precio.pack()
    precio1 = tk.Entry(ventana_registrar)
    precio1.pack()

    stock = tk.Label(ventana_registrar, text="INGRESA EL STOCK", font=(FUENTE, 11, "bold"))
    stock.pack()
    stock1 = tk.Entry(ventana_registrar)
    stock1.pack()

    ubicacion = tk.Label(ventana_registrar, text="INGRESA LA UBICACION", font=(FUENTE, 11, "bold"))
    ubicacion.pack()
    ubicacion1 = tk.Entry(ventana_registrar)
    ubicacion1.pack()

    def guardar_producto():

        id_producto = label_id1.get().strip()
        nombre_producto = nombre1.get().strip()
        categoria_producto = categoria1.get().strip()
        ubicacion_producto = ubicacion1.get().strip()

        # No se permite guardar el producto si falta algun dato.
        if not all((id_producto, nombre_producto, categoria_producto, ubicacion_producto,
                    precio1.get().strip(), stock1.get().strip())):
            messagebox.showerror("Datos incompletos", "Completa todos los campos.", parent=ventana_registrar)
            return

        # Cada producto debe tener un ID unico para poder identificarlo.
        if any(producto["id"] == id_producto for producto in productos):
            messagebox.showerror("ID duplicado", "Ya existe un producto con ese ID.", parent=ventana_registrar)
            return

        # Convierte precio y stock a enteros y muestra un aviso si no son validos.
        try:
            precio_producto = int(precio1.get())
            stock_producto = int(stock1.get())
        except ValueError:
            messagebox.showerror("Dato inválido", "El precio y el stock deben ser números enteros.", parent=ventana_registrar)
            return

        producto = { #Diccionario
            "id": id_producto,
            "nombre": nombre_producto,
            "categoria": categoria_producto,
            "precio": precio_producto,
            "stock": stock_producto,
            "ubicacion": ubicacion_producto
}

        productos.append(producto) #Esta linea sirve para agregar el producto que acabo de crear a la lista de productos
        actualizar_conteo_productos()

        messagebox.showinfo("Producto guardado", "El producto se registró correctamente.", parent=ventana_registrar)
        ventana_registrar.destroy()
    crear_boton(ventana_registrar, "Guardar producto", guardar_producto, COLOR_VERDE).pack(pady=12)

def mostrar_productos(productos_filtrados=None, titulo="Inventario de productos"):
    lista_productos = productos if productos_filtrados is None else productos_filtrados
    ventana_mostrar = tk.Toplevel()
    configurar_ventana_secundaria(ventana_mostrar, titulo, "820x440")
    ventana_mostrar.minsize(680, 340)

    contenedor = tk.Frame(ventana_mostrar, bg=COLOR_FONDO, padx=24, pady=22)
    contenedor.pack(fill="both", expand=True)
    tk.Label(
        contenedor,
        text="Inventario de productos",
        bg=COLOR_FONDO,
        fg=COLOR_TINTA,
        font=(FUENTE, 18, "bold")
    ).pack(anchor="w", pady=(0, 14))
    if not lista_productos:
        tk.Label(
            contenedor,
            text="Aún no hay productos registrados." if productos_filtrados is None else "No se encontraron productos.",
            bg=COLOR_FONDO,
            fg=COLOR_SECUNDARIO,
            font=(FUENTE, 10)
        ).pack(anchor="w", pady=(0, 12))

    estilo = ttk.Style(ventana_mostrar)
    estilo.configure("Inventario.Treeview", rowheight=30, font=(FUENTE, 10))
    estilo.configure("Inventario.Treeview.Heading", font=(FUENTE, 9, "bold"))
    estilo.map("Inventario.Treeview", background=[("selected", COLOR_VERDE)])

    columnas = ("id", "nombre", "categoria", "precio", "stock", "ubicacion")
    tabla = ttk.Treeview(
        contenedor,
        columns=columnas,
        show="headings",
        style="Inventario.Treeview"
    )
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

def buscar_desde_panel():
    consulta = busqueda_entry.get().strip()
    if consulta == "Buscar por ID o nombre":
        consulta = ""

    if not consulta:
        mostrar_productos()
        return

    consulta = consulta.casefold()
    coincidencias = [
        producto for producto in productos
        if consulta in producto["id"].casefold() or consulta in producto["nombre"].casefold()
    ]
    mostrar_productos(coincidencias, "Resultados de búsqueda")

def buscar_producto():
    ventana_buscar = tk.Toplevel()
    configurar_ventana_secundaria(ventana_buscar, "Buscar producto", "440x320")
    ventana_buscar.minsize(400, 280)

    tk.Label(ventana_buscar, text="INGRESA EL ID DEL PRODUCTO", font=(FUENTE, 11, "bold")).pack(pady=(18, 4))
    entrada_id = tk.Entry(ventana_buscar)
    entrada_id.pack()
    resultado = tk.Label(ventana_buscar, text="", justify="left", font=(FUENTE, 10), bg=COLOR_SUPERFICIE, padx=12, pady=10)
    resultado.pack(fill="x", padx=24, pady=12)

    def buscar_por_id():
        id_buscar = entrada_id.get().strip()
        # next devuelve None cuando ningun producto coincide con el ID.
        producto_encontrado = next(
            (producto for producto in productos if producto["id"] == id_buscar),
            None
        )

        if producto_encontrado is None:
            resultado.config(text="PRODUCTO NO ENCONTRADO")
            return

        resultado.config(text=(
            f"ID: {producto_encontrado['id']}\n"
            f"Nombre: {producto_encontrado['nombre']}\n"
            f"Categoría: {producto_encontrado['categoria']}\n"
            f"Precio: {producto_encontrado['precio']}\n"
            f"Stock: {producto_encontrado['stock']}\n"
            f"Ubicación: {producto_encontrado['ubicacion']}"
        ))

    crear_boton(ventana_buscar, "Buscar", buscar_por_id, COLOR_VERDE).pack(pady=8)

def actualizar_producto():
    ventana_actualizar = tk.Toplevel()
    configurar_ventana_secundaria(ventana_actualizar, "Actualizar producto", "460x540")
    ventana_actualizar.minsize(420, 500)

    tk.Label(ventana_actualizar, text="ID DEL PRODUCTO", font=(FUENTE, 11, "bold")).pack(pady=(12, 4))
    entrada_id = tk.Entry(ventana_actualizar)
    entrada_id.pack()

    producto_seleccionado = None
    campos = {}
    for clave, etiqueta in (
        ("nombre", "NUEVO NOMBRE"),
        ("categoria", "NUEVA CATEGORIA"),
        ("precio", "NUEVO PRECIO"),
        ("ubicacion", "NUEVA UBICACION")
    ):
        tk.Label(ventana_actualizar, text=etiqueta, font=(FUENTE, 10, "bold")).pack(pady=(5, 2))
        campos[clave] = tk.Entry(ventana_actualizar)
        campos[clave].pack()

    def cargar_producto():
        nonlocal producto_seleccionado
        # Conserva el producto encontrado para modificarlo despues.
        producto_seleccionado = next(
            (producto for producto in productos if producto["id"] == entrada_id.get().strip()),
            None
        )

        if producto_seleccionado is None:
            boton_guardar.config(state="disabled")
            messagebox.showerror("Producto no encontrado", "No existe un producto con ese ID.", parent=ventana_actualizar)
            return

        # Rellena el formulario con los datos actuales para editarlos.
        for clave, campo in campos.items():
            campo.delete(0, tk.END)
            campo.insert(0, producto_seleccionado[clave])
        boton_guardar.config(state="normal")

    def guardar_cambios():
        if producto_seleccionado is None:
            return

        valores = {clave: campo.get().strip() for clave, campo in campos.items()}
        # Los campos editables deben estar completos antes de actualizar.
        if not all(valores.values()):
            messagebox.showerror("Datos incompletos", "Completa todos los campos.", parent=ventana_actualizar)
            return

        # El precio se guarda como entero, igual que al registrar.
        try:
            precio_nuevo = int(valores["precio"])
        except ValueError:
            messagebox.showerror("Precio inválido", "El precio debe ser un número entero.", parent=ventana_actualizar)
            return

        # Actualiza solo los campos permitidos el ID y el stock se conservan.
        producto_seleccionado.update({
            "nombre": valores["nombre"],
            "categoria": valores["categoria"],
            "precio": precio_nuevo,
            "ubicacion": valores["ubicacion"]
        })
        messagebox.showinfo("Producto actualizado", "Los datos se actualizaron correctamente.", parent=ventana_actualizar)
        ventana_actualizar.destroy()

    crear_boton(ventana_actualizar, "Cargar producto", cargar_producto, COLOR_SUPERFICIE, texto_color=COLOR_TINTA).pack(pady=8)
    boton_guardar = crear_boton(ventana_actualizar, "Guardar cambios", guardar_cambios, COLOR_VERDE)
    boton_guardar.config(state="disabled")
    boton_guardar.pack()

def eliminar_producto():
    ventana_eliminar = tk.Toplevel()
    configurar_ventana_secundaria(ventana_eliminar, "Eliminar producto", "420x230")
    ventana_eliminar.minsize(380, 210)

    tk.Label(ventana_eliminar, text="ID DEL PRODUCTO", font=(FUENTE, 11, "bold")).pack(pady=(16, 4))
    entrada_id = tk.Entry(ventana_eliminar)
    entrada_id.pack()

    def confirmar_eliminacion():
        id_producto = entrada_id.get().strip()
        if not id_producto:
            messagebox.showerror("ID requerido", "Ingresa el ID del producto.", parent=ventana_eliminar)
            return

        # Busca el producto antes de pedir confirmacion para eliminarlo.
        producto = next((producto for producto in productos if producto["id"] == id_producto), None)
        if producto is None:
            messagebox.showerror("Producto no encontrado", "No existe un producto con ese ID.", parent=ventana_eliminar)
            return

        confirmar = messagebox.askyesno(
            "Confirmar eliminación",
            f"¿Deseas eliminar el producto '{producto['nombre']}'?",
            parent=ventana_eliminar
        )
        if not confirmar:
            return

        productos.remove(producto)
        actualizar_conteo_productos()
        messagebox.showinfo("Producto eliminado", "El producto se eliminó correctamente.", parent=ventana_eliminar)
        ventana_eliminar.destroy()

    crear_boton(ventana_eliminar, "Eliminar producto", confirmar_eliminacion, COLOR_ROJO).pack(pady=12)

def gestionar_stock(es_entrada):
    titulo = "ENTRADA DE MERCANCÍA" if es_entrada else "SALIDA DE MERCANCÍA"
    ventana_stock = tk.Toplevel()
    configurar_ventana_secundaria(ventana_stock, titulo.title(), "420x300")
    ventana_stock.minsize(380, 270)

    tk.Label(ventana_stock, text="ID DEL PRODUCTO", font=(FUENTE, 11, "bold")).pack(pady=(14, 4))
    entrada_id = tk.Entry(ventana_stock)
    entrada_id.pack()

    tk.Label(ventana_stock, text="CANTIDAD", font=(FUENTE, 11, "bold")).pack(pady=(10, 4))
    entrada_cantidad = tk.Entry(ventana_stock)
    entrada_cantidad.pack()

    def aplicar_movimiento():
        id_producto = entrada_id.get().strip()
        # La cantidad debe ser un entero positivo para cualquier movimiento.
        try:
            cantidad = int(entrada_cantidad.get())
        except ValueError:
            messagebox.showerror("Cantidad inválida", "Ingresa una cantidad entera.", parent=ventana_stock)
            return

        if cantidad <= 0:
            messagebox.showerror("Cantidad inválida", "La cantidad debe ser mayor que cero.", parent=ventana_stock)
            return

        # Busca el producto al que se aplicara la entrada o salida.
        producto = next((producto for producto in productos if producto["id"] == id_producto), None)
        if producto is None:
            messagebox.showerror("Producto no encontrado", "No existe un producto con ese ID.", parent=ventana_stock)
            return

        # Evita que una salida deje el inventario con stock negativo.
        if not es_entrada and cantidad > producto["stock"]:
            messagebox.showerror("Stock insuficiente", "No hay suficiente stock para realizar la salida.", parent=ventana_stock)
            return

        # Las entradas suman unidades y las salidas las descuentan.
        if es_entrada:
            producto["stock"] += cantidad
        else:
            producto["stock"] -= cantidad

        messagebox.showinfo(
            "Stock actualizado",
            f"Movimiento realizado. Stock actual: {producto['stock']}",
            parent=ventana_stock
        )
        ventana_stock.destroy()

    crear_boton(
        ventana_stock,
        "Aplicar entrada" if es_entrada else "Aplicar salida",
        aplicar_movimiento,
        COLOR_VERDE if es_entrada else COLOR_AMBAR,
        fondo_activo=COLOR_VERDE_HOVER if es_entrada else COLOR_AMBAR_HOVER
    ).pack(pady=12)

def crear_mosaico(parent, icono, texto, comando, color_icono):
    mosaico = tk.Frame(
        parent,
        bg=COLOR_SUPERFICIE,
        highlightbackground=COLOR_LINEA,
        highlightthickness=1,
        width=190,
        height=150
    )
    mosaico.grid_propagate(False)
    icono_label = tk.Label(
        mosaico,
        text=icono,
        bg=COLOR_SUPERFICIE,
        fg=color_icono,
        font=("Segoe UI Symbol", 34)
    )
    icono_label.pack(expand=True, pady=(12, 0))
    texto_label = tk.Label(
        mosaico,
        text=texto.upper(),
        bg=COLOR_SUPERFICIE,
        fg=COLOR_SECUNDARIO,
        font=(FUENTE, 9, "bold"),
        wraplength=160,
        justify="center"
    )
    texto_label.pack(pady=(0, 14))

    componentes = (mosaico, icono_label, texto_label)
    for componente in componentes:
        componente.config(cursor="hand2")
        componente.bind("<Button-1>", lambda event, accion=comando: accion())
        componente.bind(
            "<Enter>",
            lambda event, elementos=componentes: [elemento.config(bg="#F8FBFC") for elemento in elementos]
        )
        componente.bind(
            "<Leave>",
            lambda event, elementos=componentes: [elemento.config(bg=COLOR_SUPERFICIE) for elemento in elementos]
        )
    return mosaico

modulos = (
    ("＋", "Registrar producto", registrar, COLOR_VERDE),
    ("▤", "Inventario", mostrar_productos, COLOR_MARCA),
    ("⌕", "Buscar producto", buscar_producto, COLOR_MARCA),
    ("↻", "Actualizar producto", actualizar_producto, COLOR_VERDE),
    ("×", "Eliminar producto", eliminar_producto, COLOR_ROJO),
    ("↑", "Entrada de mercancía", lambda: gestionar_stock(True), COLOR_VERDE),
    ("↓", "Salida de mercancía", lambda: gestionar_stock(False), COLOR_AMBAR)
)

for indice, (icono, texto, comando, color_icono) in enumerate(modulos):
    mosaico = crear_mosaico(rejilla_modulos, icono, texto, comando, color_icono)
    mosaico.grid(row=indice // 4, column=indice % 4, sticky="nsew", padx=7, pady=7)

tk.Label(
    pie,
    text="Sistema listo",
    bg=COLOR_FONDO,
    fg=COLOR_SECUNDARIO,
    font=(FUENTE, 9)
).pack(side="left")
crear_boton(pie, "Salir", ventana.destroy, COLOR_SUPERFICIE, texto_color=COLOR_SECUNDARIO).pack(side="right")

ventana.mainloop()