import tkinter as tk
from tkinter import messagebox

from ui_comun import (
    COLOR_FONDO,
    COLOR_SECUNDARIO,
    COLOR_SUPERFICIE,
    COLOR_TINTA,
    COLOR_VERDE,
    FUENTE,
    configurar_ventana,
    crear_boton,
)


def abrir(parent, productos):
    ventana = tk.Toplevel(parent)
    configurar_ventana(ventana, parent, "Actualizar producto", "620x570")
    ventana.minsize(540, 500)

    panel = tk.Frame(ventana, bg=COLOR_FONDO, padx=24, pady=20)
    panel.pack(fill="both", expand=True)
    tk.Label(
        panel,
        text="Actualizar producto",
        bg=COLOR_FONDO,
        fg=COLOR_TINTA,
        font=(FUENTE, 20, "bold")
    ).pack(anchor="w")
    tk.Label(
        panel,
        text="Busca un artículo y modifica su información",
        bg=COLOR_FONDO,
        fg=COLOR_SECUNDARIO,
        font=(FUENTE, 10)
    ).pack(anchor="w", pady=(3, 16))

    barra_busqueda = tk.Frame(panel, bg=COLOR_FONDO)
    barra_busqueda.pack(fill="x", pady=(0, 10))
    tk.Label(
        barra_busqueda,
        text="ID DEL PRODUCTO",
        bg=COLOR_FONDO,
        fg=COLOR_TINTA,
        font=(FUENTE, 9, "bold")
    ).pack(side="left", padx=(0, 10))
    entrada_id = tk.Entry(barra_busqueda, font=(FUENTE, 10))
    entrada_id.pack(side="left", fill="x", expand=True, ipady=6)

    producto_seleccionado = None
    campos = {}
    formulario = tk.Frame(panel, bg=COLOR_SUPERFICIE, padx=20, pady=18)
    formulario.pack(fill="x", pady=(8, 12))
    formulario.columnconfigure(0, weight=1, uniform="campos")
    formulario.columnconfigure(1, weight=1, uniform="campos")
    for indice, (clave, etiqueta) in enumerate((
        ("nombre", "NOMBRE"),
        ("categoria", "CATEGORÍA"),
        ("precio", "PRECIO"),
        ("ubicacion", "UBICACIÓN")
    )):
        fila, columna = divmod(indice, 2)
        grupo = tk.Frame(formulario, bg=COLOR_SUPERFICIE)
        grupo.grid(row=fila, column=columna, sticky="ew", padx=(0, 14) if columna == 0 else (0, 0), pady=(0, 14))
        tk.Label(
            grupo,
            text=etiqueta,
            bg=COLOR_SUPERFICIE,
            fg=COLOR_TINTA,
            font=(FUENTE, 9, "bold")
        ).pack(anchor="w")
        campo = tk.Entry(grupo, font=(FUENTE, 10), state="disabled")
        campo.pack(fill="x", ipady=7, pady=(5, 0))
        campos[clave] = campo

    estado = tk.Label(
        panel,
        text="Busca un producto para habilitar la edición.",
        bg=COLOR_FONDO,
        fg=COLOR_SECUNDARIO,
        font=(FUENTE, 9)
    )
    estado.pack(anchor="w", pady=(0, 12))

    def cargar_producto():
        nonlocal producto_seleccionado
        producto_seleccionado = next(
            (producto for producto in productos if producto["id"] == entrada_id.get().strip()),
            None
        )

        if producto_seleccionado is None:
            for campo in campos.values():
                campo.config(state="normal")
                campo.delete(0, tk.END)
                campo.config(state="disabled")
            boton_guardar.config(state="disabled")
            estado.config(text="No se encontró un producto con ese ID.", fg="#A8443F")
            return

        for clave, campo in campos.items():
            campo.config(state="normal")
            campo.delete(0, tk.END)
            campo.insert(0, producto_seleccionado[clave])
        estado.config(
            text=f"Producto cargado · Stock actual: {producto_seleccionado['stock']} unidades",
            fg=COLOR_VERDE
        )
        boton_guardar.config(state="normal")

    def guardar_cambios():
        if producto_seleccionado is None:
            return

        valores = {clave: campo.get().strip() for clave, campo in campos.items()}
        if not all(valores.values()):
            messagebox.showerror("Datos incompletos", "Completa todos los campos.", parent=ventana)
            return

        try:
            precio_nuevo = int(valores["precio"])
        except ValueError:
            messagebox.showerror("Precio inválido", "El precio debe ser un número entero.", parent=ventana)
            return

        producto_seleccionado.update({
            "nombre": valores["nombre"],
            "categoria": valores["categoria"],
            "precio": precio_nuevo,
            "ubicacion": valores["ubicacion"]
        })
        messagebox.showinfo("Producto actualizado", "Los datos se actualizaron correctamente.", parent=ventana)
        ventana.destroy()

    crear_boton(barra_busqueda, "Cargar", cargar_producto, COLOR_VERDE).pack(side="left", padx=(8, 0))
    entrada_id.bind("<Return>", lambda event: cargar_producto())

    acciones = tk.Frame(panel, bg=COLOR_FONDO)
    acciones.pack(fill="x")
    crear_boton(acciones, "Cancelar", ventana.destroy, COLOR_SUPERFICIE, texto_color=COLOR_SECUNDARIO).pack(side="right", padx=(8, 0))
    boton_guardar = crear_boton(acciones, "Guardar cambios", guardar_cambios, COLOR_VERDE)
    boton_guardar.config(state="disabled")
    boton_guardar.pack(side="right")
    entrada_id.focus_set()