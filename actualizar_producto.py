import tkinter as tk
from tkinter import messagebox

from ui_comun import COLOR_SUPERFICIE, COLOR_TINTA, COLOR_VERDE, FUENTE, configurar_ventana, crear_boton


def abrir(parent, productos):
    ventana = tk.Toplevel(parent)
    configurar_ventana(ventana, parent, "Actualizar producto", "460x540")
    ventana.minsize(420, 500)

    tk.Label(ventana, text="ID DEL PRODUCTO", font=(FUENTE, 11, "bold")).pack(pady=(12, 4))
    entrada_id = tk.Entry(ventana)
    entrada_id.pack()

    producto_seleccionado = None
    campos = {}
    for clave, etiqueta in (
        ("nombre", "NUEVO NOMBRE"),
        ("categoria", "NUEVA CATEGORIA"),
        ("precio", "NUEVO PRECIO"),
        ("ubicacion", "NUEVA UBICACION")
    ):
        tk.Label(ventana, text=etiqueta, font=(FUENTE, 10, "bold")).pack(pady=(5, 2))
        campos[clave] = tk.Entry(ventana)
        campos[clave].pack()

    def cargar_producto():
        nonlocal producto_seleccionado
        producto_seleccionado = next(
            (producto for producto in productos if producto["id"] == entrada_id.get().strip()),
            None
        )

        if producto_seleccionado is None:
            boton_guardar.config(state="disabled")
            messagebox.showerror("Producto no encontrado", "No existe un producto con ese ID.", parent=ventana)
            return

        for clave, campo in campos.items():
            campo.delete(0, tk.END)
            campo.insert(0, producto_seleccionado[clave])
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

    crear_boton(ventana, "Cargar producto", cargar_producto, COLOR_SUPERFICIE, texto_color=COLOR_TINTA).pack(pady=8)
    boton_guardar = crear_boton(ventana, "Guardar cambios", guardar_cambios, COLOR_VERDE)
    boton_guardar.config(state="disabled")
    boton_guardar.pack()
    entrada_id.focus_set()