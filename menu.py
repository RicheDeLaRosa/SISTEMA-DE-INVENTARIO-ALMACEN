#SISTEMA DE ALMACEN

productos = []

opcion = ""

print("---------ALMACEN CASTORES-----------")

while opcion != "8": #Lo que hace esta parte es que todo el codigo esta dentro del ciclo while, lo que hace que se repita infinitamente hasta que el usuario intruduzca la opcion de salir
    print("1. Registrar producto ") #Lo que hace aqui es mostrar el menu
    print("2. Mostrar productos ")
    print("3. Buscar producto ")
    print("4. Entrada de mercancia ")
    print("5. Salida de mercancia" )
    print("6. Actualizar producto" )
    print("7. Eliminar producto ")
    print("8. Salir ")

    opcion = input("Selecciona una opcion: ") #Aqui estamos declarando una variable la cual se llama opcion. lo que hace es que al momento de que el usuario inigrese su respuesta se almacena en opcion

    if opcion == "1": #Estas son las opciones que estan disponibles 

        print("REGISTRA EL PRODUCTO")

        id = input("Ingrese el ID: ")
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

        encontrado = False

        for producto in productos:
            if id_buscar == producto["id"]:
                print(producto["id"])
                print(producto["nombre"])
                print(producto["categoria"])
                print(producto["precio"])
                print(producto["stock"])
                print(producto["ubicacion"])
                encontrado = True

        if encontrado == False:
            print("PRODUCTO NO ENCONTRADO")

    elif opcion == "4":
        print("Entrada de mercancia")

    elif opcion == "5":
        print("Salida de mercancia")

    elif opcion == "6":
        print("Actualizar producto")

    elif opcion == "7":
        print("Eliminar producto")

    elif opcion == "8":
        print("Saliendo del programa... ")

    else: 
        print("opcion incorrecta") #Lo que hace esta parte es ver si el usuario ingresa un numero que no esta en el menu, si agrega un numero que no esta lo que hace es que aparece un mensaje diciendo que el numero que ingreso no esta en el menu
