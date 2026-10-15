import tkinter as tk
from tkinter import messagebox

from ui_comun import (
    COLOR_AMBAR,
    COLOR_AMBAR_HOVER,
    COLOR_LINEA,
    COLOR_ROJO,
    COLOR_SECUNDARIO,
    COLOR_SUPERFICIE,
    COLOR_TINTA,
    COLOR_VERDE,
    COLOR_VERDE_HOVER,
    FUENTE,
    configurar_ventana,
    crear_boton,
)


def abrir(parent, productos, es_entrada):
    """Abre el formulario de entrada o salida y actualiza el stock al confirmar."""
    titulo = "ENTRADA DE MERCANCÍA" if es_entrada else "SALIDA DE MERCANCÍA"
    ventana = tk.Toplevel(parent)
    if es_entrada:
        # La entrada usa verde para comunicar visualmente que las existencias aumentarán.
        configurar_ventana(ventana, parent, titulo.title(), "560x620")
        ventana.minsize(500, 580)

        panel = tk.Frame(ventana, bg=COLOR_SUPERFICIE)
        panel.pack(fill="both", expand=True, padx=20, pady=20)

        cabecera = tk.Frame(panel, bg=COLOR_VERDE, padx=26, pady=22)
        cabecera.pack(fill="x")
        tk.Label(
            cabecera,
            text="↑",
            bg="#E8F4F1",
            fg=COLOR_VERDE,
            font=("Segoe UI Symbol", 21, "bold"),
            width=3,
            height=1,
        ).pack(side="left", padx=(0, 16))
        textos_cabecera = tk.Frame(cabecera, bg=COLOR_VERDE)
        textos_cabecera.pack(side="left", fill="x", expand=True)
        tk.Label(
            textos_cabecera,
            text="Entrada de mercancía",
            bg=COLOR_VERDE,
            fg=COLOR_SUPERFICIE,
            font=(FUENTE, 18, "bold"),
        ).pack(anchor="w")
        tk.Label(
            textos_cabecera,
            text="Registra productos recibidos y actualiza el stock.",
            bg=COLOR_VERDE,
            fg="#D7ECE8",
            font=(FUENTE, 9),
        ).pack(anchor="w", pady=(3, 0))

        formulario = tk.Frame(panel, bg=COLOR_SUPERFICIE, padx=26, pady=22)
        formulario.pack(fill="both", expand=True)

        tk.Label(
            formulario,
            text="ID DEL PRODUCTO",
            bg=COLOR_SUPERFICIE,
            fg=COLOR_TINTA,
            font=(FUENTE, 9, "bold"),
        ).pack(anchor="w", pady=(0, 7))
        entrada_id = tk.Entry(formulario, font=(FUENTE, 11))
        entrada_id.pack(fill="x", ipady=8)
        tk.Label(
            formulario,
            text="Escribe el código del producto para consultar sus existencias.",
            bg=COLOR_SUPERFICIE,
            fg=COLOR_SECUNDARIO,
            font=(FUENTE, 9),
        ).pack(anchor="w", pady=(5, 14))

        detalle = tk.Frame(formulario, bg="#F3F7F8", padx=14, pady=12)
        detalle.pack(fill="x", pady=(0, 18))
        producto_texto = tk.StringVar(value="Escribe el ID para consultar el producto")
        tk.Label(
            detalle,
            textvariable=producto_texto,
            bg="#F3F7F8",
            fg=COLOR_TINTA,
            font=(FUENTE, 11, "bold"),
        ).pack(anchor="w")
        tk.Label(
            detalle,
            text="RESUMEN DE EXISTENCIAS",
            bg="#F3F7F8",
            fg=COLOR_SECUNDARIO,
            font=(FUENTE, 8, "bold"),
        ).pack(anchor="w", pady=(12, 6))
        resumen_stock = tk.Frame(detalle, bg="#F3F7F8")
        resumen_stock.pack(fill="x")
        actual = tk.Frame(resumen_stock, bg="#F3F7F8")
        actual.pack(side="left", fill="x", expand=True)
        nuevo = tk.Frame(resumen_stock, bg="#F3F7F8")
        nuevo.pack(side="right", fill="x", expand=True)
        tk.Label(
            actual,
            text="STOCK ACTUAL",
            bg="#F3F7F8",
            fg=COLOR_SECUNDARIO,
            font=(FUENTE, 8, "bold"),
        ).pack(anchor="w")
        tk.Label(
            nuevo,
            text="STOCK NUEVO",
            bg="#F3F7F8",
            fg=COLOR_SECUNDARIO,
            font=(FUENTE, 8, "bold"),
        ).pack(anchor="e")
        stock_actual = tk.StringVar(value="—")
        stock_nuevo = tk.StringVar(value="—")
        tk.Label(
            actual,
            textvariable=stock_actual,
            bg="#F3F7F8",
            fg=COLOR_TINTA,
            font=(FUENTE, 14, "bold"),
        ).pack(anchor="w", pady=(2, 0))
        tk.Label(
            nuevo,
            textvariable=stock_nuevo,
            bg="#F3F7F8",
            fg=COLOR_VERDE,
            font=(FUENTE, 14, "bold"),
        ).pack(anchor="e", pady=(2, 0))

        tk.Label(
            formulario,
            text="CANTIDAD RECIBIDA",
            bg=COLOR_SUPERFICIE,
            fg=COLOR_TINTA,
            font=(FUENTE, 9, "bold"),
        ).pack(anchor="w", pady=(0, 7))
        entrada_cantidad = tk.Entry(formulario, font=(FUENTE, 13, "bold"))
        entrada_cantidad.pack(fill="x", ipady=8)
        tk.Label(
            formulario,
            text="Ingresa un número entero mayor que cero.",
            bg=COLOR_SUPERFICIE,
            fg=COLOR_SECUNDARIO,
            font=(FUENTE, 9),
        ).pack(anchor="w", pady=(5, 0))

        # Actualiza el nombre y calcula el stock esperado mientras se completa la entrada.
        def actualizar_vista_previa(event=None):
            id_producto = entrada_id.get().strip()
            producto = next((item for item in productos if item["id"] == id_producto), None)
            if producto is None:
                producto_texto.set(
                    "Producto no encontrado"
                    if id_producto
                    else "Escribe el ID para consultar el producto"
                )
                stock_actual.set("—")
                stock_nuevo.set("—")
                boton_aplicar.config(state="disabled")
                return

            producto_texto.set(producto["nombre"])
            stock = producto["stock"]
            stock_actual.set(str(stock))
            try:
                cantidad = int(entrada_cantidad.get())
            except ValueError:
                cantidad = 0
            if cantidad > 0:
                stock_nuevo.set(str(stock + cantidad))
                boton_aplicar.config(state="normal")
            else:
                stock_nuevo.set("—")
                boton_aplicar.config(state="disabled")

        entrada_id.bind("<KeyRelease>", actualizar_vista_previa)
        entrada_id.bind("<Return>", lambda event: entrada_cantidad.focus_set())
        entrada_cantidad.bind("<KeyRelease>", actualizar_vista_previa)
        entrada_cantidad.bind("<Return>", lambda event: aplicar_movimiento())
        ventana.bind("<Escape>", lambda event: ventana.destroy())
    else:
        # La salida usa ámbar y presenta el stock restante antes de confirmar el retiro.
        configurar_ventana(ventana, parent, titulo.title(), "560x620")
        ventana.minsize(500, 580)

        panel = tk.Frame(ventana, bg=COLOR_SUPERFICIE)
        panel.pack(fill="both", expand=True, padx=20, pady=20)

        cabecera = tk.Frame(panel, bg=COLOR_AMBAR, padx=26, pady=22)
        cabecera.pack(fill="x")
        tk.Label(
            cabecera,
            text="↓",
            bg="#F8EFE5",
            fg=COLOR_AMBAR,
            font=("Segoe UI Symbol", 21, "bold"),
            width=3,
            height=1,
        ).pack(side="left", padx=(0, 16))
        textos_cabecera = tk.Frame(cabecera, bg=COLOR_AMBAR)
        textos_cabecera.pack(side="left", fill="x", expand=True)
        tk.Label(
            textos_cabecera,
            text="Salida de mercancía",
            bg=COLOR_AMBAR,
            fg=COLOR_SUPERFICIE,
            font=(FUENTE, 18, "bold"),
        ).pack(anchor="w")
        tk.Label(
            textos_cabecera,
            text="Registra unidades retiradas y verifica el stock disponible.",
            bg=COLOR_AMBAR,
            fg="#F4E5D4",
            font=(FUENTE, 9),
        ).pack(anchor="w", pady=(3, 0))

        formulario = tk.Frame(panel, bg=COLOR_SUPERFICIE, padx=26, pady=22)
        formulario.pack(fill="both", expand=True)

        tk.Label(
            formulario,
            text="ID DEL PRODUCTO",
            bg=COLOR_SUPERFICIE,
            fg=COLOR_TINTA,
            font=(FUENTE, 9, "bold"),
        ).pack(anchor="w", pady=(0, 7))
        entrada_id = tk.Entry(formulario, font=(FUENTE, 11))
        entrada_id.pack(fill="x", ipady=8)
        tk.Label(
            formulario,
            text="Escribe el código del producto para consultar sus existencias.",
            bg=COLOR_SUPERFICIE,
            fg=COLOR_SECUNDARIO,
            font=(FUENTE, 9),
        ).pack(anchor="w", pady=(5, 14))

        detalle = tk.Frame(formulario, bg="#F3F7F8", padx=14, pady=12)
        detalle.pack(fill="x", pady=(0, 18))
        producto_texto = tk.StringVar(value="Escribe el ID para consultar el producto")
        tk.Label(
            detalle,
            textvariable=producto_texto,
            bg="#F3F7F8",
            fg=COLOR_TINTA,
            font=(FUENTE, 11, "bold"),
        ).pack(anchor="w")
        tk.Label(
            detalle,
            text="RESUMEN DE EXISTENCIAS",
            bg="#F3F7F8",
            fg=COLOR_SECUNDARIO,
            font=(FUENTE, 8, "bold"),
        ).pack(anchor="w", pady=(12, 6))
        resumen_stock = tk.Frame(detalle, bg="#F3F7F8")
        resumen_stock.pack(fill="x")
        actual = tk.Frame(resumen_stock, bg="#F3F7F8")
        actual.pack(side="left", fill="x", expand=True)
        restante = tk.Frame(resumen_stock, bg="#F3F7F8")
        restante.pack(side="right", fill="x", expand=True)
        tk.Label(
            actual,
            text="STOCK DISPONIBLE",
            bg="#F3F7F8",
            fg=COLOR_SECUNDARIO,
            font=(FUENTE, 8, "bold"),
        ).pack(anchor="w")
        tk.Label(
            restante,
            text="DESPUÉS DE SALIDA",
            bg="#F3F7F8",
            fg=COLOR_SECUNDARIO,
            font=(FUENTE, 8, "bold"),
        ).pack(anchor="e")
        stock_actual = tk.StringVar(value="—")
        stock_nuevo = tk.StringVar(value="—")
        tk.Label(
            actual,
            textvariable=stock_actual,
            bg="#F3F7F8",
            fg=COLOR_TINTA,
            font=(FUENTE, 14, "bold"),
        ).pack(anchor="w", pady=(2, 0))
        etiqueta_stock_nuevo = tk.Label(
            restante,
            textvariable=stock_nuevo,
            bg="#F3F7F8",
            fg=COLOR_AMBAR,
            font=(FUENTE, 14, "bold"),
        )
        etiqueta_stock_nuevo.pack(anchor="e", pady=(2, 0))

        tk.Label(
            formulario,
            text="CANTIDAD A RETIRAR",
            bg=COLOR_SUPERFICIE,
            fg=COLOR_TINTA,
            font=(FUENTE, 9, "bold"),
        ).pack(anchor="w", pady=(0, 7))
        entrada_cantidad = tk.Entry(formulario, font=(FUENTE, 13, "bold"))
        entrada_cantidad.pack(fill="x", ipady=8)
        mensaje_cantidad = tk.StringVar(value="Ingresa un número entero mayor que cero.")
        mensaje_cantidad_label = tk.Label(
            formulario,
            textvariable=mensaje_cantidad,
            bg=COLOR_SUPERFICIE,
            fg=COLOR_SECUNDARIO,
            font=(FUENTE, 9),
        )
        mensaje_cantidad_label.pack(anchor="w", pady=(5, 0))

        # Valida la disponibilidad y anticipa el resultado de descontar la cantidad.
        def actualizar_vista_previa(event=None):
            id_producto = entrada_id.get().strip()
            producto = next((item for item in productos if item["id"] == id_producto), None)
            if producto is None:
                producto_texto.set(
                    "Producto no encontrado"
                    if id_producto
                    else "Escribe el ID para consultar el producto"
                )
                stock_actual.set("—")
                stock_nuevo.set("—")
                mensaje_cantidad.set("Ingresa un número entero mayor que cero.")
                mensaje_cantidad_label.config(fg=COLOR_SECUNDARIO)
                etiqueta_stock_nuevo.config(fg=COLOR_AMBAR)
                boton_aplicar.config(state="disabled")
                return

            producto_texto.set(producto["nombre"])
            stock = producto["stock"]
            stock_actual.set(str(stock))
            try:
                cantidad = int(entrada_cantidad.get())
            except ValueError:
                cantidad = 0

            if cantidad <= 0:
                # No muestra un resultado ni permite confirmar cantidades inválidas.
                stock_nuevo.set("—")
                mensaje_cantidad.set("Ingresa un número entero mayor que cero.")
                mensaje_cantidad_label.config(fg=COLOR_SECUNDARIO)
                etiqueta_stock_nuevo.config(fg=COLOR_AMBAR)
                boton_aplicar.config(state="disabled")
            elif cantidad > stock:
                # Advierte antes de aplicar cuando el retiro supera las existencias.
                stock_nuevo.set("Insuficiente")
                mensaje_cantidad.set(f"Stock insuficiente: solo hay {stock} unidades disponibles.")
                mensaje_cantidad_label.config(fg=COLOR_ROJO)
                etiqueta_stock_nuevo.config(fg=COLOR_ROJO)
                boton_aplicar.config(state="disabled")
            else:
                stock_nuevo.set(str(stock - cantidad))
                mensaje_cantidad.set(f"Quedarán {stock - cantidad} unidades en inventario.")
                mensaje_cantidad_label.config(fg=COLOR_SECUNDARIO)
                etiqueta_stock_nuevo.config(fg=COLOR_AMBAR)
                boton_aplicar.config(state="normal")

        entrada_id.bind("<KeyRelease>", actualizar_vista_previa)
        entrada_id.bind("<Return>", lambda event: entrada_cantidad.focus_set())
        entrada_cantidad.bind("<KeyRelease>", actualizar_vista_previa)
        entrada_cantidad.bind("<Return>", lambda event: aplicar_movimiento())
        ventana.bind("<Escape>", lambda event: ventana.destroy())

    # Valida los datos y modifica el stock solo cuando el movimiento es válido.
    def aplicar_movimiento():
        id_producto = entrada_id.get().strip()
        try:
            cantidad = int(entrada_cantidad.get())
        except ValueError:
            messagebox.showerror("Cantidad inválida", "Ingresa una cantidad entera.", parent=ventana)
            return

        if cantidad <= 0:
            messagebox.showerror("Cantidad inválida", "La cantidad debe ser mayor que cero.", parent=ventana)
            return

        producto = next((producto for producto in productos if producto["id"] == id_producto), None)
        if producto is None:
            messagebox.showerror("Producto no encontrado", "No existe un producto con ese ID.", parent=ventana)
            return

        # Se repite la validación de stock al confirmar para proteger la operación.
        if not es_entrada and cantidad > producto["stock"]:
            messagebox.showerror("Stock insuficiente", "No hay suficiente stock para realizar la salida.", parent=ventana)
            return

        # El signo del cambio depende del tipo de movimiento seleccionado.
        if es_entrada:
            producto["stock"] += cantidad
        else:
            producto["stock"] -= cantidad

        messagebox.showinfo(
            "Stock actualizado",
            f"Movimiento realizado. Stock actual: {producto['stock']}",
            parent=ventana
        )
        ventana.destroy()

    # El botón principal queda deshabilitado hasta tener un producto y una cantidad válidos.
    if es_entrada:
        acciones = tk.Frame(panel, bg=COLOR_SUPERFICIE, padx=26, pady=12)
        acciones.pack(fill="x", side="bottom")
        tk.Frame(panel, bg=COLOR_LINEA, height=1).pack(fill="x", side="bottom")
        crear_boton(
            acciones,
            "Cancelar",
            ventana.destroy,
            COLOR_SUPERFICIE,
            texto_color=COLOR_SECUNDARIO,
        ).pack(side="right", padx=(8, 0))
        boton_aplicar = crear_boton(
            acciones,
            "Aplicar entrada",
            aplicar_movimiento,
            COLOR_VERDE,
            fondo_activo=COLOR_VERDE_HOVER,
        )
        boton_aplicar.pack(side="right", pady=4)
        boton_aplicar.config(state="disabled")
        actualizar_vista_previa()
    else:
        acciones = tk.Frame(panel, bg=COLOR_SUPERFICIE, padx=26, pady=12)
        acciones.pack(fill="x", side="bottom")
        tk.Frame(panel, bg=COLOR_LINEA, height=1).pack(fill="x", side="bottom")
        crear_boton(
            acciones,
            "Cancelar",
            ventana.destroy,
            COLOR_SUPERFICIE,
            texto_color=COLOR_SECUNDARIO,
        ).pack(side="right", padx=(8, 0))
        boton_aplicar = crear_boton(
            acciones,
            "Aplicar salida",
            aplicar_movimiento,
            COLOR_AMBAR,
            fondo_activo=COLOR_AMBAR_HOVER,
        )
        boton_aplicar.pack(side="right", pady=4)
        boton_aplicar.config(state="disabled")
        actualizar_vista_previa()
    entrada_id.focus_set()