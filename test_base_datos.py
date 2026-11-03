import sqlite3
import tempfile
import unittest
from contextlib import closing
from pathlib import Path

from base_datos import BaseDatosInventario, producto_requiere_reposicion


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
            "stock_minimo": 0,
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
            "stock_minimo": 0,
        }
        self.base_datos.registrar_producto(producto)
        self.base_datos.actualizar_stock("P-002", 9)
        producto_actualizado = {
            **producto,
            "nombre": "Clavos grandes",
            "precio": 15,
            "stock_minimo": 2,
        }
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
            "stock_minimo": 0,
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
            "stock_minimo": 0,
        }
        self.base_datos.registrar_producto(producto)

        with self.assertRaises(sqlite3.IntegrityError):
            self.base_datos.registrar_producto(producto)

    def test_registra_entrada_y_salida_en_el_historial(self):
        producto = {
            "id": "P-005",
            "nombre": "Marcadores",
            "categoria": "Papelería",
            "precio": 12,
            "stock": 10,
            "ubicacion": "D-1",
            "stock_minimo": 5,
        }
        self.base_datos.registrar_producto(producto)

        self.assertEqual(
            self.base_datos.registrar_movimiento_stock("P-005", "Entrada", 4, "Compra"), 14
        )
        self.assertEqual(
            self.base_datos.registrar_movimiento_stock("P-005", "Salida", 3, "Uso interno"), 11
        )

        historial = self.base_datos.listar_movimientos()
        self.assertEqual(len(historial), 2)
        self.assertEqual(
            {clave: historial[0][clave] for clave in (
                "tipo", "producto_id", "producto_nombre", "cantidad", "stock_anterior",
                "stock_nuevo", "motivo"
            )},
            {
                "tipo": "Salida",
                "producto_id": "P-005",
                "producto_nombre": "Marcadores",
                "cantidad": 3,
                "stock_anterior": 14,
                "stock_nuevo": 11,
                "motivo": "Uso interno",
            },
        )
        self.assertTrue(historial[0]["fecha"])
        self.assertEqual(self.base_datos.listar_productos()[0]["stock"], 11)

    def test_salida_invalida_no_cambia_stock_ni_crea_historial(self):
        producto = {
            "id": "P-006",
            "nombre": "Carpetas",
            "categoria": "Papelería",
            "precio": 20,
            "stock": 2,
            "ubicacion": "D-2",
            "stock_minimo": 1,
        }
        self.base_datos.registrar_producto(producto)

        with self.assertRaises(ValueError):
            self.base_datos.registrar_movimiento_stock("P-006", "Salida", 3, "Pedido")
        with self.assertRaises(ValueError):
            self.base_datos.registrar_movimiento_stock("P-006", "Entrada", 1, " ")

        self.assertEqual(self.base_datos.listar_productos()[0]["stock"], 2)
        self.assertEqual(self.base_datos.listar_movimientos(), [])

    def test_inicializar_agrega_motivo_a_historial_existente(self):
        ruta = Path(self.directorio_temporal.name) / "historial_anterior.db"
        with closing(sqlite3.connect(ruta)) as conexion:
            with conexion:
                conexion.execute("""
                    CREATE TABLE movimientos (
                        id INTEGER PRIMARY KEY AUTOINCREMENT,
                        fecha TEXT NOT NULL,
                        producto_id TEXT NOT NULL,
                        producto_nombre TEXT NOT NULL,
                        tipo TEXT NOT NULL,
                        cantidad INTEGER NOT NULL,
                        stock_anterior INTEGER NOT NULL,
                        stock_nuevo INTEGER NOT NULL
                    )
                """)
                conexion.execute("""
                    INSERT INTO movimientos (
                        fecha, producto_id, producto_nombre, tipo, cantidad,
                        stock_anterior, stock_nuevo
                    )
                    VALUES ('2026-01-01 10:00:00', 'P-007', 'Plumas', 'Entrada', 2, 0, 2)
                """)

        base_datos_anterior = BaseDatosInventario(ruta)
        base_datos_anterior.inicializar()

        self.assertEqual(base_datos_anterior.listar_movimientos()[0]["motivo"], "Sin especificar")

    def test_inicializar_agrega_minimo_a_productos_existentes(self):
        ruta = Path(self.directorio_temporal.name) / "productos_anteriores.db"
        with closing(sqlite3.connect(ruta)) as conexion:
            with conexion:
                conexion.execute("""
                    CREATE TABLE productos (
                        id TEXT PRIMARY KEY,
                        nombre TEXT NOT NULL,
                        categoria TEXT NOT NULL,
                        precio INTEGER NOT NULL,
                        stock INTEGER NOT NULL,
                        ubicacion TEXT NOT NULL
                    )
                """)
                conexion.execute("""
                    INSERT INTO productos (id, nombre, categoria, precio, stock, ubicacion)
                    VALUES ('P-008', 'Lapices', 'Papelería', 5, 4, 'A-2')
                """)

        base_datos_anterior = BaseDatosInventario(ruta)
        base_datos_anterior.inicializar()

        self.assertEqual(base_datos_anterior.listar_productos()[0]["stock_minimo"], 0)

    def test_lista_productos_que_necesitan_reposicion(self):
        productos = (
            {
                "id": "P-009",
                "nombre": "Papel",
                "categoria": "Papelería",
                "precio": 5,
                "stock": 3,
                "ubicacion": "A-1",
                "stock_minimo": 3,
            },
            {
                "id": "P-010",
                "nombre": "Gomas",
                "categoria": "Papelería",
                "precio": 2,
                "stock": 4,
                "ubicacion": "A-1",
                "stock_minimo": 3,
            },
            {
                "id": "P-011",
                "nombre": "Reglas",
                "categoria": "Papelería",
                "precio": 8,
                "stock": 0,
                "ubicacion": "A-1",
                "stock_minimo": 0,
            },
        )
        for producto in productos:
            self.base_datos.registrar_producto(producto)

        self.assertEqual(
            [
                producto["id"]
                for producto in self.base_datos.listar_productos()
                if producto_requiere_reposicion(producto)
            ],
            ["P-009", "P-011"],
        )

    def test_rechaza_minimo_negativo(self):
        producto = {
            "id": "P-012",
            "nombre": "Grapas",
            "categoria": "Oficina",
            "precio": 3,
            "stock": 4,
            "ubicacion": "A-1",
            "stock_minimo": -1,
        }

        with self.assertRaises(ValueError):
            self.base_datos.registrar_producto(producto)


if __name__ == "__main__":
    unittest.main()
