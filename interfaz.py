import tkinter as tk #Lo que hace esta linea es crear la interfaz grafica

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

        id_producto = label_id1.get() #Obtiene el ID y lo gurda en id_producto
        nombre_producto = nombre1.get()
        categoria_producto = categoria1.get()
        precio_producto = int(precio1.get())
        stock_producto = int(stock1.get())
        ubicacion_producto = ubicacion1.get()

        producto = { #Diccionario
            "id": id_producto,
            "nombre": nombre_producto,
            "categoria": categoria_producto,
            "precio": precio_producto,
            "stock": stock_producto,
            "ubicacion": ubicacion_producto
}

        productos.append(producto) #Esta linea sirve para agregar el producto que acabo de crear a la lista de productos

        print(id_producto)
        print(nombre_producto)
        print(categoria_producto)
        print(precio_producto)
        print(stock_producto)
        print(ubicacion_producto)
    guardar = tk.Button(ventana_registrar,command=guardar_producto, text="GUARDAR", font=("Arial", 15))
    guardar.pack()


boton_registrar = tk.Button(ventana, command=registrar, text="Registrar producto", font=("Arial", 15)) #este apartado esta conectado con la funcion Registrar, ya que estamos utilizando el commant para que al momento de que le de clic al boton de registrar producto genere el mensaje
boton_registrar.pack()

boton_buscar = tk.Button(ventana, text="Buscar producto", font=("Arial", 15))
boton_buscar.pack()

boton_mostrar = tk.Button(ventana, text="Mostrar productos", font=("Arial", 15))
boton_mostrar.pack()

boton_entrada = tk.Button(ventana, text="Entrada de mercancia", font=("Arial", 15))
boton_entrada.pack()

boton_salida = tk.Button(ventana, text="Salida de mercancia", font=("Arial", 15))
boton_salida.pack()

boton_actualizar = tk.Button(ventana, text="Actualizar producto", font=("Arial", 15))
boton_actualizar.pack()

boton_eliminar = tk.Button(ventana, text="Eliminar producto", font=("Arial", 15))
boton_eliminar.pack()

boton_salir = tk.Button(ventana, text="Salir", font=("Arial", 15))
boton_salir.pack()

ventana.mainloop()