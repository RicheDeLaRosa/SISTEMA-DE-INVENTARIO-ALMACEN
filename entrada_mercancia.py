from movimiento_stock import abrir as abrir_movimiento


def abrir(parent, productos):
    abrir_movimiento(parent, productos, es_entrada=True)