import tkinter as tk
from tkinter import messagebox

from ui_comun import COLOR_AMBAR, COLOR_AMBAR_HOVER, COLOR_VERDE, COLOR_VERDE_HOVER, FUENTE, configurar_ventana, crear_boton


def abrir(parent, productos, es_entrada):
    titulo = "ENTRADA DE MERCANCÍA" if es_entrada else "SALIDA DE MERCANCÍA"
    ventana = tk.Toplevel(parent)
    configurar_ventana(ventana, parent, titulo.title(), "420x300")
    ventana.minsize(380, 270)

    tk.Label(ventana, text="ID DEL PRODUCTO", font=(FUENTE, 11, "bold")).pack(pady=(14, 4))
    entrada_id = tk.Entry(ventana)
    entrada_id.pack()

    tk.Label(ventana, text="CANTIDAD", font=(FUENTE, 11, "bold")).pack(pady=(10, 4))
    entrada_cantidad = tk.Entry(ventana)
    entrada_cantidad.pack()

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

        if not es_entrada and cantidad > producto["stock"]:
            messagebox.showerror("Stock insuficiente", "No hay suficiente stock para realizar la salida.", parent=ventana)
            return

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

    crear_boton(
        ventana,
        "Aplicar entrada" if es_entrada else "Aplicar salida",
        aplicar_movimiento,
        COLOR_VERDE if es_entrada else COLOR_AMBAR,
        fondo_activo=COLOR_VERDE_HOVER if es_entrada else COLOR_AMBAR_HOVER
    ).pack(pady=12)
    entrada_id.focus_set()