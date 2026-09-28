import tkinter as tk #Lo que hace esta linea es crear la interfaz grafica
from tkinter import messagebox

ventana = tk.Tk() #Lo que hace esta linea es crear nuestra ventana principal

ventana.title("ALMACEN RICHIE") #Coloca el titulo en la ventana 

ventana.geometry("800x600")

productos = []

titulo = tk.Label( #Aqui estamos controlando los detalles del titulo
    ventana,
    text="ALMACEN RICHIE",
    font=("Arial", 24)
)
titulo.pack()


def registrar(): #Lo que hacemos aqui es crear una funcion para que al momento de precioar el boton nos aparezca el mensaje de registrar
    ventana_registrar = tk.Toplevel() #Esta linea lo que hace es generar otra ventana al darle click en registrar producto
    ventana_registrar.title("REGISTRAR PRODUCTO")
    ventana_registrar.geometry("400x400")

    label_id = tk.Label(ventana_registrar, text="ID", font=("Arial", 15))
    label_id.pack()
    label_id1 = tk.Entry(ventana_registrar)
    label_id1.pack()

    nombre = tk.Label(ventana_registrar, text="INGRESA EL NOMBRE", font=("Arial", 15))
    nombre.pack()
    nombre1 = tk.Entry(ventana_registrar)
    nombre1.pack()

    categoria = tk.Label(ventana_registrar, text="INGRESA LA CATEGORIA", font=("Arial", 15))
    categoria.pack()
    categoria1 = tk.Entry(ventana_registrar)
    categoria1.pack()

    precio = tk.Label(ventana_registrar, text="INGRESA EL PRECIO", font=("Arial", 15))
    precio.pack()
    precio1 = tk.Entry(ventana_registrar)
    precio1.pack()

    stock = tk.Label(ventana_registrar, text="INGRESA EL STOCK", font=("Arial", 15))
    stock.pack()
    stock1 = tk.Entry(ventana_registrar)
    stock1.pack()

    ubicacion = tk.Label(ventana_registrar, text="INGRESA LA UBICACION", font=("Arial", 15))
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

        messagebox.showinfo("Producto guardado", "El producto se registró correctamente.", parent=ventana_registrar)
        ventana_registrar.destroy()
    guardar = tk.Button(ventana_registrar,command=guardar_producto, text="GUARDAR", font=("Arial", 15))
    guardar.pack()

def mostrar_productos():
    ventana_mostrar = tk.Toplevel()
    ventana_mostrar.title("MOSTRAR PRODUCTOS")
    ventana_mostrar.geometry("400x400")

    for producto in productos: #esta linea significa, por cada producto que exisra dentro de la lista productos haz lo siguiente
        texto = tk.Label(ventana_mostrar, text=producto)
        texto.pack()

def buscar_producto():
    ventana_buscar = tk.Toplevel()
    ventana_buscar.title("BUSCAR PRODUCTO")
    ventana_buscar.geometry("400x300")

    tk.Label(ventana_buscar, text="INGRESA EL ID DEL PRODUCTO", font=("Arial", 15)).pack()
    entrada_id = tk.Entry(ventana_buscar)
    entrada_id.pack()
    resultado = tk.Label(ventana_buscar, text="", justify="left", font=("Arial", 12))
    resultado.pack(pady=10)

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

    tk.Button(ventana_buscar, command=buscar_por_id, text="BUSCAR", font=("Arial", 12)).pack()

def actualizar_producto():
    ventana_actualizar = tk.Toplevel()
    ventana_actualizar.title("ACTUALIZAR PRODUCTO")
    ventana_actualizar.geometry("400x500")

    tk.Label(ventana_actualizar, text="ID DEL PRODUCTO", font=("Arial", 15)).pack()
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
        tk.Label(ventana_actualizar, text=etiqueta, font=("Arial", 12)).pack()
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

    tk.Button(ventana_actualizar, command=cargar_producto, text="CARGAR PRODUCTO", font=("Arial", 12)).pack(pady=8)
    boton_guardar = tk.Button(
        ventana_actualizar,
        command=guardar_cambios,
        text="GUARDAR CAMBIOS",
        font=("Arial", 12),
        state="disabled"
    )
    boton_guardar.pack()

def eliminar_producto():
    ventana_eliminar = tk.Toplevel()
    ventana_eliminar.title("ELIMINAR PRODUCTO")
    ventana_eliminar.geometry("400x200")

    tk.Label(ventana_eliminar, text="ID DEL PRODUCTO", font=("Arial", 15)).pack()
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
        messagebox.showinfo("Producto eliminado", "El producto se eliminó correctamente.", parent=ventana_eliminar)
        ventana_eliminar.destroy()

    tk.Button(ventana_eliminar, command=confirmar_eliminacion, text="ELIMINAR", font=("Arial", 12)).pack(pady=10)

def gestionar_stock(es_entrada):
    titulo = "ENTRADA DE MERCANCÍA" if es_entrada else "SALIDA DE MERCANCÍA"
    ventana_stock = tk.Toplevel()
    ventana_stock.title(titulo)
    ventana_stock.geometry("400x250")

    tk.Label(ventana_stock, text="ID DEL PRODUCTO", font=("Arial", 15)).pack()
    entrada_id = tk.Entry(ventana_stock)
    entrada_id.pack()

    tk.Label(ventana_stock, text="CANTIDAD", font=("Arial", 15)).pack()
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

    tk.Button(ventana_stock, command=aplicar_movimiento, text="APLICAR", font=("Arial", 12)).pack(pady=10)

boton_registrar = tk.Button(ventana, command=registrar, text="Registrar producto", font=("Arial", 15)) #este apartado esta conectado con la funcion Registrar, ya que estamos utilizando el commant para que al momento de que le de clic al boton de registrar producto genere el mensaje
boton_registrar.pack()

boton_buscar = tk.Button(ventana, command=buscar_producto, text="Buscar producto", font=("Arial", 15))
boton_buscar.pack()

boton_mostrar = tk.Button(ventana, command=mostrar_productos, text="Mostrar productos", font=("Arial", 15))
boton_mostrar.pack()

boton_entrada = tk.Button(ventana, command=lambda: gestionar_stock(True), text="Entrada de mercancia", font=("Arial", 15))
boton_entrada.pack()

boton_salida = tk.Button(ventana, command=lambda: gestionar_stock(False), text="Salida de mercancia", font=("Arial", 15))
boton_salida.pack()

boton_actualizar = tk.Button(ventana, command=actualizar_producto, text="Actualizar producto", font=("Arial", 15))
boton_actualizar.pack()

boton_eliminar = tk.Button(ventana, command=eliminar_producto, text="Eliminar producto", font=("Arial", 15))
boton_eliminar.pack()

boton_salir = tk.Button(ventana, command=ventana.destroy, text="Salir", font=("Arial", 15))
boton_salir.pack()

ventana.mainloop()