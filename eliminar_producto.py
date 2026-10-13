import tkinter as tk
from tkinter import messagebox

from ui_comun import COLOR_ROJO, FUENTE, configurar_ventana, crear_boton


def abrir(parent, productos, actualizar_conteo):
    ventana = tk.Toplevel(parent)
    configurar_ventana(ventana, parent, "Eliminar producto", "420x230")
    ventana.minsize(380, 210)

    tk.Label(ventana, text="ID DEL PRODUCTO", font=(FUENTE, 11, "bold")).pack(pady=(16, 4))
    entrada_id = tk.Entry(ventana)
    entrada_id.pack()

    def confirmar_eliminacion():
        id_producto = entrada_id.get().strip()
        if not id_producto:
            messagebox.showerror("ID requerido", "Ingresa el ID del producto.", parent=ventana)
            return

        producto = next((producto for producto in productos if producto["id"] == id_producto), None)
        if producto is None:
            messagebox.showerror("Producto no encontrado", "No existe un producto con ese ID.", parent=ventana)
            return

        confirmar = messagebox.askyesno(
            "Confirmar eliminación",
            f"¿Deseas eliminar el producto '{producto['nombre']}'?",
            parent=ventana
        )
        if not confirmar:
            return

        productos.remove(producto)
        actualizar_conteo()
        messagebox.showinfo("Producto eliminado", "El producto se eliminó correctamente.", parent=ventana)
        ventana.destroy()

    crear_boton(ventana, "Eliminar producto", confirmar_eliminacion, COLOR_ROJO).pack(pady=12)
    entrada_id.focus_set()