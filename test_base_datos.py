import sqlite3
import tempfile
import unittest
from pathlib import Path

from base_datos import BaseDatosInventario


class BaseDatosInventarioTests(unittest.TestCase):
    def setUp(self):
        self.directorio_temporal = tempfile.TemporaryDirectory()
        self.base_datos = BaseDatosInventario(Path(self.directorio_temporal.name) / "inventario.db")
        self.base_datos.inicializar()

    def tearDown(self):
        self.directorio_temporal.cleanup()

    def test_guarda_y_carga_productos_al_reabrir_la_base(self):
        producto = {
            "id": "P-001",
            "nombre": "Tornillos",
            "categoria": "Ferretería",
            "precio": 25,
            "stock": 12,
            "ubicacion": "A-1",
        }
        self.base_datos.registrar_producto(producto)

        productos_cargados = BaseDatosInventario(self.base_datos.ruta).listar_productos()

        self.assertEqual(productos_cargados, [producto])

    def test_actualiza_producto_y_stock(self):
        producto = {
            "id": "P-002",
            "nombre": "Clavos",
            "categoria": "Ferretería",
            "precio": 10,
            "stock": 5,
            "ubicacion": "B-2",
        }
        self.base_datos.registrar_producto(producto)
        self.base_datos.actualizar_stock("P-002", 9)
        producto_actualizado = {**producto, "nombre": "Clavos grandes", "precio": 15}
        self.base_datos.actualizar_producto(producto_actualizado)

        self.assertEqual(
            self.base_datos.listar_productos(),
            [{**producto_actualizado, "stock": 9}],
        )

    def test_elimina_producto(self):
        producto = {
            "id": "P-003",
            "nombre": "Cinta",
            "categoria": "Empaque",
            "precio": 8,
            "stock": 3,
            "ubicacion": "C-1",
        }
        self.base_datos.registrar_producto(producto)

        self.base_datos.eliminar_producto("P-003")

        self.assertEqual(self.base_datos.listar_productos(), [])

    def test_rechaza_ids_duplicados(self):
        producto = {
            "id": "P-004",
            "nombre": "Producto",
            "categoria": "General",
            "precio": 1,
            "stock": 1,
            "ubicacion": "A-1",
        }
        self.base_datos.registrar_producto(producto)

        with self.assertRaises(sqlite3.IntegrityError):
            self.base_datos.registrar_producto(producto)


if __name__ == "__main__":
    unittest.main()
