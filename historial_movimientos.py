import sqlite3
import tkinter as tk
from tkinter import messagebox, ttk

from base_datos import BaseDatosInventario
from ui_comun import (
    COLOR_FONDO,
    COLOR_LINEA,
    COLOR_SECUNDARIO,
    COLOR_SUPERFICIE,
    COLOR_TINTA,
    COLOR_VERDE,
    FUENTE,
    configurar_ventana,
    crear_boton,
)


def abrir(parent, base_datos: BaseDatosInventario):
    """Muestra el registro cronológico de entradas y salidas de mercancía."""
    ventana = tk.Toplevel(parent)
    configurar_ventana(ventana, parent, "Historial de movimientos", "1040x560")
    ventana.minsize(760, 420)

    contenedor = tk.Frame(ventana, bg=COLOR_FONDO, padx=24, pady=20)
    contenedor.pack(fill="both", expand=True)
    tk.Label(
        contenedor,
        text="Historial de movimientos",
        bg=COLOR_FONDO,
        fg=COLOR_TINTA,
        font=(FUENTE, 20, "bold"),
    ).pack(anchor="w")
    tk.Label(
        contenedor,
        text="Consulta las entradas y salidas registradas en el almacén.",
        bg=COLOR_FONDO,
        fg=COLOR_SECUNDARIO,
        font=(FUENTE, 10),
    ).pack(anchor="w", pady=(3, 16))

    columnas = (
        "fecha",
        "tipo",
        "producto_id",
        "producto_nombre",
        "cantidad",
        "stock_anterior",
        "stock_nuevo",
        "motivo",
    )
    encabezados = {
        "fecha": "Fecha y hora",
        "tipo": "Movimiento",
        "producto_id": "ID",
        "producto_nombre": "Producto",
        "cantidad": "Cantidad",
        "stock_anterior": "Stock anterior",
        "stock_nuevo": "Stock nuevo",
        "motivo": "Motivo",
    }
    anchos = {
        "fecha": 155,
        "tipo": 110,
        "producto_id": 100,
        "producto_nombre": 200,
        "cantidad": 90,
        "stock_anterior": 120,
        "stock_nuevo": 110,
        "motivo": 220,
    }
    estilo = ttk.Style(ventana)
    estilo.configure(
        "Movimientos.Treeview",
        rowheight=32,
        font=(FUENTE, 10),
        background=COLOR_SUPERFICIE,
        fieldbackground=COLOR_SUPERFICIE,
    )
    estilo.configure("Movimientos.Treeview.Heading", font=(FUENTE, 9, "bold"), padding=(8, 8))
    estilo.map(
        "Movimientos.Treeview",
        background=[("selected", COLOR_VERDE)],
        foreground=[("selected", COLOR_SUPERFICIE)],
    )

    marco_tabla = tk.Frame(
        contenedor,
        bg=COLOR_SUPERFICIE,
        highlightbackground=COLOR_LINEA,
        highlightthickness=1,
    )
    marco_tabla.pack(fill="both", expand=True)
    tabla = ttk.Treeview(
        marco_tabla,
        columns=columnas,
        show="headings",
        style="Movimientos.Treeview",
    )
    for columna in columnas:
        tabla.heading(columna, text=encabezados[columna], anchor="w")
        tabla.column(columna, width=anchos[columna], minwidth=75, anchor="w", stretch=True)
    tabla.pack(side="left", fill="both", expand=True)
    barra_vertical = ttk.Scrollbar(marco_tabla, orient="vertical", command=tabla.yview)
    barra_vertical.pack(side="right", fill="y")
    barra_horizontal = ttk.Scrollbar(contenedor, orient="horizontal", command=tabla.xview)
    barra_horizontal.pack(fill="x")
    tabla.configure(yscrollcommand=barra_vertical.set, xscrollcommand=barra_horizontal.set)

    estado = tk.Label(
        contenedor,
        bg=COLOR_FONDO,
        fg=COLOR_SECUNDARIO,
        font=(FUENTE, 9),
    )
    estado.pack(anchor="w", pady=(8, 0))

    def actualizar_tabla():
        try:
            movimientos = base_datos.listar_movimientos()
        except (sqlite3.Error, OSError) as error:
            messagebox.showerror(
                "Error de base de datos",
                f"No se pudo cargar el historial.\n\n{error}",
                parent=ventana,
            )
            return

        tabla.delete(*tabla.get_children())
        for movimiento in movimientos:
            tabla.insert("", "end", values=tuple(movimiento[columna] for columna in columnas))
        estado.config(
            text=f"{len(movimientos)} movimientos registrados."
            if movimientos
            else "Todavía no hay movimientos registrados."
        )

    acciones = tk.Frame(contenedor, bg=COLOR_FONDO)
    acciones.pack(fill="x", pady=(12, 0))
    crear_boton(acciones, "Actualizar", actualizar_tabla, COLOR_VERDE).pack(side="right")
    actualizar_tabla()
