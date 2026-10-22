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
