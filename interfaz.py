import tkinter as tk
import sqlite3
from tkinter import messagebox

import actualizar_producto
import buscar_producto
import eliminar_producto
import entrada_mercancia
import inventario
import registrar_producto
import salida_mercancia
from base_datos import BaseDatosInventario
from ui_comun import (
    COLOR_AMBAR,
    COLOR_FONDO,
    COLOR_LINEA,
    COLOR_MARCA,
    COLOR_ROJO,
    COLOR_SECUNDARIO,
    COLOR_SUPERFICIE,
    COLOR_TINTA,
    COLOR_VERDE,
    FUENTE,
    crear_boton,
)


def crear_mosaico(parent, icono, texto, comando, color_icono):
    """Construye una tarjeta de navegación reutilizable para cada módulo."""
    mosaico = tk.Frame(
        parent,
        bg=COLOR_SUPERFICIE,
        highlightbackground=COLOR_LINEA,
        highlightthickness=1,
        width=190,
        height=150
    )
    mosaico.grid_propagate(False)
    icono_label = tk.Label(
        mosaico,
        text=icono,
        bg=COLOR_SUPERFICIE,
        fg=color_icono,
        font=("Segoe UI Symbol", 34)
    )
    icono_label.pack(expand=True, pady=(12, 0))
    texto_label = tk.Label(
        mosaico,
        text=texto.upper(),
        bg=COLOR_SUPERFICIE,
        fg=COLOR_SECUNDARIO,
        font=(FUENTE, 9, "bold"),
        wraplength=160,
        justify="center"
    )
    texto_label.pack(pady=(0, 14))

    componentes = (mosaico, icono_label, texto_label)
    for componente in componentes:
        componente.config(cursor="hand2")
        componente.bind("<Button-1>", lambda event, accion=comando: accion())
        componente.bind(
            "<Enter>",
            lambda event, elementos=componentes: [elemento.config(bg="#F8FBFC") for elemento in elementos]
        )
        componente.bind(
            "<Leave>",
            lambda event, elementos=componentes: [elemento.config(bg=COLOR_SUPERFICIE) for elemento in elementos]
        )
    return mosaico


def main():
    """Configura la ventana principal y conecta los módulos de inventario."""
    ventana = tk.Tk()
    ventana.title("ALMACEN RICHIE")
    ventana.geometry("940x700")
    ventana.minsize(760, 620)
    ventana.configure(bg=COLOR_FONDO)
    ventana.option_add("*Font", f"{{{FUENTE}}} 10")
    ventana.option_add("*Label.background", COLOR_FONDO)
    ventana.option_add("*Label.foreground", COLOR_TINTA)
    ventana.option_add("*Entry.background", COLOR_SUPERFICIE)
    ventana.option_add("*Entry.foreground", COLOR_TINTA)
    ventana.option_add("*Entry.insertBackground", COLOR_VERDE)
    ventana.option_add("*Entry.relief", "flat")
    ventana.option_add("*Entry.highlightThickness", 1)
    ventana.option_add("*Entry.highlightBackground", COLOR_LINEA)
    ventana.option_add("*Entry.highlightColor", COLOR_VERDE)
    ventana.option_add("*Button.background", COLOR_SUPERFICIE)
    ventana.option_add("*Button.foreground", COLOR_TINTA)
    ventana.option_add("*Button.activeBackground", COLOR_FONDO)
    ventana.option_add("*Button.activeForeground", COLOR_TINTA)
    ventana.option_add("*Button.relief", "flat")
    ventana.option_add("*Button.borderWidth", 0)

    base_datos = BaseDatosInventario()
    try:
        base_datos.inicializar()
        productos = base_datos.listar_productos()
    except (sqlite3.Error, OSError) as error:
        messagebox.showerror(
            "Error de base de datos",
            f"No se pudo iniciar el inventario.\n\n{error}",
            parent=ventana
        )
        ventana.destroy()
        return

    # La lista compartida mantiene sincronizada la interfaz con la base de datos.
    conteo_productos = tk.StringVar(value="0")

    def actualizar_conteo():
        conteo_productos.set(str(len(productos)))

    cabecera = tk.Frame(ventana, bg=COLOR_SUPERFICIE, padx=26, pady=16)
    cabecera.pack(fill="x")
    fila_marca = tk.Frame(cabecera, bg=COLOR_SUPERFICIE)
    fila_marca.pack(fill="x")
    marca = tk.Frame(fila_marca, bg=COLOR_MARCA, padx=13, pady=7)
    marca.pack(side="left")
    tk.Label(marca, text="ALMACÉN", bg=COLOR_MARCA, fg=COLOR_SUPERFICIE, font=(FUENTE, 8, "bold")).pack(anchor="w")
    tk.Label(marca, text="RICHIE", bg=COLOR_MARCA, fg=COLOR_SUPERFICIE, font=(FUENTE, 17, "bold")).pack(anchor="w")
    tk.Label(
        fila_marca,
        text="CONTROL DE INVENTARIO",
        bg=COLOR_SUPERFICIE,
        fg=COLOR_MARCA,
        font=(FUENTE, 10, "bold")
    ).pack(side="left", padx=16)

    indicador = tk.Frame(fila_marca, bg=COLOR_SUPERFICIE, padx=8, pady=4)
    indicador.pack(side="right")
    tk.Label(indicador, text="PRODUCTOS", bg=COLOR_SUPERFICIE, fg=COLOR_SECUNDARIO, font=(FUENTE, 8, "bold")).pack(anchor="e")
    tk.Label(indicador, textvariable=conteo_productos, bg=COLOR_SUPERFICIE, fg=COLOR_TINTA, font=(FUENTE, 20, "bold")).pack(anchor="e")

    barra_busqueda = tk.Frame(ventana, bg=COLOR_SUPERFICIE, padx=26)
    barra_busqueda.pack(fill="x")
    contenedor_busqueda = tk.Frame(barra_busqueda, bg=COLOR_SUPERFICIE)
    contenedor_busqueda.pack(anchor="center", pady=(8, 18))
    busqueda_entry = tk.Entry(contenedor_busqueda, width=42, font=(FUENTE, 11))
    busqueda_entry.pack(side="left", ipady=7, padx=(0, 6))
    busqueda_entry.insert(0, "Buscar por ID o nombre")
    busqueda_entry.config(fg=COLOR_SECUNDARIO)

    def enfocar_busqueda(event):
        if busqueda_entry.get() == "Buscar por ID o nombre":
            busqueda_entry.delete(0, tk.END)
            busqueda_entry.config(fg=COLOR_TINTA)

    def restaurar_busqueda(event):
        if not busqueda_entry.get().strip():
            busqueda_entry.insert(0, "Buscar por ID o nombre")
            busqueda_entry.config(fg=COLOR_SECUNDARIO)

    def buscar_desde_panel():
        # Desde el inicio se puede abrir el inventario completo o solo coincidencias.
        consulta = busqueda_entry.get().strip()
        if consulta == "Buscar por ID o nombre":
            consulta = ""
        if not consulta:
            inventario.abrir(ventana, productos)
            return

        consulta = consulta.casefold()
        coincidencias = [
            producto for producto in productos
            if consulta in producto["id"].casefold() or consulta in producto["nombre"].casefold()
        ]
        inventario.abrir(ventana, productos, coincidencias, "Resultados de búsqueda")

    busqueda_entry.bind("<FocusIn>", enfocar_busqueda)
    busqueda_entry.bind("<FocusOut>", restaurar_busqueda)
    busqueda_entry.bind("<Return>", lambda event: buscar_desde_panel())
    crear_boton(contenedor_busqueda, "Buscar", buscar_desde_panel, COLOR_MARCA).pack(side="left")

    contenido = tk.Frame(ventana, bg=COLOR_FONDO, padx=26, pady=22)
    contenido.pack(fill="both", expand=True)
    tk.Label(
        contenido,
        text="Módulos de inventario",
        bg=COLOR_FONDO,
        fg=COLOR_TINTA,
        font=(FUENTE, 18, "bold")
    ).pack(anchor="w", pady=(0, 12))
    rejilla_modulos = tk.Frame(contenido, bg=COLOR_FONDO)
    rejilla_modulos.pack(fill="both", expand=True)
    for columna in range(4):
        rejilla_modulos.columnconfigure(columna, weight=1, uniform="modulos")
    for fila in range(2):
        rejilla_modulos.rowconfigure(fila, weight=1, uniform="filas_modulos")

    # Cada tarjeta enlaza una acción con el mismo inventario compartido.
    modulos = (
        ("＋", "Registrar producto", lambda: registrar_producto.abrir(ventana, productos, actualizar_conteo, base_datos), COLOR_VERDE),
        ("▤", "Inventario", lambda: inventario.abrir(ventana, productos), COLOR_MARCA),
        ("⌕", "Buscar producto", lambda: buscar_producto.abrir(ventana, productos), COLOR_MARCA),
        ("↻", "Actualizar producto", lambda: actualizar_producto.abrir(ventana, productos, base_datos), COLOR_VERDE),
        ("×", "Eliminar producto", lambda: eliminar_producto.abrir(ventana, productos, actualizar_conteo, base_datos), COLOR_ROJO),
        ("↑", "Entrada de mercancía", lambda: entrada_mercancia.abrir(ventana, productos, base_datos), COLOR_VERDE),
        ("↓", "Salida de mercancía", lambda: salida_mercancia.abrir(ventana, productos, base_datos), COLOR_AMBAR)
    )

    for indice, (icono, texto, comando, color_icono) in enumerate(modulos):
        mosaico = crear_mosaico(rejilla_modulos, icono, texto, comando, color_icono)
        mosaico.grid(row=indice // 4, column=indice % 4, sticky="nsew", padx=7, pady=7)

    pie = tk.Frame(contenido, bg=COLOR_FONDO)
    pie.pack(fill="x")
    tk.Frame(pie, bg=COLOR_LINEA, height=1).pack(fill="x", pady=(12, 12))
    tk.Label(pie, text="Sistema listo", bg=COLOR_FONDO, fg=COLOR_SECUNDARIO, font=(FUENTE, 9)).pack(side="left")
    crear_boton(pie, "Salir", ventana.destroy, COLOR_SUPERFICIE, texto_color=COLOR_SECUNDARIO).pack(side="right")

    ventana.mainloop()


if __name__ == "__main__":
    main()