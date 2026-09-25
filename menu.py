#SISTEMA DE ALMACEN

productos = []

opcion = ""

print("---------ALMACEN RICHIE-----------")

while opcion != "8": #Lo que hace esta parte es que todo el codigo esta dentro del ciclo while, lo que hace que se repita infinitamente hasta que el usuario intruduzca la opcion de salir
    print("1. Registrar producto ") #Lo que hace aqui es mostrar el menu
    print("2. Mostrar productos ")
    print("3. Buscar producto ")
    print("4. Entrada de mercancia ")
    print("5. Salida de mercancia" )
    print("6. Actualizar, Nombre, Categoria, Precio, Ubicacion" )
    print("7. Eliminar producto ")
    print("8. Salir ")

    opcion = input("Selecciona una opcion: ") #Aqui estamos declarando una variable la cual se llama opcion. lo que hace es que al momento de que el usuario inigrese su respuesta se almacena en opcion

    if opcion == "1": #Estas son las opciones que estan disponibles 

        print("REGISTRA EL PRODUCTO")

        id = input("Ingrese el ID: ")

        encontrado = False #Colocamos esta validacion al inicio para asi comprobar si el ID ya esta registrado, si el ID ya se encuentra registrado arroja el mensaje de que ya se encuentra registrado, de lo contrario si no esta registrado continua ingresando los datos del producto
        for producto in productos:
            if id == producto["id"]:
                encontrado = True

        if encontrado == False:  
            nombre = input("Ingrese el nombre: ")
            categoria = input("Ingrese la categoria: ")
            precio = int(input("Ingrese el precio: "))                
            stock = int(input("Ingrese el stock: "))
            ubicacion = input("Ingrese la ubicacion: ")

            productos.append({
                "id": id,
                "nombre": nombre,
                "categoria": categoria,
                "precio": precio,
                "stock": stock,
                "ubicacion": ubicacion,
        })
        else:
            print("EL ID YA EXISTE")

    elif opcion == "2":

        for producto in productos: # Por cada producto que exista dentro de la lista productos, guarda temporalmente ese producto en la variable producto
            print(producto["id"])
            print(producto["nombre"])
            print(producto["categoria"])
            print(producto["precio"])
            print(producto["stock"])
            print(producto["ubicacion"])

    elif opcion == "3":
        print("INGRESE EL ID DEL PRODUCTO")
        id_buscar = input("¿QUE ID DESEAS BUSCAR?")

        encontrado = False #Marca que si encontro uno

        for producto in productos:
            if id_buscar == producto["id"]: #Este apartado lo que hace es comparar el id  buscado con el id de cada producto que este registrado
                print(producto["id"]) # Si el id coincide, muestra todos los datos del producto
                print(producto["nombre"])
                print(producto["categoria"])
                print(producto["precio"])
                print(producto["stock"])
                print(producto["ubicacion"])
                encontrado = True

        if encontrado == False: #Si se termina de recorrer la lista y nunca se encontro conincidencia imprime que el producto no fue encontrado
            print("PRODUCTO NO ENCONTRADO")

    elif opcion == "4":
        id_entrada = input("¿QUE ID DESEAS BUSCAR? ")
        encontrado = False

        for producto in productos: #Sigue la misma logica del apartado buscar producto. lo que hace es comparar el id buscado con el id de qie producto registrado
            if id_entrada == producto["id"]: #Si el id coincide muestra todos los datos del producto

                encontrado = True

                cantidad = int(input("¿CUANTAS UNIDADES VAN A ENTRAR? "))
                if cantidad > 0:
                    producto["stock"] = producto["stock"] + cantidad #Lo que hace este apartado es hacer la operacion que va a SUMAR la cantidad que va entrar con el stock que ya hay
                    print(producto)
                else:
                    print("NO SE PUEDEN AGREGAR NUMEROS NEGATIVOS")

        if encontrado == False:
            print("NO SE PUEDEN AGREGAR CANTIDADES MENORES O IGUALES A 0")

    elif opcion == "5":
        id_salida = input("¿QUE ID DESEAS BUSCAR? ")
        encontrado = False
        
        for producto in productos:
            if id_salida == producto["id"]:
                encontrado = True
        
                cantidad = int(input("¿CUANTAS UNIDADES VAN A SALIR? "))
                if cantidad > 0:
                    if cantidad <= producto["stock"]:
                        producto["stock"] = producto["stock"] - cantidad #Lo que hace este apartado es la operacion que va a RESTAR la cantidad que va a salir con el stock que ya hay
                        print(producto) #Si hay suficiente stock para salir muestra los datos del producto
                    else:
                        print("NO HAY SUFICIENTE STOCK PARA SALIR") #De lo contrario si no hay suficiente stock para salir mmuestra este mensaje

                else:
                    print("NO SE PUEDEN SACAR CANTIDADES MENORES O IGUALES A 0")

        if encontrado ==  False:
            print("PRODUCTO NO ENCONTRADO")

    elif opcion == "6":
        id_actualizar = input("¿QUE ID DESEAS BUSCAR? ")
        encontrado = False

        for producto in productos:
            if id_actualizar == producto["id"]:
                encontrado = True

                nuevo_precio = int(input("Ingrese el nuevo precio: ")) #En este apartado el nuevo precio que se ingrese se guarda en la variable (nuevo_precio)
                nuevo_nombre = (input("Ingrese el nuevo nombre: "))
                nuevo_categoria = (input("Ingrese la nueva categoria: "))
                nuevo_ubicacion = (input("Ingrese la nueva ubicacion: "))

                producto["precio"] = nuevo_precio #Aqui estamos modificando el diccionario para que el nuevo precio remplaze el precio anterior
                producto["nombre"] = nuevo_nombre
                producto["categoria"] = nuevo_categoria
                producto["ubicacion"] = nuevo_ubicacion

                print(producto)

        if encontrado == False:
            print("PRODUCTO NO ENCONTRADO")

    elif opcion == "7":
        id_eliminar = input("¿QUE ID DESEAS BUSCAR? ")

        encontrado = False
        
        for producto in productos:
            if id_eliminar == producto["id"]:
                encontrado = True
                productos.remove(producto)

        if encontrado == False:
            print("PRODUCTO NO ENCONTRADO")

    elif opcion == "8":
        print("Saliendo del programa... ")

    else: 
        print("opcion incorrecta") #Lo que hace esta parte es ver si el usuario ingresa un numero que no esta en el menu, si agrega un numero que no esta lo que hace es que aparece un mensaje diciendo que el numero que ingreso no esta en el menu
