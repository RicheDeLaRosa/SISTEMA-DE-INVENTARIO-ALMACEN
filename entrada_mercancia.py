from movimiento_stock import abrir as abrir_movimiento


def abrir(parent, productos):
    """Abre el formulario compartido en modo de ingreso de unidades."""
    abrir_movimiento(parent, productos, es_entrada=True)