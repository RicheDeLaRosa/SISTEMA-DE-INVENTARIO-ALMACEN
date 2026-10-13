import tkinter as tk
from tkinter import messagebox

from ui_comun import COLOR_FONDO, COLOR_SUPERFICIE, COLOR_TINTA, COLOR_SECUNDARIO, COLOR_VERDE, FUENTE, configurar_ventana, crear_boton


def abrir(parent, productos, actualizar_conteo):
    ventana = tk.Toplevel(parent)
    configurar_ventana(ventana, parent, "Registrar producto", "560x520")
    ventana.minsize(500, 480)

    panel = tk.Frame(ventana, bg=COLOR_SUPERFICIE, padx=26, pady=22)
    panel.pack(fill="both", expand=True, padx=18, pady=18)
    tk.Label(
        panel,
        text="Registrar producto",
        bg=COLOR_SUPERFICIE,
        fg=COLOR_TINTA,
        font=(FUENTE, 19, "bold")
    ).pack(anchor="w")
    tk.Label(
        panel,
        text="Completa la información del artículo",
        bg=COLOR_SUPERFICIE,
        fg=COLOR_SECUNDARIO,
        font=(FUENTE, 10)
    ).pack(anchor="w", pady=(3, 18))

    formulario = tk.Frame(panel, bg=COLOR_SUPERFICIE)
    formulario.pack(fill="x", expand=True)
    formulario.columnconfigure(0, weight=1, uniform="campos")
    formulario.columnconfigure(1, weight=1, uniform="campos")
    campos = {}

    def crear_campo(clave, etiqueta, fila, columna):
        grupo = tk.Frame(formulario, bg=COLOR_SUPERFICIE)
        grupo.grid(row=fila, column=columna, sticky="ew", padx=(0, 12) if columna == 0 else (0, 0), pady=(0, 14))
        tk.Label(
            grupo,
            text=etiqueta,
            bg=COLOR_SUPERFICIE,
            fg=COLOR_TINTA,
            font=(FUENTE, 9, "bold")
        ).pack(anchor="w")
        campo = tk.Entry(grupo, font=(FUENTE, 10))
        campo.pack(fill="x", ipady=7, pady=(5, 0))
        campos[clave] = campo

    crear_campo("id", "ID DEL PRODUCTO", 0, 0)
    crear_campo("nombre", "NOMBRE", 0, 1)
    crear_campo("categoria", "CATEGORÍA", 1, 0)
    crear_campo("precio", "PRECIO", 1, 1)
    crear_campo("stock", "STOCK INICIAL", 2, 0)
    crear_campo("ubicacion", "UBICACIÓN", 2, 1)

    def guardar_producto():
        id_producto = campos["id"].get().strip()
        nombre_producto = campos["nombre"].get().strip()
        categoria_producto = campos["categoria"].get().strip()
        ubicacion_producto = campos["ubicacion"].get().strip()

        if not all((id_producto, nombre_producto, categoria_producto, ubicacion_producto,
                    campos["precio"].get().strip(), campos["stock"].get().strip())):
            messagebox.showerror("Datos incompletos", "Completa todos los campos.", parent=ventana)
            return

        if any(producto["id"] == id_producto for producto in productos):
            messagebox.showerror("ID duplicado", "Ya existe un producto con ese ID.", parent=ventana)
            return

        try:
            precio_producto = int(campos["precio"].get())
            stock_producto = int(campos["stock"].get())
        except ValueError:
            messagebox.showerror("Dato inválido", "El precio y el stock deben ser números enteros.", parent=ventana)
            return

        productos.append({
            "id": id_producto,
            "nombre": nombre_producto,
            "categoria": categoria_producto,
            "precio": precio_producto,
            "stock": stock_producto,
            "ubicacion": ubicacion_producto
        })
        actualizar_conteo()
        messagebox.showinfo("Producto guardado", "El producto se registró correctamente.", parent=ventana)
        ventana.destroy()

    acciones = tk.Frame(panel, bg=COLOR_SUPERFICIE)
    acciones.pack(fill="x", pady=(8, 0))
    crear_boton(acciones, "Cancelar", ventana.destroy, COLOR_SUPERFICIE, texto_color=COLOR_SECUNDARIO).pack(side="right", padx=(8, 0))
    crear_boton(acciones, "Guardar producto", guardar_producto, COLOR_VERDE).pack(side="right")
    campos["id"].focus_set()
    ventana.bind("<Return>", lambda event: guardar_producto())