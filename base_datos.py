import sqlite3
from contextlib import closing, contextmanager
from pathlib import Path


class BaseDatosInventario:
    """Administra el almacenamiento persistente de productos del inventario."""

    def __init__(self, ruta=None):
        self.ruta = Path(ruta) if ruta is not None else Path(__file__).with_name("inventario.db")

    @contextmanager
    def _conexion(self):
        self.ruta.parent.mkdir(parents=True, exist_ok=True)
        with closing(sqlite3.connect(self.ruta)) as conexion:
            with conexion:
                yield conexion

    def inicializar(self):
        """Crea la tabla de productos si todavía no existe."""
        with self._conexion() as conexion:
            conexion.execute("""
                CREATE TABLE IF NOT EXISTS productos (
                    id TEXT PRIMARY KEY,
                    nombre TEXT NOT NULL,
                    categoria TEXT NOT NULL,
                    precio INTEGER NOT NULL,
                    stock INTEGER NOT NULL,
                    ubicacion TEXT NOT NULL
                )
            """)
            conexion.execute("""
                CREATE TABLE IF NOT EXISTS movimientos (
                    id INTEGER PRIMARY KEY AUTOINCREMENT,
                    fecha TEXT NOT NULL DEFAULT (datetime('now', 'localtime')),
                    producto_id TEXT NOT NULL,
                    producto_nombre TEXT NOT NULL,
                    tipo TEXT NOT NULL CHECK (tipo IN ('Entrada', 'Salida')),
                    cantidad INTEGER NOT NULL CHECK (cantidad > 0),
                    stock_anterior INTEGER NOT NULL,
                    stock_nuevo INTEGER NOT NULL,
                    motivo TEXT NOT NULL DEFAULT 'Sin especificar'
                )
            """)
            columnas_movimientos = {
                fila[1] for fila in conexion.execute("PRAGMA table_info(movimientos)")
            }
            if "motivo" not in columnas_movimientos:
                conexion.execute("""
                    ALTER TABLE movimientos
                    ADD COLUMN motivo TEXT NOT NULL DEFAULT 'Sin especificar'
                """)

    def listar_productos(self):
        """Devuelve los productos almacenados en el orden en que se registraron."""
        with self._conexion() as conexion:
            filas = conexion.execute("""
                SELECT id, nombre, categoria, precio, stock, ubicacion
                FROM productos
                ORDER BY rowid
            """).fetchall()
        return [
            {
                "id": fila[0],
                "nombre": fila[1],
                "categoria": fila[2],
                "precio": fila[3],
                "stock": fila[4],
                "ubicacion": fila[5],
            }
            for fila in filas
        ]

    def registrar_producto(self, producto):
        with self._conexion() as conexion:
            conexion.execute("""
                INSERT INTO productos (id, nombre, categoria, precio, stock, ubicacion)
                VALUES (?, ?, ?, ?, ?, ?)
            """, (
                producto["id"],
                producto["nombre"],
                producto["categoria"],
                producto["precio"],
                producto["stock"],
                producto["ubicacion"],
            ))

    def actualizar_producto(self, producto):
        with self._conexion() as conexion:
            cursor = conexion.execute("""
                UPDATE productos
                SET nombre = ?, categoria = ?, precio = ?, ubicacion = ?
                WHERE id = ?
            """, (
                producto["nombre"],
                producto["categoria"],
                producto["precio"],
                producto["ubicacion"],
                producto["id"],
            ))
            if cursor.rowcount == 0:
                raise ValueError(f"No existe un producto con ID '{producto['id']}'.")

    def eliminar_producto(self, id_producto):
        with self._conexion() as conexion:
            cursor = conexion.execute("DELETE FROM productos WHERE id = ?", (id_producto,))
            if cursor.rowcount == 0:
                raise ValueError(f"No existe un producto con ID '{id_producto}'.")

    def actualizar_stock(self, id_producto, stock):
        with self._conexion() as conexion:
            cursor = conexion.execute(
                "UPDATE productos SET stock = ? WHERE id = ?",
                (stock, id_producto),
            )
            if cursor.rowcount == 0:
                raise ValueError(f"No existe un producto con ID '{id_producto}'.")

    def registrar_movimiento_stock(self, id_producto, tipo, cantidad, motivo):
        """Actualiza el stock y guarda el movimiento como una operación atómica."""
        if tipo not in ("Entrada", "Salida"):
            raise ValueError("El tipo de movimiento debe ser 'Entrada' o 'Salida'.")
        if not isinstance(cantidad, int) or cantidad <= 0:
            raise ValueError("La cantidad del movimiento debe ser un entero mayor que cero.")
        if not isinstance(motivo, str) or not motivo.strip():
            raise ValueError("El motivo del movimiento es obligatorio.")
        motivo = motivo.strip()

        with self._conexion() as conexion:
            fila = conexion.execute(
                "SELECT nombre, stock FROM productos WHERE id = ?",
                (id_producto,),
            ).fetchone()
            if fila is None:
                raise ValueError(f"No existe un producto con ID '{id_producto}'.")

            nombre, stock_anterior = fila
            if tipo == "Salida" and cantidad > stock_anterior:
                raise ValueError("No hay suficiente stock para realizar la salida.")

            stock_nuevo = stock_anterior + cantidad if tipo == "Entrada" else stock_anterior - cantidad
            conexion.execute(
                "UPDATE productos SET stock = ? WHERE id = ?",
                (stock_nuevo, id_producto),
            )
            conexion.execute("""
                INSERT INTO movimientos (
                    producto_id, producto_nombre, tipo, cantidad, stock_anterior, stock_nuevo,
                    motivo
                )
                VALUES (?, ?, ?, ?, ?, ?, ?)
            """, (
                id_producto,
                nombre,
                tipo,
                cantidad,
                stock_anterior,
                stock_nuevo,
                motivo,
            ))

        return stock_nuevo

    def listar_movimientos(self):
        """Devuelve el historial del más reciente al más antiguo."""
        with self._conexion() as conexion:
            filas = conexion.execute("""
                SELECT fecha, tipo, producto_id, producto_nombre, cantidad,
                       stock_anterior, stock_nuevo, motivo
                FROM movimientos
                ORDER BY id DESC
            """).fetchall()
        return [
            {
                "fecha": fila[0],
                "tipo": fila[1],
                "producto_id": fila[2],
                "producto_nombre": fila[3],
                "cantidad": fila[4],
                "stock_anterior": fila[5],
                "stock_nuevo": fila[6],
                "motivo": fila[7],
            }
            for fila in filas
        ]
