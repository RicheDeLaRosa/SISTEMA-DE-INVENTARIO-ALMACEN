import tkinter as tk

from ui_comun import COLOR_SUPERFICIE, COLOR_TINTA, COLOR_VERDE, FUENTE, configurar_ventana, crear_boton


def abrir(parent, productos):
    ventana = tk.Toplevel(parent)
    configurar_ventana(ventana, parent, "Buscar producto", "440x320")
    ventana.minsize(400, 280)

    tk.Label(ventana, text="INGRESA EL ID DEL PRODUCTO", font=(FUENTE, 11, "bold")).pack(pady=(18, 4))
    entrada_id = tk.Entry(ventana)
    entrada_id.pack()
    resultado = tk.Label(
        ventana,
        text="",
        justify="left",
        font=(FUENTE, 10),
        bg=COLOR_SUPERFICIE,
        fg=COLOR_TINTA,
        padx=12,
        pady=10
    )
    resultado.pack(fill="x", padx=24, pady=12)

    def buscar_por_id():
        id_buscar = entrada_id.get().strip()
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

    crear_boton(ventana, "Buscar", buscar_por_id, COLOR_VERDE).pack(pady=8)
    entrada_id.focus_set()
    ventana.bind("<Return>", lambda event: buscar_por_id())