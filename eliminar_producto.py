import tkinter as tk
import sqlite3
from tkinter import messagebox

from base_datos import BaseDatosInventario
from ui_comun import (
    COLOR_FONDO,
    COLOR_LINEA,
    COLOR_ROJO,
    COLOR_SECUNDARIO,
    COLOR_SUPERFICIE,
    COLOR_TINTA,
    FUENTE,
    configurar_ventana,
    crear_boton,
)


def abrir(parent, productos, actualizar_conteo, base_datos: BaseDatosInventario):
    """Permite revisar un producto y confirmar su eliminación del inventario."""
    ventana = tk.Toplevel(parent)
    configurar_ventana(ventana, parent, "Eliminar producto", "560x440")
    ventana.minsize(480, 400)

    panel = tk.Frame(ventana, bg=COLOR_FONDO, padx=24, pady=20)
    panel.pack(fill="both", expand=True)
    tk.Label(
        panel,
        text="Eliminar producto",
        bg=COLOR_FONDO,
        fg=COLOR_TINTA,
        font=(FUENTE, 20, "bold")
    ).pack(anchor="w")
    tk.Label(
        panel,
        text="Busca el artículo y revisa sus datos antes de eliminarlo",
        bg=COLOR_FONDO,
        fg=COLOR_SECUNDARIO,
        font=(FUENTE, 10)
    ).pack(anchor="w", pady=(3, 18))

    barra_busqueda = tk.Frame(panel, bg=COLOR_FONDO)
    barra_busqueda.pack(fill="x", pady=(0, 16))
    tk.Label(
        barra_busqueda,
        text="ID DEL PRODUCTO",
        bg=COLOR_FONDO,
        fg=COLOR_TINTA,
        font=(FUENTE, 9, "bold")
    ).pack(side="left", padx=(0, 10))
    id_producto = tk.StringVar()
    entrada_id = tk.Entry(barra_busqueda, textvariable=id_producto, font=(FUENTE, 10))
    entrada_id.pack(side="left", fill="x", expand=True, ipady=6)

    ficha = tk.Frame(
        panel,
        bg=COLOR_SUPERFICIE,
        padx=18,
        pady=16,
        highlightbackground=COLOR_LINEA,
        highlightthickness=1
    )
    ficha.pack(fill="x", expand=True)
    nombre_producto = tk.Label(
        ficha,
        text="Producto sin cargar",
        bg=COLOR_SUPERFICIE,
        fg=COLOR_SECUNDARIO,
        font=(FUENTE, 15, "bold")
    )
    nombre_producto.pack(anchor="w")
    detalle_producto = tk.Label(
        ficha,
        text="Busca un ID para mostrar los detalles.",
        bg=COLOR_SUPERFICIE,
        fg=COLOR_SECUNDARIO,
        font=(FUENTE, 10),
        justify="left"
    )
    detalle_producto.pack(anchor="w", pady=(8, 0))
    estado = tk.Label(panel, text="", bg=COLOR_FONDO, fg=COLOR_SECUNDARIO, font=(FUENTE, 9))
    estado.pack(anchor="w", pady=(10, 8))

    producto_seleccionado = None

    acciones = tk.Frame(panel, bg=COLOR_FONDO)
    acciones.pack(fill="x", pady=(12, 0))

    def confirmar_eliminacion():
        # Solicita confirmación antes de retirar definitivamente el registro.
        if producto_seleccionado is None:
            return

        confirmar = messagebox.askyesno(
            "Confirmar eliminación",
            f"¿Deseas eliminar el producto '{producto_seleccionado['nombre']}'?",
            parent=ventana
        )
        if not confirmar:
            return

        try:
            base_datos.eliminar_producto(producto_seleccionado["id"])
        except (sqlite3.Error, ValueError) as error:
            messagebox.showerror(
                "Error de base de datos",
                f"No se pudo eliminar el producto.\n\n{error}",
                parent=ventana
            )
            return

        productos.remove(producto_seleccionado)
        actualizar_conteo()
        messagebox.showinfo("Producto eliminado", "El producto se eliminó correctamente.", parent=ventana)
        ventana.destroy()

    def buscar_producto():
        # Carga la ficha y habilita la eliminación solo si encuentra el ID.
        nonlocal producto_seleccionado
        id_buscar = id_producto.get().strip()
        producto_seleccionado = next(
            (producto for producto in productos if producto["id"] == id_buscar),
            None
        )
        if producto_seleccionado is None:
            nombre_producto.config(text="Producto no encontrado", fg=COLOR_ROJO)
            detalle_producto.config(text="Verifica el ID e intenta nuevamente.")
            estado.config(text="No se encontró un producto con ese ID.", fg=COLOR_ROJO)
            boton_eliminar.config(state="disabled")
            return

        nombre_producto.config(text=producto_seleccionado["nombre"], fg=COLOR_TINTA)
        detalle_producto.config(text=(
            f"ID: {producto_seleccionado['id']}\n"
            f"Categoría: {producto_seleccionado['categoria']}\n"
            f"Precio: {producto_seleccionado['precio']}    ·    "
            f"Existencias: {producto_seleccionado['stock']}\n"
            f"Ubicación: {producto_seleccionado['ubicacion']}"
        ))
        estado.config(text="Confirma que este es el artículo que deseas eliminar.", fg=COLOR_SECUNDARIO)
        boton_eliminar.config(state="normal")

    def invalidar_seleccion(*args):
        # Si cambia el ID, obliga a buscar de nuevo antes de permitir eliminar.
        nonlocal producto_seleccionado
        producto_seleccionado = None
        boton_eliminar.config(state="disabled")
        nombre_producto.config(text="Producto sin cargar", fg=COLOR_SECUNDARIO)
        detalle_producto.config(text="Busca un ID para mostrar los detalles.")
        estado.config(text="")

    crear_boton(barra_busqueda, "Buscar", buscar_producto, COLOR_TINTA).pack(side="left", padx=(8, 0))
    crear_boton(acciones, "Cancelar", ventana.destroy, COLOR_SUPERFICIE, texto_color=COLOR_SECUNDARIO).pack(side="right", padx=(8, 0))
    boton_eliminar = crear_boton(acciones, "Eliminar producto", confirmar_eliminacion, COLOR_ROJO)
    boton_eliminar.config(state="disabled")
    boton_eliminar.pack(side="right")
    id_producto.trace_add("write", invalidar_seleccion)
    entrada_id.bind("<Return>", lambda event: buscar_producto())
    entrada_id.focus_set()